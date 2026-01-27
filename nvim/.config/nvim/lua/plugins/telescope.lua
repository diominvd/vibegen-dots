return {
  "nvim-telescope/telescope.nvim",
  dependencies = { "nvim-lua/plenary.nvim" },
  config = function()
    local telescope = require("telescope")
    local builtin = require("telescope.builtin")

    telescope.setup({
      defaults = {
        borderchars = { "─", "│", "─", "│", "┌", "┐", "┘", "└" },
      }
    })
    vim.keymap.set("n", "<leader>ff", function()
      builtin.find_files({
        hidden = true,
        no_ignore = false
      })
    end, { desc = "Find Files" })
    vim.keymap.set("n", "<leader>fg", function()
      builtin.live_grep({
        additional_args = function()
          return { "--hidden" }
        end
      })
    end, { desc = "Live Grep" })
    vim.keymap.set("n", "<leader>fb", builtin.buffers, { desc = "Telescope Buffers" })
    vim.keymap.set("n", "<leader>fk", builtin.keymaps, { desc = "Search keybinds" })
  end
}
