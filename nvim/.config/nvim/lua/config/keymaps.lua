local keymap = vim.keymap

vim.keymap.set("n", "<leader>k", "2<C-w>w", { desc = "Jump to code" })

vim.keymap.set("n", "<leader>w", ":w<CR>", { desc = "Save" })
vim.keymap.set("n", "<leader>wq", ":wqa<CR>", { desc = "Save and exit" })
vim.keymap.set("n", "<leader>qq", ":qa!<CR>", { desc = "Exit without save" })

vim.keymap.set("i", "jk", "<Esc>", { desc = "Exit insert mode" })
vim.keymap.set("i", "kj", "<Esc>", { desc = "Exit insert mode" })

keymap.set("n", "<C-h>", "<C-w>h", { desc = "Left window" })
keymap.set("n", "<C-j>", "<C-w>j", { desc = "Bottom window" })
keymap.set("n", "<C-k>", "<C-w>k", { desc = "Top window" })
keymap.set("n", "<C-l>", "<C-w>l", { desc = "Right window" })

keymap.set("n", "<Esc>", ":noh<CR>", { desc = "Clear search" })

keymap.set("v", "<", "<gv")
keymap.set("v", ">", ">gv")

keymap.set("v", "J", ":m '>+1<CR>gv=gv")
keymap.set("v", "K", ":m '<-2<CR>gv=gv")

