set nocompatible

filetype on
filetype plugin on

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

imap  <c-r>=InsertTabWrapper()
set complete=""
set complete+=.
set complete+=k
set complete+=b
set complete+=t

autocmd BufWritePre *.py normal m`:%s/\s\+$//e ``

autocmd BufRead *.py set smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class

let g:snippetsEmu_key = "<C-j>"

vmap <C-C> "+yi
imap <C-V> "+gPi

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

" CTRL-Tab is Next tab
nnoremap <C-Tab> :tabnext<CR>
" CTRL-Shift-Tab is Previous tab
nnoremap <C-S-Tab> :tabprevious<CR>
" use Alt-Left and Alt-Right to move current tab to left or right
nnoremap <silent> <A-Left> :execute 'silent! tabmove ' . (tabpagenr()-2)<CR>
nnoremap <silent> <A-Right> :execute 'silent! tabmove ' . tabpagenr()<CR>
" CTRL-F4 is :tabclose
nnoremap <C-F4> :tabclose<CR>
set showtabline=2
" Tab is Next window
nnoremap <Tab> <C-W>w
" Shift-Tab is Previous window
 nnoremap <S-Tab> <C-W>W
