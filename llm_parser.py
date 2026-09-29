import ast

class FunctionParser:
    """Parst Python-Funktionen und extrahiert Parameter sowie den Return-Ausdruck."""
    
    @staticmethod
    def parse_function_str(code_str: str):
        try:
            tree = ast.parse(code_str)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Extrahierte Argument-Namen (z.B. ['price', 'discount'])
                    arg_names = [arg.arg for arg in node.args.args]
                    
                    # Suche nach der Return-Anweisung
                    for sub_node in ast.walk(node):
                        if isinstance(sub_node, ast.Return):
                            # Wandle den AST-Knoten des Return-Ausdrucks zurück in String-Form
                            return_expr = ast.unparse(sub_node.value)
                            return {
                                "func_name": node.name,
                                "args": arg_names,
                                "return_expr": return_expr
                            }
        except Exception as e:
            return {"error": f"AST Parsing Fehler: {str(e)}"}
            
        return {"error": "Keine gültige Python-Funktion mit Return-Statement gefunden."}


if __name__ == "__main__":
    test_code = """
def calculate_discounted_price(price, discount):
    return price - (price * discount * 2)
"""
    result = FunctionParser.parse_function_str(test_code)
    print("AST Parser Test-Ergebnis:", result)