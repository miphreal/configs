import json
import typing as t
from pathlib import Path

FN_KEYS = [f"f{i}" for i in range(1, 25)]
MODIFIERS = ["caps_lock", "left_command", "left_control", "left_option", "left_shift", "right_command", "right_control", "right_option", "right_shift", "fn", "command", "control", "option", "shift", "left_alt", "left_gui", "right_alt", "right_gui", "any"]

MODIFIER_GROUPS = {
    "command": {"left_command", "right_command"},
    "control": {"left_control", "right_control"},
    "option": {"left_option", "right_option"},
    "shift": {"left_shift", "right_shift"},
    "any": {"fn", "command", "control", "option", "shift"},
}
KEY_ALIASES = {
    "cmd": "command",
    "opt": "option",
    "ctrl": "control",
    "left_alt": "left_option",
    "right_alt": "right_option",
    "left_gui": "left_command",
    "right_gui": "right_command",
}

def uniq(keys: t.Iterable[str]):
    _index: set[str] = set()
    for k in keys:
        if k not in _index:
            _index.add(k)
            yield k

def replace_alias(key: str):
    return KEY_ALIASES.get(key, key)

def replace_aliases(keys: t.Iterable[str]):
    for k in keys:
        yield replace_alias(k)


def expand_modifiers(modifiers: t.Iterable[str]):
    expanded = list(uniq(replace_aliases(modifiers)))
    for short_name, group in reversed(MODIFIER_GROUPS.items()):
        if short_name in expanded:
            idx = expanded.index(short_name)
            expanded[idx: idx + 1] = group
    return expanded


def reduce_modifiers(modifiers: list[str]):
    reduced = modifiers.copy()

    for short_name, group in MODIFIER_GROUPS.items():
        if group.issubset(reduced):
            idx = min(reduced.index(k) for k in group)
            for k in group:
                reduced.remove(k)
            reduced[idx:idx] = [short_name]

    if "any" in reduced:
        return ["any"]

    return reduced



key_sets = dict(
    apple_vendor_keyboard_key_code = ["mission_control", "spotlight", "dashboard", "function", "launchpad", "expose_all", "expose_desktop", "brightness_up", "brightness_down", "language"],
    apple_vendor_top_case_key_code = ["keyboard_fn", "brightness_up", "brightness_down", "video_mirror", "illumination_toggle", "illumination_up", "illumination_down"],
    consumer_key_code = [
         "dictation", "power", "menu", "menu_pick", "menu_up", "menu_down", "menu_left", "menu_right", "menu_escape", "menu_value_increase", "menu_value_decrease", "data_on_screen", "closed_caption", "closed_caption_select", "vcr_or_tv", "broadcast_mode", "snapshot", "still", "picture_in_picture_toggle", "picture_in_picture_swap", "red_menu_button", "green_menu_button", "blue_menu_button", "yellow_menu_button", "aspect", "three_dimensional_mode_select", "display_brightness_increment", "display_brightness_decrement", "fast_forward", "rewind", "scan_next_track", "scan_previous_track", "eject", "play_or_pause", "voice_command", "mute", "volume_increment", "volume_decrement", "al_word_processor", "al_text_editor", "al_spreadsheet", "al_graphics_editor", "al_presentation_app", "al_database_app", "al_email_reader", "al_newsreader", "al_voicemail", "al_contacts_or_address_book", "al_Calendar_Or_Schedule", "al_task_or_project_manager", "al_log_or_journal_or_timecard", "al_checkbook_or_finance", "al_calculator", "al_a_or_v_capture_or_playback", "al_local_machine_browser", "al_lan_or_wan_browser", "al_internet_browser", "al_remote_networking_or_isp_connect", "al_network_conference", "al_network_chat", "al_telephony_or_dialer", "al_logon", "al_logoff", "al_logon_or_logoff", "al_control_panel", "al_command_line_processor_or_run", "al_process_or_task_manager", "al_select_task_or_application", "al_next_task_or_application", "al_previous_task_or_application", "al_preemptive_halt_task_or_application", "al_integrated_help_center", "al_documents", "al_thesaurus", "al_dictionary", "al_desktop", "al_spell_check", "al_grammer_check", "al_wireless_status", "al_keyboard_layout", "al_virus_protection", "al_encryption", "al_screen_saver", "al_alarms", "al_clock", "al_file_browser", "al_power_status", "al_image_browser", "al_audio_browser", "al_movie_browser", "al_digital_rights_manager", "al_digital_wallet", "al_instant_messaging", "al_oem_feature_browser", "al_oem_help", "al_online_community", "al_entertainment_content_browser", "al_online_shopping_browswer", "al_smart_card_information_or_help", "al_market_monitor_or_finance_browser", "al_customized_corporate_news_browser", "al_online_activity_browswer", "al_research_or_search_browswer", "al_audio_player", "al_message_status", "al_contact_sync", "al_navigation", "al_contextaware_desktop_assistant", "ac_home", "ac_back", "ac_forward", "ac_refresh", "ac_bookmarks", "fastforward",
    ],
    pointing_button = [f"button{i}" for i in range(1, 33)],
    key_code = [
          "left_option", "left_command", "right_option", "right_command", "japanese_eisuu", "japanese_kana", "japanese_pc_nfer", "japanese_pc_xfer", "japanese_pc_katakana", "vk_none", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "return_or_enter", "escape", "delete_or_backspace", "tab", "spacebar", "hyphen", "equal_sign", "open_bracket", "close_bracket", "backslash", "non_us_pound", "semicolon", "quote", "grave_accent_and_tilde", "comma", "period", "slash", "caps_lock", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "print_screen", "scroll_lock", "pause", "insert", "home", "page_up", "delete_forward", "end", "page_down", "right_arrow", "left_arrow", "down_arrow", "up_arrow", "keypad_num_lock", "keypad_slash", "keypad_asterisk", "keypad_hyphen", "keypad_plus", "keypad_enter", "keypad_1", "keypad_2", "keypad_3", "keypad_4", "keypad_5", "keypad_6", "keypad_7", "keypad_8", "keypad_9", "keypad_0", "keypad_period", "non_us_backslash", "application", "power", "keypad_equal_sign", "f13", "f14", "f15", "f16", "f17", "f18", "f19", "f20", "f21", "f22", "f23", "f24", "execute", "help", "menu", "select", "stop", "again", "undo", "cut", "copy", "paste", "find", "mute", "volume_down", "volume_up", "locking_caps_lock", "locking_num_lock", "locking_scroll_lock", "keypad_comma", "keypad_equal_sign_as400", "international1", "international2", "international3", "international4", "international5", "international6", "international7", "international8", "international9", "lang1", "lang2", "lang3", "lang4", "lang5", "lang6", "lang7", "lang8", "lang9", "alternate_erase", "sys_req_or_attention", "cancel", "clear", "prior", "return", "separator", "out", "oper", "clear_or_again", "cr_sel_or_props", "ex_sel", "left_control", "left_shift", "left_alt", "left_gui", "right_control", "right_shift", "right_alt", "right_gui",
    ]
)

