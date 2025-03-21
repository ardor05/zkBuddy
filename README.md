<div align="center">
  <img src="https://github.com/user-attachments/assets/c0dc63de-5907-4f18-8c0c-c2766ca683af" alt="logo" width="300">
</div>

# zkBuddy

zkBuddy is a private AI chatbot that integrates emotion recognition and zero-knowledge proofs (zkML) into a single Streamlit application. It uses Gemini's Generative AI to generate chat responses, YOLO to detect user emotions from images, and a Rust module (built with PyO3 and maturin) to compile cryptographic circuits and simulate GKR-based proofs. This approach ensures that sensitive computations are verified in zero-knowledge without exposing the underlying data.

## Features

- **Chatbot Interface:** Powered by Gemini Generative AI.
- **Emotion Recognition:** Detects user emotions using a YOLO model.
- **Zero-Knowledge Proofs:** Simulates circuit compilation and zkML proof generation with Polyhedra’s Expander Compiler Collection.
- **Streamlit UI:** An interactive web interface for easy interaction.

## Requirements

- **Python 3.12** (ensure your virtual environment uses this version)
- **Rust** (latest stable or nightly)
- [**maturin**](https://maturin.rs) for building the Python extension from Rust
- Streamlit (`pip install streamlit`)
- Google Generative AI (with a valid API key)
- Ultralyitcs YOLO (with a pre-trained model file `best.pt`)
- Polyhedra’s Expander Compiler Collection (declared as a git dependency in Cargo.toml)

## Installation

### 1. Set Up the Virtual Environment

1. Clone the repository and navigate into it:

   ```bash
   git clone https://github.com/ardor05/zkBuddy.git
   cd zkBuddy
   ```

2. Create and activate a virtual environment:

   **Windows (PowerShell):**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```
   **macOS/Linux:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install Python dependencies:

   ```bash
   pip install streamlit google-generativeai ultralytics
   ```

### 2. Build the Rust Module

1. Ensure Rust is installed via [rustup](https://rustup.rs).

2. Install maturin:

   ```bash
   pip install maturin
   ```

3. Build and install the Rust module into your virtual environment:

   ```bash
   maturin develop -b pyo3
   ```

   *Note:* The Rust module is built with PyO3 and installed as a Python package (e.g., `zk_buddy`). Check `pip list` to confirm installation.

## Usage

### Running the Streamlit App

With your virtual environment activated, run:

```bash
python -m streamlit run .\main.py
```

- **Chat Interface:** Type a message to receive a response from Gemini.
- **Emotion Detection:** Upload an image using the sidebar to detect emotions.
- **zkML Proof Logging:** The Rust module compiles the cryptographic circuit and simulates a GKR proof. The proof details are printed to the terminal (and are hidden from the UI).

## Project Structure

```
zkBuddy/
├── Cargo.toml           # Rust project configuration
├── pyproject.toml       # Maturin build configuration
├── README.md            # This file
├── main.py              # Streamlit application
├── src/
│   └── lib.rs           # Rust source code for zkBuddy
├── .venv/               # Python virtual environment (created locally)
└── best.pt              # YOLO model for emotion detection
```

## Key Technologies

- **Expander Compiler Collection by Polyhedra:**  
  The heart of zkBuddy is built on Polyhedra’s Expander Compiler Collection. The Rust code in `src/lib.rs` leverages this technology to define and compile cryptographic circuits (for example, a simple circuit that asserts x equals y). It further simulates GKR proof generation and exposes a function (`run_zkbuddy`) to Python via PyO3, enabling zero-knowledge proof capabilities without revealing sensitive data.

- **Gemini AI:**  
  zkBuddy integrates Gemini’s Generative AI to produce dynamic and contextually rich chat responses. This technology drives the conversational aspect of the chatbot, ensuring that users receive intelligent and relevant replies.

- **YOLO (You Only Look Once):**  
  For emotion recognition, zkBuddy employs a YOLO model to analyze uploaded images. This enables the system to detect and interpret user emotions, which are then used to adjust the chatbot’s responses accordingly.

- **Python & Streamlit:**  
  The Python code in `main.py` provides a user-friendly Streamlit-based interface that brings together the power of Gemini AI, YOLO for emotion detection, and the underlying Rust-based cryptographic proof system.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## Disclaimer

This project have been developed for Explore Expander Bootcamp by Polyhedra & organized by Encode Club. Thank you to all people that contributing to zkBuddy.

