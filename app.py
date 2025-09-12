# existing local venv: source ../3-simple-chatbot/.venv/bin/activate ()
# for new env: python -m venv .venv ; source .venv/bin/activate

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run()


    '''TO RUN IN TERMINAL: python3.11 app.py'''