def key(k: str):
    k = k.lower().strip()
    for n, k_set in key_sets.items():
        if k in k_set:
            return {n: k}

    return {"key_code": k}


def is_fn_rule(data: dict):
    return (
        data.get("type") is None
        and data["from"].get("key_code", "") in FN_KEYS
    )

def is_simple_rule(data: dict):
    return (
        data.get("type") is None
        and not is_fn_rule(data)
    )




def rule_from_def(from_: str, simul_opts: dict | None = None):
    keys: list[str] = []
    modifiers: list[str] = []
    optional_modifiers: list[str] = []
    exclude_modifiers = set()

    for k in from_.split() :
        optional = '?' in k
        exclude = k.startswith('-')
        k = replace_alias(k.replace('?', '').replace('-', '').strip())

        if (exclude or optional) and k not in MODIFIERS:
            raise Exception(f"{k} must be a modifier")

        if k in MODIFIERS:
            if exclude:
                exclude_modifiers.add(k)
            elif optional:
                optional_modifiers.append(k)
            else:
                modifiers.append(k)
        else:
            keys.append(k)

    modifiers = expand_modifiers(modifiers)
    optional_modifiers = expand_modifiers(optional_modifiers)

    if exclude_modifiers:
        exclude_modifiers = expand_modifiers(exclude_modifiers)
        assert 'any' not in exclude_modifiers
        modifiers = [k for k in modifiers if k not in exclude_modifiers]
        optional_modifiers = [k for k in optional_modifiers if k not in exclude_modifiers]

    modifiers = reduce_modifiers(modifiers)
    optional_modifiers = reduce_modifiers(optional_modifiers)

    from_def: dict[str, t.Any] = {}

    special_any_keys = {"key_code", "consumer_key_code", "pointing_button"}
    regular_keys = [k for k in keys if k not in special_any_keys]
    any_keys = [k for k in keys if k in special_any_keys]

    if regular_keys and any_keys:
        raise Exception(f"Please specify either 'any' or regular keys, not both")
    if len(any_keys) > 1:
        raise Exception("Please specify single 'any' key")

    if len(regular_keys) == 1:
        from_def.update(key(regular_keys[0]))
    elif len(regular_keys) > 1:
        from_def["simultaneous"] = [key(k) for k in regular_keys]
    elif any_keys:
        from_def["any"] = any_keys[0]
    elif modifiers:
        # only modifiers are defined
        first_modifier = modifiers.pop(0)
        from_def.update(key(first_modifier))
    else:
        raise Exception(f"Invalid spec: {from_}")

    if modifiers:
        from_def["modifiers"] = {"mandatory": sorted(modifiers)}
    if optional_modifiers:
        from_def.setdefault("modifiers", {})
        from_def["modifiers"]["optional"] = sorted(optional_modifiers)

    if simul_opts:
        from_def["simultaneous_options"] = simul_opts

    return from_def


