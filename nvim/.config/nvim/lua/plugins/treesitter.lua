-- Template: Treesitter for Nvim 0.11+
return {
    "nvim-treesitter/nvim-treesitter",
    build = ":TSUpdate",
    event = { "BufReadPost", "BufNewFile" },
    opts = {
        ensure_installed = {
            "python", "lua", "vim", "vimdoc",
            "markdown", "markdown_inline", "bash"
        },
        auto_install = true,

        highlight = {
            enable = true,
            additional_vim_regex_highlighting = false,
        },
        indent = { enable = true },
    },
}
