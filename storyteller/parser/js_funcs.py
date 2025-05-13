from tree_sitter import Parser
from tree_sitter_languages import get_language

_JS_LANG = get_language("javascript") #->uses the pre-compiled grammar
_parser = Parser()
_parser.set_language(_JS_LANG)
print("Parser Ok")
def extract_function_names(source: bytes)->list[str]:
    """
    Returning a list of function/method names in the given js source.
    """
    tree = _parser.parse(source)
    root = tree.root_node
    names: list[str] = []
    def walk(node):
    # 1️⃣  stand-alone function declarations
        if node.type == "function_declaration":
            ident = next((c for c in node.children if c.type == "identifier"), None)
            if ident:
                names.append(source[ident.start_byte : ident.end_byte].decode().strip())

        # 2️⃣  class / object methods  (method_definition)
        elif node.type == "method_definition":
            ident = next(
                (
                    c
                    for c in node.children
                    if c.type in (
                        "property_identifier",          #  baz()
                        "private_property_identifier",  #  #secret()
                        "identifier",                   #  uncommon fallback
                        "property_name"                 #  ["computed"]()  – rarely hit
                    )
                ),
                None,
            )
            if ident:
                names.append(source[ident.start_byte : ident.end_byte].decode().strip())

        # 3️⃣  variable assignments whose initializer is a function / arrow function
        elif node.type == "variable_declarator":
            ident = next((c for c in node.children if c.type == "identifier"), None)
            init  = node.children[-1] if node.children else None
            if (
                ident
                and init
                and init.type in (
                    "arrow_function",
                    "function",
                    "function_expression",
                    "generator_function",
                    "async_function"
                )
            ):
                names.append(source[ident.start_byte : ident.end_byte].decode().strip())

        # recurse
        for child in node.children:
            walk(child)

    walk(root)
    return names 