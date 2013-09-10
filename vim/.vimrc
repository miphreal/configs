set nocompatible

filetype on
filetype plugin on
filetype indent on

let g:pymode_lint_write = 0
let g:pymode_run_key = 'R'

set tabstop=4
set shiftwidth=4
set smarttab
set expandtab
set softtabstop=4

set autoindent

let python_highlight_all = 1

set t_Co=256

autocmd FileType python set omnifunc=pythoncomplete#Complete
autocmd FileType javascript set omnifunc=javascriptcomplete#CompleteJS
autocmd FileType html set omnifunc=htmlcomplete#CompleteTags
autocmd FileType css set omnifunc=csscomplete#CompleteCSS

function InsertTabWrapper()
 let col = col('.') - 1
 if !col || getline('.')[col - 1] !~ '\k'
 return "\"
 else
 return "\<c-p>"
 endif
endfunction

set complete=""
set complete+=.
set complete+=k
set complete+=b
set complete+=t

autocmd BufWritePre *.py normal m`:%s/\s\+$//e ``

autocmd BufRead *.py set smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class

let g:snippetsEmu_key = "<C-j>"


colorscheme desert
syntax on

"set nu
set mouse=a

set termencoding=utf-8
"set novisualbell

set t_vb=

set backspace=indent,eol,start whichwrap+=<,>,[,]

set showtabline=0

set wrap
set linebreak

set nobackup
set noswapfile
set encoding=utf-8
set fileencodings=utf8,cp1251
set guioptions-=T
set guioptions-=r

set showtabline=2

