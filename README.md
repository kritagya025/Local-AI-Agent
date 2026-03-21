# 🤖 Offline AI Enterprise Assistant

A privacy-focused AI assistant that runs **completely offline** using **Ollama**. Process sensitive data, generate code, and summarize documents locally without any data leaving your machine.

---

## 🌐 Live Landing Page

Users can download the desktop application from our live site:
👉 **[Download Offline AI Assistant](https://hj-anand.github.io/Local-AI-Agent/download-site/)**

---

## 🚀 Features

- **💻 Code Wizard:** Generate, debug, and explain code using `deepseek-coder:6.7b`.
- **📄 Document Intelligence:** Upload PDFs for instant summaries or ask specific questions using `mistral`.
- **🎙️ Voice Commands:** Interact with the AI using your voice (Powered by offline SpeechRecognition).
- **🔒 Privacy First:** No cloud APIs, no data collection. Everything stays on your hardware.
- ** ️ Desktop App:** Now available as a native Electron desktop application.
- ** 🐏 Memory Optimized:** Automatically manages model switching to save RAM.

---

## 🛠️ Prerequisites

Before you start, ensure you have the following installed:

1.  **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
2.  **Node.js & npm**: Required for the Desktop (Electron) app. [Download Node.js](https://nodejs.org/)
3.  **Ollama**: The engine for running local LLMs.
    - **Windows/Mac**: Download from [ollama.com](https://ollama.com/download)
    - **Linux**: Run `curl -fsSL https://ollama.com/install.sh | sh`

---

## 📦 Installation & Setup

### 1. Clone & Prepare

Open your terminal (Command Prompt/PowerShell on Windows, Terminal on Mac/Linux) and navigate to the project folder.

### 2. Set Up Virtual Environment (Recommended)

**Windows:**

```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Mac / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install backend dependencies
pip install -r requirements.txt
pip install SpeechRecognition pocketsphinx

# Install desktop app dependencies
cd electron-app
npm install
cd ..
```

### 4. Download AI Models

Ensure Ollama is running, then run these commands in your terminal:

```bash
ollama pull mistral
ollama pull deepseek-coder:6.7b
```

---

## 🏃 Launching the Assistant

### Option 1: Desktop Mode (Recommended)

1.  **Start the Backend:**
    Open a terminal in the root folder and run:
    ```bash
    python app.py
    ```
2.  **Start the Desktop App:**
    Open a **second** terminal, navigate to the `electron-app` folder, and run:
    ```bash
    cd electron-app
    npm start
    ```

### Option 2: Web Browser Mode

1.  **Start the Backend:**
    ```bash
    python app.py
    ```
2.  **Access the Interface:**
    Open your browser and search for: [http://localhost:5000](http://localhost:5000)

---

## 🏗️ Packaging for Distribution (Desktop Only)

To generate a standalone `.exe` or portable app for your OS:

```bash
cd electron-app
npm run build
```

The output will be found in `electron-app/dist/`.

---

## ⚙️ How It Works

This project is optimized for machines with limited RAM (e.g., 8GB or 16GB).

- When you use **Coding features**, it automatically stops the document model to free up space and loads `deepseek-coder`.
- When you use **Document features**, it stops the coding model and loads `mistral`.
- All interactions happen via a local API on port `11434`.

---

## 📂 Project Structure

- `app.py`: Flask server and API endpoints.
- `index.html`: Modern, interactive frontend.
- `electron-app/`: Electron desktop application files.
- `download-site/`: Landing page for web-based app distribution.
- `utils/`:
  - `ai_handler.py`: Logic for model switching and Ollama API communication.
  - `pdf_reader.py`: PDF text extraction logic.
- `uploads/`: Temporary storage for uploaded documents.
- `ELECTRON_SETUP.md`: Detailed guide for Electron configuration.
- `requirements.txt`: Python package dependencies.
