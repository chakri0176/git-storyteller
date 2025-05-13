from tree_sitter import Parser
from tree_sitter_languages import get_language

# Initialize JavaScript parser
_JS_LANG = get_language("javascript")
_PARSER = Parser()
_PARSER.set_language(_JS_LANG)


def extract_symbols(src: bytes) -> dict[str, list[str]]:
    """
    Parse JavaScript source and return a dict with lists of:
      - functions
      - classes
      - variables (non-function initializers)
    """
    tree = _PARSER.parse(src)
    root = tree.root_node
    symbols = {"functions": [], "classes": [], "variables": []}

    def add(name: str, category: str):
        symbols[category].append(name.strip())

    def walk(node):
        t = node.type
        # class declarations
        if t == "class_declaration":
            ident = next((c for c in node.children if c.type == "identifier"), None)
            if ident:
                add(src[ident.start_byte:ident.end_byte].decode(), "classes")

        # function declarations and methods
        if t in ("function_declaration", "method_definition"):
            ident = next((c for c in node.children if c.type in ("identifier", "property_identifier")), None)
            if ident:
                add(src[ident.start_byte:ident.end_byte].decode(), "functions")

        # variable assignments
        if t == "variable_declarator":
            ident = next((c for c in node.children if c.type == "identifier"), None)
            init = node.children[-1] if node.children else None
            func_like = ("arrow_function", "function", "function_expression")
            if ident and init:
                if init.type in func_like:
                    # arrow or function expressions are functions
                    add(src[ident.start_byte:ident.end_byte].decode(), "functions")
                else:
                    # non-function initializers are variables
                    add(src[ident.start_byte:ident.end_byte].decode(), "variables")

        # recurse
        for child in node.children:
            walk(child)

    walk(root)
    # dedupe and sort
    for key in symbols:
        symbols[key] = sorted(set(symbols[key]))
    return symbols
