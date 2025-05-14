import discord
from discord.ext import commands
import json
import re
import traceback
import asyncio

# Load config
try:
    with open("config.json") as f:
        config = json.load(f)
except Exception as e:
    print("❌ Failed to load config.json:", e)
    exit()

# Load badwords
try:
    with open("badwords.txt", encoding="utf-8") as f:
        badwords = [w.strip().lower().replace('\u200b', '') for w in f.readlines()]
except Exception as e:
    print("❌ Failed to load badwords.txt:", e)
    exit()

# Load stored roles from JSON
try:
    with open("stored_roles.json", "r") as f:
        stored_roles = json.load(f)
except Exception as e:
    print("❌ Failed to load stored_roles.json, creating a new one.")
    stored_roles = {}

# Setting up intents (message_content intent for reading messages)
intents = discord.Intents.default()
intents.message_content = True  # Enables message content intent
intents.guilds = True
intents.messages = True
intents.members = True

bot = commands.Bot(command_prefix=config["prefix"], intents=intents, status=discord.Status.invisible)

last_messages = {}

# Helper: Send log embed
async def send_log_embed(user, reason, channel, content):
    try:
        log_channel = bot.get_channel(config["log_channel_id"])
        if not log_channel:
            return
        embed = discord.Embed(
            title="🚨 AutoMod Triggered",
            description=f"**User:** {user.mention} (`{user.id}`)\n"
                        f"**Channel:** {channel.mention}\n"
                        f"**Reason:** {reason}",
            color=discord.Color.red()
        )
        embed.add_field(name="❌ Message", value=f"```{content[:1000]}```", inline=False)
        embed.set_footer(text="AutoMod Logger")
        await log_channel.send(embed=embed)
    except Exception as e:
        print("Error sending log embed:", e)

# Helper: DM user
async def dm_user(user, reason, content):
    try:
        embed = discord.Embed(
            title="⚠️ Message Deleted by AutoMod",
            description=f"Your message was removed for the following reason:\n\n**{reason}**",
            color=discord.Color.orange()
        )
        embed.add_field(name="❌ Message", value=f"```{content[:1000]}```", inline=False)
        await user.send(embed=embed)
    except discord.Forbidden:
        # DMs are closed
        pass
    except Exception as e:
        print("Error sending DM:", e)

# Helper: Temporarily remove roles and restore after 30 seconds
async def temporarily_remove_roles(user):
    try:
        # Save current roles
        original_roles = [role.id for role in user.roles]
        stored_roles[str(user.id)] = original_roles

        # Remove roles
        await user.edit(roles=[])
        # Store roles to file
        with open("stored_roles.json", "w") as f:
            json.dump(stored_roles, f)

        # Wait for 30 seconds
        await asyncio.sleep(30)

        # Restore original roles
        roles_to_add = [discord.utils.get(user.guild.roles, id=role_id) for role_id in original_roles]
        await user.edit(roles=roles_to_add)

    except Exception as e:
        print("Error temporarily removing roles:", e)

# Message Listener
@bot.event
async def on_message(message):
    try:
        if message.author.bot or not message.guild:
            return

        msg = message.content.lower().replace('\u200b', '')
        user = message.author
        channel = message.channel

        # Badwords
        if config.get("enable_badwords_filter", False):
            if any(word in msg for word in badwords):
                await message.delete()
                await send_log_embed(user, "Bad Language Detected", channel, message.content)
                await dm_user(user, "Bad Language Detected", message.content)
                await temporarily_remove_roles(user)  # Remove roles temporarily
                return

        # Invite Links
        if config.get("enable_invite_filter", False):
            if re.search(r"(discord\.gg/|discord\.com/invite/)", msg):
                await message.delete()
                await send_log_embed(user, "Discord Invite Link", channel, message.content)
                await dm_user(user, "Discord Invite Link", message.content)
                await temporarily_remove_roles(user)  # Remove roles temporarily
                return

        # Anti-Link (URLs)
        if config.get("enable_antilink_filter", False):
            if re.search(r"https?://", msg):
                await message.delete()
                await send_log_embed(user, "External Link Detected", channel, message.content)
                await dm_user(user, "External Link Detected", message.content)
                await temporarily_remove_roles(user)  # Remove roles temporarily
                return

        # CAPS Spam
        if config.get("enable_caps_filter", False):
            caps = sum(1 for c in message.content if c.isupper())
            if len(message.content) > 8 and caps > len(message.content) * 0.7:
                await message.delete()
                await send_log_embed(user, "Excessive CAPS", channel, message.content)
                await dm_user(user, "Excessive CAPS", message.content)
                await temporarily_remove_roles(user)  # Remove roles temporarily
                return

        # Repeated Messages
        if config.get("enable_repeat_filter", False):
            if user.id in last_messages and last_messages[user.id] == msg:
                await message.delete()
                await send_log_embed(user, "Repeated Message", channel, message.content)
                await dm_user(user, "Repeated Message", message.content)
                await temporarily_remove_roles(user)  # Remove roles temporarily
                return
            last_messages[user.id] = msg

    except Exception as e:
        print("⚠️ Error in on_message:")
        traceback.print_exc()

    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (Invisible Mode ON)")

# Basic error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    print(f"⚠️ Command error: {error}")
    await ctx.send("❌ An error occurred while processing your command.")

bot.run(config["token"])
