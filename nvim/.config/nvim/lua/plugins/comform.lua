return {
  "stevearc/conform.nvim",
  event = { "BufWritePre" },
  cmd   = { "ConformInfo" },
  keys  = {
    {
      "<leader>f",
      function()
        require("conform").format({ async = true, lsp_fallback = true })
      end,
      mode = "",
      desc = "Format file",
    },
  },
  opts  = {
    formatters_by_ft = {
      python = { "isort", "black" },
      yaml = { "prettier" },
      lua = { "stylua" },
    },
    format_on_save = {
      timeout_ms = 500,
      lsp_fallback = true,
    },
  },
}
