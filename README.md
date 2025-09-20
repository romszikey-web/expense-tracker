# 💰 Personal Expense Tracker

A Django web application for tracking personal expenses with AI-powered insights using Google's Gemini API.

## ✨ Features

- **User Authentication**: Secure login and registration system
- **Expense Tracking**: Add, view, and categorize your expenses
- **AI Insights**: Get intelligent spending analysis powered by Gemini AI
- **Monthly Analysis**: Compare current and previous month spending
- **Category Breakdown**: See spending patterns by category
- **Nigerian Naira Support**: Built with NGN currency in mind

## 🚀 Tech Stack

- **Backend**: Django 5.2.6
- **Database**: SQLite (development)
- **AI Integration**: Google Gemini API
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Django built-in auth system

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Google Gemini API key

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/romszikey-web/expense-tracker.git
   cd expense-tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   GEMINI_API_KEY=your-gemini-api-key-here
   DEBUG=True
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Visit the application**
   
   Open your browser and go to: `http://127.0.0.1:8000`

## 🔑 Getting a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Create a new API key
4. Add the key to your `.env` file

## 📱 Usage

1. **Register/Login**: Create an account or login
2. **Add Expenses**: Record your daily expenses with categories
3. **View Insights**: Visit `/expenses/insights/` for AI-powered analysis
4. **Track Progress**: Monitor your spending patterns over time

```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Google Gemini API for AI insights
- Django framework for rapid development
- Bootstrap for responsive design

## 📞 Support

If you have any questions or run into issues, please open an issue on GitHub.

---

**Happy expense tracking! 💸**