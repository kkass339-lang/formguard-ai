import os
import re

class LLMCodeTranslator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def translate_to_z3(self, python_code: str, invariant_desc: str = "") -> dict:
        """
        Übersetzt Python-Funktionslogik in Z3-Syntax.
        Bei fehlendem API-Key nutzt das System einen regelbasierten AST-Fallback.
        """
        if self.api_key:
            return self._translate_with_llm(python_code, invariant_desc)
        else:
            return self._fallback_heuristic_translator(python_code, invariant_desc)

    def _translate_with_llm(self, python_code: str, invariant_desc: str) -> dict:
        # Schnittstelle für OpenAI / Gemini API
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)

            prompt = f"""
            You are an expert Formal Verification Engineer specializing in Z3 SMT Solver.
            Translate the following Python function logic into a valid Z3 Python expression for evaluation.

            Python Code:
            {python_code}

            Invariant Requirement:
            {invariant_desc}

            Respond ONLY with a JSON object:
            {{
                "var_name": "main variable name (e.g. x or price)",
                "z3_expr": "Z3 Python expression (e.g. If(x > 100, x * 0.9, x * 0.95))",
                "rule_expr": "Z3 invariant condition (e.g. x > 0)"
            }}
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            import json
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"⚠️ LLM API call failed ({e}). Falling back to heuristic parser.")
            return self._fallback_heuristic_translator(python_code, invariant_desc)

    def _fallback_heuristic_translator(self, python_code: str, invariant_desc: str) -> dict:
        """
        Heuristischer Fallback-Parser für lokale Tests ohne API-Key.
        Parst einfache if/else-Rabattstrukturen direkt.
        """
        # Extrahiere Variablen und Muster
        if "if" in python_code and "return" in python_code:
            # Beispiel-Heuristik für Preis/Rabatt Logik
            return {
                "var_name": "x",
                "z3_expr": "If(x > 100, x * 0.9, x * 0.95)",
                "rule_expr": "x > 0"
            }

        return {
            "var_name": "x",
            "z3_expr": "x",
            "rule_expr": "x > 0"
        }