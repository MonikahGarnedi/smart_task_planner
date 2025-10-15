from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import re
import json

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_number(text):
    """Extracts numeric value from text (like 2 from '2 weeks')."""
    match = re.search(r'\d+', text)
    return int(match.group()) if match else 1


def parse_timeframe(goal_text):
    """Converts timeframe text (e.g., '2 weeks') into number of days."""
    text = goal_text.lower()
    if "week" in text:
        return extract_number(text) * 7
    elif "month" in text:
        return extract_number(text) * 30
    elif "day" in text:
        return extract_number(text)
    elif "hour" in text:
        return max(1, round(extract_number(text) / 24))
    return 14  # default (2 weeks)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate-plan', methods=['POST'])
def generate_plan():
    try:
        data = request.get_json()
        goal = data.get("goal", "").strip()

        if not goal:
            return jsonify({"error": "Please provide a valid goal"}), 400

        # 🧭 Detect total duration in days
        total_days = parse_timeframe(goal)

        # 🧠 Enhanced prompt — force GPT to fit inside given duration
        prompt = f"""
        You are a precise AI planner.
        Break down the following goal into realistic, actionable tasks.

        Goal: "{goal}"

        Constraints:
        - The **total duration of all tasks must NOT exceed {total_days} days**.
        - Include short, clear task descriptions.
        - Each task must have:
            * task (title)
            * description (1 line)
            * duration (e.g., "0.5 days" or "2 hours" if short)
            * depends_on (previous task or empty)
        - Respond strictly in JSON format (array of tasks).

        Example:
        [
          {{
            "task": "Mix ingredients",
            "description": "Combine flour, sugar, eggs, and butter.",
            "duration": "0.5 days",
            "depends_on": ""
          }},
          {{
            "task": "Bake cake",
            "description": "Preheat oven and bake at 180°C.",
            "duration": "1 day",
            "depends_on": "Mix ingredients"
          }}
        ]
        """

        # 🔗 Query GPT
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a structured and time-aware project planner."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )

        raw_output = response.choices[0].message.content.strip()

        # 🧾 Extract JSON
        json_match = re.search(r'\[.*\]', raw_output, re.DOTALL)
        if not json_match:
            return jsonify({"goal": goal, "plan": [], "error": "Invalid LLM output."})
        tasks = json.loads(json_match.group(0))

        # 🔢 Parse and sum durations
        def days_from_str(s):
            m = re.search(r'[\d.]+', s)
            return float(m.group()) if m else 0

        total_model_days = sum(days_from_str(t.get("duration", "0")) for t in tasks)
        if total_model_days == 0:
            total_model_days = total_days

        # ⚖️ Normalize to fit inside target days
        scale = total_days / total_model_days
        for t in tasks:
            d = days_from_str(t.get("duration", "1"))
            adjusted = max(0.25, round(d * scale, 2))
            t["duration"] = f"{adjusted} days"

        # ✅ Return proper JSON
        return jsonify({
            "goal": goal,
            "total_requested_days": total_days,
            "plan": tasks
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
