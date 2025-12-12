from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey123"  # Needed for session storage

# ------------------------------
# Personalized Decision Tree
# ------------------------------

TREE = {
    "start": {
        "question": "Welcome! What's your name?",
        "options": {
            "1": ("Enter name", "enter_name")
        }
    },

    "enter_name": {
        "question": "Please type your name below and submit.",
        "options": {},  # Special handling
    },

    "greeting": {
        "question": "Hello, {name}! Do you want to begin the allyship assessment?",
        "options": {
            "1": ("Yes, let's start", "intention_check"),
            "2": ("No, maybe later", "end_later"),
        }
    },

    "intention_check": {
        "question": "{name}, what is your true intention in offering support to Joanna?",
        "options": {
            "1": ("Genuine care and respect for autonomy", "self_reflection"),
            "2": ("Mixed motives, like approval-seeking or expectation", "self_reflection"),
            "3": ("Not sure", "self_reflection"),
        }
    },

    "self_reflection": {
        "question": "{name}, can you honestly examine your motives without judgment?",
        "options": {
            "1": ("Yes", "consent_awareness"),
            "2": ("No", "self_inquiry_loop"),
        }
    },

    "self_inquiry_loop": {
        "question": (
            "{name}, let's do a self-inquiry:\n"
            "- Are you seeking approval or trying to fix?\n"
            "- Are you emotionally grounded to help without burdening?\n"
            "- Can you respect boundaries without resentment?"
        ),
        "options": {
            "1": ("Yes, I can", "consent_awareness"),
            "2": ("No, I need more self-reflection", "end_self_reflection_needed"),
        }
    },

    "consent_awareness": {
        "question": (
            "{name}, have you observed if Joanna would ever welcome support from you?"
        ),
        "options": {
            "1": ("Yes", "capacity_check"),
            "2": ("Maybe / Not sure", "ask_for_consent"),
            "3": ("No", "end_respect_boundaries"),
        }
    },

    "ask_for_consent": {
        "question": (
            "{name}, you can ask Joanna neutrally: "
            "'Would it be okay if I were someone who could show up as a friend when you want?'"
        ),
        "options": {
            "1": ("She says yes", "capacity_check"),
            "2": ("She says maybe", "conditional_consent"),
            "3": ("She says no", "end_respect_boundaries"),
        }
    },

    "conditional_consent": {
        "question": (
            "{name}, she wants the option without expectation. Do you agree to honor this fully?"
        ),
        "options": {
            "1": ("Yes", "capacity_check"),
            "2": ("No", "end_respect_boundaries"),
        }
    },

    "capacity_check": {
        "question": "{name}, do you have the emotional capacity to show up as requested?",
        "options": {
            "1": ("Yes, I can handle it", "ethical_support"),
            "2": ("Limited capacity, can be transparent", "ethical_support"),
            "3": ("No capacity", "end_cannot_support"),
        }
    },

    "ethical_support": {
        "question": (
            "{name}, you may now offer support ethically:\n"
            "- Follow Joanna's boundaries\n"
            "- Offer without expecting\n"
            "- Stay flexible and patient"
        ),
        "options": {
            "1": ("Finish", "end_success")
        }
    },

    # ----------------------------------
    # End nodes
    # ----------------------------------
    "end_self_reflection_needed": {"end": "Self-reflection required. Take time before offering support."},
    "end_respect_boundaries": {"end": "Respect Joanna's boundaries. Do not proceed."},
    "end_cannot_support": {"end": "Without capacity, offering support may be harmful."},
    "end_success": {"end": "Congratulations, {name}! You may ethically show up as a friend when invited."},
    "end_later": {"end": "Take your time, {name}. You can return later to begin the assessment."}
}

# ------------------------------
# Routes
# ------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    session.clear()
    return redirect(url_for("node", node="start"))


@app.route("/node/<node>", methods=["GET", "POST"])
def node(node):
    data = TREE.get(node)

    if not data:
        return "Invalid node", 404

    # Handle end nodes
    if "end" in data:
        question_text = data["end"]
        if "name" in session:
            question_text = question_text.format(name=session["name"])
        return render_template("node.html", question=question_text, options={}, end=True)

    # Handle special name entry
    if node == "enter_name" and request.method == "POST":
        name_input = request.form.get("name_input", "").strip()
        if name_input:
            session["name"] = name_input
            return redirect(url_for("node", node="greeting"))
        else:
            return render_template("enter_name.html", error="Please enter a name.")

    # Format question with name if available
    question_text = data["question"]
    if "name" in session:
        question_text = question_text.format(name=session["name"])

    return render_template(
        "node.html",
        question=question_text,
        options=data.get("options", {}),
        end=False
    )

# ------------------------------
# Run
# ------------------------------

if __name__ == "__main__":
    app.run(debug=True)
