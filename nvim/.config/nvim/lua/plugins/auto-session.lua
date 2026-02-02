return {
  'rmagatti/auto-session',
  lazy = false,
  opts = {
    log_level = 'error',
    auto_session_enable_last_session = false,
    auto_session_root_dir = vim.fn.stdpath('data') .. '/sessions/',
    auto_session_enabled = true,
    auto_save_enabled = true,
    auto_restore_enabled = true,
    auto_session_suppress_dirs = { '~/', '~/Downloads', '/tmp' },
    auto_session_use_git_branch = false,
    pre_save_cmds = {
      function()
        vim.cmd('silent! Neotree close')
      end
    },
    post_restore_cmds = {},
  },
}
