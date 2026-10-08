🌦️ Telegram Weather Bot

A multilingual Telegram bot that provides real-time weather information for cities around the world using the OpenWeather API.

✨ Features

- 🌍 Get weather information for different cities.
- 🌤️ Retrieve real-time weather data.
- 🇺🇿 Uzbek language support.
- 🇹🇷 Turkish language support.
- 🇬🇧 English language support.
- 🤖 Simple and user-friendly Telegram interface.

🛠️ Technologies Used

- Python
- pyTelegramBotAPI (TeleBot)
- OpenWeather API
- Requests
- python-dotenv

⚙️ Installation

1. Clone the repository

git clone YOUR_REPOSITORY_URL
cd telegram-weather-bot

Replace "YOUR_REPOSITORY_URL" with your GitHub repository URL.

2. Create a virtual environment

python -m venv .venv

Activate it on Windows PowerShell:

.\.venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create a ".env" file in the project root directory:

TOKEN=your_telegram_bot_token
API_KEY=your_openweather_api_key

Replace the example values with your own credentials. Make sure your ".env" file is never uploaded to GitHub.

5. Run the bot

python main.py

🔐 Security

Never share your Telegram bot token or OpenWeather API key publicly. Keep your ".env" file private.

👨‍💻 Author

Developed as a Python project to practice Telegram bot development, API integration, and environment variable management.