import sys
import json
from core.formguard_core import FormGuardVerifier

def run_cli():
    print("🛡️  Running FormGuard AI Automated Verification...\n")
    
    # Der Variablenname, den die Verifikationsengine prüft
    var_name = "x"
    
    # Beispiel-Code: Weist x einen Wert zu
    code_input = "x = 10"
    
    # Regel/Invariante: x muss größer als 0 sein
    rule_input = "x > 0"
    
    engine = FormGuardVerifier()
    
    # Aufruf der exakten Methode aus deiner Engine
    result = engine.verify_dynamic_code(var_name, code_input, rule_input)
    
    print(f"Verification Status: {result.get('status', 'COMPLETED')}")
    print(f"Message: {result.get('message', 'Verification run finished.')}")
    
    if result.get("counterexample") or result.get("status") == "FAILED":
        print("\n❌ CRITICAL LOGIC FLAW DETECTED!")
        print("Counterexample / Details:")
        print(json.dumps(result, indent=2))
        sys.exit(1)  # Beendet mit Fehlercode 1 (stoppt CI/CD Pipeline bei Fehler)
    else:
        print("\n✅ Verification Successful: Invariants hold strictly.")
        sys.exit(0)  # Beendet erfolgreich (0 = Alles ok)

if __name__ == "__main__":
    run_cli()