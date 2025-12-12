from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey_game"

# ------------------------------
# Stats & Multi-Path Tree
# ------------------------------

TREE = {
    "start": {
        "question": (
            "Welcome, intrepid adventurer of subtle passions. Your task is to affirm Yehuda, "
            "a human of exquisite and particular interests. Be warned: this journey will confront your ego, "
            "challenge your capacity for reflection, and demand attention to detail. Are you prepared?"
        ),
        "options": {
            "1": ("Yes, I will attempt this arduous task", "gelato_intro"),
            "2": ("No, I need more courage", "end_not_ready"),
        }
    },

    # Gelato branch
    "gelato_intro": {
        "question": (
            "Gelato: more than dessert, it is an existential experience. "
            "Do you wish to meditate on textures and flavors before proceeding, or act without reflection?"
        ),
        "options": {
            "1": ("Meditate deeply on gelato", "gelato_flavors"),
            "2": ("Act without reflection", "dubai_chocolate_intro"),
        }
    },

    "gelato_flavors": {
        "question": (
            "Consider pistachio, chocolate, stracciatella: delicate interplay of cream, air, and subtle crunch. "
            "Can you honor Yehuda's preference without inserting your own faint biases?"
        ),
        "options": {
            "1": ("Yes, I can suppress my biases", "dubai_chocolate_intro"),
            "2": ("No, ego interferes", "loop_gelato_reflection"),
        }
    },

    "loop_gelato_reflection": {
        "question": (
            "You hesitate. Look into your own tendencies: do you retreat or recommit to careful affirmation?"
        ),
        "options": {
            "1": ("Recommit, however trembling", "dubai_chocolate_intro"),
            "2": ("Retreat, acknowledge limits", "end_self_reflection_needed"),
        }
    },

    # Dubai Chocolate branch
    "dubai_chocolate_intro": {
        "question": (
            "Dubai chocolate: saffron, cardamom, rosewater. Will you study these flavors deeply "
            "or nod along without comprehension?"
        ),
        "options": {
            "1": ("Study deeply", "dubai_chocolate_flavors"),
            "2": ("Nod along", "mini_split_intro"),
        }
    },

    "dubai_chocolate_flavors": {
        "question": (
            "Reflect on cacao origin, roast, and bitter-sweet balance. "
            "Can you affirm without imposing ego-driven opinions?"
        ),
        "options": {
            "1": ("Yes, ego subdued", "mini_split_intro"),
            "2": ("No, ego intrudes", "mini_split_intro"),
        }
    },

    # Mini split AC branch
    "mini_split_intro": {
        "question": (
            "Mini split AC systems: a symbol of comfort, autonomy, and obsessive precision. "
            "Will you immerse yourself in technical reflection, or bluff confidently?"
        ),
        "options": {
            "1": ("Immerse in technical reflection", "mini_split_specs"),
            "2": ("Bluff confidently", "affirmation_summary"),
        }
    },

    "mini_split_specs": {
        "question": (
            "Consider SEER ratings, inverter tech, silent operation. "
            "Can you affirm without condescension or irony?"
        ),
        "options": {
            "1": ("Yes, fully affirm", "affirmation_summary"),
            "2": ("No, too intimidating", "loop_ac_reflection"),
        }
    },

    "loop_ac_reflection": {
        "question": (
            "Pause. Breathe. Will you recommit to affirming Yehuda while confronting your ego?"
        ),
        "options": {
            "1": ("Yes, recommit", "affirmation_summary"),
            "2": ("No, retreat", "end_self_reflection_needed"),
        }
    },

    # Summary node
    "affirmation_summary": {
        "question": (
            "You have navigated the labyrinth of gelato, Dubai chocolate, and mini split AC systems. "
            "Shall we review your choices, the evolution of your stats, and the subtle reflection of your ego?"
        ),
        "options": {
            "1": ("Yes, show summary", "end_success"),
        }
    },

    # End nodes
    "end_not_ready": {
        "end": "You hesitated and withdrew. Perhaps reflection will aid future affirmation."
    },
    "end_self_reflection_needed": {
        "end": "Internal conflicts prevent further progress. Self-reflection required."
    },
    "end_success": {
        "end": "Congratulations! You have affirmed Yehuda’s interests while navigating your ego and reflection carefully."
    },
}

# ------------------------------
# Routes & Game Logic
# ------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    session.clear()
    session['answers'] = []
    session['stats'] = {'integrity': 50, 'reflection': 50, 'ego_risk': 50}
    return redirect(url_for("node", node="start"))

@app.route("/node/<node>", methods=["GET", "POST"])
def node(node):
    data = TREE.get(node)
    if not data:
        return "Invalid node", 404

    if 'answers' not in session:
        session['answers'] = []

    if request.method == "POST":
        next_node = request.form.get("option")
        if next_node:
            # Adjust stats slightly based on choices
            if next_node in ['gelato_flavors', 'dubai_chocolate_flavors', 'mini_split_specs']:
                session['stats']['reflection'] += 10
                session['stats']['ego_risk'] -= 5
            elif next_node in ['loop_gelato_reflection', 'loop_ac_reflection']:
                session['stats']['reflection'] += 5
                session['stats']['ego_risk'] += 5
            session['answers'].append(f"{data['question']} You chose: {request.form.get('option_text', next_node)}.")
            return redirect(url_for("node", node=next_node))

    # End node
    if "end" in data:
        paragraph = " ".join(session.get('answers', []))
        final_message = f"{data['end']}\n\nSummary of your choices:\n{paragraph}"
        return render_template("node.html", question=final_message, options={}, end=True, stats=session['stats'])

    return render_template("node.html", question=data["question"], options=data.get("options", {}), end=False, stats=session['stats'])

# ------------------------------
# Run App
# ------------------------------

if __name__ == "__main__":
    app.run(debug=True)
