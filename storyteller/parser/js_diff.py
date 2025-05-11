from pathlib import Path
from tree_sitter import Parser
from tree_sitter_languages import get_language
from storyteller.parser.js_funcs import extract_function_names

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
