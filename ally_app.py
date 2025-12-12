from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey123"

# ------------------------------
# Ultra-Convoluted Personalized Decision Tree
# ------------------------------

TREE = {
    "start": {
        "question": "Welcome! Please type your name below and submit to begin the allyship assessment.",
        "options": {},  # special handling for text input
    },

    "greeting": {
        "question": "Hello, {name}! Do you want to start the allyship assessment now?",
        "options": {
            "1": ("Yes, let's begin", "intention_check"),
            "2": ("No, maybe later", "end_later"),
        }
    },

    # ----------------- Intention -----------------
    "intention_check": {
        "question": "{name}, what is your underlying intention in offering support to Joanna?",
        "options": {
            "1": ("Genuine care and respect", "self_reflection_1"),
            "2": ("Mixed motives like approval-seeking", "self_reflection_1"),
            "3": ("Uncertain / confused", "self_reflection_1"),
        }
    },

    # ----------------- Self Reflection Loops -----------------
    "self_reflection_1": {
        "question": "{name}, can you honestly acknowledge your motives without judgment?",
        "options": {
            "1": ("Yes", "self_reflection_2"),
            "2": ("No, need to reflect more", "loop_self_reflection_1"),
        }
    },

    "self_reflection_2": {
        "question": "{name}, can you support without expecting reciprocity or approval?",
        "options": {
            "1": ("Yes", "consent_awareness"),
            "2": ("No, must reflect further", "loop_self_reflection_2"),
        }
    },

    "loop_self_reflection_1": {
        "question": (
            "{name}, take a moment to consider your motives carefully. Are you ready to proceed?"
        ),
        "options": {
            "1": ("Yes, I am ready", "self_reflection_1"),
            "2": ("No, pause longer", "end_self_reflection_needed"),
        }
    },

    "loop_self_reflection_2": {
        "question": (
            "{name}, notice the tension in your capacity. Can you pause and revisit your intentions later?"
        ),
        "options": {
            "1": ("Yes, I can pause", "self_reflection_1"),
            "2": ("No, continue anyway", "consent_awareness"),
        }
    },

    # ----------------- Consent -----------------
    "consent_awareness": {
        "question": "{name}, have you observed any indication that Joanna might welcome support?",
        "options": {
            "1": ("Yes", "capacity_check_1"),
            "2": ("Maybe, uncertain", "ask_for_consent"),
            "3": ("No", "end_respect_boundaries"),
        }
    },

    "ask_for_consent": {
        "question": (
            "{name}, you may ask Joanna neutrally: "
            "'Would it be okay if I could be someone who shows up as a friend whenever you want?'"
        ),
        "options": {
            "1": ("She says yes", "capacity_check_1"),
            "2": ("She says maybe", "conditional_consent"),
            "3": ("She says no", "end_respect_boundaries"),
        }
    },

    "conditional_consent": {
        "question": "{name}, she wants the option without expectation. Do you fully commit to respecting this?",
        "options": {
            "1": ("Yes, fully committed", "capacity_check_1"),
            "2": ("No, I am hesitant", "end_respect_boundaries"),
        }
    },

    # ----------------- Capacity Checks -----------------
    "capacity_check_1": {
        "question": "{name}, do you currently have the emotional capacity to support ethically?",
        "options": {
            "1": ("Yes, fully", "capacity_check_2"),
            "2": ("Partially, I can be transparent", "capacity_check_2"),
            "3": ("No, I need to wait", "end_cannot_support"),
        }
    },

    "capacity_check_2": {
        "question": (
            "{name}, can you support without taking over, imposing, or expecting reciprocation?"
        ),
        "options": {
            "1": ("Yes", "offer_support"),
            "2": ("No", "loop_capacity_reflection"),
        }
    },

    "loop_capacity_reflection": {
        "question": (
            "{name}, pause and reflect on your limits. Are you ready to reassess your capacity now?"
        ),
        "options": {
            "1": ("Yes, reassess", "capacity_check_2"),
            "2": ("No, I need more time", "end_self_reflection_needed"),
        }
    },

    # ----------------- Offering Support -----------------
    "offer_support": {
        "question": (
            "{name}, you may now offer support ethically:\n"
            "- Respect Joanna's boundaries\n"
            "- Stay responsive when invited\n"
            "- Remain non-intrusive and patient"
        ),
        "options": {
            "1": ("Proceed to long-term planning", "long_term_support"),
        }
    },

    # ----------------- Long-Term Support -----------------
    "long_term_support": {
        "question": (
            "{name}, do you commit to long-term allyship?\n"
            "Consider: waiting for invitations, respecting boundaries, transparency, patience."
        ),
        "options": {
            "1": ("Yes, fully committed", "ethical_support"),
            "2": ("No, I need more preparation", "loop_self_reflection_2"),
        }
    },

    "ethical_support": {
        "question": (
            "{name}, you are now in Ethical Support Mode.\n"
            "Stay responsive, non-intrusive, and always follow Joanna's boundaries."
        ),
        "options": {
            "1": ("Finish assessment", "end_success"),
        }
    },

    # ----------------- End Nodes -----------------
    "end_later": {"end": "Take your time, {name}. You can return later to begin the assessment."},
    "end_self_reflection_needed": {"end": "Self-reflection needed. Pause and ground yourself, {name}."},
    "end_respect_boundaries": {"end": "Respect Joanna's boundaries fully. Do not proceed, {name}."},
    "end_cannot_support": {"end": "You do not have capacity. Offering support may be harmful, {name}."},
    "end_success": {"end": "Congratulations, {name}! You may ethically show up as a friend when invited."},
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

    # Handle first name entry
    if node == "start" and request.method == "POST":
        name_input = request.form.get("name_input", "").strip()
        if name_input:
            session["name"] = name_input
            return redirect(url_for("node", node="greeting"))
        else:
            return render_template("node.html", question=data["question"], options={}, end=False, error="Please enter a name.")

    # Prepare question text
    question_text = data["question"]
    if "name" in session:
        question_text = question_text.format(name=session["name"])

    return render_template("node.html", question=question_text, options=data.get("options", {}), end=False, error=None)

# ------------------------------
# Run
# ------------------------------

if __name__ == "__main__":
    app.run(debug=True)