def set_var(name: str, value: str | int | bool):
    return {"set_variable": {"name": name, "value": value}}

def set_lang(lang_code: str):
    return {"select_input_source": {"language": f"^{lang_code}$"}}

def to_sh(command: str):
    return {"shell_command": command}

def to_notification(id: str, msg: str):
    return {"set_notification_message": {"id": id, "text": msg}}

def parse_val(val: str):
    match val:
        case bool_val if bool_val.lower() in {'true', 'false', 'on', 'off'}:
            return bool_val.lower() in {'true', 'on'}
        case int_val if int_val.isdigit():
            return int(int_val)
        case str_val:
            return str_val


def parse_to_def(to_: str) -> dict:
    to_ = to_.strip()
    to_def = {}

    to_events = []
    to_if_alone = []
    to_if_held_down = []

    to_after_key_up = []

    to_specs = to_.split(';')
    for spec in to_specs:
        _to_events = to_events
        spec = spec.strip()

        if spec.startswith('on-held->'):
            _to_events = to_if_held_down
            spec = spec.removeprefix('on-held->')
        elif spec.startswith('on-alone->'):
            _to_events = to_if_alone
            spec = spec.removeprefix('on-alone->')
        elif spec.startswith('on-keyup->'):
            _to_events = to_after_key_up
            spec = spec.removeprefix('on-keyup->')
        elif spec.startswith('on-keydown->'):
            _to_events = to_events
            spec = spec.removeprefix('on-keydown->')

        if spec.startswith('$'):
            # handle setting variables
            spec = spec.removeprefix('$').split('=', 1)
            match spec:
                case [var] if var:
                    val = False if var.endswith('!') else True
                    _to_events.append(set_var(var, val))

                case [var, val]:
                    if '/' in val:
                        val_set, val_unset = val.split('/', 1)
                        _to_events.append(set_var(var, parse_val(val_set)))
                        to_after_key_up.append(set_var(var, parse_val(val_unset)))
                    else:
                        _to_events.append(set_var(var, parse_val(val)))

                case _:
                    raise Exception(f"Unsupported 'to' spec: {spec}")

        elif spec.startswith('lang:'):
            # handle selecting input source
            _to_events.append(set_lang(spec[5:]))

        elif spec.startswith('sh:'):
            # handle sh command target
            _to_events.append(to_sh(spec.removeprefix('sh:')))

        elif spec.startswith('app:'):
            # handle sh command target
            app_name = spec.removeprefix("app:")
            _to_events.append(to_sh(f"open -a '{app_name}'"))

        elif spec.startswith('notify:'):
            # show notification
            _, msg_id, msg = spec.split(':')
            _to_events.append(to_notification(msg_id, msg))

        else:
            _to_events.append(key(spec))

    if to_events:
        to_def['to'] = to_events
    if to_if_alone:
        to_def['to_if_alone'] = to_if_alone
    if to_if_held_down:
        to_def['to_if_held_down'] = to_if_held_down
    if to_after_key_up:
        to_def['to_after_key_up'] = to_after_key_up

    return to_def


def parse_conditions(cond_: str):
    conditions = []

    for spec in cond_.split(','):
        spec = spec.strip()

        neg = spec.startswith('!')
        spec = spec.removeprefix('!')

        if spec.startswith('$'):
            # condition with var
            spec = spec.removeprefix('$')
            match spec.split('=', 1):
                case [var]:
                    val = True
                case [var, val]:
                    val = parse_val(val)
                case _:
                    raise Exception(f"Unsupported condition: {spec}")

            conditions.append({"type": 'variable_unless' if neg else 'variable_if', "name": var, "value": val})

        elif spec.startswith('lang=') or spec in {'en', 'ru', 'pl', 'by'}:
            # language condition
            spec.removeprefix('lang=')
            langs = spec.split('|')
            conditions.append({"type": 'input_source_unless' if neg else 'input_source_if', "input_sources": [{"language": f"^{l}$"} for l in langs]})

        elif spec.startswith('app=') or spec.startswith('^') and spec.endswith('$'):
            # app condition
            conditions.append({"type": 'frontmost_application_unless' if neg else 'frontmost_application_if', "bundle_identifiers": [spec[4:]]})

    return conditions



