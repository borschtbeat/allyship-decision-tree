from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey_labyrinth_v2"

# ------------------------------
# Stats & Sequence Tracking
# ------------------------------
INITIAL_STATS = {'integrity': 50, 'reflection': 50, 'ego_risk': 50}
MAX_REFLECTION = 100
MAX_EGO = 100

# Track sequences for mini-puzzles
PUZZLE_SEQUENCES = {
    "affirm_order": ["gelato_intro", "dubai_chocolate_intro", "mini_split_intro"]
}

# ------------------------------
# Node Tree with Mechanics
# ------------------------------
TREE = {
    "start": {
        "question": (
            "Welcome, brave explorer of cognitive oddities. "
            "Your mission: affirm Yehuda’s interests across Gelato, Dubai Chocolate, and Mini Split AC. "
            "Beware: your ego, attention, and reflection will be tested."
        ),
        "options": {
            "1": {"text": "Yes, I accept this daunting challenge", "next": "gelato_intro"},
            "2": {"text": "No, I must flee reality", "next": "end_not_ready"},
        }
    },

    # ---------------- Gelato Branch ----------------
    "gelato_intro": {
        "question": (
            "Gelato: not mere dessert, but an existential experience. "
            "Do you meditate on its flavors or proceed recklessly?"
        ),
        "options": {
            "1": {"text": "Meditate deeply", "next": "gelato_flavors", "stats": {"reflection": +10, "ego_risk": -5}},
            "2": {"text": "Act recklessly", "next": "dubai_chocolate_intro", "stats": {"ego_risk": +10}},
        }
    },
    "gelato_flavors": {
        "question": (
            "Consider pistachio, stracciatella, chocolate — metaphors for your own anxieties. "
            "Do you fully confront them or partially avoid reflection?"
        ),
        "options": {
            "1": {"text": "Fully confront", "next": "gelato_secret_meditation", "stats": {"reflection": +15, "integrity": +5}},
            "2": {"text": "Partially avoid", "next": "loop_gelato_reflection", "stats": {"ego_risk": +5}},
        }
    },
    "gelato_secret_meditation": {
        "requirements": {"reflection_min": 60, "ego_max": 50},  # conditional unlock
        "question": (
            "Secret Gelato Meditation unlocked! Pistachio cream as metaphor for impermanence. "
            "Do you meditate fully or retreat?"
        ),
        "options": {
            "1": {"text": "Meditate fully", "next": "dubai_chocolate_intro", "stats": {"reflection": +10, "ego_risk": -10}},
            "2": {"text": "Retreat", "next": "loop_gelato_reflection", "stats": {"ego_risk": +10}},
        }
    },
    "loop_gelato_reflection": {
        "question": (
            "You hesitate. Recommit or retreat? This may loop until you confront your ego."
        ),
        "options": {
            "1": {"text": "Recommit", "next": "dubai_chocolate_intro", "stats": {"reflection": +5, "ego_risk": +5}},
            "2": {"text": "Retreat", "next": "end_self_reflection_needed"},
        }
    },

    # ---------------- Dubai Chocolate Branch ----------------
    "dubai_chocolate_intro": {
        "question": (
            "Dubai Chocolate: saffron, cardamom, rosewater, existential dread. "
            "Study deeply or nod blindly?"
        ),
        "options": {
            "1": {"text": "Study deeply", "next": "dubai_chocolate_flavors", "stats": {"reflection": +10}},
            "2": {"text": "Nod blindly", "next": "mini_split_intro", "stats": {"ego_risk": +5}},
        }
    },
    "dubai_chocolate_flavors": {
        "question": (
            "Reflect on origin, roast, bitter-sweet harmony. Can you affirm without ego interference?"
        ),
        "options": {
            "1": {"text": "Suppress ego", "next": "mini_split_intro", "stats": {"reflection": +10, "ego_risk": -5}},
            "2": {"text": "Ego interferes", "next": "mini_split_intro", "stats": {"ego_risk": +10}},
        }
    },

    # ---------------- Mini Split AC Branch ----------------
    "mini_split_intro": {
        "question": (
            "Mini Split AC systems: hum silently, control comfort, represent obsession. "
            "Immerse in technical reflection or bluff confidently?"
        ),
        "options": {
            "1": {"text": "Immerse", "next": "mini_split_specs", "stats": {"reflection": +10}},
            "2": {"text": "Bluff", "next": "affirmation_summary", "stats": {"ego_risk": +10}},
        }
    },
    "mini_split_specs": {
        "question": (
            "SEER ratings, inverter tech, silent operation. Affirm without condescension or irony?"
        ),
        "options": {
            "1": {"text": "Yes, affirm humbly", "next": "affirmation_summary", "stats": {"integrity": +10}},
            "2": {"text": "No, too intimidating", "next": "loop_ac_reflection", "stats": {"ego_risk": +10}},
        }
    },
    "loop_ac_reflection": {
        "question": (
            "Your ego trembles. Recommit or retreat?"
        ),
        "options": {
            "1": {"text": "Recommit", "next": "affirmation_summary", "stats": {"reflection": +5, "ego_risk": +5}},
            "2": {"text": "Retreat", "next": "end_self_reflection_needed"},
        }
    },

    # ---------------- Mini-Puzzle Hidden Node ----------------
    "affirmation_order_puzzle": {
        "requirements": {"sequence": PUZZLE_SEQUENCES["affirm_order"]},
        "question": (
            "You notice a hidden order challenge: affirm Gelato, Dubai Chocolate, and Mini Split AC in sequence. "
            "Success unlocks the secret meta-reflection node."
        ),
        "options": {
            "1": {"text": "Attempt sequence", "next": "secret_meta_reflection", "stats": {"integrity": +15, "reflection": +10}},
        }
    },
    "secret_meta_reflection": {
        "question": (
            "Congratulations! You unlocked the meta-reflection: your careful attention has been noted. "
            "You now understand the absurd labyrinth of affirmation at a higher level."
        ),
        "options": {
            "1": {"text": "Proceed to summary", "next": "affirmation_summary"},
        }
    },

    # ---------------- Affirmation Summary ----------------
    "affirmation_summary": {
        "question": (
            "You have traversed Gelato, Dubai Chocolate, Mini Split AC, confronted loops, puzzles, and hidden paths. "
            "Shall we review your labyrinthine choices and evolving stats?"
        ),
        "options": {
            "1": {"text": "Yes, show summary", "next": "end_success"},
        }
    },

    # ---------------- End Nodes ----------------
    "end_not_ready": {"end": "You fled. Courage may return another day."},
    "end_self_reflection_needed": {"end": "Hesitation signals need for self-reflection."},
    "end_success": {"end": "Congratulations! You affirmed Yehuda's interests while navigating absurd labyrinthine challenges."}
}

