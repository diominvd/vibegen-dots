return {
  "nvim-lualine/lualine.nvim",
  config = function()
    local colors = {
      bg     = "#282828",
      fg     = "#ebdbb2",
      yellow = "#fabd2f",
      cyan   = "#8ec07c",
      darkbg = "#1d2021",
    }

    require("lualine").setup({
      options = {
        theme = {
          normal = {
            a = { fg = colors.darkbg, bg = colors.fg, gui = "bold" },
            z = { fg = colors.darkbg, bg = colors.fg, gui = "bold" },
            b = { fg = colors.fg, bg = "NONE" },
            c = { fg = colors.fg, bg = "NONE" },
            x = { fg = colors.fg, bg = "NONE" },
            y = { fg = colors.fg, bg = "NONE" },
          },
          insert = { a = { fg = colors.darkbg, bg = colors.cyan, gui = "bold" } },
          visual = { a = { fg = colors.darkbg, bg = colors.yellow, gui = "bold" } },
        },
        component_separators = "",
        section_separators = "",
        globalstatus = true,
      },
      sections = {
        lualine_a = { "mode" },
        lualine_b = { { "filename", path = 1 } },
        lualine_c = { { "diagnostics", color = { bg = "NONE" } } },
        lualine_x = {
          {
            function()
              return _G.code_tracker and _G.code_tracker.get() or ""
            end,
            icon = "󱑁",
            separator = "|"
          },
          "filetype"
        },
        lualine_y = {},
        lualine_z = { "location" },
      },
    })
  end
}
