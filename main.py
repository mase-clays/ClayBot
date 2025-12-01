import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("NEW_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")



DECISION_TREE = {
    "root": {
        "question": "What kind of issue are you having?",
        "reactions": {
            "📷": "camera_issue",
            "🔫": "gun_issue",
            "🖥️": "game_issue"
        }
    },
    "camera_issue": {
        "question": "Which camera?",
        "reactions": {
            "1️⃣": "profile_camera",
            "2️⃣": "tracking_camera"
        }
    },
    "profile_camera": {
        "steps": [
            "Check if the profile camera is powered on.",
            "Ensure the lens is uncovered.",
            "Restart Motive."
        ]
    }
}


user_state = {}  # user_id -> current node



@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    # get current node for this user
    current_node = user_state.get(user.id, "root")
    node_data = DECISION_TREE[current_node]

    emoji = str(reaction.emoji)
    if emoji not in node_data.get("reactions", {}):
        return

    next_node = node_data["reactions"][emoji]
    user_state[user.id] = next_node

    next_data = DECISION_TREE[next_node]
    if "question" in next_data:
        msg = await reaction.message.channel.send(next_data["question"])
        for r in next_data["reactions"]:
            await msg.add_reaction(r)
    elif "steps" in next_data:
        await reaction.message.channel.send("\n".join(next_data["steps"]))
        user_state[user.id] = "root"








print(TOKEN)

bot.run(TOKEN)









"""this is the latest attempt at a discord bot, for foh staff to use to
troubleshoot basic errors and issues they might come across while working"""

TROUBLESHOOTING = {
    "1": {
        "title": "Camera not working",
        "children":{
            "1.1":{
                "title": "Profile Camera",

            }
        }

    }
}