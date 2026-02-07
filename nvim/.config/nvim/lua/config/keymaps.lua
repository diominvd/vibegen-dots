-- -----------------------------------------------------
-- Remapping
-- -----------------------------------------------------
vim.keymap.set("x", "p", [["_dP"]])

-- -----------------------------------------------------
-- Save & Exit Commands (Leader + w/q)
-- -----------------------------------------------------
vim.keymap.set("n", "<leader>w", ":w<CR>", { noremap = true, desc = "Save current file" })
vim.keymap.set("n", "<leader>wq", ":wqa<CR>", { noremap = true, desc = "Save all and exit" })
vim.keymap.set("n", "<leader>qq", ":qa!<CR>", { noremap = true, desc = "Exit without saving" })
vim.keymap.set("n", "<leader>er", ":e!<CR>", { noremap = true, desc = "Reload current file (force)" })

-- -----------------------------------------------------
-- Insert Mode Escape
-- -----------------------------------------------------
vim.keymap.set("i", "jk", "<Esc>", { noremap = true, desc = "Exit insert mode" })
vim.keymap.set("i", "kj", "<Esc>", { noremap = true, desc = "Exit insert mode" })

-- -----------------------------------------------------
-- Window Navigation (Ctrl + hjkl)
-- -----------------------------------------------------
vim.keymap.set("n", "<C-h>", "<C-w>h", { noremap = true, desc = "Navigate to left window" })
vim.keymap.set("n", "<C-j>", "<C-w>j", { noremap = true, desc = "Navigate to bottom window" })
vim.keymap.set("n", "<C-k>", "<C-w>k", { noremap = true, desc = "Navigate to top window" })
vim.keymap.set("n", "<C-l>", "<C-w>l", { noremap = true, desc = "Navigate to right window" })

-- -----------------------------------------------------
-- Search
-- -----------------------------------------------------
vim.keymap.set("n", "<Esc>", ":noh<CR>", { noremap = true, desc = "Clear search highlights" })
vim.keymap.set("n", "n", "nzzzv", { noremap = true, desc = "Next search result (centered)" })
vim.keymap.set("n", "N", "Nzzzv", { noremap = true, desc = "Previous search result (centered)" })

-- -----------------------------------------------------
-- Visual Mode: Indentation & Block Movement
-- -----------------------------------------------------
vim.keymap.set("v", "<", "<gv", { noremap = true, desc = "Decrease indentation (keep selection)" })
vim.keymap.set("v", ">", ">gv", { noremap = true, desc = "Increase indentation (keep selection)" })
vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv", { noremap = true, desc = "Move selection down" })
vim.keymap.set("v", "K", ":m '<-2<CR>gv=gv", { noremap = true, desc = "Move selection up" })

-- -----------------------------------------------------
-- Line Operations
-- -----------------------------------------------------
vim.keymap.set({ "n", "v" }, "<leader>d", "\"_d", { noremap = true, desc = "Remove to black hole" })
vim.keymap.set({ "n", "v" }, "<leader>y", "yy", { noremap = true, desc = "Yank current line" })
vim.keymap.set("n", "Y", "y$", { noremap = true, desc = "Yank to end of line" })

-- -----------------------------------------------------
-- Window Management
-- -----------------------------------------------------
vim.keymap.set("n", "<leader>sv", ":vsplit<CR>", { noremap = true, desc = "Split window vertically" })
vim.keymap.set("n", "<leader>sh", ":split<CR>", { noremap = true, desc = "Split window horizontally" })
vim.keymap.set("n", "<leader>q", ":close<CR>", { noremap = true, desc = "Close current split" })
