from datetime import date

from flask import Flask, render_template

app = Flask(__name__)


EVENTS = {
    "monday": [
        {"time": "09:00", "title": "Team standup"},
        {"time": "14:00", "title": "Project planning"},
    ],
    "tuesday": [
        {"time": "10:30", "title": "Design review"},
        {"time": "16:00", "title": "Client sync"},
    ],
    "wednesday": [
        {"time": "08:45", "title": "Sprint board update"},
        {"time": "13:00", "title": "Lunch and learn"},
    ],
    "thursday": [
        {"time": "11:00", "title": "Engineering demo"},
        {"time": "15:30", "title": "Roadmap grooming"},
    ],
    "friday": [
        {"time": "09:30", "title": "Weekly retrospective"},
        {"time": "12:00", "title": "Team lunch"},
    ],
    "saturday": [
        {"time": "10:00", "title": "Personal errands"},
    ],
    "sunday": [
        {"time": "18:00", "title": "Plan upcoming week"},
    ],
}


@app.route("/")
def index():
    today = date.today()
    day_key = today.strftime("%A").lower()
    today_events = EVENTS.get(day_key, [])

    return render_template(
        "index.html",
        today=today.strftime("%B %d, %Y"),
        weekday=today.strftime("%A"),
        events=today_events,
    )


if __name__ == "__main__":
    app.run(debug=True)
