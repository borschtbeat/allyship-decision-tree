from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey789"

# ------------------------------
# Ultra-Verbose Yehuda Assessment Tree
# ------------------------------

TREE = {
    "start": {
        "question": (
            "Greetings, intrepid explorer of subtle passions. Before you lies the task of affirming Yehuda, "
            "a human being of exceedingly particular interests. This is not a task for the faint-hearted, nor "
            "for those unwilling to gaze into the reflective pool of their own motives. Do you, with your fragile ego "
            "and tentative intentions, believe yourself capable of embarking on this journey of affirmational exploration? "
            "You must confront not only Yehuda's peculiar affinities, but also the unsettling depths of your own internal scripts."
        ),
        "options": {
            "1": ("Yes, I suppose I can try", "gelato_intro"),
            "2": ("No, I am not ready to face my inadequacies", "end_not_ready"),
        }
    },

    # ----------------- Gelato -----------------
    "gelato_intro": {
        "question": (
            "Ah, gelato. Such an innocent word, yet it harbors multitudes. You may think, 'It’s just frozen cream,' "
            "but oh, how naive you would be. Each flavor, each velvety texture, each whisper of cold air brushing the tongue "
            "is laden with the psychic weight of existential joy and minor trauma. Do you wish to pause and meditate upon "
            "the metaphysical implications of gelato before attempting to converse meaningfully with Yehuda?"
        ),
        "options": {
            "1": ("Yes, I shall meditate, however painfully", "gelato_flavor_reflection"),
            "2": ("No, let me plunge recklessly into affirmation", "dubai_chocolate_intro"),
        }
    },

    "gelato_flavor_reflection": {
        "question": (
            "Consider, if you can without shattering your sense of self: the pistachio, the hazelnut, "
            "the chocolate that is not chocolate but a reflection of lost childhood dreams. Can you truly honor Yehuda’s preference "
            "without succumbing to the insidious pull of your own vanilla biases? Remember, self-deception is the first whisper of catastrophe."
        ),
        "options": {
            "1": ("Yes, I can sublimate my biases", "gelato_textural_depth"),
            "2": ("No, I am too self-absorbed", "dubai_chocolate_intro"),
        }
    },

    "gelato_textural_depth": {
        "question": (
            "Do you possess the courage, or perhaps the foolhardy audacity, to discuss gelato with Yehuda "
            "in a manner that conveys awareness of aeration, crystallization, and the slight, terrifying unpredictability of melted edges? "
            "This is a test not only of your capacity to affirm but of your humility in acknowledging the sublime in small things."
        ),
        "options": {
            "1": ("Yes, I shall proceed with trembling respect", "dubai_chocolate_intro"),
            "2": ("No, my trembling will betray me", "loop_gelato_reflection"),
        }
    },

    "loop_gelato_reflection": {
        "question": (
            "Pause. Breathe. Perhaps stare into a reflective surface and ask: 'Am I ready to encounter the unmediated experience of gelato, "
            "to affirm without contaminating the sacred sphere of Yehuda’s delight?' Will you recommit, or forever remain in hesitant limbo?"
        ),
        "options": {
            "1": ("Yes, I recommit, however shakily", "dubai_chocolate_intro"),
            "2": ("No, I fear my own incompetence", "end_self_reflection_needed"),
        }
    },

    # ----------------- Dubai Chocolate -----------------
    "dubai_chocolate_intro": {
        "question": (
            "Onward, to Dubai chocolate — a terrain of complexity and occasional absurdity. "
            "You may think chocolate is merely sweet, but Yehuda knows better. There is saffron, cardamom, rosewater, "
            "and perhaps a lingering whisper of existential dread. Do you wish to linger in contemplation of these aromas, "
            "or barrel ahead with reckless affirmation?"
        ),
        "options": {
            "1": ("Yes, I shall inhale deeply the essence of Dubai chocolate", "dubai_chocolate_flavors"),
            "2": ("No, forward, with all my naive certainty", "mini_split_intro"),
        }
    },

    "dubai_chocolate_flavors": {
        "question": (
            "Think carefully: are you prepared to honor the delicate interplay between bitter cacao and fleeting sweetness, "
            "to recognize that each bite is an allegory of choice, mortality, and subtle preference? "
            "Can you discuss this without unintentionally asserting your unworthy opinions upon Yehuda?"
        ),
        "options": {
            "1": ("Yes, I can suppress my ego", "mini_split_intro"),
            "2": ("No, ego inevitably seeps through", "mini_split_intro"),
        }
    },

    # ----------------- Mini Split AC -----------------
    "mini_split_intro": {
        "question": (
            "Finally, we reach the towering edifice of Yehuda’s interests: the mini split air conditioning system. "
            "Ah, SEER ratings, inverter technologies, ductless configurations — these are not mere appliances. "
            "They are symbols of autonomy, comfort, and a peculiar obsession with silent hums. "
            "Do you dare to study them in sufficient depth to affirm Yehuda competently, or will you bluff your way through with hollow nods?"
        ),
        "options": {
            "1": ("Yes, I shall study until my mind aches", "mini_split_specs"),
            "2": ("No, I shall bluff and hope for the best", "affirmation_summary"),
        }
    },

    "mini_split_specs": {
        "question": (
            "Consider: the energy efficiency, the positioning of indoor units, the subtle art of temperature zoning. "
            "Do you now feel capable of discussing these systems without the faintest tremor of condescension or unintended irony "
            "creeping into your words?"
        ),
        "options": {
            "1": ("Yes, tremor subdued", "affirmation_summary"),
            "2": ("No, the weight is too great", "loop_ac_reflection"),
        }
    },

    "loop_ac_reflection": {
        "question": (
            "Pause. Reflect. Feel the unsettling pull of inadequacy. Can you, after meditation and gentle self-scolding, "
            "recommit to affirming Yehuda’s interests without contamination of your ego?"
        ),
        "options": {
            "1": ("Yes, I recommit, trembling and enlightened", "affirmation_summary"),
            "2": ("No, I retreat into shadow", "end_self_reflection_needed"),
        }
    },

    # ----------------- Affirmation Summary -----------------
    "affirmation_summary": {
        "question": (
            "You have traversed the labyrinthine corridors of gelato, Dubai chocolate, and mini split air conditioning systems. "
            "Shall we now summarize your journey, your choices, your tentative acts of affirmation, and gaze collectively upon the tapestry "
            "of your own hesitant self-awareness?"
        ),
        "options": {
            "1": ("Yes, show me the tapestry", "end_success"),
        }
    },

    # ----------------- End Nodes -----------------
    "end_not_ready": {
        "end": "You hesitated and withdrew. Perhaps one day you will find the courage to face your own subtle flaws and affirm Yehuda's interests with care."
    },
    "end_self_reflection_needed": {
        "end": "Your internal conflicts are too pronounced. Self-reflection and contemplation are required before any genuine affirmation can occur."
    },
    "end_success": {
        "end": "Congratulations. You have wandered through the cognitive jungle of Yehuda’s interests, faced your own psychological eccentricities, and emerged with the capacity to affirm responsibly."
    },
}

# ------------------------------
# Routes
# ------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    session.clear()
    session['answers'] = []
    return redirect(url_for("node", node="start"))

@app.route("/node/<node>", methods=["GET", "POST"])
def node(node):
    data = TREE.get(node)
    if not data:
        return "Invalid node", 404

    if 'answers' not in session:
        session['answers'] = []

    # Handle POST selection
    if request.method == "POST":
        next_node = request.form.get("option")
        if next_node:
            selected_text = None
            for key, (text, n_node) in data.get("options", {}).items():
                if n_node == next_node:
                    selected_text = text
                    break
            if selected_text:
                session['answers'].append(f"{data['question']} You chose: {selected_text}.")
            return redirect(url_for("node", node=next_node))

    # Handle end nodes
    if "end" in data:
        paragraph = " ".join(session.get('answers', []))
        final_message = f"{data['end']}\n\nSummary of your choices:\n{paragraph}"
        return render_template("node.html", question=final_message, options={}, end=True, error=None)

    return render_template("node.html", question=data["question"], options=data.get("options", {}), end=False, error=None)

# ------------------------------
# Run
# ------------------------------

if __name__ == "__main__":
    app.run(debug=True)
