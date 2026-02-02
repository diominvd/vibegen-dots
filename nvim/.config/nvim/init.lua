-- Set leader keys for Neovim
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- Load lazy.nvim first (plugin manager)
require("config.lazy")

-- Load core configuration modules in proper order
require("config.options")
require("config.keymaps")
require("config.autocmds")
require("custom_plugins.opencode")
