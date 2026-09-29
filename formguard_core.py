from z3 import Solver, Real, sat, unsat, Not

class MultiVariableFormGuard:
    def __init__(self):
        self.solver = Solver()
        self.variables = {}

    def get_var(self, var_name: str):
        if var_name not in self.variables:
            self.variables[var_name] = Real(var_name)
        return self.variables[var_name]

    def verify_invariant(self, code_expr_str: str, invariant_str: str, var_names: list):
        self.solver.reset()
        var_dict = {name: self.get_var(name) for name in var_names}
        
        if "price" in var_dict:
            self.solver.add(var_dict["price"] >= 0)
        if "discount" in var_dict:
            self.solver.add(var_dict["discount"] >= 0, var_dict["discount"] <= 1.0)

        final_price = Real("final_price")
        eval_scope = {**var_dict, "final_price": final_price, "Real": Real, "Not": Not}
        
        expr_eval = eval(code_expr_str, {}, eval_scope)
        self.solver.add(final_price == expr_eval)

        inv_eval = eval(f"Not({invariant_str})", {}, eval_scope)
        self.solver.add(inv_eval)

        result = self.solver.check()

        if result == sat:
            model = self.solver.model()
            counterexample = {d.name(): str(model[d]) for d in model.decls()}
            return {
                "status": "SAT",
                "safe": False,
                "message": "⚠️ LOGIKFEHLER GEFUNDEN (Gegenbeispiel existiert)",
                "counterexample": counterexample
            }
        elif result == unsat:
            return {
                "status": "UNSAT",
                "safe": True,
                "message": "✅ MATHEMATISCH BEWIESEN (Keine Regelverletzung möglich)",
                "counterexample": None
            }
        else:
            return {"status": "UNKNOWN", "safe": False, "message": "Unentscheidbar", "counterexample": None}