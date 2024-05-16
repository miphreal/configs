hs.console.clearConsole()

hs.loadSpoon("SpoonInstall")
spoon.SpoonInstall:andUse("ReloadConfiguration", { start = true })

hs.application.enableSpotlightForNameSearches(true)

--[[
  TODO:
    - autofocus top window when moving cursor from one screen to another
]]--

--
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

function cur_space_wins()
  local wins = hs.window.orderedWindows() -- returns wins in current space only
  local cur_wins = {}
  pretty(wins, "wins")

  for _, win in ipairs(wins) do
    if win:title() then
      table.insert(cur_wins, win)
    end
  end

  return cur_wins
end

pretty(cur_space_wins())

local conf = {
  spaces = {
    [1] = {
      apps = { "Arc" },
    },
    [2] = {
      apps = { "Kitty", "Visual Studio Code" },
    },
    [3] = {
      apps = { "Obsidian", "Notion" },
5   },
    [4] = {
      apps = { "Mail", "Calendar" },
    },
    [5] = {
      apps = { "Telegram", "Slack", "Microsoft Teams" },
    },
    [6] = {apps={}},
    [7] = {apps={}},
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

--
-- Drag window under cursor (cmd + left mouse)
--
draggable_win = {
  win = nil,
  drag_event = hs.eventtap.new({ hs.eventtap.event.types.leftMouseDragged }, function(e)
    if not draggable_win.win then
      return nil
    end

    local dx = e:getProperty(hs.eventtap.event.properties.mouseEventDeltaX)
    local dy = e:getProperty(hs.eventtap.event.properties.mouseEventDeltaY)

    draggable_win.win:move({ dx, dy }, nil, false, 0)
  end),

  kb_event = hs.eventtap.new({ hs.eventtap.event.types.flagsChanged }, function(e)
    local flags = e:getFlags()

    if flags.cmd then
      draggable_win.win = get_window_under_mouse()
      draggable_win.drag_event:start()
    else
      draggable_win.win = nil
      draggable_win.drag_event:stop()
    end
  end),

  start = function()
    draggable_win.kb_event:start()
  end,
}

function get_window_under_mouse()
  local pos = hs.geometry.new(hs.mouse.getAbsolutePosition())
  local screen = hs.mouse.getCurrentScreen()

  return hs.fnutils.find(hs.window.orderedWindows(), function(w)
    return screen == w:screen() and pos:inside(w:frame())
  end)
end

-- draggable_win.start()
