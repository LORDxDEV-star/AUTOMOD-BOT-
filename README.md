

# Discord Auto Moderation Bot

A powerful Discord bot designed to automate moderation tasks such as filtering offensive content, logging, and more. This bot aims to provide a safe and friendly environment for your community by enforcing custom rules, filtering bad words, and notifying users about inappropriate behavior.

## Features

* **Content Moderation**: Automatically detect and delete messages containing bad words or offensive content.
* **Customizable Word List**: You can easily add your own list of bad words in the `badwords.txt` file.
* **Logging System**: Keep track of deleted messages and offenders with logs.
* **Role Management**: Automatically removes user roles for 30 seconds if they post bad words, and then restores them after the timeout.
* **Notification System**: Sends a professional DM to users who violate the rules.

## Requirements

* Python 3.8 or higher
* `discord.py` library
* A `badwords.txt` file containing a list of inappropriate words (editable by you)
* A `config.json` for bot configuration
* `json` module for data storage

## Installation

1. **Clone the repository** or download the project files.

   ```bash
   git clone https://github.com/LORDxDEV-star/AUTOMOD-BOT-
   cd AUTOMOD-BOT-
   ```

2. **Install dependencies**:

   * Make sure you have Python 3.8 or higher installed.
   * Install the required libraries using `pip`.

   ```bash
   pip install discord.py
   ```

3. **Set up your bot on Discord**:

   * Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new bot.
   * Get your bot’s token and store it in the `config.json` file.

4. **Edit `badwords.txt`**:

   * Add words or phrases you want to block in your server, one per line.

   **Example `badwords.txt`**:

   ```txt
   examplebadword1
   examplebadword2
   curseword1
   offensivephrase1
   ```

5. **Configure `config.json`**:

   * Add your bot’s token and any other necessary settings.

   **Example `config.json`**:

   ```json
   {
       "token": "YOUR_BOT_TOKEN",
       "log_channel_id": "YOUR_LOG_CHANNEL_ID",
       "prefix": "!"
   }
   ```

6. **Run the bot**:

   ```bash
   python main.py
   ```

## How It Works

* The bot checks each message in the server for bad words listed in `badwords.txt`.
* If a bad word is detected, the bot:

  1. Deletes the message.
  2. Temporarily removes all roles from the user for 30 seconds.
  3. Sends a DM to the user with a warning.
  4. Logs the action in the specified log channel.
  5. After 30 seconds, restores the user's roles.

## Customizing the Bot

### Bad Words Filtering

You can modify the `badwords.txt` file to include any terms you want to block. Simply add one word or phrase per line, and the bot will block messages containing these words.

### Logging System

All deleted messages and actions are logged in the channel specified in the `config.json` file. The bot will log the following:

* Deleted message content
* User who sent the message
* Time of the action

### Role Management

The bot removes roles for 30 seconds from any user who posts a message containing a bad word. After the timeout, their roles are restored automatically.

### Custom DM Message

You can customize the DM message sent to users who break the rules by modifying the message in the code.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository, make improvements, and create a pull request. All contributions are welcome!

OUR DISCORD SUPPORT SERVER https://discord.gg/lunardevs
