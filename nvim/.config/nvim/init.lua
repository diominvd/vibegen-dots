vim.g.mapleader = " "
vim.g.maplocalleader = " "

require("config.options")
require("config.keymaps")
require("config.autocmds")
require("config.lazy")

local function apply_transparency()
    local hl_groups = {
        "Normal", "NormalNC", "NormalFloat",
        "NeoTreeNormal", "NeoTreeNormalNC", "SignColumn", "EndOfBuffer"
    }
    for _, group in ipairs(hl_groups) do
        vim.api.nvim_set_hl(0, group, { bg = "none", ctermbg = "none" })
    end
end

local function reload_theme()
    local matugen_path = vim.fn.expand("$HOME/.config/nvim/lua/colors.lua")

    local f = io.open(matugen_path, "r")
    if f then
        f:close()
        local ok, err = pcall(dofile, matugen_path)
        if not ok then
            vim.notify("Error loading colors.lua: " .. tostring(err), vim.log.levels.ERROR)
        end
    else
        pcall(vim.cmd, 'colorscheme base16')
    end

    package.loaded["plugins.lualine"] = nil
    local status_ok, lualine = pcall(require, "plugins.lualine")

    if status_ok then
        if type(lualine) == "table" and lualine.config then
            lualine.config()
        end
    end

    vim.api.nvim_set_hl(0, "Comment", { italic = true })

    apply_transparency()
end

vim.api.nvim_create_autocmd("Signal", {
    pattern = "SIGUSR1",
    callback = function()
        reload_theme()
        vim.notify("Matugen colors updated!", vim.log.levels.INFO)
    end,
})

reload_theme()
