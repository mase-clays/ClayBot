# ClayBot AI Coding Instructions

## Project Overview
ClayBot is a Discord bot designed to help FOH (Front of House) staff troubleshoot common venue issues via emoji-based interactive troubleshooting. The bot implements a decision tree navigation system where users progress through questions to reach actionable troubleshooting steps.

## Architecture

### Core Components
- **`bot.py`** (production): Main Discord bot implementation using discord.py. Implements reaction-based UI with persistent user session state and navigation history.
- **`decision_tree.py`**: Declarative knowledge base defining the troubleshooting tree structure (nodes with questions/reactions mapping to next nodes or solution steps).
- **`main.py`**: Legacy/experimental implementation. Current production uses `bot.py`.
- **`database.sql`**: Schema for gun issue tracking (not currently integrated into bot).

### Decision Tree Data Structure
All nodes are defined in `DECISION_TREE` dict in `decision_tree.py`. Node types:

```python
# Decision node (has reactions → leads elsewhere)
"node_name": {
    "question": "User facing question text",
    "reactions": {
        "emoji": "next_node_name",
        "emoji2": "another_node_name"
    }
}

# Leaf node (has steps → troubleshooting solution)
"leaf_name": {
    "steps": [
        "Step 1 instruction",
        "Step 2 instruction"
    ]
}
```

### State Management Pattern
User sessions stored in `user_state` dict: `{ user_id: { "current": node_name, "history": [prev_nodes], "last_msg": msg_id } }`

**Critical detail**: Only the latest message ID matters for reaction handling. History enables back-button functionality.

## Key Workflows

### Adding New Troubleshooting Paths
1. Add node(s) to `DECISION_TREE` in `decision_tree.py` following the structure above
2. Ensure emoji keys in "reactions" dicts are valid Discord reaction emojis
3. Test via `!menu` command in Discord, following the emoji prompts

### Modifying Questions/Steps
Edit strings directly in the decision tree node definitions. Changes take effect on bot restart.

### Handling Bot Reactions
The `on_reaction_add` event in `bot.py` handles three cases:
- **Custom reactions** (emoji in current node's "reactions"): Navigate to next node
- **Back button** (`⬅️`): Pop from history or reset to root
- **Restart button** (`🔁`): Clear history and return to root

## Development Notes

### Setup
- Requires `.env` with `NEW_TOKEN=<discord_bot_token>`
- Uses discord.py library (see imports in `bot.py`)
- Bot runs with `!` command prefix

### Testing Entry Point
Run `bot.py` directly. Use `!menu` in Discord to start troubleshooting flow.

### Codebase Patterns
- **Lazy initialization**: User session created on first `!menu` command or reaction
- **Minimal context wrapping**: `on_reaction_add` creates SimpleNamespace context for `send_node` compatibility
- **Emoji mapping conventions**: Current structure uses weapon/equipment themed emojis (📷 camera, 🔫 gun, 🎮 game, 📟 terminal)
- **No validation on tree edits**: Syntax errors in decision_tree.py will cause KeyError at runtime. Always test new nodes.

### Known Issues / In-Progress
- `decision_tree.py` has syntax errors (missing colons in some node definitions) that will crash runtime
- `database.sql` schema exists but integration incomplete
- `knowledge.json` is empty (placeholder for future expansion)
- `training.py` is non-functional stub code

## Integration Points

### External Dependencies
- **discord.py**: Message/reaction handling and bot framework
- **python-dotenv**: Environment variable loading for token

### Message Flow
1. User reacts with emoji to Discord message
2. `on_reaction_add` event triggers
3. User session state looked up or initialized
4. Decision tree traversed based on emoji mapping
5. Next node rendered via `send_node()` with reactions added
6. Loop continues until leaf node reached, then session resets

## Conventions to Follow

- Node names use `snake_case` (e.g., `profile_camera`, `double_peg_3_leds`)
- Question text is concise and user-friendly
- Steps are imperative, numbered implicitly by list order
- Always include back/restart navigation in decision nodes (handled auto-magically by `send_node`)
- Emoji choices should intuitively map to categories (current pattern is working well)
