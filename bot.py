import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from decision_tree import DECISION_TREE

intents = discord.Intents.default()
intents.message_content = True


load_dotenv()
TOKEN = os.getenv("NEW_TOKEN")
bot = commands.Bot(command_prefix="!", intents=intents)


def format_node_name(name):
    # Convert "profile_camera" → "Profile Camera"
    return name.replace("_", " ").title()


#this keeps track of the users location within the tree.
user_state={}

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

@bot.command()
async def menu(ctx):
    user_state[ctx.author.id] = "root"
    await send_node(ctx, "root")
    

async def send_node(ctx, node_name):
    node = DECISION_TREE[node_name]

    # If node has troubleshooting steps, send them
    if "steps" in node:
        steps_text = "\n".join(node["steps"])
        await ctx.send(f"**Troubleshooting Steps:**\n{steps_text}")

        user_state[ctx.author.id] = "root"
        return

    # Build labelled menu text
    menu_lines = [f"**{node['question']}**\n"]
    for emoji, next_node in node["reactions"].items():
        menu_lines.append(f"{emoji} — {format_node_name(next_node)}")

    menu_text = "\n".join(menu_lines)

    # Send message
    msg = await ctx.send(menu_text)

    # Add reactions
    for emoji in node["reactions"]:
        await msg.add_reaction(emoji)

    user_state[(ctx.author.id, "last_msg")] = msg.id



@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    
    last_msg_id = user_state.get((user.id, "last_msg"))
    if reaction.message.id != last_msg_id:
        return
    
    current_node = user_state.get(user.id, "root")
    node = DECISION_TREE[current_node]

    emoji = str(reaction.emoji)

    if emoji not in node.get("reactions", {}):
        return
    
    next_node = node["reactions"][emoji]
    user_state[user.id] = next_node


    ctx = await bot.get_context(reaction.message)
    await send_node(ctx, next_node)


bot.run(TOKEN)


#trying this out

#ok finally my days