def rule(def_: str, to_: t.Any = None, from_simul_opts: dict | None = None, **opts):
    rule_def = {}

    if '=>' in def_:
        assert to_ is None
        from_, to_ = def_.split('=>', 1)
        from_ = from_.strip()
        to_ = to_.strip()
    else:
        from_ = def_

    if ':' in from_:
        conditions_, from_ = from_.split(':')
        from_ = from_.strip()
        if parsed := parse_conditions(conditions_):
            rule_def['conditions'] = parsed

    from_def = rule_from_def(from_, simul_opts=from_simul_opts)
    rule_def['from'] = from_def

    if isinstance(to_, str):
        rule_def.update(parse_to_def(to_))

    rule_def.update(opts)

    if len(rule_def) == 2 and len(rule_def["from"]) == 1 and len(rule_def.get('to', [])) == 1:
        # it's a simple definition
        return rule_def

    return {"type": "basic", **rule_def}


def virtual_hid_keyboard():
    pass


def profile(name: str, rules = None, selected = False, **params):
    complex_rules = []
    simple_rules = []
    fn_keys = []

    for r in rules or []:
        if is_fn_rule(r):
            fn_keys.append(r)
        elif is_simple_rule(r):
            simple_rules.append(r)
        else:
            complex_rules.append(r)

    return {
        "name": name,
        "parameters": {
            "delay_milliseconds_before_open_device": 1000,
            **params,
        },
        "selected": selected,
        "simple_modifications": simple_rules or [],
        "complex_modifications": {
            "parameters": {
                "basic.simultaneous_threshold_milliseconds": 50,
                "basic.to_delayed_action_delay_milliseconds": 500,
                "basic.to_if_alone_timeout_milliseconds": 1000,
                "basic.to_if_held_down_threshold_milliseconds": 500,
                "mouse_motion_to_scroll.speed": 100
            },
            "rules": [
                {
                    "description": "Custom complex rules",
                    "manipulators": complex_rules or [],
                }
            ],
        },
        "fn_function_keys": fn_keys or [],
        "virtual_hid_keyboard": {
            "country_code": 0,
            "indicate_sticky_modifier_keys_state": True,
            "mouse_key_xy_scale": 100
        }
    }

def parse_profile(name: str, rules: str, **params):
    parsed_rules = []
    for rule_spec in rules.splitlines():
        rule_spec = rule_spec.strip()
        if rule_spec.startswith('#'):
            continue
        if rule_spec:
            parsed_rules.append(rule(rule_spec))
    return profile(name, rules=parsed_rules, **params)


karabiner_conf = {
    "global": {
        "ask_for_confirmation_before_quitting": True,
        "check_for_updates_on_startup": False,
        "show_in_menu_bar": True,
        "show_profile_name_in_menu_bar": False,
        "unsafe_ui": False,
    },
    "profiles": [
        parse_profile(
            "Default",
            selected=True,
            rules="""
                # Simple remaps
                non_us_backslash => grave_accent_and_tilde

                # Fn keys
                f1 => display_brightness_decrement
                f2 => display_brightness_increment
                f3 => mission_control
                f4 => spotlight
                f5 => illumination_down
                f6 => illumination_up
                f7 => rewind
                f8 => play_or_pause
                f9 => fast_forward
                f10 => mute
                f11 => volume_decrement
                f12 => volume_increment

                # Apps hotkeys
                # cmd 1 => app:Google Chrome
                # cmd 2 => app:kitty
                # cmd 3 => app:Visual Studio Code
                # cmd 4 => app:Mail

                # Complex rules
                !$vim_mode=on: cmd option v => $vim_mode=on
                 $vim_mode=on: cmd option v => $vim_mode=off
                    $vim_mode=on: h left_control => left_arrow
                    $vim_mode=on: j left_control => down_arrow
                    $vim_mode=on: k left_control => up_arrow
                    $vim_mode=on: l left_control => right_arrow

                # Caps Lock => Ctrl or Esc (if pressed alone)
                caps_lock ?any -right_shift -cmd => left_control; on-alone->escape

                # Caps Lock + Right Shift => toggle Caps Lock
                caps_lock right_shift => caps_lock

                # Switch to certain languages
                cmd option l => $lang_mode=on/off
                    $lang_mode=on: e ?any => lang:en
                    $lang_mode=on: r ?any => lang:ru
                    $lang_mode=on: p ?any => lang:pl
            """,
        ),
    ],
}


def karabiner(conf):
    conf['brew::karabiner-elements']
    conf(config=conf['path::{{ user.config }}/karabiner/karabiner.json'])

    with (Path(__file__).parent / 'karabiner.json').open('wt') as f:
        json.dump(karabiner_conf, f, sort_keys=True, indent=4)

    conf.render('karabiner.json', conf.config)

