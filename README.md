# TalentScout - Hiring Assistant Chatbot

An AI-powered chatbot that collects candidate information and generates technical interview questions based on their tech stack.

## 🚀 Features

- **Welcome & Greeting** - Friendly introduction with clear purpose explanation
- **Information Collection** - Collects candidate details (Name, Email, Phone, Experience, Position, Location, Tech Stack)
- **Smart Validation** - Email and phone number validation
- **Tech Stack Parsing** - Automatically normalizes technology names (e.g., "react" → "React")
- **AI-Powered Questions** - Generates 3 technical questions per technology using OpenAI GPT
- **Fallback Questions** - Built-in questions for common technologies when API key is not provided
- **Context Awareness** - Remembers candidate name throughout the conversation
- **Professional Exit** - Graceful conversation ending with personalized message

## 🛠️ Tech Stack

- **Python** - Core programming language
- **Streamlit** - Web UI framework
- **OpenAI API** - For generating technical questions (optional)

## 📋 Requirements

- Python 3.8+
- streamlit
- openai
- python-dotenv

## ⚡ Installation

1. Clone or download this repository
2. Install dependencies:
   
```
bash
   pip install -r requirements.txt
   
```

3. (Optional) Add your OpenAI API key to `.env`:
   
```
   OPENAI_API_KEY=your_api_key_here
   
```
   > Note: The app works without an API key using built-in fallback questions!

## 🎯 Usage

Run the application:
```
bash
py -m streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 💬 Conversation Flow

1. **Start** - Welcome message appears automatically
2. **Name** - Enter your full name
3. **Email** - Provide valid email address
4. **Phone** - Enter phone number (10+ digits)
5. **Experience** - Years of experience
6. **Position** - Desired job position
7. **Location** - Current city
8. **Tech Stack** - Enter technologies (comma-separated, e.g., "Python, Django, React")
9. **Questions** - Answer generated technical questions
10. **End** - Professional completion message

## 🔧 Exit Keywords

The conversation can be ended anytime by typing:
- exit
- quit
- bye
- goodbye
- thank you
- thanks for your time

## 📁 Project Structure

```
AIML/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .env              # Environment variables (create from template)
├── SPEC.md          # Detailed specification
└── README.md        # This file
```

## 🎨 UI Features

- Modern gradient header with company branding
- Color-coded chat bubbles (blue for bot, green for user)
- Real-time sidebar with candidate information
- Tech stack tags with orange styling
- Technical question cards with amber accent
- Smooth fade-in animations
- Responsive layout

## 🔐 Privacy

- All data is stored in session state only (not persisted)
- No data is sent to external servers (except OpenAI API if key is provided)
- Conversation data is cleared when the page is refreshed

## 📝 License

MIT License

## 👤 Author

TalentScout Hiring Assistant

---

Made with ❤️ using Streamlit and OpenAI
