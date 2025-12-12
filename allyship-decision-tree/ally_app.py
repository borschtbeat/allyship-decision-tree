#!/usr/bin/env python3
# Ultra-Complex Allyship Decision Tree (Text-based, Clickable Menus)
# ---------------------------------------------------------------
# “Should I (a man) offer to show up for Joanna as a friend?”
#
# Designed for maximal complexity while maintaining readability.

import sys
import time

# ---- Utility Functions ----

def slow(text):
    """Print text slowly for effect."""
    for c in text:
        print(c, end='', flush=True)
        time.sleep(0.002)
    print()

def choose(prompt, options):
    """
    Display a menu and allow user to click (enter) a choice.
    Returns the key of the chosen option.
    """
    slow("\n" + prompt + "\n")
    for key, label in options.items():
        print(f"  [{key}] {label}")
    while True:
        choice = input("\nSelect option: ").strip()
        if choice in options:
            return choice
        print("Invalid choice. Try again.")


# ---- The Decision Tree ----

def root_intention():
    choice = choose(
        "ROOT NODE (0): What is your true intention?",
        {
            "1": "Genuine care & respect for Joanna's autonomy",
            "2": "Motivated by guilt, approval-seeking, romantic longing, or saviorism",
            "3": "I'm not sure what my intention is"
        }
    )
    if choice == "1":
        return intention_integrity(True)
    elif choice == "2":
        return intention_integrity(False)
    else:
        return self_inquiry()


def intention_integrity(passed):
    if not passed:
        slow("\nYou acknowledged non-ideal motivations → Intention-Integrity Check triggered.")
    else:
        slow("\nProceeding through intention check with positive alignment…")

    choice = choose(
        "0A: Can you strip your offer of all expectations?",
        {
            "1": "Yes",
            "2": "No"
        }
    )

    if choice == "1":
        return external_safety()
    else:
        return self_inquiry()


def self_inquiry():
    slow("\n0B: Self-Inquiry Loop engaged. Reflect on these questions:")
    slow("• Are you asking for her trust before earning it?")
    slow("• Are you trying to fix instead of support?")
    slow("• Are you emotionally grounded enough to help without burdening?")
    choice = choose(
        "Did you answer YES to at least 2/3?",
        {
            "1": "Yes",
            "2": "No"
        }
    )
    if choice == "1":
        return root_intention()
    else:
        return allyship_readiness()


def allyship_readiness():
    slow("\n0C: Allyship Readiness Node Activated.")
    choice = choose(
        "Do you respect boundaries without resentment?",
        {
            "1": "Yes, fully",
            "2": "No, boundaries frustrate me"
        }
    )
    if choice == "2":
        return end("Not ready. True allyship requires respect without resentment.")

    choice2 = choose(
        "Do you accept that allyship means offering proximity ONLY when invited?",
        {
            "1": "Yes",
            "2": "No"
        }
    )
    if choice2 == "2":
        return end("Not ready. Allyship requires non-intrusiveness.")

    choice3 = choose(
        "Can you be dependable without being intrusive?",
        {
            "1": "Yes",
            "2": "No"
        }
    )
    if choice3 == "2":
        return end("Not ready. Work on balanced presence.")
    
    return external_safety()


def external_safety():
    choice = choose(
        "1: External Safety Check — Does Joanna feel safe around you?",
        {
            "1": "Yes",
            "2": "Unsure",
            "3": "No"
        }
    )
    if choice == "1":
        return consent_autonomy()
    elif choice == "2":
        return safety_clarity()
    else:
        return end("STOP. Respect boundaries. Safety is non-negotiable.")


def safety_clarity():
    choice = choose(
        "1A: Ask neutrally: 'Would it feel comfortable if I offered support?'",
        {
            "1": "Yes, I can ask",
            "2": "No, I can't ask"
        }
    )
    if choice == "1":
        return consent_autonomy()
    else:
        return end("Without comfort asking, support cannot proceed.")


def consent_autonomy():
    choice = choose(
        "2: Has Joanna EVER shown she would welcome support?",
        {
            "1": "Yes",
            "2": "No / Not sure"
        }
    )
    if choice == "1":
        return capacity_check()
    else:
        return consent_inquiry()


def consent_inquiry():
    choice = choose(
        "2A: Ask: 'Would you want me to be someone who can show up when you want?'",
        {
            "1": "She says YES",
            "2": "She says MAYBE",
            "3": "She says NO"
        }
    )
    if choice == "1":
        return capacity_check()
    elif choice == "2":
        return conditional_consent()
    else:
        return end("She said no. Respect and do not revisit unless she initiates.")


def conditional_consent():
    choice = choose(
        "2B: Does she want the OPTION of support without expectation?",
        {
            "1": "Yes",
            "2": "No",
            "3": "Wants to revisit later"
        }
    )
    if choice == "1":
        return capacity_check()
    elif choice == "2":
        return end("Respectfully withdraw; boundaries are clear.")
    else:
        return long_term_mode()


def long_term_mode():
    slow("\n5: Entering Long-Term Allyship Mode.")
    slow("Maintain respectful distance and only re-check if SHE brings it up later.")
    return end("Outcome: Stay present without pressure.")


def capacity_check():
    choice = choose(
        "3: Do YOU have emotional capacity to show up?",
        {
            "1": "Yes, enough capacity",
            "2": "Capacity limited",
            "3": "No capacity"
        }
    )
    if choice == "1":
        return healthy_capacity()
    elif choice == "2":
        return limited_capacity()
    else:
        return end("Without capacity, offering support would be dishonest.")


def healthy_capacity():
    choice = choose(
        "3A: Can you support without taking over, depending, or expecting?",
        {
            "1": "Yes",
            "2": "No"
        }
    )
    if choice == "1":
        return the_offer()
    else:
        return end("Support requires non-intrusive balance.")


def limited_capacity():
    choice = choose(
        "3B: Can you transparently say your capacity is limited?",
        {
            "1": "Yes",
            "2": "No"
        }
    )
    if choice == "1":
        return the_offer()
    else:
        return end("Transparency is required; without it, you shouldn't offer.")


def the_offer():
    choice = choose(
        "4: Make the Offer:\n"
        "'Would you want me to be someone who can show up as a friend whenever you want?'",
        {
            "1": "She says YES",
            "2": "She says NO",
            "3": "She says MAYBE"
        }
    )
    if choice == "1":
        return post_consent()
    elif choice == "2":
        return end("Respectfully step back. Allyship honors 'No.'")
    else:
        return conditional_consent()


def post_consent():
    slow("\n6: Post-Consent Behavior Mode.")
    choice = choose(
        "Clarify boundaries?",
        {
            "1": "Yes, clarify boundaries",
            "2": "Skip boundary clarification (NOT recommended)"
        }
    )
    if choice == "1":
        return ethical_support()
    else:
        return end("Skipping boundaries risks harm. Clarify next time.")


def ethical_support():
    slow("\n6A: Ethical Support Mode Activated.")
    slow("• Offer, don't impose\n• Follow consent\n• Accept shifting boundaries\n• Avoid emotional dependency")
    return end("Outcome: You can ethically show up as a friend when she wants.")


def end(message):
    slow("\n--- FINAL RESULT ---")
    slow(message)
    slow("-------------------\n")
    sys.exit(0)


# ---- Run the Program ----
if __name__ == "__main__":
    slow("Welcome to the Ultra-Complex Allyship Decision Tree.\n")
    root_intention()