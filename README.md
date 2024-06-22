<p align="center">

<h1 align="center">Medi-Guardian</h1>
<p align="center">
  <em>A platform for medical fact checking and information retrieval.</em>
</p>

## 📍 Overview

***Objective***

Medi-Guardian is a powerful chatbot designed to assist users by processing multimedia inputs for transcript generation & providing medical advice. It leverages advanced LLM models to interpret audio & video inputs.

***Motivation***

People usually beleive on remedies and solutions avaliable on social media platforms which may cause them serious health issues. So, we aim to provide a platform where users can get cross the check and get validation of thier information.

---
## 🧩 Features

### 📲 Chat History
- Capable to remember past conversations by using SQLite to store metadata and transcripts for efficient retrieval.

### 📹 Multimedia Handling
- Supports video uploads and audio extraction for transcript generation.

### 📺 YouTube Integration
- Enables input of YouTube links, downloads the audio, and generates transcripts.

---

## 🚀 Getting Started

**System Requirements:**

  - Python 3.9+
  - Package manager: `pip` , `chocolatey`<em> (recommended)</em>
  - LLM service: `OpenAI Whisper`, `Google Gemini`

**Repository URL or Local Path:**

Make sure to have a repository URL or local directory path ready for the CLI.

- [**GitHub**](https://github.com/navalthanik/MediGuardianbyTripleTrouble)

**Choosing an LLM Service:**

- [**OpenAI**](https://platform.openai.com/docs/quickstart/account-setup): Recommended, requires an account setup and API key.
- [**Google Gemini**](https://ai.google.dev/tutorials/python_quickstart): Requires a Google Cloud account and API key.

### ⚙️ Installation Steps

#### 1. Clone the repository
>
> ```sh
> git clone https://github.com/navalthanik/MediGuardianbyTripleTrouble.git
> ```

#### 2. Make a virtual environment for python by below command (optional)
>
> ```sh
> python -m venv virtual-environment-name
> ```
   - Activate: `virtual-environment-name\Scripts\activate`

### 3. Open your project folder in terminal (command line)

### 4. Install Dependencies
> ```sh
>pip install -r requirements.txt
> ```
Additional Dependencies:

▹ **Install PyTorch** (If you have a CUDA-supported GPU)
   >```sh
   >pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   > ```

▹ **Install FFMPEG** (Recommended to run in PowerShell as Administrator)
   - Set Execution Policy: 
   >```sh
   >Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   >```
   - Install FFMPEG: 
   >```sh
   >choco install ffmpeg`
   >```

### 5. Run the Application ![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)
#### Using `streamlit` 

>  `streamlit run myapp.py`

### 📷 Output
#### Medi-Guardian App UI on Streamlit.
![Medi-Guardian Output Screenshot](https://github.com/navalthanik/MediGuardianbyTripleTrouble/assets/99556620/d21f6617-2d88-4269-b47d-e26f563cc5c4)
