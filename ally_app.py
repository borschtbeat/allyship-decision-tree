from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ------------------------------
# Decision Tree Structure
# ------------------------------

TREE = {
    "root": {
        "question": "ROOT NODE (0): What is your true intention?",
        "options": {
            "1": ("Genuine care & respect for Joanna's autonomy", "intention_yes"),
            "2": ("Motivated by guilt, approval-seeking, romantic longing, or saviorism", "intention_no"),
            "3": ("I'm not sure what my intention is", "self_inquiry"),
        }
    },

    # ----------------------------------
    # Intention Checks
    # ----------------------------------
    "intention_yes": {
        "question": "0A: Can you strip your offer of all expectations?",
        "options": {
            "1": ("Yes", "external_safety"),
            "2": ("No", "self_inquiry"),
        }
    },

    "intention_no": {
        "question": "0A: Can you strip your offer of all expectations?",
        "options": {
            "1": ("Yes", "external_safety"),
            "2": ("No", "self_inquiry"),
        }
    },

    # ----------------------------------
    # Self-Inquiry Loop
    # ----------------------------------
    "self_inquiry": {
        "question": (
            "0B: Self-Inquiry Loop\n"
            "Did you answer YES to at least 2/3?\n"
            "• Are you asking for her trust before earning it?\n"
            "• Are you trying to fix instead of support?\n"
            "• Are you emotionally grounded enough to help without burdening?"
        ),
        "options": {
            "1": ("Yes", "root"),
            "2": ("No", "allyship_readiness"),
        }
    },

    # ----------------------------------
    # Allyship Readiness
    # ----------------------------------
    "allyship_readiness": {
        "question": "0C: Do you respect boundaries without resentment?",
        "options": {
            "1": ("Yes", "allyship_readiness_2"),
            "2": ("No", "end_not_ready_1"),
        }
    },

    "allyship_readiness_2": {
        "question": "Do you accept that allyship means only offering proximity when INVITED?",
        "options": {
            "1": ("Yes", "allyship_readiness_3"),
            "2": ("No", "end_not_ready_2"),
        }
    },

    "allyship_readiness_3": {
        "question": "Can you be dependable without being intrusive?",
        "options": {
            "1": ("Yes", "external_safety"),
            "2": ("No", "end_not_ready_3"),
        }
    },

    # ----------------------------------
    # Safety Checks
    # ----------------------------------
    "external_safety": {
        "question": "1: Does Joanna feel safe around you?",
        "options": {
            "1": ("Yes", "consent_autonomy"),
            "2": ("Unsure", "safety_clarity"),
            "3": ("No", "end_safety"),
        }
    },

    "safety_clarity": {
        "question": "1A: Can you ask neutrally: 'Would it feel comfortable if I offered support?'",
        "options": {
            "1": ("Yes", "consent_autonomy"),
            "2": ("No", "end_cannot_ask"),
        }
    },

    # ----------------------------------
    # Consent & Autonomy
    # ----------------------------------
    "consent_autonomy": {
        "question": "2: Has Joanna EVER shown she would welcome support?",
        "options": {
            "1": ("Yes", "capacity_check"),
            "2": ("No / Not sure", "consent_inquiry"),
        }
    },

    "consent_inquiry": {
        "question": "2A: She is asked: 'Would you want me to be someone who can show up when you want?'",
        "options": {
            "1": ("She says YES", "capacity_check"),
            "2": ("She says MAYBE", "conditional_consent"),
            "3": ("She says NO", "end_boundaries_no"),
        }
    },

    "conditional_consent": {
        "question": "2B: Does she want the OPTION of support without expectation?",
        "options": {
            "1": ("Yes", "capacity_check"),
            "2": ("No", "end_no_option"),
            "3": ("Wants to revisit later", "long_term_mode"),
        }
    },

    "long_term_mode": {
        "question": "5: Long-Term Allyship Mode.\nStay present. Wait for HER to reopen the topic.",
        "options": {
            "1": ("Finish", "end_longterm")
        }
    },

    # ----------------------------------
    # Capacity Checks
    # ----------------------------------
    "capacity_check": {
        "question": "3: Do YOU have emotional capacity to show up?",
        "options": {
            "1": ("Yes, enough capacity", "capacity_healthy"),
            "2": ("Capacity limited", "capacity_limited"),
            "3": ("No capacity", "end_no_capacity"),
        }
    },

    "capacity_healthy": {
        "question": "3A: Can you support without taking over, depending, or expecting?",
        "options": {
            "1": ("Yes", "offer"),
            "2": ("No", "end_invasive"),
        }
    },

    "capacity_limited": {
        "question": "3B: Can you be transparent about limited capacity?",
        "options": {
            "1": ("Yes", "offer"),
            "2": ("No", "end_dishonest"),
        }
    },

    # ----------------------------------
    # Offer
    # ----------------------------------
    "offer": {
        "question": (
            "4: OFFER:\n"
            "'Would you want me to be someone who can show up as a friend whenever you want?'"
        ),
        "options": {
            "1": ("She says YES", "post_consent"),
            "2": ("She says NO", "end_no"),
            "3": ("She says MAYBE", "conditional_consent"),
        }
    },

    # ----------------------------------
    # Post-Consent Behavior
    # ----------------------------------
    "post_consent": {
        "question": "6: Clarify boundaries?",
        "options": {
            "1": ("Yes, clarify", "ethical_support"),
            "2": ("Skip (NOT recommended)", "end_skip_boundaries"),
        }
    },

    "ethical_support": {
        "question": "6A: Ethical Support Mode.\nOffer, don't impose. Follow consent. Stay flexible.",
        "options": {
            "1": ("Finish", "end_ethical")
        }
    },

    # ----------------------------------
    # End Nodes
    # ----------------------------------
    "end_not_ready_1": {"end": "Not ready: boundaries frustrate you."},
    "end_not_ready_2": {"end": "Not ready: allyship requires invitation-based support."},
    "end_not_ready_3": {"end": "Not ready: intrusive tendencies detected."},
    "end_safety": {"end": "STOP. She does not feel safe. Allyship means respecting that fully."},
    "end_cannot_ask": {"end": "If you cannot ask safely, you cannot offer support."},
    "end_boundaries_no": {"end": "She said NO. You must fully respect this boundary."},
    "end_no_option": {"end": "She does NOT want the option of support. Respect this completely."},
    "end_longterm": {"end": "Outcome: Long-term allyship. Wait for her to reopen the topic."},
    "end_no_capacity": {"end": "Without capacity, offering support would be dishonest."},
    "end_invasive": {"end": "You cannot support without taking over. You must work on this first."},
    "end_dishonest": {"end": "Transparency is required. You cannot proceed."},
    "end_no": {"end": "She said NO. Respectfully step back."},
    "end_skip_boundaries": {"end": "Skipping boundary-setting risks harm. Revisit this responsibly."},
    "end_ethical": {"end": "You can ethically show up as a friend when she wants. 🎉"}
}


# ------------------------------
# Routes
# ------------------------------

@app.route("/")
def index():
    return redirect(url_for("node", node="root"))


@app.route("/node/<node>", methods=["GET"])
def node(node):
    data = TREE.get(node)

    if not data:
        return "Invalid node", 404

    # END NODE
    if "end" in data:
        return render_template(
            "node.html",
            question=data["end"],
            options={},
            end=True
        )

    # DECISION NODE
    return render_template(
        "node.html",
        question=data["question"],
        options=data["options"],
        end=False
    )


# ------------------------------
# Main
# ------------------------------

if __name__ == "__main__":
    app.run(debug=True)
