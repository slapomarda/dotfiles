" ==============================
" Inizio vim-plug
" ==============================
call plug#begin('~/.local/share/nvim/plugged')

" Esempio plugin: gruvbox
Plug 'EdenEast/nightfox.nvim'
Plug 'tomasr/molokai'
Plug 'srcery-colors/srcery-vim'
Plug 'flazz/vim-colorschemes'
Plug 'lervag/vimtex'        " il migliore per compilare e navigare file .tex
Plug 'KeitaNakamura/tex-conceal.vim'  " nasconde i comandi per una vista più pulita
Plug 'SirVer/ultisnips'
Plug 'honza/vim-snippets'
" Puoi aggiungere altri plugin qui
" Plug 'tpope/vim-fugitive'
" Plug 'scrooloose/nerdtree'

call plug#end()
" ==============================
" Fine vim-plug
" ==============================


" ==============================
" Configurazioni base per Vim
" ==============================



" Mostra i numeri di riga
set number

" Evidenzia la linea corrente
set cursorline

" Abilita mouse (per selezionare, copiare, trascinare)
set mouse=a

" Evidenzia la sintassi
syntax on
set termguicolors  " Abilita colori veri (24-bit)

" Colore del tema (ne puoi cambiare)
" colorscheme nightfox
let g:srcery_hard_black = '#000000'
let g:srcery_bg = [g:srcery_hard_black,0]
colorscheme srcery
set termguicolors
set background=dark

" Sfondo trasparente+
hi Normal guibg=NONE ctermbg=NONE
hi NonText guibg=NONE ctermbg=NONE




" Indentazione automatica
set smartindent
" lunghezza tab = 2 spazi
set tabstop=2
set shiftwidth=2   " lunghezza rientro automatico
set expandtab       " usa spazi invece di tab

" Ricorda il file e la posizione dell'ultimo cursore
if has("autocmd")
  au BufReadPost * if line("'\"") > 0 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif

" Mostra la barra di stato sempre
set laststatus=2

" Ignora maiuscole/minuscole nella ricerca
set ignorecase
set smartcase

" Undo infinito anche dopo chiusura file
set undofile

" Evidenzia le ricerca
set hlsearch

" Mostra i suggerimenti mentre scrivi / cerca
set incsearch

let g:tex_flavor = 'latex'     " default LaTeX
let g:vimtex_view_method = 'zathura' " usa Skim per PDF
let g:vimtex_quickfix_mode = 0    " non aprire quickfix automaticamente
let g:vimtex_compiler_latexmk = {
      \ 'build_dir' : '',
      \ 'callback' : 1,
      \ 'continuous' : 1,
      \ 'executable' : 'latexmk',
      \ 'options' : ['-pdf', '-interaction=nonstopmode', '-synctex=1'],
      \}
set conceallevel=1
let g:tex_conceal = 'abdmg' " nasconde comandi ma mantiene simboli
filetype plugin indent on

augroup vimtex_auto_open
    autocmd!
    " Quando apri un file tex
    autocmd BufReadPost *.tex VimtexCompile
    autocmd BufReadPost *.tex VimtexView
augroup END

" set directory=~/.vim/swap//
set noswapfile

" ==========================
" Auto-clean file LaTeX
" ==========================
augroup latex_clean
  autocmd!
  autocmd BufUnload,BufLeave *.tex call CleanLatexFiles()
augroup END

function! CleanLatexFiles()
  " Prende il nome base del file corrente (senza estensione)
  let l:basename = expand('%:r')

  " Lista delle estensioni da mantenere
  let l:keep = ['tex', 'pdf', 'toc']

  " Trova tutti i file con stesso nome base
  for l:file in split(glob(l:basename . '.*'), '\n')
    let l:ext = fnamemodify(l:file, ':e')
    if index(l:keep, l:ext) == -1
      call delete(l:file)
    endif
  endfor
endfunction

"ROBA PER SNIPPETS
let g:UltiSnipsSnippetDirectories=["UltiSnips"]
let g:UltiSnipsExpandTrigger="<tab>"
let g:UltiSnipsJumpForwardTrigger="<tab>"
let g:UltiSnipsJumpBackwardTrigger="<s-tab>"

" ==============================
" Fine configurazione base
" ==============================
