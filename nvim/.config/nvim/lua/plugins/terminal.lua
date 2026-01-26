return {
    'akinsho/toggleterm.nvim',
    version = "*",
    config = function()
        require("toggleterm").setup({
            size = 10,
            open_mapping = [[<C-t>]],
            direction = 'horizontal',
            start_in_insert = true,
            persist_size = true,
        })

        function _G.set_terminal_keymaps()
            local opts = {buffer = 0}
            vim.keymap.set('t', '<esc>', [[<C-\><C-n>]], opts)
            vim.keymap.set('t', '<C-h>', [[<C-\><C-n><C-w>h]], opts)
            vim.keymap.set('t', '<C-j>', [[<C-\><C-n><C-w>j]], opts)
            vim.keymap.set('t', '<C-k>', [[<C-\><C-n><C-w>k]], opts)
            vim.keymap.set('t', '<C-l>', [[<C-\><C-n><C-w>l]], opts)
            vim.keymap.set("t", "<leader>k", [[<C-\><C-n>2<C-w>w]], { desc = "Jump to code" })
        end

        vim.api.nvim_create_autocmd("TermOpen", {
            pattern = "term://*",
            callback = function()
                _G.set_terminal_keymaps()
            end,
        })

        vim.keymap.set('n', '<C-Up>', ':resize +2<CR>')
        vim.keymap.set('n', '<C-Down>', ':resize -2<CR>')
    end
}
