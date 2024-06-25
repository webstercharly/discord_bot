# MyBot Application

## Overview
MyBot is a versatile Discord bot designed to enhance server management and engagement through dynamic configurations and interactive commands. It integrates various functionalities such as automated configurations, role management, and stock updates, all tailored to the specific needs of Discord communities.

## Features
- **Dynamic Configuration Reload:** Automatically detects and applies configuration changes without restarting the bot.
- **Extensible Command Framework:** Allows easy addition of new commands and features via a cog-based architecture.
- **Interactive Stock Updates:** Provides real-time updates on product availability using external APIs, complete with rich embeds.

## Getting Started
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/webstercharly/discord_bot
   ```
2. **Install Dependencies:**
   Depending on your setup, you might need to install specific Python libraries or Discord API dependencies. Ensure you have Python and necessary libraries installed to run the bot.
   ```bash
   pip install discord.py==1.7.3 aiohttp==3.7.4 PyYAML==5.4.1
   ```
3. **Configure Bot Token and Permissions:**
   Edit the `config.yml` file to include your Discord bot token and necessary permissions.
4. **Run the Bot:**
   ```bash
   python src/main.py
   ```

## Usage
- **Commands Setup:** Define your commands and events in respective cog files under the `bot/cogs` directory.
- **Configuration Management:** Update settings in real-time by modifying the `config.yml` and corresponding cog configuration files.
- **Launching the Bot:** Use the `!` prefix for commands (customisable) and interact with the bot as defined in your command setup.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
