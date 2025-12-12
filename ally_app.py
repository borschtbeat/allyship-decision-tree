from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey123"  # Needed for session storage

# ------------------------------
# Ultra-Complicated Personalized Decision Tree
# ------------------------------

TREE = {
    "start": {
        "question": "Welcome! What's your name?",
        "options": {"1": ("Enter name", "enter_name")}
    },
    "enter_name": {
        "question": "Please type your name below and submit.",
        "options": {}  # Handled specially
    },

    "greeting": {
        "question": "Hello, {name}! Do you want to begin the allyship assessment?",
        "options": {
            "1": ("Yes, let's start", "intention_check"),
            "2": ("No, maybe later", "end_later")
        }
    },

    # ----------------- Intention Checks -----------------
    "intention_check": {
        "question": "{name}, what is your core intention in offering support to Joanna?",
        "options": {
            "1": ("Genuine care and respect", "self_reflection_1"),
            "2": ("Mixed motives, e.g., approval-seeking", "self_reflection_1"),
            "3": ("Uncertain or confused", "self_reflection_1")
        }
    },

    # ----------------- Self Reflection -----------------
    "self_reflection_1": {
        "question": (
            "{name}, reflect honestly: Are you seeking approval or trying to fix rather than support?"
        ),
        "options": {
            "1": ("Yes, I am aware and can manage", "self_reflection_2"),
            "2": ("No, I need more introspection", "loop_self_reflection")
        }
    },

    "self_reflection_2": {
        "question": (
            "{name}, can you remain emotionally grounded and help without burdening Joanna?"
        ),
        "options": {
            "1": ("Yes", "consent_awareness"),
            "2": ("No", "loop_self_reflection")
        }
    },

    "loop_self_reflection": {
        "question": (
            "{name}, let's loop back: Take a deep pause, reflect on your motives, and return when ready."
        ),
        "options": {
            "1": ("I'm ready to continue", "self_reflection_1")
        }
    },

    # ----------------- Consent Awareness -----------------
    "consent_awareness": {
        "question": "{name}, have you observed if Joanna might welcome your support?",
        "options": {
            "1": ("Yes, signs of welcome", "capacity_check_1"),
            "2": ("Maybe, unsure", "ask_for_consent"),
            "3": ("No, she seems uncomfortable", "end_respect_boundaries")
        }
    },

    "ask_for_consent": {
        "question": (
            "{name}, you may ask neutrally: "
            "'Would it be okay if I could be someone who shows up as a friend whenever you want?'"
        ),
        "options": {
            "1": ("She says yes", "capacity_check_1"),
            "2": ("She says maybe", "conditional_consent_1"),
            "3": ("She says no", "end_respect_boundaries")
        }
    },

    "conditional_consent_1": {
        "question": (
            "{name}, she wants the option without expectation. Do you fully agree to honor this?"
        ),
        "options": {
            "1": ("Yes", "capacity_check_1"),
            "2": ("No", "end_respect_boundaries")
        }
    },

    # ----------------- Capacity Checks -----------------
    "capacity_check_1": {
        "question": "{name}, do you currently have the emotional capacity to support ethically?",
        "options": {
            "1": ("Yes, fully", "capacity_check_2"),
            "2": ("Partially, can be transparent", "capacity_check_2"),
            "3": ("No, need to wait", "end_cannot_support")
        }
    },

    "capacity_check_2": {
        "question": (
            "{name}, can you support without taking over, expecting reciprocation, or overstepping?"
        ),
        "options": {
            "1": ("Yes", "offer_support"),
            "2": ("No", "loop_capacity_reflection")
        }
    },

    "loop_capacity_reflection": {
        "question": (
            "{name}, take time to assess your limits and boundaries. Returning only when ready is crucial."
        ),
        "options": {
            "1": ("I'm ready now", "capacity_check_2")
        }
    },

    # ----------------- Offer -----------------
    "offer_support": {
        "question": (
            "{name}, you may now offer support ethically:\n"
            "- Follow Joanna's boundaries\n"
            "- Offer without expecting\n"
            "- Stay flexible and patient"
        ),
        "options": {
            "1": ("Proceed to long-term planning", "long_term_support")
        }
    },

    # ----------------- Long-Term Support -----------------
    "long_term_support": {
        "question": (
            "{name}, do you commit to long-term allyship if she accepts?\n"
            "Includes:\n"
            "1. Waiting for invitations\n"
            "2. Respecting all boundaries\n"
            "3. Transparency about your capacity"
        ),
        "options": {
            "1": ("Yes, fully committed", "ethical_support_2"),
            "2": ("No, need more preparation", "loop_self_reflection")
        }
    },

    "ethical_support_2": {
        "question": (
            "{name}, you are in Ethical Support Mode:\n"
            "Remain responsive when invited, non-intrusive, and mindful of Joanna's autonomy."
        ),
        "options": {
            "1": ("Finish assessment", "end_success")
        }
    },

    # ----------------- End Nodes -----------------
    "end_later": {"end": "Take your time, {name}. You can return later to begin the assessment."},
    "end_self_reflection_needed": {"end": "Self-reflection needed. Wait until fully grounded, {name}."},
    "end_respect_boundaries": {"end": "Respect Joanna's boundaries fully, {name}. Do not proceed."},
    "end_cannot_support": {"end": "You do not have capacity. Offering support may be harmful, {name}."},
    "end_success": {"end": "Congratulations, {name}! You may ethically show up as a friend when invited."}
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
