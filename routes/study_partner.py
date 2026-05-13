from flask import Blueprint, request, jsonify
from models.planner import generate_plan

study_partner = Blueprint('study_partner', __name__)

# 📅 STUDY PLANNER
@study_partner.route('/planner', methods=['POST'])
def planner():
    data = request.json

    subjects = data.get('subjects')
    hours = data.get('hours')
    days = data.get('days')

    plan = generate_plan(subjects, hours, days)

    return jsonify(plan)


# 📚 RESOURCE FINDER (UPGRADED)
@study_partner.route('/resources', methods=['POST'])
def get_resources():
    topic = request.json.get('topic')

    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    return jsonify({
        "youtube": f"https://www.youtube.com/results?search_query={topic}+tutorial+explained",
        "articles": f"https://www.google.com/search?q={topic}+full+explanation+beginner+guide",
        "pdfs": f"https://www.google.com/search?q={topic}+notes+filetype:pdf"
    })