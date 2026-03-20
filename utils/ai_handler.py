import requests
import json
import subprocess

# Local Ollama endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Models
MODELS = {
    "coding_smart": "deepseek-coder:6.7b",
    "coding_fast": "codellama",
    "document": "mistral"
}

def stop_model(model_name):
    """
    Stops a running model in Ollama to free up RAM.
    """
    try:
        # Check if ollama is available first
        if subprocess.run(["which", "ollama"], capture_output=True).returncode != 0:
            print("Ollama command not found in path.")
            return

        print(f"Stopping model: {model_name}")
        # subprocess.run(["ollama", "stop", model_name], check=True)
        # Note: 'ollama stop' is a command to unload models. 
        # Since we want to ensure only one runs at a time as per requirement.
        subprocess.run(["ollama", "stop", model_name], capture_output=True)
    except Exception as e:
        print(f"Error stopping model {model_name}: {e}")

def ask_ai(prompt, task_type):
    """
    Sends a prompt to Ollama after ensuring the correct model is used.
    """
    # Determine which model to use and which to stop
    if task_type == "coding_smart":
        target_model = MODELS["coding_smart"]
        other_models = [MODELS["coding_fast"], MODELS["document"]]
    elif task_type == "coding_fast":
        target_model = MODELS["coding_fast"]
        other_models = [MODELS["coding_smart"], MODELS["document"]]
    else:
        target_model = MODELS["document"]
        other_models = [MODELS["coding_smart"], MODELS["coding_fast"]]

    # 1. Stop the unused models
    for model in other_models:
        stop_model(model)

    # 2. Preparation for request
    # Note: Ollama will automatically load the target_model when we call the API.
    
    payload = {
        "model": target_model,
        "prompt": prompt,
        "stream": False
    }

    print(f"Sending request to Ollama using model: {target_model}")
    
    try:
        # 3. Send the prompt to Ollama API
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return result.get("response", "No response from AI.")
        
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Ollama: {str(e)}. Make sure Ollama is running."
