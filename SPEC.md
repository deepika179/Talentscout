# TalentScout - Hiring Assistant Chatbot Specification

## 1. Project Overview
- **Project Name**: TalentScout Hiring Assistant
- **Type**: AI-Powered Chatbot Web Application
- **Core Functionality**: An intelligent chatbot that collects candidate information, generates technical questions based on tech stack, and maintains conversation context throughout the hiring process.
- **Target Users**: Job candidates interacting with TalentScout's recruitment process

## 2. UI/UX Specification

### Layout Structure
- **Single Page Application**: Streamlit-based chat interface
- **Header**: Company branding with logo placeholder and title
- **Main Content**: Chat message container (scrollable)
- **Input Area**: Fixed bottom input field with send button
- **Sidebar**: Candidate information summary panel

### Visual Design
- **Color Palette**:
  - Primary: `#1E3A5F` (Deep Navy Blue)
  - Secondary: `#2E7D32` (Success Green)
  - Accent: `#FF6F00` (Amber Orange)
  - Background: `#F5F7FA` (Light Gray)
  - Bot Message: `#E3F2FD` (Light Blue)
  - User Message: `#E8F5E9` (Light Green)
  - Error: `#D32F2F` (Red)

- **Typography**:
  - Font Family: "Poppins" for headings, "Roboto" for body
  - Heading Size: 24px
  - Body Size: 16px
  - Small Text: 14px

- **Spacing**:
  - Message Gap: 12px
  - Container Padding: 20px
  - Border Radius: 12px

- **Visual Effects**:
  - Smooth message appearance animation
  - Subtle shadow on message bubbles
  - Hover effects on buttons
  - Typing indicator animation

### Components
- **Chat Message Bubbles**: Different colors for user vs bot
- **Input Field**: Text input with placeholder and send button
- **Candidate Info Card**: Sidebar panel showing collected info
- **Tech Tags**: Styled chips for technology stack
- **Exit Banner**: Warning message when exiting
- **Loading Spinner**: During LLM question generation

## 3. Functionality Specification

### Core Features

#### 3.1 Greeting System
- Display welcome message on session start
- Brief purpose explanation
- Clear instructions for exit keywords
- Exit keywords: "exit", "quit", "bye", "goodbye", "thank you"

#### 3.2 Information Collection
Collect in sequential order:
1. **Full Name** - Required, min 2 characters
2. **Email** - Required, valid email format
3. **Phone Number** - Required, 10+ digits
4. **Years of Experience** - Required, numeric
5. **Desired Position** - Required
6. **Current Location** - Required
7. **Tech Stack** - Required, comma-separated

#### 3.3 Tech Stack Parsing
- Accept comma-separated input (e.g., "Python, Django, MySQL")
- Normalize technology names
- Handle variations (e.g., "react" → "React")
- Store as list

#### 3.4 Question Generation
- Use LLM (OpenAI GPT API)
- Generate 3-5 questions per technology
- Questions should be intermediate level
- Store generated questions to avoid repetition
- Display one question at a time

#### 3.5 Context Management
- Streamlit session state for persistence
- Track conversation history
- Remember candidate name throughout
- Track which questions have been asked
- Handle follow-up responses

#### 3.6 Fallback Mechanism
- Detect irrelevant messages
- Redirect back to current question
- Provide helpful hints
- Don't break conversation flow

#### 3.7 Conversation End
- Professional thank you message
- Include candidate name
- Mention next steps
- Clear session state option

### User Interactions Flow
```
Start → Greeting → Name → Email → Phone → Experience → 
Position → Location → Tech Stack → Question Generation → 
Q&A Phase → End
```

### Edge Cases
- Empty input handling
- Invalid email format
- Invalid phone format
- Partial tech stack input
- API failures (graceful degradation)
- Session timeout handling

## 4. Technical Architecture

### File Structure
```
AIML/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env               # API keys (not committed)
└── SPEC.md            # This specification
```

### Dependencies
- streamlit>=1.28.0
- openai>=1.3.0
- python-dotenv>=1.0.0

### Environment Variables
- OPENAI_API_KEY: OpenAI API key for question generation

## 5. Acceptance Criteria

### Visual Checkpoints
- [ ] Chat interface loads without errors
- [ ] Messages appear with correct styling
- [ ] User and bot messages have distinct colors
- [ ] Input field is functional and styled
- [ ] Sidebar shows candidate information

### Functional Checkpoints
- [ ] Welcome message displays on start
- [ ] Exit keywords properly terminate conversation
- [ ] All 7 candidate fields collect correctly
- [ ] Email validation works
- [ ] Phone validation works
- [ ] Tech stack parses correctly
- [ ] Questions generate for each technology
- [ ] Context maintains throughout conversation
- [ ] Fallback handles irrelevant input
- [ ] End conversation is professional
