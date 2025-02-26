import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ok')
def ok():
    return render_template('ok.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Получаем порт из переменной окружения
    app.run(host='0.0.0.0', port=port, debug=True)  # Указываем 0.0.0.0, чтобы приложение было доступно снаружи