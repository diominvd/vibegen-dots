return {
  "nvim-neo-tree/neo-tree.nvim",
  branch = "v3.x",
  dependencies = {
    "nvim-lua/plenary.nvim",
    "nvim-tree/nvim-web-devicons",
    "MunifTanjim/nui.nvim",
  },
  config = function()
    require("neo-tree").setup({
      hide_root_node = true,
      retain_hidden_root_indent = false,

      window = {
        width = 40,
        mappings = {
          ["l"] = "open",
          ["h"] = "close_node",
        }
      },

      default_component_configs = {
        indent = {
          with_expanders = false,
          expander_collapsed = "",
          expander_expanded = "",
        },
        icon = {
          folder_closed = "",
          folder_open = "",
          folder_empty = "󰉋",
          highlight = "NeoTreeDirectoryIcon",
        },
        git_status = {
          symbols = {
            added     = "",
            modified  = "",
            deleted   = "",
            renamed   = "",
            untracked = "",
            ignored   = "",
            unstaged  = "",
            staged    = "",
            conflict  = "",
          }
        },
      },

      filesystem = {
        highlight_git_status = "none",
        highlight_opened_files = "none",
        filtered_items = {
          visible = true,
          hide_dotfiles = false,
          hide_gitignored = false,
        },
      },
    })

    local function clean_ui()
      local groups = {
        "NeoTreeNormal",
        "NeoTreeNormalNC",
        "NeoTreeEndOfBuffer",
        "NeoTreeVertSplit",
        "NeoTreeWinSeparator",
        "NeoTreeSignColumn",
      }
      for _, group in ipairs(groups) do
        vim.api.nvim_set_hl(0, group, { bg = "NONE", ctermbg = "NONE" })
      end
    end

    clean_ui()
    vim.api.nvim_create_autocmd("ColorScheme", { callback = clean_ui })

    vim.keymap.set("n", "<leader>e", ":Neotree toggle<CR>", { silent = true })
    vim.keymap.set("n", "<leader>o", ":Neotree focus<CR>", { silent = true })
  end
}
