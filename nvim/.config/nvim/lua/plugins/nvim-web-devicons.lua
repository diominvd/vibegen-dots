return {
  "nvim-tree/nvim-web-devicons",
  config = function()
    require('nvim-web-devicons').setup({
      -- Включаем глобально
      default = true,
      -- Переопределяем цвета под Gruvbox, если нужно
      override = {
        zsh = {
          icon = "󱆃",
          color = "#8ec07c",
          name = "Zsh"
        },
        -- Можешь добавить специфичные файлы здесь
      },
    })
  end
}
