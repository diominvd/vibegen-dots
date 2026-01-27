return {
  "windwp/nvim-autopairs",
  event = "InsertEnter",
  opts = {
    check_ts = true,
    disable_filetype = { "TelescopePrompt" },
  },
  config = function(_, opts)
    require("nvim-autopairs").setup(opts)
  end
}
