import sys
import os
import json
import argparse
from core.formguard_core import FormGuardVerifier
from core.llm_parser import LLMCodeTranslator

def run_cli():
    parser = argparse.ArgumentParser(description="FormGuard AI - Automated Logic Verification CLI")
    parser.add_argument("file", nargs="?", default=None, help="Path to Python source file")
    args = parser.parse_args()

    print("🛡️  FormGuard AI Automated Logic Verification Engine")
    print("--------------------------------------------------")

    if args.file and os.path.exists(args.file):
        print(f"📄 Target Source File: {args.file}")
        with open(args.file, "r", encoding="utf-8") as f:
            raw_code = f.read()
    else:
        print("ℹ️  No target file specified. Using default Python pricing logic...")
        raw_code = """
def calculate_price(x):
    if x > 100:
        return x * 0.9
    return x * 0.95
"""

    print("\n🧠 Step 1: Extracting Z3 Formal Logic via LLM Parser...")
    translator = LLMCodeTranslator()
    parsed_spec = translator.translate_to_z3(
        python_code=raw_code,
        invariant_desc="Price/value x must always remain greater than 0"
    )

    print(f"   ├─ Extracted Variable : {parsed_spec['var_name']}")
    print(f"   ├─ Generated Z3 Expr  : {parsed_spec['z3_expr']}")
    print(f"   └─ Invariant Rule     : {parsed_spec['rule_expr']}")

    print("\n🔬 Step 2: Executing Z3 Formal Mathematical Verification...")
    engine = FormGuardVerifier()
    result = engine.verify_dynamic_code(
        var_name=parsed_spec["var_name"],
        code_str=parsed_spec["z3_expr"],
        rule_str=parsed_spec["rule_expr"]
    )

    status = result.get("status", "UNKNOWN")
    message = result.get("message", "")

    print(f"\nVerification Status: {status}")
    print(f"Message: {message}")

    if status in ["FAILED", "ERROR", "SAT"] or result.get("counterexample"):
        print("\n❌ CRITICAL LOGIC FLAW OR INVARIANT VIOLATION DETECTED!")
        if result.get("counterexample"):
            print("Counterexample Input Vectors:")
            print(json.dumps(result["counterexample"], indent=2))
        sys.exit(1)
    else:
        print("\n✅ Verification Successful: Logic holds strictly across all state spaces.")
        sys.exit(0)

if __name__ == "__main__":
    run_cli()