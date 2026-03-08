# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal dotfiles/configs repository managed by [`confctl`](https://github.com/miphreal/confctl) — a Python-based configuration management tool. Configs are organized by OS (`macos/`, `linux/`) with each tool/component in its own subdirectory.

## How confctl works

Each component has a `.confbuild.py` file that defines:
- **Dependencies**: `conf["brew::package"]` installs via Homebrew; `conf["pipx::package"]` via pipx; `conf[":target"]` references a sibling target in the same file; `conf["./subdir"]` references a subdirectory's `.confbuild.py`
- **Template rendering**: `conf.render("template.j2", "~/destination")` renders Jinja2 templates (`.j2` files) to their target locations
- **Context variables**: `conf(key=value)` sets variables available in templates via `{{ key }}`; `dep('path')` accesses variables from dependencies
- **Shell commands**: `conf.sh("command")` executes shell commands
- **Path/dir helpers**: `conf['path::~/file']` resolves a file path; `conf['dir::~/dir']` ensures a directory exists

The root `.confbuild.py` detects the OS and delegates to `macos/` or `linux/`. The `macos/.confbuild.py` orchestrates all macOS components.

## Applying configs

```bash
confctl apply          # apply all configs for the current OS
confctl apply //macos/zsh   # apply a specific target
```

The `confctl` binary is at `~/.local/bin/confctl`.

## Key components (macOS)

| Directory | Purpose |
|-----------|---------|
| `macos/zsh/` | ZSH config — renders `.zshrc`, `.zprofile`, `.zshenv` templates |
| `macos/karabiner/` | Karabiner-Elements config with a custom DSL for key remapping rules (see `rule()`, `parse_profile()`) |
| `macos/commands/` | Scripts deployed to `~/.local/opt/scripts/`; `.sh` files are rendered as Jinja2 templates |
| `macos/git/` | Git and lazygit configuration |
| `macos/kitty/`, `macos/wezterm/` | Terminal emulator configs |
| `macos/starship/` | Starship prompt config |
| `macos/fonts.py` | Nerd Fonts installation via Homebrew |
| `macos/.confbuild.py` | Top-level macOS orchestrator; also defines `common`, `asdf`, `fzf`, `yazi`, `bitwarden` targets |

## Branches

- `dev` — development branch (feature branches should be based on this)
- `main` — release branch
