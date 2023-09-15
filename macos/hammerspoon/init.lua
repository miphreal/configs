hs.console.clearConsole()

hs.loadSpoon("SpoonInstall")
spoon.SpoonInstall:andUse("ReloadConfiguration", { start = true })
spoon.SpoonInstall:andUse("Keychain")

hs.application.enableSpotlightForNameSearches(true)

local spaces = hs.spaces.spacesForScreen()

local function pretty(arg, msg)
  print("----> ", msg)
  print(hs.inspect.inspect(arg))
  print("<---- ", msg)
end

local function smart_space_switcher(apps, space)
  local apps_map = {}
  for i, app in ipairs(apps) do
    apps_map[app] = i
  end

  local space_id = spaces[space]

  return function()
    local cur_space_id = hs.spaces.focusedSpace()

    -- It's the same space, so just switch between apps
    if cur_space_id == space_id then
      local front_app = hs.application.frontmostApplication()
      local front_app_name = front_app:name()
      front_app:mainWindow():focus()
      local next_app = apps[1]
      local known_app_idx = apps_map[front_app_name]
      if known_app_idx then
        next_app = apps[known_app_idx % #apps + 1]
      end
      hs.application.launchOrFocus(next_app)
      print("focused", next_app)

      local app = hs.application.find(next_app)
      if app then
        local app_spaces = hs.spaces.windowSpaces(app:mainWindow())
        if app_spaces then
          local right_space = false
          for _, val in ipairs(app_spaces) do
            if val == space_id then
              right_space = true
              break
            end
          end

          -- App was declared for this space but appeared on another,
          -- so we want to move it back to the right space
          if not right_space then
            print("incorrect space for", app:name())
            hs.spaces.moveWindowToSpace(app:mainWindow(), space_id)

            print("switch to space", space)
            hs.spaces.gotoSpace(spaces[space])
          end
        end
      end
    else
      -- Switching to another space
      print("switch to space", space)
      hs.eventtap.keyStroke({ "cmd", "ctrl", "alt" }, tostring(space))
      if #apps == 1 then
        print("try to focus", apps[1])
        print("focused", hs.application.launchOrFocus(apps[1]))
      end
    end
  end
end



local conf = {
  spaces = {
    [1] = {
      apps = { "Google Chrome" },
    },
    [2] = {
      apps = { "Kitty" },
    },
    [3] = {
      apps = { "Visual Studio Code" },
    },
    [4] = {
      apps = { "Notion", "Mail", "Calendar" },
    },
    [5] = {
      apps = { "Telegram", "Slack", "Microsoft Teams" },
    },
  },
}

for space_num, space_conf in ipairs(conf.spaces) do
  -- `cmd N` -- go to the N space; if N is the current space, cyrcles through the defined apps
  hs.hotkey.bind({ "cmd" }, tostring(space_num), smart_space_switcher(space_conf.apps, space_num))

  -- use `cmd shift N` to move window to certain space
  hs.hotkey.bind({ "cmd", "shift" }, tostring(space_num), function()
    local active_win = hs.window.frontmostWindow()
    hs.spaces.moveWindowToSpace(active_win, spaces[space_num], true)
  end)
end

hs.layout.apply({
  { "Google Chrome", nil, nil, hs.layout.maximized, nil, nil },
})
