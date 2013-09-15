const GLib = imports.gi.GLib;

function unpack_priorities_tuple(tuple) {
    return [tuple.get_child_value(0).get_boolean(), tuple.get_child_value(1).get_string()[0], tuple.get_child_value(2).get_boolean(), tuple.get_child_value(3).get_boolean()];
}

function unpack_priorities_dictionary(prio_dict, target) {
    for (let j = 0; j < prio_dict.n_children(); j++) {
        let dict = prio_dict.get_child_value(j);
        for (let i = 0; i < dict.n_children() - 1;) {
            target[dict.get_child_value(i).get_string()[0]] = unpack_priorities_tuple(dict.get_child_value(i + 1));
            i += 2;
        }
    }
}

function pack_priorities_tuple(tuple) {
    let children = [GLib.Variant.new_boolean(tuple[0]), GLib.Variant.new_string(tuple[1]), GLib.Variant.new_boolean(tuple[2]), GLib.Variant.new_boolean(tuple[3])];
    return GLib.Variant.new_tuple(children, children.length);
}

function pack_priorities_dictionary(dict) {
    let array = [];
    for (let key in dict) {
        if(dict.hasOwnProperty(key)) {
            let key_pack = GLib.Variant.new_string(key);
            let value_pack = pack_priorities_tuple(dict[key]);
            array.push(GLib.Variant.new_dict_entry(key_pack, value_pack));
        }
    }
    return GLib.Variant.new_array(GLib.VariantType.new("{s(bsbb)}"), array, array.length);
}
/* vi: set expandtab tabstop=4 shiftwidth=4: */
