# open_bot

**open_bot** is an open-source Discord bot written in Python, built primarily using the `discord.py` library.  
It is licensed under the MIT License (see `LICENSE`).

---

## Features

- Modular command system
- Logging utilities
- Admin and info commands
- Event handling via `on_ready`
- Easy to extend with new commands or events

---

## Dependencies

| Library         | Version  | License |                   Purpose                    |
|-----------------|----------|---------|----------------------------------------------|
| `discord.py`    | >=2.3.0  |   MIT   | Core Discord bot framework                   |
| `python-dotenv` | >=1.0.0  |   MIT   | Load environment variables from `.env` files |

> These dependencies are **not included in the repository**. They must be installed separately.

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/mattsva/open_bot.git
cd open_bot
```

### 2. Create a Python virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root (like the `.env.example` file):

```text
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=your_guild/server_id_here
```

- Replace `your_bot_token_here` with your bot token from the Discord Developer Portal.  
- Replace `your_guild/server_id_here` with your guild token from Discord, you may know it as Server ID.
- **Never share `.env`**.  
- You can add other environment variables here if needed for extensions.

---

## Running the Bot

Start the bot with:

```bash
python bot.py
```

- Logs will be printed to the console.  
- Logging behavior can be configured in `utils/logger.py` (console, file, or Discord output).  
- Commands are located in `commands/` and can be extended easily.  
- Event handlers are in `on_ready.py` or additional event files you add.

---

## Configuration

- `config.py` contains global settings under the `Meta` class.  
- Settings include:
 - Logging options
 - Other configurable constants for the bot  
- Update `Meta` to change global behavior without modifying bot code directly.

---

## Contributing

- Fork the repository and submit pull requests for bug fixes or features.  
- Keep code style consistent with existing modules.  
- Do **not commit secrets** (`.env`, API tokens, passwords, etc.).

---

## Best Practices

- Keep your Discord token safe: never commit `.env` or post it publicly.  
- Use `python-dotenv` to load local secrets.  
- Only include your own code in the repository; install external dependencies via `pip`.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for full details.

Copyright (c) 2026 mattsva
