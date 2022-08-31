return require("packer").startup({
  function(use)
    -- Packer can manage itself
    use 'wbthomason/packer.nvim'

    -- -- LSP
    -- use "neovim/nvim-lspconfig"

    -- Theme: icons
    use {
      "kyazdani42/nvim-web-devicons",
      config = function()
        require('config.nvim-web-devicons')
      end,
    }

    -- File Tree
    use {
      "kyazdani42/nvim-tree.lua",
      config = function()
        require("config.nvim-tree")
      end,
    }

    -- Markdown preview
    use {
      "iamcco/markdown-preview.nvim",
      run = function()
        vim.fn["mkdp#util#install"]()
      end,
      ft = { "markdown" },
      cmd = "MarkdownPreview",
    }

    -- Highlight colors in text
    use {
      "norcalli/nvim-colorizer.lua",
      event = "BufReadPre",
      config = function()
        require("config.colorizer")
      end,
    }

    -- Git Gutter
    -- use {
    --   'lewis6991/gitsigns.nvim',
    --   requires = { 'nvim-lua/plenary.nvim' },
    --   event = "BufReadPre",
    --   config = function()
    --     require("config.gitsigns")
    --   end,
    -- }
    -- use {
    --   "kdheepak/lazygit.nvim",
    --   cmd = "LazyGit",
    --   config = function() vim.g.lazygit_floating_window_use_plenary = 0 end
    -- }
    use({
      "TimUntersberger/neogit",
      cmd = "Neogit",
      config = function()
        require("config.neogit")
      end,
    })

    -- Text objects
    use "wellle/targets.vim"

    -- Zen Mode
    use {
      "folke/zen-mode.nvim",
      config = function()
        require("zen-mode")
      end
    }

    -- Search
    use {
      'nvim-telescope/telescope.nvim',
      requires = {{'nvim-lua/popup.nvim'}, {'nvim-lua/plenary.nvim'}}
    }

    -- Theme
    use 'folke/tokyonight.nvim'

    -- Help
    use {
      "folke/which-key.nvim",
      config = function()
        require("which-key").setup {}
      end,
    }
    -- use "DanilaMihailov/vim-tips-wiki"

  end,
  config = {}
})
