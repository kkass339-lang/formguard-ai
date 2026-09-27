from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from core.formguard_core import FormGuardVerifier

app = Flask(__name__, template_folder='templates')
CORS(app)

verifier = FormGuardVerifier()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/verify', methods=['POST'])
def verify_code():
    data = request.json or {}
    
    # Werte direkt aus den Eingabefeldern des Frontends lesen
    var_name = data.get('var_name', 'x')
    code_str = data.get('code_str', 'x * 2 - 10')
    rule_str = data.get('rule_str', 'And(x > 0, y < 0)')
    
    # Dynamische Z3-Verifikation ausführen
    result = verifier.verify_dynamic_code(var_name, code_str, rule_str)
    
    return jsonify(result)

if __name__ == '__main__':
    print("🚀 FormGuard AI Server läuft auf http://127.0.0.1:5000")
    app.run(port=5000, debug=True)