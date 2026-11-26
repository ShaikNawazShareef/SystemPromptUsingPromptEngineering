# ⚒️ SystemPrompt AI

SystemPrompt AI is a Python-based AI prompt engineering application powered by Google Gemini. It transforms simple user instructions into structured, professional prompts and generates intelligent responses using a two-stage AI workflow.

## 🚀 Features

- **Prompt Enhancement:** Converts basic prompts into professional prompts.
- **AI Response Generation:** Generates responses using Google Gemini.
- **Role-Based Instructions:** Allows users to define the AI's role.
- **Context Awareness:** Accepts additional context to improve results.
- **Structured Output:** Organizes prompts using six essential components.
- **Automatic Retry:** Handles temporary API errors with retry logic.
- **Fallback Models:** Switches to an alternative Gemini model when needed.
- **Interactive CLI:** Provides a simple terminal-based interface.

## 🧠 System Prompts

PromptForge AI uses two different system prompts to complete its workflow.

### 1. Prompt Improvement System Prompt

```text
You are an expert Prompt Engineer.

Your job is to transform rough user prompts
into professional and effective AI prompts.

Include these six components:

1. Role
2. Context
3. Task
4. Specific Instructions
5. Constraints
6. Expected Output Format

Important rules:

- Understand the user's original intention.
- Improve clarity and structure.
- Use simple and professional language.
- Do not answer the original question.
- Only generate the improved prompt.
```

### 2. AI Response Generation System Prompt

```text
You are acting in the following role: {role}.

Follow the improved prompt carefully.

Rules:

- Use simple English.
- Give clear explanations.
- Provide practical examples.
- Include Python code when requested.
- Use headings and bullet points where useful.
- Avoid unnecessary information.
```

## ⚙️ How It Works

PromptForge AI follows a two-stage workflow:

**Stage 1: Prompt Engineering**

The application accepts:
- Original user prompt
- AI role
- Additional context
- Expected output format

Gemini transforms these inputs into a professional prompt.

**Stage 2: AI Response Generation**

The improved prompt is passed to Gemini again to generate the final answer.

## 🛠️ Technologies Used

- Python
- Google Gemini API
- Google GenAI SDK
- Python Dotenv
- Environment Variables

## 📁 Project Structure

```text
PromptForge-AI/
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## 📦 Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/PromptForge-AI.git
```

**2. Navigate to the project directory**

```bash
cd PromptForge-AI
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure your Gemini API key**

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
GEMINI_FALLBACK_MODEL=gemini-3.8-flash
```

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

**5. Run the application**

```bash
python main.py
```

## 💻 Usage

1. Enter your original prompt.
2. Specify the AI role.
3. Provide additional context.
4. Select the expected output format.
5. Let PromptForge AI improve your prompt.
6. Receive the final AI-generated response.

## 🔄 Error Handling

The application includes:
- Automatic retries for temporary API errors.
- Exponential backoff with random delays.
- Fallback model switching.
- API error and authentication handling.
- Keyboard interruption handling.

## 🎯 Target Audience

- Students
- Python Developers
- AI Beginners
- Content Creators
- Researchers
- Working Professionals

## 🔮 Future Enhancements

- Graphical User Interface (GUI).
- Prompt history and management.
- Multiple AI model support.
- Prompt templates.
- Export improved prompts.
- Web application deployment.

## 👨‍💻 Author

**Shaik Nawaz Shareef**

GitHub: https://github.com/ShaikNawazShareef


---

⭐ If you find PromptForge AI useful, consider giving this repository a star!
