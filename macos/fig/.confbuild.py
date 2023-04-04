ZSH_RC_PRE="""
# Fig pre block. Keep at the top of this file.
[[ -f "$HOME/.fig/shell/zshrc.pre.zsh" ]] && builtin source "$HOME/.fig/shell/zshrc.pre.zsh"
"""
ZSH_RC_POST="""
# Fig post block. Keep at the bottom of this file.
[[ -f "$HOME/.fig/shell/zshrc.post.zsh" ]] && builtin source "$HOME/.fig/shell/zshrc.post.zsh"
"""

ZSH_PROFILE="""
# Fig post block. Keep at the bottom of this file.
[[ -f "$HOME/.fig/shell/zprofile.post.zsh" ]] && builtin source "$HOME/.fig/shell/zprofile.post.zsh"
"""


def fig(conf):
    conf['brew::fig']
    conf(
        zsh_rc={
            "pre": ZSH_RC_PRE,
            "post": ZSH_RC_POST,
        },
        zsh_profile=ZSH_PROFILE,
    )