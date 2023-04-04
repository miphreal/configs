def main(conf):
    conf(
        zsh_profile='eval "$(/opt/homebrew/bin/brew shellenv)"',
        homepage="https://brew.sh/",
    )
    if not conf.sh("which brew"):
        conf.msg("Please install homebrew first: {{ homepage }}")
        conf.force_stop("homebrew is not installed")