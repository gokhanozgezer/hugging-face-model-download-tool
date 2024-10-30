# Hugging Face Model Download Tool

This is a **Hugging Face model download tool** developed by **Gokhan Ozgezer**. The tool allows users to search, authenticate, and download models from the Hugging Face Hub conveniently, with support for Turkish and English languages.

## Features

- **Authentication** using your Hugging Face API token.
- **Search** and download models directly from the Hugging Face Hub.
- **Localization support**: Turkish and English messages based on system language.
- **Graceful cancellation** with `CTRL + C`.
- **Token caching** for convenience in subsequent sessions.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/gokhanozgezer/hugging-face-model-download-tool.git
cd hugging-face-model-download-tool
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Ensure you have the messages.json file
The messages.json file in the same directory as main.py. This file stores the multilingual messages used by the program.

---

## Usage

### Running the Tool
Execute the following command to start the tool:

```bash
python main.py
```

---

## Authentication

- The tool will attempt to use a cached Hugging Face token from previous sessions if available.
- If no token is found, it will prompt for your API token.
  - Enter the token to log in, or type `q` to quit.
 
### Searching for Models

- Enter a search query to find models on the Hugging Face Hub.
- The tool will display up to 10 matching models.
- Choose a model by entering its index number, or type `q` to quit the program.

### Downloading Models

- Selected models will be downloaded to a local `models/` directory.
- If the model is already partially downloaded, only the missing files will be completed.

---

## Configuration

### Handling Language Settings

- The tool automatically detects the system language:
  - If your system language starts with `tr`, Turkish will be used.
  - For all other languages, English will be the default.

### Cancelling Operations

- You can cancel the current operation using `CTRL + C`. The program will gracefully exit, printing a cancellation message.

---

## File Structure

```bash
hugging-face-model-download-tool/
│
├── main.py              # Main Python script
├── messages.json        # Localization messages (TR & EN)
└── requirements.txt     # Dependencies
```

---

## Error Handling

- If an invalid token is provided, the tool will prompt you to re-enter the token.
- If no models are found for a search query, the program will notify you and allow you to search again.
- In the event of unexpected errors during model download, the error message will be displayed.

---

## Contribution

Feel free to fork the repository and submit pull requests. Contributions, improvements, and bug fixes are welcome!
