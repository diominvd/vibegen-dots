return {
  'sainnhe/gruvbox-material',
  lazy = false,
  priority = 1000,
  config = function()
    vim.g.gruvbox_material_background = 'hard'
    vim.g.gruvbox_material_foreground = 'material'
    vim.g.gruvbox_material_transparent_background = 1
    vim.g.gruvbox_material_better_performance = 1
    vim.cmd.colorscheme('gruvbox-material')

    local bg_groups = { "Normal", "NormalNC", "SignColumn", "FoldColumn", "NormalFloat" }
    for _, group in ipairs(bg_groups) do
      vim.api.nvim_set_hl(0, group, { bg = "none" })
    end
  end,
}
