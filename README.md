rocks- Python/Flask Project

rocks is a Python and Flask project that integrates local AI (Ollama) with a Slack bot. It provides a modular platform for automation, internal support, and experimentation with language models. Ideal for corporate projects, intelligent bots, and interactive dashboards.

Key Features:
- Flask web server with REST endpoints and web interface.
- Ollama integration for local AI processing.
- Slack bot to answer questions and execute commands.
- Modular structure for easy maintenance and expansion.
- Secure credential storage using a .env file.
- Detailed logging for monitoring and auditing.

Technologies Used:
- Python 3.x
- Flask
- Ollama
- Slack API
- Git/GitHub for version control
- VSCode as IDE
- .env for sensitive variables (tokens, secrets)

Prerequisites:
- Python 3.10 or higher
- Pip installed and updated
- Ollama running locally (ollama serve)
- Slack account with Bot Token and Signing Secret

Installation and Running:
1. Clone the repository:
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject

2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows

3. Install dependencies:
   pip install -r requirements.txt

4. Configure the .env file with your credentials:
   SLACK_SIGNING_SECRET=your_secret
   SLACK_BOT_TOKEN=your_token
   OLLAMA_URL=http://localhost:11434

5. Run the Flask server:
   python app.py

6. Open your browser at:
   http://localhost:5000

Project Structure:
ROCKS/
 ├── app.py                 # Flask entry point
 ├── requirements.txt       # Project dependencies
 ├── .env.example           # Sample environment variables
 ├── templates/             # HTML / Jinja templates
 ├── static/                # CSS, JS, images
 ├── services/              # AI & Slack logic
 │    └── ollama_service.py
 ├── dados/                 # Local data (ignored by Git)
 ├── venv/                  # Virtual environment (ignored by Git)
 └── README.md              # This file

Security:
- Never commit the .env file or any credential files.
- The dados/ folder is fully ignored by Git.
- Always handle Slack and Ollama tokens securely.

Next Steps / Improvements:
- Implement CI/CD for automatic deployment.
- Advanced multi-user support.
- Interactive dashboard with usage statistics.
- Detailed logging and interaction history.
- Support for additional AI models (e.g., GPT, LLaMA).

Usage Tips:
- Keep your virtual environment active.
- Update requirements.txt when installing new packages:
  pip freeze > requirements.txt
- Create dados/sample/ for test data without committing it to Git.

License:
MIT License © Diego Rocha

Useful Links:
- Flask Documentation: https://flask.palletsprojects.com/
- Ollama Docs: https://ollama.com/docs
- Slack API: https://api.slack.com/