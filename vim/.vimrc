set nocompatible

"Включаем распознавание типов файлов и типо-специфичные плагины:
filetype on
filetype plugin on

"Настройки табов для Python, согласно рекоммендациям
set tabstop=4 
set shiftwidth=4
set smarttab
set expandtab "Ставим табы пробелами
set softtabstop=4 "4 пробела в табе

"Автоотступ
set autoindent

"Подсвечиваем все что можно подсвечивать
let python_highlight_all = 1

"Включаем 256 цветов в терминале, мы ведь работаем из иксов?
"Нужно во многих терминалах, например в gnome-terminal
set t_Co=256

"Настройка omnicomletion для Python (а так же для js, html и css)
autocmd FileType python set omnifunc=pythoncomplete#Complete
autocmd FileType javascript set omnifunc=javascriptcomplete#CompleteJS
autocmd FileType html set omnifunc=htmlcomplete#CompleteTags
autocmd FileType css set omnifunc=csscomplete#CompleteCSS

"Авто комплит по табу
function InsertTabWrapper()
 let col = col('.') - 1
 if !col || getline('.')[col - 1] !~ '\k'
 return "\"
 else
 return "\<c-p>"
 endif
endfunction

imap  <c-r>=InsertTabWrapper()"Показываем все полезные опции автокомплита сразу
set complete=""
set complete+=.
set complete+=k
set complete+=b
set complete+=t

"Перед сохранением вырезаем пробелы на концах (только в .py файлах)
autocmd BufWritePre *.py normal m`:%s/\s\+$//e ``

"В .py файлах включаем умные отступы после ключевых слов
autocmd BufRead *.py set smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class

"вместо tab по умолчанию (на табе автокомплит)
let g:snippetsEmu_key = "<C-j>"

" Копи/паст по Ctrl+C/Ctrl+V
vmap <C-C> "+yi
imap <C-V> "+gPi

colorscheme desert "Цветовая схема
syntax on "Включить подсветку синтаксиса

"set nu "Включаем нумерацию строк
set mouse=a "Включить поддержку мыши

set termencoding=utf-8 "Кодировка терминала
"set novisualbell "Не мигать 

set t_vb= "Не пищать! (Опции 'не портить текст', к сожалению, нету)

"Удобное поведение backspace
set backspace=indent,eol,start whichwrap+=<,>,[,]

"Вырубаем черточки на табах
set showtabline=0

"Колоночка, чтобы показывать плюсики для скрытия блоков кода:
"set foldcolumn=1

"Переносим на другую строчку, разрываем строки
set wrap
set linebreak

"Вырубаем .swp и ~ (резервные) файлы
set nobackup
set noswapfile
set encoding=utf-8 " Кодировка файлов по умолчанию
set fileencodings=utf8,cp1251 " Возможные кодировки файлов, если файл не в unicode кодировке
set guioptions-=T " Toggle Toolbar
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
