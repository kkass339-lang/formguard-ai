from z3 import *

class FormGuardVerifier:
    def __init__(self):
        pass

    def verify_dynamic_code(self, var_name, code_str, rule_str):
        """
        Interpretiert dynamischen Python-Code und Sicherheitsregeln
        und prüft diese mittels Z3.
        """
        solver = Solver()
        
        # Z3 Variable dynamisch erstellen
        x = Real(var_name)
        
        # Sicherer Ausführungs-Kontext für eval()
        eval_globals = {
            "x": x,
            "Real": Real,
            "If": If,
            "And": And,
            "Or": Or,
            "Not": Not
        }
        
        try:
            # Code-Ausdruck & Regel-Ausdruck sicher auswerten
            y = eval(code_str, eval_globals)
            rule = eval(rule_str, {"x": x, "y": y, "And": And, "Or": Or, "Not": Not})
            
            # Fehlerbedingung dem Solver hinzufügen
            solver.add(rule)
            
            # Prüfen
            if solver.check() == sat:
                model = solver.model()
                
                # Werte aus Z3 Modell auslesen
                input_val = model[x]
                
                # Falls Ausgabe ein Z3-Wert ist, berechnen
                if hasattr(y, 'simplify'):
                    output_val = model.eval(y)
                else:
                    output_val = y
                    
                return {
                    "status": "SAT",
                    "message": "CRITICAL VULNERABILITY DETECTED",
                    "counterexample": {
                        "input": str(input_val),
                        "output": str(output_val)
                    }
                }
            else:
                return {
                    "status": "UNSAT",
                    "message": "CODE MATHEMATICALLY VERIFIED SAFE"
                }
                
        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Syntax- oder Parsing-Fehler: {str(e)}"
            }