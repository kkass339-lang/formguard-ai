from z3 import *

class FormGuardVerifier:
    def __init__(self):
        pass

    def verify_dynamic_code(self, var_name, code_str, rule_str):
        """
        Interpretiert dynamischen Python-Code und Sicherheitsregeln
        und prüft diese mittels Z3 SMT-Solver.
        """
        solver = Solver()
        x = Real(var_name)
        
        eval_globals = {
            "x": x,
            "Real": Real,
            "If": If,
            "And": And,
            "Or": Or,
            "Not": Not
        }
        
        try:
            expr = eval(code_str, eval_globals)
            rule = eval(rule_str, eval_globals)
            
            # Wir ersetzen 'x' in der Regel durch das Ergebnis von 'expr'
            # und suchen nach einem Gegenbeispiel (Not(rule)):
            rule_substituted = substitute(rule, (x, expr))
            solver.add(Not(rule_substituted))
            
            check_result = solver.check()
            
            if check_result == unsat:
                return {
                    "status": "UNSAT",
                    "message": "Verification Successful: Invariant holds strictly across all inputs."
                }
            elif check_result == sat:
                m = solver.model()
                return {
                    "status": "SAT",
                    "message": "CRITICAL VULNERABILITY DETECTED",
                    "counterexample": {
                        "input": str(m[x]),
                        "output": str(expr)
                    }
                }
            else:
                return {
                    "status": "UNKNOWN",
                    "message": "Solver could not determine satisfiability."
                }
        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Syntax or Parsing Error: {str(e)}"
            }