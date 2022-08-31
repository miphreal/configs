local cmd = vim.cmd

vim.g.mapleader = " "
vim.g.maplocalleader = ","

vim.o.autoread = true -- Auto read a file when it's changed from the outside
vim.o.autowrite = true -- enable auto write
vim.o.clipboard = "unnamedplus" -- sync with system clipboard
vim.o.conceallevel = 2 -- Hide * markup for bold and italic
vim.o.confirm = true -- confirm to save changes before exiting modified buffer
vim.o.cursorline = true -- Enable highlighting of the current line
vim.o.encoding = "utf-8"
vim.o.expandtab = true
vim.o.grepformat = "%f:%l:%c:%m"
vim.o.grepprg = "rg --vimgrep"
vim.o.guifont = "FiraCode Nerd Font:h12"
vim.o.hidden = true -- Enable modified buffers in background
vim.o.history = 500
vim.o.ignorecase = true -- Ignore case when searching
vim.o.inccommand = "split" -- preview incremental substitute
vim.o.joinspaces = false -- No double spaces with join after a dot
vim.o.list = true -- Show some invisible characters (tabs...
vim.o.mouse = "a" -- enable mouse mode
vim.o.number = true
vim.o.relativenumber = true -- Relative line numbers
vim.o.shiftround = true -- Round indent
vim.o.shiftwidth = 4
vim.o.showmode = false -- dont show mode since we have a statusline
vim.o.signcolumn = "yes" -- Always show the signcolumn, otherwise it would shift the text each time
vim.o.smartcase = true -- When searching try to be smart about cases
vim.o.smartindent = true -- Insert indents automatically
vim.o.softtabstop = 4
vim.o.splitbelow = true -- Put new windows below current
vim.o.splitright = true -- Put new windows right of current
vim.o.tabstop = 4
vim.o.termguicolors = true -- True color support
vim.o.title = true
vim.o.undofile = true
vim.o.undolevels = 10000
vim.o.updatetime = 200 -- save swap file and trigger CursorHold
vim.o.wildmenu = true
vim.o.wildmode = "longest:full,full" -- Command-line completion mode
vim.o.wrap = false -- Disable line wrap

cmd("set whichwrap+=<,>,[,]") -- Move cursor to the next/pref line https://superuser.com/questions/35389/in-vim-how-do-i-make-the-left-and-right-arrow-keys-change-line

-- syntax
cmd("syntax enable")
cmd("filetype plugin indent on")

-- show cursor line only in active window
cmd([[
  autocmd InsertLeave,WinEnter * set cursorline
  autocmd InsertEnter,WinLeave * set nocursorline
]])

-- go to last loc when opening a buffer
cmd([[
  autocmd BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | execute "normal! g`\"" | endif
]])

-- cmd([[
--   autocmd BufWritePost plugins.lua PackerCompile
-- ]])
