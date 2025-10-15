# smart_task_planner
# Overview
Smart Task Planner is an AI-powered web application that converts natural language goals into actionable, time-bound task plans. It leverages OpenAI’s language model to reason about dependencies, durations, and task structures, ensuring each plan is practical and fits within the specified timeline.

For example, entering a goal such as “Make a cake in 2 days” will produce a detailed, step-by-step plan with corresponding durations and dependencies that total exactly 2 days.

# Features
Accepts natural language input describing a goal and timeline.

Automatically extracts and understands time constraints (days, weeks, months, or hours).

Generates SMART (Specific, Measurable, Achievable, Realistic, Time-bound) task plans.

Dynamically adjusts task durations to fit within the requested timeline.

Displays readable, structured task lists with durations, dependencies, and descriptions.

Includes an optional frontend with Tailwind CSS for a clean, minimal interface.

# System Architecture
# Components
# Frontend:
A simple web interface (HTML, CSS, JavaScript) that collects user goals and displays the generated plan in a readable format.
# Backend (Flask API):
Receives user input from the frontend.

Extracts the timeline (e.g., “2 weeks” → 14 days).

Calls the OpenAI API to generate detailed task plans.

Adjusts durations proportionally to match the requested timeframe.

Returns structured task data in JSON format.

LLM (OpenAI GPT-4o-mini):

Performs natural language reasoning and generates structured plans.
# Tech Stack
Component	Technology

Frontend	HTML, Tailwind CSS, JavaScript

Backend	Python (Flask)

AI Model	OpenAI GPT-4o-mini

Data Format	JSON

Optional Tools	Flask-CORS, Regular Expressions
# Project Structure
smart_task_planner/
│
├── app.py                     # Flask backend
├── requirements.txt            # Dependencies
├── templates/
│   └── index.html              # Frontend UI
├── static/
│   └── script.js               # Frontend logic
└── README.md                   # Project documentation

# Installation and Setup
1-> Python 3.8 or higher

2-> OpenAI API key (you can create one at https://platform.openai.com/account/api-keys)
# Steps
1-> Clone the repository

git clone https://github.com/yourusername/smart-task-planner.git

cd smart-task-planner

2-> Create a virtual environment

python -m venv venv

source venv/bin/activate     # On Windows: venv\Scripts\activate

3-> Install dependencies

pip install -r requirements.txt

4-> Set your OpenAI API key

Windows (Command Prompt):

setx OPENAI_API_KEY "your_openai_api_key_here"

macOS/Linux (Terminal):

export OPENAI_API_KEY="your_openai_api_key_here"

5-> Run the Flask server

python app.py

6-> Open the application

Visit http://127.0.0.1:5000 in your browser.


# Usage
1-> Enter a goal in the input box, including a timeline (e.g., “Plan a conference in 3 weeks”, “Make a cake in 2 days”).

2-> Click Generate Plan.

3-> The application will:

Understand your timeline.

Generate a sequence of detailed, realistic tasks.

Display each task with duration, dependency, and a short description.

The total duration will match the timeline provided in your input.

# Example
Input:

Make a cake in 2 days

Output:

Goal: Make a cake in 2 days

1. Gather Ingredients
   Max Duration: 0.5 days
   Depends on: —
   Description: Collect flour, sugar, eggs, and butter.

2. Prepare Batter
   Max Duration: 0.5 days
   Depends on: Gather Ingredients
   Description: Mix ingredients until smooth.

3. Bake Cake
   Max Duration: 0.75 days
   Depends on: Prepare Batter
   Description: Bake at 180°C until golden brown.

4. Decorate & Serve
   Max Duration: 0.25 days
   Depends on: Bake Cake
   Description: Frost and serve the finished cake.

# Key Functionalities
1-> Time Parsing: Automatically extracts numeric time and units from user goals.

2-> Normalization: Scales durations so total time equals the user-specified timeframe.

3-> Dynamic Output: Returns JSON data and renders it as human-readable text.

4-> Error Handling: Handles invalid inputs, missing API keys, and malformed responses.

# Example API Request and Response
-> POST /generate-plan

Request Body:
{
  "goal": "Launch a website in 3 weeks"
}

-> Response Example:
{
  "goal": "Launch a website in 3 weeks",
  "timeframe_text": "3 weeks",
  "total_days": 21,
  "plan": [
    {
      "task": "Market Research",
      "description": "Analyze target audience and competitors.",
      "duration": "3 days",
      "depends_on": ""
    },
    {
      "task": "UI/UX Design",
      "description": "Design wireframes and prototypes.",
      "duration": "4 days",
      "depends_on": "Market Research"
    }
  ]
}

# Error Handling
Error Type	Description

Invalid Input	Returned if no goal text is provided.

Invalid API Key	Occurs if OpenAI API key is missing or incorrect.

Insufficient Quota	Occurs if your OpenAI account has exceeded usage limits.

Parsing Error	Returned if model output is not valid JSON.

# Future Enhancements
Gantt chart visualization for task timelines.

Progress tracking with completion percentages.

User authentication and plan history.

Export plans to PDF or calendar formats.

Integration with project management tools (Notion, Trello, Asana).

# Reference Images
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/122f1aaf-d271-4eeb-9cf6-83d379fd1f9c" />

# Demo Video
https://drive.google.com/file/d/131E3pxUuVM_52fQxU9eCPorfvQKllQ_n/view?usp=sharing

# License

This project is open-source and available under the MIT License
