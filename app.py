from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import atexit
from utils.ai_handler import ask_ai, MODELS, stop_model
from utils.pdf_reader import extract_text

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
TEMP_CODE_FOLDER = 'temp_code'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_CODE_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def cleanup():
    """Stops all running models on application exit."""
    print("Cleaning up: Stopping AI models...")
    for model_name in MODELS.values():
        stop_model(model_name)

# Register cleanup function to run on exit
atexit.register(cleanup)

@app.route('/')
def index():
    """Serves the main frontend page."""
    return send_from_directory('.', 'index.html')

@app.route('/generate-code', methods=['POST'])
def generate_code():
    data = request.json
    user_prompt = data.get('prompt')
    mode = data.get('mode', 'smart')
    
    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    # Prompt style: "You are an expert software engineer. Write code for the following request."
    ai_prompt = f"You are an expert software engineer. Write code for the following request: {user_prompt}"
    
    task_type = "coding_fast" if mode == "fast" else "coding_smart"
    response = ask_ai(ai_prompt, task_type)
    return jsonify({"response": response})

@app.route('/debug-code', methods=['POST'])
def debug_code():
    data = request.json
    code = data.get('code')
    mode = data.get('mode', 'smart')
    
    if not code:
        return jsonify({"error": "No code provided"}), 400
    
    ai_prompt = f"You are an expert programmer. Find errors in this code and explain them: \n\n{code}"
    
    task_type = "coding_fast" if mode == "fast" else "coding_smart"
    response = ask_ai(ai_prompt, task_type)
    return jsonify({"response": response})

@app.route('/explain-code', methods=['POST'])
def explain_code():
    data = request.json
    code = data.get('code')
    mode = data.get('mode', 'smart')
    
    if not code:
        return jsonify({"error": "No code provided"}), 400
    
    ai_prompt = f"Explain how this code works step by step: \n\n{code}"
    
    task_type = "coding_fast" if mode == "fast" else "coding_smart"
    response = ask_ai(ai_prompt, task_type)
    return jsonify({"response": response})

@app.route('/summarize-document', methods=['POST'])
def summarize_doc():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Extract text using pdfplumber
        extracted_text = extract_text(file_path)
        if not extracted_text:
            return jsonify({"error": "Failed to extract text from PDF"}), 500
        
        # We can limit the text length for the AI if it's too large
        ai_prompt = f"Summarize the following document in bullet points:\n\n{extracted_text[:4000]}"
        
        response = ask_ai(ai_prompt, "doc_summarize")
        return jsonify({"response": response})

@app.route('/ask-question', methods=['POST'])
def ask_question():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    question = request.form.get('question')
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
        
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        extracted_text = extract_text(file_path)
        if not extracted_text:
            return jsonify({"error": "Failed to extract text from PDF"}), 500
            
        ai_prompt = f"Using the content of the following document, answer this question: '{question}'\n\nDocument Content:\n{extracted_text[:4000]}"
        
        response = ask_ai(ai_prompt, "doc_qa")
        return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
