return {
  -- LSP configuration with Mason package manager
  "neovim/nvim-lspconfig",
  dependencies = {
    "williamboman/mason.nvim",
    "williamboman/mason-lspconfig.nvim",
    "folke/neodev.nvim", -- Add Neovim API support for the linter
  },
  config = function()
    -- Safe neodev connection (prevents nvim from crashing if the plugin is not yet downloaded)
    local neodev_status, neodev = pcall(require, "neodev")
    if neodev_status then
      neodev.setup({
        library = { plugins = { "nvim-dap-ui" }, types = true },
      })
    end

    require("mason").setup()
    require("mason-lspconfig").setup({
      -- Automatic server installation
      ensure_installed = { "pyright", "lua_ls" },
      handlers = {
        -- Default handler for all servers
        function(server_name)
          require("lspconfig")[server_name].setup({})
        end,

        -- Specific settings for Lua (removes Undefined global vim)
        ["lua_ls"] = function()
          require("lspconfig").lua_ls.setup({
            settings = {
              Lua = {
                diagnostics = {
                  -- Tell the linter that 'vim' exists
                  globals = { "vim" },
                },
                workspace = {
                  checkThirdParty = false,
                  -- Connect Neovim runtime
                  library = vim.api.nvim_get_runtime_file("", true),
                },
                telemetry = { enable = false },
              },
            },
          })
        end,
      },
    })

    -- LSP keybindings (attached to buffer when LSP activates)
    vim.api.nvim_create_autocmd("LspAttach", {
      group = vim.api.nvim_create_augroup("UserLspConfig", {}),
      callback = function(ev)
        local opts = { buffer = ev.buf, noremap = true, silent = true }

        -- Navigation
        vim.keymap.set("n", "gd", vim.lsp.buf.definition,
          vim.tbl_extend("force", opts, { desc = "Go to definition" }))
        vim.keymap.set("n", "gD", vim.lsp.buf.declaration,
          vim.tbl_extend("force", opts, { desc = "Go to declaration" }))
        vim.keymap.set("n", "gi", vim.lsp.buf.implementation,
          vim.tbl_extend("force", opts, { desc = "Go to implementation" }))
        vim.keymap.set("n", "gr", vim.lsp.buf.references,
          vim.tbl_extend("force", opts, { desc = "Go to references" }))

        -- Documentation & Hover
        vim.keymap.set("n", "K", vim.lsp.buf.hover,
          vim.tbl_extend("force", opts, { desc = "Show hover documentation" }))
        vim.keymap.set("n", "<leader>lh", vim.lsp.buf.signature_help,
          vim.tbl_extend("force", opts, { desc = "Show signature help" }))

        -- Actions & Refactoring
        vim.keymap.set({ "n", "v" }, "<leader>ca", vim.lsp.buf.code_action,
          vim.tbl_extend("force", opts, { desc = "Code action" }))
        vim.keymap.set("n", "<leader>rn", vim.lsp.buf.rename,
          vim.tbl_extend("force", opts, { desc = "Rename symbol" }))
        vim.keymap.set("n", "<leader>fm", vim.lsp.buf.format,
          vim.tbl_extend("force", opts, { desc = "Format buffer" }))

        -- Diagnostics
        vim.keymap.set("n", "<leader>ld", vim.diagnostic.open_float,
          vim.tbl_extend("force", opts, { desc = "Show line diagnostics" }))
        vim.keymap.set("n", "[d", vim.diagnostic.goto_prev,
          vim.tbl_extend("force", opts, { desc = "Previous diagnostic" }))
        vim.keymap.set("n", "]d", vim.diagnostic.goto_next,
          vim.tbl_extend("force", opts, { desc = "Next diagnostic" }))
        vim.keymap.set("n", "<leader>ll", vim.diagnostic.setloclist,
          vim.tbl_extend("force", opts, { desc = "Set location list" }))
      end,
    })

    -- Global diagnostic display configuration
    vim.diagnostic.config({
      virtual_text = true,
      signs = true,
      underline = true,
      update_in_insert = false,
      severity_sort = true,
    })
  end,
}