# ------------------------------
# Helper Functions
# ------------------------------
def check_requirements(node_id):
    node = TREE[node_id]
    reqs = node.get("requirements", {})
    stats = session.get("stats", INITIAL_STATS)
    sequence = session.get("sequence", [])
    # Check reflection
    if "reflection_min" in reqs and stats["reflection"] < reqs["reflection_min"]:
        return False
    if "ego_max" in reqs and stats["ego_risk"] > reqs["ego_max"]:
        return False
    if "sequence" in reqs and sequence[-len(reqs["sequence"]):] != reqs["sequence"]:
        return False
    return True

# ------------------------------
# Routes
# ------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    session.clear()
    session['answers'] = []
    session['stats'] = INITIAL_STATS.copy()
    session['sequence'] = []
    return redirect(url_for("node", node="start"))

@app.route("/node/<node>", methods=["GET", "POST"])
def node(node):
    data = TREE.get(node)
    if not data:
        return "Invalid node", 404

    if 'answers' not in session:
        session['answers'] = []

    if request.method == "POST":
        selected = request.form.get("option")
        selected_text = request.form.get("option_text", "")
        next_node = TREE[node]["options"][selected]["next"]
        stats_effects = TREE[node]["options"][selected].get("stats", {})

        # Update stats dynamically
        for k, v in stats_effects.items():
            session['stats'][k] = max(0, session['stats'][k] + v)
            if k == "reflection":
                session['stats'][k] = min(MAX_REFLECTION, session['stats'][k])
            if k == "ego_risk":
                session['stats'][k] = min(MAX_EGO, session['stats'][k])

        # Track sequence for puzzles
        session['sequence'].append(node)

        # Track paragraph summary
        session['answers'].append(f"{data['question']} You chose: {selected_text}")

        # Check if next node is hidden/puzzle
        if "requirements" in TREE.get(next_node, {}) and not check_requirements(next_node):
            # skip to fallback if requirements not met
            return redirect(url_for("node", node="affirmation_summary"))

        return redirect(url_for("node", node=next_node))

    # End node
    if "end" in data:
        paragraph = " ".join(session.get('answers', []))
        final_message = f"{data['end']}\n\nSummary of your choices:\n{paragraph}"
        return render_template("node.html", question=final_message, options={}, end=True, stats=session['stats'])

    return render_template("node.html", question=data["question"], options=data.get("options", {}), end=False, stats=session['stats'])

# ------------------------------
# Run
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)
