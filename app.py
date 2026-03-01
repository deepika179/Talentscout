"""
TalentScout - Hiring Assistant Chatbot
An AI-powered chatbot that collects candidate information and generates technical questions.
"""

import streamlit as st
import openai
import os
import re
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="TalentScout - Hiring Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Roboto:wght@400;500;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #F5F7FA 0%, #E4E8EC 100%);
    }
    
    .header-container {
        background: linear-gradient(135deg, #1E3A5F 0%, #2C5282 100%);
        padding: 20px 30px;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(30, 58, 95, 0.3);
    }
    
    .header-title {
        font-family: 'Poppins', sans-serif;
        color: #FFFFFF;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
    }
    
    .header-subtitle {
        font-family: 'Roboto', sans-serif;
        color: #B8C5D6;
        font-size: 14px;
        margin-top: 5px;
    }
    
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 20px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    .message {
        padding: 15px 20px;
        border-radius: 15px;
        margin-bottom: 12px;
        font-family: 'Roboto', sans-serif;
        font-size: 15px;
        line-height: 1.6;
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .bot-message {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        color: #1E3A5F;
        border-left: 4px solid #1E3A5F;
        margin-right: 50px;
    }
    
    .user-message {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        color: #1B5E20;
        border-right: 4px solid #2E7D32;
        margin-left: 50px;
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px;
        padding: 12px 20px;
        font-family: 'Roboto', sans-serif;
        font-size: 15px;
        border: 2px solid #E0E0E0;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1E3A5F;
        box-shadow: 0 0 0 3px rgba(30, 58, 95, 0.1);
    }
    
    .stButton > button {
        border-radius: 25px;
        padding: 12px 30px;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        background: linear-gradient(135deg, #1E3A5F 0%, #2C5282 100%);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(30, 58, 95, 0.4);
    }
    
    .sidebar-title {
        font-family: 'Poppins', sans-serif;
        color: #1E3A5F;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #1E3A5F;
    }
    
    .info-item {
        font-family: 'Roboto', sans-serif;
        margin-bottom: 12px;
        padding: 10px;
        background: #F5F7FA;
        border-radius: 8px;
    }
    
    .info-label {
        color: #666;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .info-value {
        color: #1E3A5F;
        font-size: 15px;
        font-weight: 500;
        margin-top: 3px;
    }
    
    .tech-tag {
        display: inline-block;
        padding: 5px 12px;
        background: linear-gradient(135deg, #FF6F00 0%, #FF8F00 100%);
        color: white;
        border-radius: 20px;
        font-size: 13px;
        font-family: 'Roboto', sans-serif;
        margin: 3px;
    }
    
    .question-card {
        background: linear-gradient(135deg, #FFF8E1 0%, #FFECB3 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #FF6F00;
        margin: 10px 0;
    }
    
    .question-tech {
        color: #FF6F00;
        font-weight: 600;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .question-text {
        color: #5D4037;
        font-size: 16px;
        margin-top: 8px;
        line-height: 1.5;
    }
    
    .exit-banner {
        background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
        padding: 15px 20px;
        border-radius: 10px;
        border-left: 4px solid #D32F2F;
        color: #C62828;
        font-family: 'Roboto', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize all session state variables."""
    defaults = {
        'conversation_stage': 'greeting',
        'candidate_info': {},
        'messages': [],
        'current_question_index': 0,
        'generated_questions': {},
        'tech_stack': [],
        'current_tech_index': 0,
        'questions_asked': [],
        'waiting_for_answer': False,
        'current_question': None,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Add initial greeting message if messages list is empty
    if not st.session_state.messages:
        st.session_state.messages.append({
            'text': "Hello! I'm TalentScout, your AI-powered hiring assistant. I'm here to help you through our technical assessment process. Let's get started!",
            'is_user': False,
            'timestamp': datetime.now().isoformat()
        })


def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """Validate phone number (minimum 10 digits)."""
    digits = re.sub(r'\D', '', phone)
    return len(digits) >= 10


def parse_tech_stack(tech_string):
    """Parse and normalize tech stack input."""
    if not tech_string:
        return []
    
    techs = [t.strip() for t in tech_string.split(',')]
    techs = [t for t in techs if t]
    
    normalization_map = {
        'react': 'React', 'reactjs': 'React',
        'angular': 'Angular', 'angularjs': 'Angular',
        'vue': 'Vue.js', 'vuejs': 'Vue.js',
        'node': 'Node.js', 'nodejs': 'Node.js',
        'python': 'Python', 'django': 'Django', 'flask': 'Flask',
        'java': 'Java', 'spring': 'Spring', 'springboot': 'Spring Boot',
        'javascript': 'JavaScript', 'typescript': 'TypeScript',
        'mysql': 'MySQL', 'mongodb': 'MongoDB',
        'postgresql': 'PostgreSQL', 'postgres': 'PostgreSQL',
        'redis': 'Redis', 'docker': 'Docker', 'kubernetes': 'Kubernetes',
        'aws': 'AWS', 'azure': 'Azure', 'gcp': 'GCP', 'git': 'Git',
    }
    
    normalized = []
    for tech in techs:
        tech_lower = tech.lower()
        normalized.append(normalization_map.get(tech_lower, tech))
    
    return list(set(normalized))


def generate_questions_with_llm(tech_stack):
    """Generate technical questions using OpenAI API."""
    if not tech_stack:
        return {}
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return generate_fallback_questions(tech_stack)
    
    try:
        openai.api_key = api_key
        questions = {}
        
        for tech in tech_stack:
            prompt = f"""Generate 3 intermediate-level technical interview questions for {tech}.
Format as JSON array: ["Q1", "Q2", "Q3"]"""

            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a technical interview question generator. Respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            try:
                tech_questions = json.loads(content)
                questions[tech] = tech_questions
            except json.JSONDecodeError:
                questions[tech] = generate_fallback_for_tech(tech)
        
        return questions
        
    except Exception as e:
        st.error(f"Error generating questions: {str(e)}")
        return generate_fallback_questions(tech_stack)


def generate_fallback_questions(tech_stack):
    """Generate fallback questions when API is not available."""
    fallback_data = {
        'Python': [
            "Explain the difference between list and tuple in Python.",
            "What are Python decorators and how would you create one?",
            "Describe the concept of Python's Global Interpreter Lock (GIL).",
        ],
        'Django': [
            "Explain the Django ORM and how model queries work.",
            "What is Django middleware and how do you create custom middleware?",
            "Describe Django's authentication system.",
        ],
        'React': [
            "Explain the difference between useState and useEffect hooks.",
            "What is the Virtual DOM and how does React use it?",
            "Describe React's component lifecycle methods.",
        ],
        'JavaScript': [
            "Explain closures in JavaScript with an example.",
            "What is the difference between == and ===?",
            "Describe the event loop in JavaScript.",
        ],
        'Java': [
            "Explain the difference between abstract class and interface.",
            "What is the purpose of the 'final' keyword in Java?",
            "Describe the Java garbage collection mechanism.",
        ],
        'Spring Boot': [
            "What is dependency injection in Spring?",
            "Explain the difference between @Component, @Service, and @Repository.",
            "How does Spring Boot auto-configuration work?",
        ],
        'MySQL': [
            "Explain the difference between INNER JOIN and LEFT JOIN.",
            "What are database indexes and how do they improve performance?",
            "Describe the concept of database normalization.",
        ],
        'MongoDB': [
            "Explain the difference between SQL and NoSQL databases.",
            "What are MongoDB aggregation pipelines?",
            "Describe MongoDB's document structure.",
        ],
        'Node.js': [
            "Explain the event-driven architecture of Node.js.",
            "What is the purpose of package.json in a Node.js project?",
            "Describe asynchronous programming in Node.js.",
        ],
    }
    
    questions = {}
    for tech in tech_stack:
        questions[tech] = fallback_data.get(tech, [
            f"Explain your experience with {tech}.",
            f"What are the best practices for using {tech}?",
            f"Describe a challenging project you worked on using {tech}.",
        ])
    
    return questions


def generate_fallback_for_tech(tech):
    """Generate fallback questions for a single technology."""
    return [
        f"Explain your experience with {tech}.",
        f"What are the best practices for using {tech}?",
        f"Describe a challenging project you worked on using {tech}.",
    ]


def get_next_question():
    """Get the next question from the generated pool."""
    questions = st.session_state.generated_questions
    tech_stack = st.session_state.tech_stack
    
    if not questions or not tech_stack:
        return None, None
    
    for tech in tech_stack:
        if tech in questions:
            tech_questions = questions[tech]
            for i, q in enumerate(tech_questions):
                question_id = f"{tech}_{i}"
                if question_id not in st.session_state.questions_asked:
                    st.session_state.questions_asked.append(question_id)
                    return q, tech
    
    return None, None


def check_exit_keywords(message):
    """Check if message contains exit keywords."""
    exit_keywords = ['exit', 'quit', 'bye', 'goodbye', 'thank you', 'thanks for your time']
    return any(keyword in message.lower() for keyword in exit_keywords)


def process_message(message):
    """Process user message based on current conversation stage."""
    
    if check_exit_keywords(message):
        return 'exit', None
    
    stage = st.session_state.conversation_stage
    
    if stage == 'greeting':
        return 'name', "Great! Let's get started. What is your full name?"
    
    elif stage == 'name':
        if len(message.strip()) < 2:
            return 'name', "Please enter a valid name (at least 2 characters)."
        st.session_state.candidate_info['name'] = message.strip()
        return 'email', "Nice to meet you! What is your email address?"
    
    elif stage == 'email':
        if not validate_email(message):
            return 'email', "Please enter a valid email address (e.g., john@example.com)."
        st.session_state.candidate_info['email'] = message.strip()
        return 'phone', "Thank you! What is your phone number?"
    
    elif stage == 'phone':
        if not validate_phone(message):
            return 'phone', "Please enter a valid phone number (at least 10 digits)."
        st.session_state.candidate_info['phone'] = message.strip()
        return 'experience', "How many years of experience do you have?"
    
    elif stage == 'experience':
        try:
            exp = int(message.strip())
            if exp < 0:
                return 'experience', "Please enter a valid number of years (0 or more)."
            st.session_state.candidate_info['experience'] = exp
            return 'position', "What position are you applying for?"
        except ValueError:
            return 'experience', "Please enter a valid number for years of experience."
    
    elif stage == 'position':
        if len(message.strip()) < 2:
            return 'position', "Please enter a valid position name."
        st.session_state.candidate_info['position'] = message.strip()
        return 'location', "What is your current location (city)?"
    
    elif stage == 'location':
        if len(message.strip()) < 2:
            return 'location', "Please enter a valid location."
        st.session_state.candidate_info['location'] = message.strip()
        return 'tech_stack', "Please enter your tech stack (comma-separated technologies, e.g., Python, Django, MySQL, React)"
    
    elif stage == 'tech_stack':
        techs = parse_tech_stack(message)
        if not techs:
            return 'tech_stack', "Please enter at least one technology in your tech stack."
        st.session_state.tech_stack = techs
        st.session_state.candidate_info['tech_stack'] = techs
        return 'generating_questions', None
    
    elif stage == 'answering':
        return 'next_question', None
    
    return stage, None


def display_message(message, is_user=False):
    """Display a message in the chat."""
    css_class = "user-message" if is_user else "bot-message"
    st.markdown(f'<div class="message {css_class}">{message}</div>', unsafe_allow_html=True)


def display_question(question, tech):
    """Display a technical question with styling."""
    st.markdown(f"""
        <div class="question-card">
            <div class="question-tech">{tech}</div>
            <div class="question-text">{question}</div>
        </div>
    """, unsafe_allow_html=True)


def display_candidate_info():
    """Display candidate information in sidebar."""
    info = st.session_state.candidate_info
    
    st.markdown('<div class="sidebar-title">📋 Candidate Information</div>', unsafe_allow_html=True)
    
    fields = {
        'name': 'Full Name',
        'email': 'Email',
        'phone': 'Phone',
        'experience': 'Experience',
        'position': 'Position',
        'location': 'Location',
    }
    
    for key, label in fields.items():
        if key in info:
            value = info[key]
            if key == 'experience':
                value = f"{value} years"
            st.markdown(f"""
                <div class="info-item">
                    <div class="info-label">{label}</div>
                    <div class="info-value">{value}</div>
                </div>
            """, unsafe_allow_html=True)
    
    if 'tech_stack' in info and info['tech_stack']:
        st.markdown('<div class="info-label" style="margin-top: 15px;">Tech Stack</div>', unsafe_allow_html=True)
        techs_html = ' '.join([f'<span class="tech-tag">{tech}</span>' for tech in info['tech_stack']])
        st.markdown(f'<div style="margin-top: 5px;">{techs_html}</div>', unsafe_allow_html=True)


def handle_submit():
    """Handle message submission from both Enter key and Send button."""
    if st.session_state.user_input.strip():
        message = st.session_state.user_input
        st.session_state.messages.append({
            'text': message,
            'is_user': True,
            'timestamp': datetime.now().isoformat()
        })
        
        new_stage, response = process_message(message)
        
        if new_stage == 'exit':
            name = st.session_state.candidate_info.get('name', 'Candidate')
            exit_message = f"👋 Thank you for your time, {name}! Our recruitment team will contact you shortly. Have a great day!"
            st.session_state.messages.append({
                'text': exit_message,
                'is_user': False,
                'timestamp': datetime.now().isoformat()
            })
            display_message(exit_message, False)
            st.session_state.conversation_stage = 'ended'
        
        elif new_stage == 'generating_questions':
            st.session_state.conversation_stage = new_stage
            st.rerun()
        
        elif new_stage == 'next_question':
            st.session_state.messages.append({
                'text': "Thank you for your answer! Let me ask the next question.",
                'is_user': False,
                'timestamp': datetime.now().isoformat()
            })
            
            question, tech = get_next_question()
            if question:
                st.session_state.current_question = question
                st.session_state.current_tech = tech
                st.session_state.messages.append({
                    'text': f"**{tech}**: {question}",
                    'is_user': False,
                    'timestamp': datetime.now().isoformat()
                })
            else:
                name = st.session_state.candidate_info.get('name', 'Candidate')
                final_message = f"🎉 Thank you, {name}! You've completed the technical assessment. Our team will review your responses and get back to you soon."
                st.session_state.messages.append({
                    'text': final_message,
                    'is_user': False,
                    'timestamp': datetime.now().isoformat()
                })
                st.session_state.conversation_stage = 'ended'
        
        elif response:
            st.session_state.messages.append({
                'text': response,
                'is_user': False,
                'timestamp': datetime.now().isoformat()
            })
            st.session_state.conversation_stage = new_stage
        
        st.session_state.user_input = ""
        st.rerun()


def main():
    """Main application function."""
    
    initialize_session_state()
    
    st.markdown("""
        <div class="header-container">
            <h1 class="header-title">🤖 TalentScout - Hiring Assistant</h1>
            <p class="header-subtitle">Your AI-powered recruitment assistant</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_main, col_sidebar = st.columns([3, 1])
    
    with col_sidebar:
        display_candidate_info()
    
    with col_main:
        chat_html = '<div class="chat-container">'
        
        for msg in st.session_state.messages:
            is_user = msg['is_user']
            css_class = "user-message" if is_user else "bot-message"
            chat_html += f'<div class="message {css_class}">{msg["text"]}</div>'
        
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)
        
        stage = st.session_state.conversation_stage
        
        if stage == 'generating_questions':
            with st.spinner('🔄 Generating technical questions based on your tech stack...'):
                tech_stack = st.session_state.tech_stack
                questions = generate_questions_with_llm(tech_stack)
                st.session_state.generated_questions = questions
            
            question, tech = get_next_question()
            if question:
                st.session_state.current_question = question
                st.session_state.current_tech = tech
                st.session_state.waiting_for_answer = True
                st.session_state.conversation_stage = 'answering'
                
                display_message(f"Great! I've generated technical questions based on your tech stack: {', '.join(tech_stack)}", False)
                display_question(question, tech)
            else:
                display_message("I wasn't able to generate questions. Would you like to continue with the application process?", False)
        
        elif stage == 'answering' and st.session_state.get('waiting_for_answer'):
            question = st.session_state.current_question
            tech = st.session_state.current_tech
            if question:
                display_question(question, tech)
        
        # Input field with Enter key support
        user_input = st.text_input(
            "Type your message...",
            key="user_input",
            placeholder="Type your answer here... (Press Enter to send)",
            label_visibility="collapsed",
            on_change=handle_submit
        )
        
        # Send button
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Send ➤"):
                handle_submit()
        
        if stage == 'ended':
            st.markdown("""
                <div class="exit-banner">
                    <strong>Conversation Ended</strong><br>
                    The session has ended. You can refresh the page to start a new conversation.
                </div>
            """, unsafe_allow_html=True)


def display_footer():
    """Display custom footer."""
    st.markdown("""
        <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #1E3A5F 0%, #2C5282 100%);
            color: white;
            text-align: center;
            padding: 10px;
            font-family: 'Roboto', sans-serif;
            font-size: 14px;
            z-index: 1000;
        }
        </style>
        <div class="footer">
            © 2026 TalentScout - Hiring Assistant | Created by Ullas N P
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
    display_footer()
