return {
  "nvim-neo-tree/neo-tree.nvim",
  branch = "v3.x",
  dependencies = {
    "nvim-lua/plenary.nvim",
    "nvim-tree/nvim-web-devicons",
    "MunifTanjim/nui.nvim",
  },
  lazy = false,
  config = function()
    require("neo-tree").setup({
      window = {
        position = "left",
        width = "35",
        mappings = {
          ["l"] = "open",
          ["h"] = "close_node"
        }
      },
      filesystem = {
        filtered_items = {
          visible = true,
        },
        follow_current_file = { enabled = true },
        hijack_netrw_behavior = "open_default",
      },
      default_component_configs = {
        git_status = {
          highlight = "NeoTreeGitStatus",
          symbols = {
            added     = "✚",
            modified  = "",
            deleted   = "✖",
            untracked = "",
            ignored   = "",
            unstaged  = "󰄱",
            staged    = "",
            conflict  = "",
          }
        },
      },
    })

    local colors = {
      add    = "#88b369",
      change = "#92a1b1",
      delete = "#b36969",
    }

    local groups = {
      NeoTreeGitAdded = colors.add,
      NeoTreeGitModified = colors.change,
      NeoTreeGitDeleted = colors.delete,
      NeoTreeGitUntracked = colors.add,
      NeoTreeGitStatusAdded = colors.add,
      NeoTreeGitStatusModified = colors.change,
      NeoTreeGitStatusDeleted = colors.delete,
    }

    for group, color in pairs(groups) do
      vim.api.nvim_set_hl(0, group, { fg = color, force = true })
    end

    vim.api.nvim_create_autocmd("VimEnter", {
      desc = "Open Neo-tree on startup",
      group = vim.api.nvim_create_augroup("NeotreeAutoOpen", { clear = true }),
      callback = function()
        local no_args = vim.fn.argc() == 0
        local is_dir = vim.fn.argc() == 1 and vim.fn.isdirectory(vim.fn.argv(0)) == 1

        if no_args or is_dir then
          vim.cmd("Neotree show")
        end
      end,
    })

    vim.keymap.set("n", "<leader>e", ":Neotree toggle<CR>", { desc = "Toggle Neo-tree" })
    vim.keymap.set("n", "<leader>o", ":Neotree focus<CR>", { desc = "Focus to Neo-tree" })
  end
}
