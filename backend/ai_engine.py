from collections import Counter


def categorize_app(app_name):

    app = app_name.lower()

    if "visual studio" in app or "vscode" in app:
        return "Coding"

    elif "github" in app:
        return "Coding"

    elif "chatgpt" in app:
        return "AI Work"

    elif "gmail" in app:
        return "Email"

    elif "youtube" in app:
        return "Learning"

    elif "linkedin" in app:
        return "Networking"

    elif "meet" in app or "zoom" in app:
        return "Meetings"

    elif "netflix" in app:
        return "Entertainment"

    elif "whatsapp" in app:
        return "Communication"

    elif "chrome" in app:
        return "Research"

    else:
        return "Other"


def calculate_score(counts):

    productive = (
        counts.get("Coding", 0)
        + counts.get("AI Work", 0)
        + counts.get("Learning", 0)
    )

    distracting = (
        counts.get("Entertainment", 0)
        + counts.get("Communication", 0)
    )

    total = productive + distracting

    if total == 0:
        return 50

    score = int((productive / total) * 100)

    return min(score, 100)


from collections import Counter


def analyze_behavior(rows):

    categories = []

    for row in rows:

        app_name = row[0]

        category = categorize_app(app_name)

        categories.append(category)

    counts = Counter(categories)

    insights = []

    coding = counts.get("Coding", 0)
    research = counts.get("Research", 0)
    entertainment = counts.get("Entertainment", 0)
    ai_work = counts.get("AI Work", 0)

    if coding > 20:
        insights.append(
            "Strong coding productivity detected."
        )

    if research > coding:
        insights.append(
            "Research activity exceeded implementation work."
        )

    if entertainment > 10:
        insights.append(
            "Entertainment usage is increasing."
        )

    if ai_work > 5:
        insights.append(
            "AI-assisted workflow is actively being used."
        )

    if len(rows) > 50:
        insights.append(
            "High context switching detected."
        )

    productivity_score = calculate_score(counts)

    dashboard_counts = {

        "coding":
            counts.get("Coding", 0)
            + counts.get("AI Work", 0),

        "browsing":
            counts.get("Research", 0)
            + counts.get("Learning", 0),

        "email":
            counts.get("Email", 0)
            + counts.get("Communication", 0)

    }

    return {
        "counts": dashboard_counts,
        "raw_counts": dict(counts),
        "insights": insights,
        "score": productivity_score
    }

def detect_focus_session(rows):

    if len(rows) < 5:

        return {
            "focused": False,
            "message": "Not enough activity data."
        }

    recent = rows[:10]

    categories = []

    for row in recent:
        categories.append(
            categorize_app(row[0])
        )

    dominant = Counter(categories).most_common(1)[0]

    category = dominant[0]
    count = dominant[1]

    if count >= 7:

        return {
            "focused": True,
            "message": f"Deep focus session detected in {category}."
        }

    return {
        "focused": False,
        "message": "Frequent context switching detected."
    }