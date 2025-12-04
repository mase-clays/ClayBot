import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from types import SimpleNamespace
from decision_tree import DECISION_TREE
#mase 4/12/2025 16:26 commit
#mase's commit from home 4/12/2025 at 20:24
intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
TOKEN = os.getenv("NEW_TOKEN")
bot = commands.Bot(command_prefix="!", intents=intents)


def format_node_name(name):
    return name.replace("_", " ").title()


# Store per-user state
# { user_id: { "current": node_name, "history": [], "last_msg": message_id } }
user_state = {}


@bot.event
async def on_ready():
    print(f"{bot.user} is online!")


@bot.command()
async def menu(ctx):
    user_state[ctx.author.id] = {
        "current": "root",
        "history": [],
        "last_msg": None
    }
    await send_node(ctx, "root")


async def send_node(ctx, node_name):
    session = user_state.setdefault(
        ctx.author.id, {"current": "root", "history": [], "last_msg": None}
    )
    session["current"] = node_name

    node = DECISION_TREE[node_name]

    # If leaf node → send troubleshooting steps
    if "steps" in node:
        steps_text = "\n".join(node["steps"])
        await ctx.channel.send(f"**Troubleshooting Steps:**\n{steps_text}")

        # Reset tree after showing solutions
        session["current"] = "root"
        session["history"] = []
        return

    # Build menu text
    menu_lines = [f"**{node['question']}**\n"]

    # Add decision options
    for emoji, next_node in node["reactions"].items():
        menu_lines.append(f"{emoji} — {format_node_name(next_node)}")

    # Add navigation options
    menu_lines.append("\n⬅️ — Back")
    menu_lines.append("🔁 — Start Over")

    menu_text = "\n".join(menu_lines)

    # Send message
    msg = await ctx.channel.send(menu_text)

    # Add decision reactions
    for emoji in node["reactions"]:
        await msg.add_reaction(emoji)

    # Add navigation reactions
    await msg.add_reaction("⬅️")
    await msg.add_reaction("🔁")

    session["last_msg"] = msg.id


@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    session = user_state.get(user.id)
    if not session:
        return

    # Only respond to the latest message
    if reaction.message.id != session.get("last_msg"):
        return

    current_node = session["current"]
    node = DECISION_TREE[current_node]
    emoji = str(reaction.emoji)

    # Create a minimal context for send_node
    ctx = SimpleNamespace(author=user, channel=reaction.message.channel)

    # --- HANDLE BACK BUTTON ---
    if emoji == "⬅️":
        if session["history"]:
            previous = session["history"].pop()
            await send_node(ctx, previous)
        else:
            # Already at root → restart
            session["current"] = "root"
            session["history"] = []
            await send_node(ctx, "root")
        return

    # --- HANDLE RESTART BUTTON ---
    if emoji == "🔁":
        session["current"] = "root"
        session["history"] = []
        await send_node(ctx, "root")
        return

    # --- NORMAL NAVIGATION ---
    if emoji not in node.get("reactions", {}):
        return

    next_node = node["reactions"][emoji]

    # Save history before moving
    session["history"].append(current_node)
    session["current"] = next_node

    await send_node(ctx, next_node)


bot.run(TOKEN)
