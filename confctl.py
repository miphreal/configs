import re
import sys
from dataclasses import dataclass
from pathlib import Path
from collections import ChainMap
from typing import Literal, Mapping
from urllib.parse import parse_qsl

try:
    from jinja2 import Template as JinjaTemplate
except ImportError:
    JinjaTemplate = None


class FStringTemplate:
    tokens: list[str]
    TEMPLATE_TERM = re.compile(r"\{\{([^}\n]+)\}\}")

    def __init__(self, template: str):
        self.tokens = self.TEMPLATE_TERM.split(template)  # every second term is expr

    @staticmethod
    def eval_expr_as_f_string(expr, ctx):
        if expr:
            f_expr = "f'''{%s}'''" % expr.replace("'''", r"\'\'\'")
            return eval(f_expr, ctx)
        return ""

    def render(self, context):
        ctx = dict(context)
        return "".join(
            self.eval_expr_as_f_string(p, ctx) if i % 2 else p
            for i, p in enumerate(self.tokens)
        )


Template = JinjaTemplate if JinjaTemplate is not None else FStringTemplate


def load_python_module(path):
    import importlib.util

    spec = importlib.util.spec_from_file_location("tmp", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Ctx(ChainMap):
    def __getattr__(self, name):
        try:
            val = self[name]
        except KeyError:
            raise AttributeError(name)

        if isinstance(val, LazyStr):
            val = str(val)
            self[name] = val
        return val


@dataclass
class LazyStr:
    template: Template
    parent_target: "TargetCtl"

    def __str__(self) -> str:
        return self.template.render(self.parent_target.ctx)


@dataclass
class Params:
    raw: str
    data: dict

    def __contains__(self, val):
        return val in self.data

    def __getitem__(self, name):
        return self.data[name]

    def __getattr__(self, name):
        return self.data[name]


class TargetCtl:
    path: Path
    name: str
    fn: callable
    ctx: Ctx
    deps: list["TargetCtl"]
    _registry: dict[str, "TargetCtl"]

    building_stage: Literal["built", "building", "initialized"] = "initialized"

    def __init__(
        self,
        registry: dict,
        root_ctx: Ctx,
        path: Path,
        name,
        fn,
        params: Params | None = None,
    ):
        self.deps = []
        self._registry = registry
        self.path = path
        self.name = name
        self.fn = fn
        if params is None:
            params = Params("", {})
        self.ctx = root_ctx.new_child(
            dict(
                params=params,
                **params.data,
                dep=self.dep,
                __name__=self.name,
            )
        )
        self.building_stage = "initialized"

    def __getattr__(self, name):
        return getattr(self.ctx, name)

    def build(self, params: Params | None = None):
        if self.building_stage != "initialized":
            return

        self.building_stage = "building"

        if params is not None:
            self.ctx = self.ctx.new_child(dict(params=params, **params.data))

        self.fn(self)
        self.building_stage = "built"

    def expand_path(self, path):
        return self.path.parent.joinpath(Path(path).expanduser())

    def dep(self, target):
        if isinstance(target, str):
            target = self.render_str(target)
            t = self._registry[target]
        else:
            t = next(_t for _t in self._registry.values() if _t.fn is target)

        t.build()
        self.deps.append(t)
        return t

    def conf(self, **kw):
        def _nest_ctx(val):
            if isinstance(val, Mapping):
                return Ctx({k: _nest_ctx(v) for k, v in val.items()})
            if isinstance(val, str):
                return LazyStr(Template(val), parent_target=self)
            return val

        for k, v in kw.items():
            self.ctx[k] = _nest_ctx(v)

    def ensure_dirs(self, *folders):
        for f in folders:
            folder = Path(self.render_str(f)).expanduser()
            folder.mkdir(parents=True, exist_ok=True)

    def sh(self, *commands):
        import subprocess
        import shlex

        outputs = []
        for cmd in commands:
            cmd = self.render_str(cmd)
            try:
                output = subprocess.check_output(cmd, shell=True)
                outputs.append(output)
            except subprocess.SubprocessError:
                outputs.append(None)

        return outputs

    def render_str(self, template):
        if isinstance(template, str):
            return Template(template).render(self.ctx)
        return template

    def render(self, src, dst, **context):
        src = self.expand_path(self.render_str(src))
        dst = Path(self.render_str(dst)).expanduser()
        self.ensure_dirs(dst.parent)

        if src.exists():
            with src.open("rt") as f:
                template = Template(f.read())
            with dst.open("wt") as f:
                f.write(template.render(self.ctx))


registry: dict[str, TargetCtl] = {}


def parse_target(t: str):
    t = t.strip()
    parts = t.split("?", 1)
    if len(parts) == 2:
        target, params = parts
        target = target.lstrip("/")
        return f"//{target}", Params(
            params, dict(parse_qsl(params, keep_blank_values=True))
        )
    return f"//{t.lstrip('//')}", Params("", {})


def main(target: str):
    root = Path.cwd()
    paths = root.rglob(".confbuild.py")

    root_ctx = Ctx()

    for path in sorted(paths):
        is_root = path.parent == root

        if is_root:
            base_name = ""
        else:
            base_name = str(path.parent.relative_to(root)).removeprefix("./")

        conf = load_python_module(path)

        targets = [
            f
            for f in vars(conf).values()
            if callable(f) and not f.__name__.startswith("_")
        ]

        if len(targets) == 1 and base_name.endswith(
            (f"/{targets[0].__name__}", "/main")
        ):
            t_name, _ = parse_target(base_name)
            registry[t_name] = TargetCtl(
                registry, root_ctx=root_ctx, name=t_name, fn=targets[0], path=path
            )

        for t in targets:
            t_name = f"{base_name}/{t.__name__}"
            t_name, _ = parse_target(t_name)
            registry[t_name] = TargetCtl(
                registry, root_ctx=root_ctx, name=t_name, fn=t, path=path
            )

        if is_root and "//main" in registry:
            root_target = registry["//main"]
            root_target.ctx = root_ctx
            registry["//"] = root_target

    t_name, t_params = parse_target(target)

    if "//" in registry:
        registry["//"].build()
    registry[t_name].build(t_params)


if __name__ == "__main__":
    main(sys.argv[1])
