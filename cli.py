import argparse
import sys
from formguard_core import MultiVariableFormGuard
from llm_parser import FunctionParser

def main():
    parser = argparse.ArgumentParser(
        description="FormGuard AI - Neuro-Symbolic Verification Engine"
    )
    
    parser.add_argument(
        "--file", "-f", type=str, help="Pfad zur Python-Datei, die gescannt werden soll."
    )
    parser.add_argument(
        "--code", "-c", type=str, help="Python-Funktion direkt als String übergeben."
    )
    parser.add_argument(
        "--invariant", "-i", type=str, required=True, 
        help="Sicherheitsinvariante, z. B. 'final_price >= 0'"
    )

    args = parser.parse_args()

    code_to_verify = ""
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                code_to_verify = f.read()
        except Exception as e:
            print(f"❌ Fehler beim Lesen der Datei: {e}")
            sys.exit(1)
    elif args.code:
        code_to_verify = args.code
    else:
        print("❌ Bitte gib eine Datei mit --file oder Code mit --code an.")
        sys.exit(1)

    # 1. AST Parsing
    print("\n🔍 Analysiere Funktion...")
    parsed_info = FunctionParser.parse_function_str(code_to_verify)
    
    if "error" in parsed_info:
        print(f"❌ {parsed_info['error']}")
        sys.exit(1)

    print(f"📌 Funktion: {parsed_info['func_name']}({', '.join(parsed_info['args'])})")
    print(f"📌 Return-Formel: {parsed_info['return_expr']}")
    print(f"🛡️ Prüfe Invariante: '{args.invariant}'")
    print("--------------------------------------------------")

    # 2. Z3 Verification
    guard = MultiVariableFormGuard()
    res = guard.verify_invariant(
        code_expr_str=parsed_info["return_expr"],
        invariant_str=args.invariant,
        var_names=parsed_info["args"]
    )

    # 3. Output
    if res["status"] == "SAT":
        print("❌ VERIFICATION FAILED!")
        print(f"Message: {res['message']}")
        print("🚨 Gegenbeispiel gefunden:")
        for var_name, val in res["counterexample"].items():
            print(f"   • {var_name} = {val}")
        sys.exit(1)
    elif res["status"] == "UNSAT":
        print("✅ VERIFICATION SUCCESSFUL!")
        print(f"Message: {res['message']}")
        sys.exit(0)
    else:
        print(f"⚠️ UNKNOWN STATUS: {res['message']}")
        sys.exit(1)

if __name__ == "__main__":
    main()