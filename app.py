from flask import Flask, render_template, request, jsonify
from compiler_engine import compile_xlang

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    data = request.json
    expr = data.get('expression', '')
    if not expr:
        return jsonify({'success': False, 'error': 'No expression provided'})
    
    results = compile_xlang(expr)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
