🛡️ FormGuard AI – Automated Logic Verification Bot
FormGuard AI is an autonomous DevSecOps verification bot designed to prevent critical business logic flaws in continuous integration pipelines. By combining LLM-driven AST translation with the rigorous mathematical guarantees of the Z3 SMT Solver, FormGuard AI validates runtime code invariants across infinite state spaces without hallucination.

🏛️ System Architecture
FormGuard AI operates on a Neuro-Symbolic Verification Engine:
```
[ Python Source Code ] ──► [ LLM Code Translator ] ──► [ Z3 Formal Expressions ]
                                                             │
                                                             ▼
[ CI/CD Gate (Exit 0/1) ] ◄── [ Counterexample Vector ] ◄── [ Z3 SMT Solver Engine ]
```

1. LLM Translation Layer (core/llm_parser.py): Translates dynamic Python business logic into formal mathematical Z3 constructs and extracts state invariants.

2. SMT Solver Core (core/formguard_core.py): Executes mathematical verification using Z3. Returns UNSAT (proven safe) or SAT (counterexample found).

3. CI/CD Integration (cli.py & GitHub Actions): Evaluates repository code against rules in .formguard.json and halts bad builds with exit code 1.

⚙️ Configuration (.formguard.json)
Project-specific verification rules are defined at the root of your repository:
```
{
  "target_file": "test_sample.py",
  "var_name": "x",
  "invariant_desc": "Value x must always remain greater than or equal to 0",
  "invariant_rule": "x >= 0"
}
```

🚀 Quickstart & Local Execution
1. Installation
Clone the repository and install dependencies:
```
git clone https://github.com/kkass339-lang/formguard-ai.git
cd formguard-ai
pip install -r requirements.txt
```

2. Run Verification CLI
Verify target source files against formal invariants:
```
python cli.py test_sample.py
```
🛠️ Tech Stack
Formal Verification: Z3 SMT Solver (z3-solver)

Parsing & Translation: OpenAI API / Heuristic AST Parser

CI/CD Automation: GitHub Actions (.github/workflows/formguard.yml)

API Engine: Flask / Python 3.10+

📄 License
Distributed under the MIT License. See LICENSE for more information.
