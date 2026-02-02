return {
  "lambdalisue/suda.vim",
  config = function()
    vim.api.nvim_create_user_command("W", "SudaWrite", {})
  end,
}
