-- khr1st's neovim config
-- keymaps are in lua/config/mappings.lua
-- install a patched font & ensure your terminal supports glyphs
-- enjoy :D

-- auto install vim-plug and plugins, if not found
local data_dir = vim.fn.stdpath('data')
if vim.fn.empty(vim.fn.glob(data_dir .. '/site/autoload/plug.vim')) == 1 then
  vim.cmd('silent !curl -fLo ' .. data_dir .. '/site/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim')
  vim.o.runtimepath = vim.o.runtimepath
  vim.cmd('autocmd VimEnter * PlugInstall --sync | source $MYVIMRC')
end

local Plug = vim.fn['plug#']

vim.g.start_time = vim.fn.reltime()
vim.loader.enable()

vim.call('plug#begin')

-- colorschemes, ui, misc
Plug('catppuccin/nvim', { ['as'] = 'catppuccin' })
Plug('ellisonleao/gruvbox.nvim', { ['as'] = 'gruvbox' })
Plug('uZer/pywal16.nvim', { ['as'] = 'pywal16' })
Plug('nvim-lualine/lualine.nvim')
Plug('nvim-tree/nvim-web-devicons')
Plug('folke/which-key.nvim')
Plug('romgrk/barbar.nvim')
Plug('goolord/alpha-nvim')
Plug('nvim-treesitter/nvim-treesitter')
Plug('mfussenegger/nvim-lint')
Plug('nvim-tree/nvim-tree.lua')
Plug('windwp/nvim-autopairs')
Plug('lewis6991/gitsigns.nvim')
Plug('numToStr/Comment.nvim')
Plug('norcalli/nvim-colorizer.lua')
Plug('ibhagwan/fzf-lua')
Plug('numToStr/FTerm.nvim')
Plug('ron-rs/ron.vim')
Plug('MeanderingProgrammer/render-markdown.nvim')
Plug('emmanueltouzery/decisive.nvim')
Plug('folke/twilight.nvim')

-- LaTeX stack
Plug('SirVer/ultisnips')
Plug('lervag/vimtex')
Plug('KeitaNakamura/tex-conceal.vim')

vim.call('plug#end')

-- ========== Settings ==========

-- UltiSnips
vim.g.UltiSnipsExpandTrigger = '<tab>'
vim.g.UltiSnipsJumpForwardTrigger = '<tab>'
vim.g.UltiSnipsJumpBackwardTrigger = '<s-tab>'

-- VimTeX
vim.g.tex_flavor = 'latex'
vim.g.vimtex_view_method = 'zathura'
vim.g.vimtex_quickfix_mode = 0

-- tex-conceal
vim.opt.conceallevel = 1
vim.g.tex_conceal = 'abdmg'
vim.cmd [[highlight Conceal ctermbg=none]]

-- Spellcheck
vim.opt.spell = true
vim.opt.spelllang = { 'en_us' }

-- Spelling fix shortcut
vim.keymap.set('i', '<C-l>', '<c-g>u<Esc>[s1z=`]a<c-g>u', { silent = true })

-- Your modular config continues
require("config.theme")
require("config.mappings")
require("config.options")
require("config.autocmd")
...
