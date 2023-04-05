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
    "left_option": {"left_alt"},
    "right_option": {"right_alt"},
    "left_command": {"left_gui"},
    "right_command": {"right_gui"},
}

def replace_aliases(keys: set[str]):
    cleared = keys.copy()
    for key, aliases in KEY_ALIASES.items():
        if keys & aliases:
            cleared -= aliases
            cleared.add(key)
    return cleared
        

def expand_modifiers(modifiers: set[str]):
    expanded = replace_aliases(modifiers)
    for short_name, group in reversed(MODIFIER_GROUPS.items()):
        if short_name in expanded:
            expanded.remove(short_name)
            expanded.update(group)
    return expanded


def reduce_modifiers(modifiers: set[str]):
    reduced = modifiers.copy()
    for short_name, group in MODIFIER_GROUPS.items():
        if  group.issubset(reduced):
            reduced -= group
            reduced.add(short_name)
    if "any" in reduced:
        return {"any"}
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
    from_modifiers = set()
    from_opt_modifiers = set()

    from_, _, simul = from_.partition("||") 

    key_combination = from_.split() 
    from_key = None

    exclude_modifiers = set()
    
    for k in key_combination:
        optional = '?' in k
        exclude = k.startswith('-')
        k = k.replace('?', '').replace('-', '').strip()
        if exclude and k in MODIFIERS:
            exclude_modifiers.add(k)
        elif exclude:
            raise Exception(f"Cannot exclude non-modifiers: {k}")
        elif k in MODIFIERS:
            if optional:
                from_opt_modifiers.add(k)
            elif from_key is None:
                from_key = k
            else:
                from_modifiers.add(k)
        else:
            from_key = k

    if exclude_modifiers:
        exclude_modifiers = expand_modifiers(exclude_modifiers)
        assert 'any' not in exclude_modifiers

        from_modifiers = expand_modifiers(from_modifiers)
        from_opt_modifiers = expand_modifiers(from_opt_modifiers)

        from_modifiers -= exclude_modifiers
        from_opt_modifiers -= exclude_modifiers

        from_modifiers = reduce_modifiers(from_modifiers)
        from_opt_modifiers = reduce_modifiers(from_opt_modifiers)

    simultaneous_keys = []
    if simul.strip():
        simultaneous_keys = [key(k) for k in simul.split()]

    from_def: dict[str, t.Any]

    if from_key in {"key_code", "consumer_key_code", "pointing_button"}:
        from_def = {"any": from_key}
    elif from_key:
        from_def = key(from_key)
    else:
        raise Exception(f"Incorrect {from_} sorce key definition")

    assert list(from_def.keys())[0] in {"key_code", "consumer_key_code", "pointing_button", "any"}

    if from_modifiers:
        from_def["modifiers"] = {"mandatory": list(from_modifiers)}
    if from_opt_modifiers:
        from_def.setdefault("modifiers", {})
        from_def["modifiers"]["optional"] = list(from_opt_modifiers)

    if simultaneous_keys:
        from_def["simultaneous"] = simultaneous_keys

    if simul_opts:
        from_def["simultaneous_options"] = simul_opts

    return from_def



def rule(from_: str, to_: t.Any = None, from_simul_opts: dict | None = None, **to_opts):
    from_def = rule_from_def(from_, simul_opts=from_simul_opts)

    if  len(from_def) == 1 and isinstance(to_, str):
        return {"from": from_def, "to": [key(to_)]}

    if isinstance(to_, str):
        to_opts['to'] = [key(to_)]
    return {"type": "basic", "from": from_def, **to_opts}


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



karabiner_conf = {
    "global": {
        "ask_for_confirmation_before_quitting": True,
        "check_for_updates_on_startup": False,
        "show_in_menu_bar": True,
        "show_profile_name_in_menu_bar": False,
        "unsafe_ui": False,
    },
    "profiles": [
        profile(
            "Default",
            selected=True,
            rules=[
                # Simple remaps
                rule("non_us_backslash", "grave_accent_and_tilde"),
                # Fn keys
                rule("f1", "display_brightness_decrement"),
                rule("f2", "display_brightness_increment"),
                rule("f3", "mission_control"),
                rule("f4", "spotlight"),
                rule("f5", "illumination_down"),
                rule("f6", "illumination_up"),
                rule("f7", "rewind"),
                rule("f8", "play_or_pause"),
                rule("f9", "fast_forward"),
                rule("f10", "mute"),
                rule("f11", "volume_decrement"),
                rule("f12", "volume_increment"),
                # Complex rules
                rule("h left_control ?any", "left_arrow"),
                rule("j left_control ?any", "down_arrow"),
                rule("k left_control ?any", "up_arrow"),
                rule("l left_control ?any", "right_arrow"),
                # Caps Lock -> Ctrl or Esc (if pressed alone)
                rule("caps_lock ?any -right_shift", "left_control", to_if_alone=[key("escape")]),
                # Caps Lock + Right Shift -> toggle Caps Lock
                rule("caps_lock right_shift", "caps_lock"),
            ],
        ),
    ],
}


def karabiner(conf):
    conf['brew::karabiner-elements']
    conf(config=conf['path::{{ user.config }}/karabiner/karabiner.json'])

    with (Path(__file__).parent / 'karabiner.json').open('wt') as f:
        json.dump(karabiner_conf, f, sort_keys=True, indent=4)

    conf.render('karabiner.json', conf.config)

