#here i will configure the decision tree 

# decision_tree.py
#addition before some dispatch
#what about now

DECISION_TREE = {
    "root": {
        "question": "What issue are you facing?",
        "reactions": {
            "📷": "camera_issue",
            "🔫": "gun_issue", 
            "🎮": "game_issue",
            "📟": "terminal_issue"
        }
    },

    "terminal_issue": {
        "question": "What is the issue?",
        "reactions": {
            "1️⃣": "Screen frozen",
            "2️⃣": "other_terminal_issue"
        }
    },

    "camera_issue": {
        "question": "Which camera?",
        "reactions": {
            "1️⃣": "profile_camera",
            "2️⃣": "boomerang_camera"
        }
    },

    "profile_camera": {
        "steps": [
            "Check if the camera is plugged in.",
            "Verify the camera is visible in Motive.",
            "Restart the profile camera.",
        ]
    },

    "gun_issue": {
        "question": "What is the issue?",
        "reactions": {
            "1️⃣": "3_leds",
            "2️⃣": "not_shooting"
        }
    },

    "3_leds": {
        "question": "Single peg or double peg?",
        "reactions": {
            "1️⃣": "single_peg_3_leds",
            "2️⃣": "double_peg_3_leds"
    }
    },

    "single_peg_3_leds": {
        "steps": [
            "Please switch the configuration (7up -> 7down).",
            "Turn the gun off and on again.",
        ]
    },

    
}
#what will happen if i do this