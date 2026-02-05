return {
  dir = vim.fn.stdpath("config") .. "/lua/custom_plugins",
  name = "code-time-tracker",
  lazy = false,

  config = function()
    local stats_file = vim.fn.stdpath("config") .. "/coding-stats.json"
    local stats = {}
    local insert_start = nil
    local current_ft = ""

    -- Load stats
    pcall(function()
      local f = io.open(stats_file, "r")
      if f then
        stats = vim.fn.json_decode(f:read("*all"))
        f:close()
      end
    end)

    -- Save stats
    local function save()
      local f = io.open(stats_file, "w")
      if f then
        f:write(vim.fn.json_encode(stats))
        f:close()
      end
    end

    -- Add time to current filetype
    local function add_time(seconds)
      if current_ft == "" then return end

      local date = os.date("%Y-%m-%d")
      stats[date] = stats[date] or {}
      stats[date][current_ft] = (stats[date][current_ft] or 0) + seconds
    end

    -- Enter insert mode
    vim.api.nvim_create_autocmd("InsertEnter", {
      callback = function()
        current_ft = vim.bo.filetype ~= "" and vim.bo.filetype or "text"
        insert_start = os.time()
      end,
    })

    -- Leave insert mode
    vim.api.nvim_create_autocmd("InsertLeave", {
      callback = function()
        if insert_start then
          local duration = os.time() - insert_start
          add_time(duration)
          insert_start = nil
          save()
        end
      end,
    })

    -- Save on exit
    vim.api.nvim_create_autocmd("VimLeavePre", {
      callback = function()
        -- Save remaining insert time if still in insert mode
        if insert_start then
          local duration = os.time() - insert_start
          add_time(duration)
        end
        save()
      end,
    })

    -- Format seconds to time
    local function format_time(seconds)
      local hours = math.floor(seconds / 3600)
      local mins = math.floor((seconds % 3600) / 60)

      if hours > 0 then
        return string.format("%dh %dm", hours, mins)
      elseif mins > 0 then
        return string.format("%dm", mins)
      else
        return string.format("%ds", seconds)
      end
    end

    -- Lualine component
    _G.code_tracker = {
      get = function()
        local date = os.date("%Y-%m-%d")
        local total = 0

        if stats[date] then
          for _, seconds in pairs(stats[date]) do
            total = total + seconds
          end
        end

        if total >= 10 then -- Show if at least 10 seconds
          return format_time(total)
        end

        return ""
      end
    }

    -- Command to show stats
    vim.api.nvim_create_user_command("CodeStats", function()
      local date = os.date("%Y-%m-%d")
      local lines = { "Typing Time Today:", "" }

      if stats[date] then
        local sorted = {}
        for ft, seconds in pairs(stats[date]) do
          table.insert(sorted, { ft = ft, seconds = seconds })
        end

        table.sort(sorted, function(a, b)
          return a.seconds > b.seconds
        end)

        local total = 0
        for _, item in ipairs(sorted) do
          table.insert(lines, string.format("  %s: %s", item.ft, format_time(item.seconds)))
          total = total + item.seconds
        end

        table.insert(lines, "")
        table.insert(lines, string.format("Total: %s", format_time(total)))
      else
        table.insert(lines, "No typing today!")
      end

      vim.notify(table.concat(lines, "\n"), vim.log.levels.INFO)
    end, {})

    print("Code tracker loaded (insert mode time)")
  end,
}
