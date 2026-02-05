import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from decision_tree import DECISION_TREE

load_dotenv()
TOKEN = os.getenv("NEW_TOKEN")

# ---------------- INTENTS ----------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------- SESSION STORAGE ----------------
# Stores per-user session
# { user_id: { current, history, path } }
user_state = {}

# ---------------- UTILITY ----------------
def format_node_name(name):
    return name.replace("_", " ").title()

# ---------------- BUTTON CLASSES ----------------
class DecisionButton(discord.ui.Button):
    def __init__(self, label, emoji, next_node, user_id):
        super().__init__(label=label, emoji=emoji, style=discord.ButtonStyle.primary)
        self.next_node = next_node
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This menu isn't for you.", ephemeral=True)
            return

        session = user_state[self.user_id]
        session["history"].append(session["current"])
        session["current"] = self.next_node
        session["path"].append(self.next_node)
        await send_node(interaction, self.next_node)


class NavButton(discord.ui.Button):
    def __init__(self, label, action, user_id):
        super().__init__(label=label, style=discord.ButtonStyle.secondary)
        self.action = action
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This menu isn't for you.", ephemeral=True)
            return

        session = user_state[self.user_id]

        if self.action == "back":
            if session["history"]:
                previous = session["history"].pop()
                session["current"] = previous
                session["path"].pop()
                await send_node(interaction, previous)
            else:
                # Already at root
                session["current"] = "root"
                session["history"] = []
                session["path"] = ["root"]
                await send_node(interaction, "root")
        elif self.action == "restart":
            session["current"] = "root"
            session["history"] = []
            session["path"] = ["root"]
            await send_node(interaction, "root")

# ---------------- OUTCOME BUTTONS ----------------
class OutcomeButton(discord.ui.Button):
    def __init__(self, label, outcome, user_id, path):
        style = discord.ButtonStyle.success if outcome=="Fixed" else discord.ButtonStyle.danger
        super().__init__(label=label, style=style)
        self.outcome = outcome
        self.user_id = user_id
        self.path = path

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This button isn't for you.", ephemeral=True)
            return

        # Send to #logs channel
        TECH_CHANNEL_ID = 1465366692464168980  # 🔹 your logs channel ID
        tech_channel = interaction.guild.get_channel(TECH_CHANNEL_ID)
        if tech_channel:
            await tech_channel.send(
                f"**Issue Update from {interaction.user.mention}**\n"
                f"Path: {' → '.join(self.path)}\nOutcome: {self.outcome}"
            )

        # Confirm to user
        await interaction.response.edit_message(
            content=f"Thanks! Outcome recorded: **{self.outcome}**",
            view=None
        )

        user_state.pop(self.user_id, None)


class OutcomeView(discord.ui.View):
    def __init__(self, user_id, path):
        super().__init__(timeout=120)
        self.add_item(OutcomeButton("✅ Fixed", "Fixed", user_id, path))
        self.add_item(OutcomeButton("❌ Still Broken", "Still Broken", user_id, path))

# ---------------- DECISION VIEW ----------------
class DecisionView(discord.ui.View):
    def __init__(self, user_id, node_name):
        super().__init__(timeout=120)
        self.user_id = user_id
        node = DECISION_TREE[node_name]

        # Add node options
        for emoji, next_node in node.get("reactions", {}).items():
            self.add_item(DecisionButton(label=format_node_name(next_node), emoji=emoji, next_node=next_node, user_id=user_id))

        # Add navigation
        self.add_item(NavButton("⬅️ Back", "back", user_id))
        self.add_item(NavButton("🔁 Restart", "restart", user_id))

# ---------------- SEND NODE ----------------
async def send_node(interaction, node_name):
    session = user_state.get(interaction.user.id)
    if not session:
        return

    node = DECISION_TREE[node_name]

    # Leaf node → show steps + outcome buttons
    if "steps" in node:
        steps_text = "\n".join(f"• {step}" for step in node["steps"])
        await interaction.response.edit_message(
            content=f"**Troubleshooting Steps**\n{steps_text}\n\nDid this fix the issue?",
            view=OutcomeView(interaction.user.id, session["path"])
        )
        return

    # Regular menu
    view = DecisionView(interaction.user.id, node_name)
    await interaction.response.edit_message(
        content=f"**{node['question']}**",
        view=view
    )

# ---------------- SLASH COMMAND ----------------
@bot.tree.command(name="menu", description="Start troubleshooting assistant")
async def menu(interaction: discord.Interaction):
    user_state[interaction.user.id] = {
        "current": "root",
        "history": [],
        "path": ["root"]
    }
    node = DECISION_TREE["root"]
    view = DecisionView(interaction.user.id, "root")
    await interaction.response.send_message(content=f"**{node['question']}**", view=view)

# ---------------- READY EVENT ----------------
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} is online and slash commands are synced!")

bot.run(TOKEN)
