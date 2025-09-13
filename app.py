# existing local venv: source ../3-simple-chatbot/.venv/bin/activate
# for new env: python -m venv .venv ; source .venv/bin/activate

from flask import Flask, request, render_template
import json
from flask_cors import CORS

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)
CORS(app)

model_name = "facebook/blenderbot-400M-distill"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
conversation_history = []

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route("/chatbot", methods=["POST"])
def handlePrompt():
    # Read prompt from HTTP request body
    data=request.get_data(as_text=True)
    data=json.loads(data)
    input_text=data["prompt"]

    # create conversation history sting
    history="\n".join(conversation_history)

    # tokenise input text and history
    inputs =  tokenizer.encode_plus(history, input_text, return_tensors='pt')

    # generate response from the model
    outputs = model.generate(**inputs, max_length=60) #  # max_length will cause model to crash at some point as history grows

    # decode the response
    response=tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # Add interaction to conversation history
    conversation_history.append(input_text)
    conversation_history.append(response)
    
    return response

if __name__ == "__main__":
    app.run()


'''TO RUN IN TERMINAL: python3.11 app.py'''

'''curl -X POST -H "Content-Type: application/json" -d '{"prompt": "Hello, how are you today?"}' 127.0.0.1:5000/chatbot
 '''