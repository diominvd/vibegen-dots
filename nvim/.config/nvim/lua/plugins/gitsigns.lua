return {
  "lewis6991/gitsigns.nvim",
  config = function()
    local colors = {
      add    = "#b8bb26",
      change = "#83a598",
      delete = "#fb4934",
    }

    require('gitsigns').setup({
      signs               = {
        add          = { text = '┃' },
        change       = { text = '┃' },
        delete       = { text = '_' },
        topdelete    = { text = '‾' },
        changedelete = { text = '~' },
        untracked    = { text = '┆' },
      },
      signcolumn          = true,
      numhl               = false,
      linehl              = false,
      word_diff           = false,

      watch_gitdir        = {
        interval = 1000,
        follow_files = true
      },
      attach_to_untracked = true,
      current_line_blame  = false,

      on_attach           = function(bufnr)
        local gs = package.loaded.gitsigns

        local function map(mode, l, r, opts)
          opts = opts or {}
          opts.buffer = bufnr
          vim.keymap.set(mode, l, r, opts)
        end

        vim.api.nvim_set_hl(0, 'GitSignsAdd', { fg = colors.add, bg = 'NONE' })
        vim.api.nvim_set_hl(0, 'GitSignsChange', { fg = colors.change, bg = 'NONE' })
        vim.api.nvim_set_hl(0, 'GitSignsDelete', { fg = colors.delete, bg = 'NONE' })

        map('n', ']c', function()
          if vim.wo.diff then return ']c' end
          vim.schedule(function() gs.next_hunk() end)
          return '<Ignore>'
        end, { expr = true })

        map('n', '[c', function()
          if vim.wo.diff then return '[c' end
          vim.schedule(function() gs.prev_hunk() end)
          return '<Ignore>'
        end, { expr = true })
      end,
    })
  end
}
