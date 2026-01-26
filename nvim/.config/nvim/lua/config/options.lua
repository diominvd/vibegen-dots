local opt = vim.opt

-- Interface
opt.number = true                    -- Номера строк
opt.relativenumber = false           -- Относительные номера
opt.signcolumn = "yes"               -- Колонка для git/диагностики
opt.cursorline = true                -- Подсветка строки
opt.scrolloff = 8                    -- Отступ при скролле
opt.wrap = false                     -- Не переносить строки

-- Tabs
opt.tabstop = 2                      -- Ширина таба
opt.shiftwidth = 2                   -- Ширина отступа
opt.expandtab = true                 -- Пробелы вместо табов
opt.smartindent = true               -- Умные отступы

-- Search
opt.ignorecase = true                -- Игнорировать регистр
opt.smartcase = true                 -- Учитывать если есть заглавные
opt.hlsearch = true                  -- Подсветка поиска

-- Other
opt.swapfile = false                 -- Без swap файлов
opt.backup = false                   -- Без backup
opt.undofile = true                  -- Сохранять историю
opt.updatetime = 250                 -- Быстрее обновление
opt.timeoutlen = 300
opt.splitright = true                -- Новые окна справа
opt.splitbelow = true                -- Новые окна снизу
opt.clipboard = "unnamedplus"        -- Системный буфер обмена
opt.mouse = "a"                      -- Мышь

vim.api.nvim_create_autocmd("ColorScheme", {
    pattern = "*",
    callback = function()
        local hl_groups = {
            "Normal", "NonText", "SignColumn", "EndOfBuffer", "MsgArea"
        }
        for _, group in ipairs(hl_groups) do
            vim.api.nvim_set_hl(0, group, { bg = "NONE", ctermbg = "NONE" })
        end
    end,
})
