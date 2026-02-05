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
            "📟": "terminal_issue",
            "❓": "unknown_issue"
        }
    },



    "terminal_issue": {
        "question": "What is the issue?",
        "reactions": {
            "1️⃣": "screen_frozen",
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

    "0_timer":{
        "steps": [
            "Please restart the game."
            ]
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
            "2️⃣": "not_shooting",
            "3️⃣": "gun_broken",
            "4️⃣": ""
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

    "double_peg_3_leds":{
        "steps": [
            "Please switch the configuration (7up -> 7down) of both guns.",
            "Check LEDs of both guns, if they have 6 then play as normal."
        ]
    },

    "game_issue":{
        "question": "What is the issue?",
        "reactions": {
            "1️⃣": "0_timer",
            "2️⃣": "other_game_issue",
            "3️⃣": "Gun_not_recognised"
        }
    },

    "Gun_not_recognised":{
        "steps": [
            "Please ensure the receiver is plugged in, and the PORT is matching with the game settings",
            "Make sure gun has LEDs, and responding to inputs correctly(vibration)",
            "Try restarting the game."
        ]
    },

    "unknown_issue":{
        "steps": [
            "Please confirm you have done the following:",
            "1. Restarted the game.",
            "2. Ensure guns have 6 LEDs.", 
            "3. Motive is up and running.",
            "4. Gun receiver is plugged in properly."

            ]
    }

    
    
}
