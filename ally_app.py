from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey123"

# ------------------------------
# Ultra-Convoluted Decision Tree (No Name Tracking)
# ------------------------------

TREE = {
    "start": {
        "question": "Welcome! Do you want to begin the allyship assessment?",
        "options": {
            "1": ("Yes, let's begin", "intention_check"),
            "2": ("No, maybe later", "end_later"),
        }
    },

    # ----------------- Intention -----------------
    "intention_check": {
        "question": "What is your underlying intention in offering support?",
        "options": {
            "1": ("Genuine care and respect", "self_reflection_1"),
            "2": ("Mixed motives like approval-seeking", "self_reflection_1"),
            "3": ("Uncertain / confused", "self_reflection_1"),
        }
    },

    # ----------------- Self Reflection Loops -----------------
    "self_reflection_1": {
        "question": "Can you honestly acknowledge your motives without judgment?",
        "options": {
            "1": ("Yes", "self_reflection_2"),
            "2": ("No, need to reflect more", "loop_self_reflection_1"),
        }
    },

    "self_reflection_2": {
        "question": "Can you support without expecting reciprocity or approval?",
        "options": {
            "1": ("Yes", "consent_awareness"),
            "2": ("No, must reflect further", "loop_self_reflection_2"),
        }
    },

    "loop_self_reflection_1": {
        "question": (
            "Take a moment to consider your motives carefully. Are you ready to proceed?"
        ),
        "options": {
            "1": ("Yes, I am ready", "self_reflection_1"),
            "2": ("No, pause longer", "end_self_reflection_needed"),
        }
    },

    "loop_self_reflection_2": {
        "question": (
            "Notice the tension in your capacity. Can you pause and revisit your intentions later?"
        ),
        "options": {
            "1": ("Yes, I can pause", "self_reflection_1"),
            "2": ("No, continue anyway", "consent_awareness"),
        }
    },

    # ----------------- Consent -----------------
    "consent_awareness": {
        "question": "Have you observed any indication that support might be welcome?",
        "options": {
            "1": ("Yes", "capacity_check_1"),
            "2": ("Maybe, uncertain", "ask_for_consent"),
            "3": ("No", "end_respect_boundaries"),
        }
    },

    "ask_for_consent": {
        "question": (
            "You may ask neutrally: 'Would it be okay if I could be someone who shows up as a friend whenever you want?'"
        ),
        "options": {
            "1": ("They say yes", "capacity_check_1"),
            "2": ("They say maybe", "conditional_consent"),
            "3": ("They say no", "end_respect_boundaries"),
        }
    },

    "conditional_consent": {
        "question": "They want the option without expectation. Do you fully commit to respecting this?",
        "options": {
            "1": ("Yes, fully committed", "capacity_check_1"),
            "2": ("No, hesitant", "end_respect_boundaries"),
        }
    },

    # ----------------- Capacity Checks -----------------
    "capacity_check_1": {
        "question": "Do you currently have the emotional capacity to support ethically?",
        "options": {
            "1": ("Yes, fully", "capacity_check_2"),
            "2": ("Partially, I can be transparent", "capacity_check_2"),
            "3": ("No, I need to wait", "end_cannot_support"),
        }
    },

    "capacity_check_2": {
        "question": "Can you support without taking over, imposing, or expecting reciprocation?",
        "options": {
            "1": ("Yes", "offer_support"),
            "2": ("No", "loop_capacity_reflection"),
        }
    },

    "loop_capacity_reflection": {
        "question": (
            "Pause and reflect on your limits. Are you ready to reassess your capacity now?"
        ),
        "options": {
            "1": ("Yes, reassess", "capacity_check_2"),
            "2": ("No, I need more time", "end_self_reflection_needed"),
        }
    },

    # ----------------- Offering Support -----------------
    "offer_support": {
        "question": (
            "You may now offer support ethically:\n"
            "- Respect boundaries\n"
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
            "Do you commit to long-term allyship?\n"
            "Includes waiting for invitations, respecting boundaries, transparency, patience."
        ),
        "options": {
            "1": ("Yes, fully committed", "ethical_support"),
            "2": ("No, I need more preparation", "loop_self_reflection_2"),
        }
    },

    "ethical_support": {
        "question": (
            "You are now in Ethical Support Mode.\n"
            "Stay responsive, non-intrusive, and always follow boundaries."
        ),
        "options": {
            "1": ("Finish assessment", "end_success"),
        }
    },

    # ----------------- End Nodes -----------------
    "end_later": {"end": "Take your time. You can return later to begin the assessment."},
    "end_self_reflection_needed": {"end": "Self-reflection needed. Pause and ground yourself before proceeding."},
    "end_respect_boundaries": {"end": "Respect boundaries fully. Do not proceed."},
    "end_cannot_support": {"end": "You do not have capacity. Offering support may be harmful."},
    "end_success": {"end": "Congratulations! You may ethically show up as a friend when invited."},
}

# ------------------------------
# Routes
# ------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("node", node="start"))

@app.route("/node/<node>", methods=["GET", "POST"])
def node(node):
    data = TREE.get(node)
    if not data:
        return "Invalid node", 404

    # Handle end nodes
    if "end" in data:
        return render_template("node.html", question=data["end"], options={}, end=True, error=None)

    # Handle POST selection
    if request.method == "POST":
        next_node = request.form.get("option")
        if next_node in TREE:
            return redirect(url_for("node", node=next_node))

    return render_template("node.html", question=data["question"], options=data.get("options", {}), end=False, error=None)

# ------------------------------
# Run
# ------------------------------

if __name__ == "__main__":
    app.run(debug=True)
