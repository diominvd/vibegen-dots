-- ============================================================================
-- Automatic Commands (Autocmds)
-- ============================================================================

local apm_group = vim.api.nvim_create_augroup("APMAutoStart", { clear = true })

vim.api.nvim_create_autocmd("VimEnter", {
  group = apm_group,
  callback = function()
    vim.defer_fn(function()
      local ok, apm = pcall(require, "vim-apm")
      if ok then
        apm:toggle_monitor()
      end
    end, 150)
  end,
})
