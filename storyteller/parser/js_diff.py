from pathlib import Path
from tree_sitter import Parser
from tree_sitter_languages import get_language
from storyteller.parser.js_funcs import extract_function_names
from storyteller.parser.js_symbols import extract_symbols

_JS_LANG = get_language("javascript")
_parser = Parser(); _parser.set_language(_JS_LANG)

def diff_functions(old_src: bytes, new_src: bytes)->dict:
    old_set = set(extract_function_names(old_src))
    new_set = set(extract_function_names(new_src))
    return {
        "added": sorted(list(new_set - old_set)),
        "removed": sorted(list(old_set - new_set)),
        "unchanged": sorted(list(old_set & new_set))
    }
def diff_symbols(old_src: bytes, new_src: bytes) -> dict:
    old = extract_symbols(old_src)
    new = extract_symbols(new_src)
    diff = {}
    for kind in ("functions", "classes", "variables"):
        o, n = set(old[kind]), set(new[kind])
        diff[kind] = {
            "added":     sorted(list(n - o)),
            "removed":   sorted(list(o - n)),
            "unchanged": sorted(list(o & n)),
        }
    return diff