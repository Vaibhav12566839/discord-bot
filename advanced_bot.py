import discord
from discord.ext import commands
import random
import os
import asyncio
import datetime
import requests

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

# Bot setup
bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = 'MTI1MDY5MjYzMTA1NTU2NDgzMA.GXpORe.frHgJj58Ax7LbnD30l0cNHOK7bw9Iw6pszqNOs'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing required argument.')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('Command not found.')
    else:
        await ctx.send('An error occurred.')

# General commands
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def greet(ctx):
    await ctx.send('Hello! How can I assist you today?')

@bot.command()
async def echo(ctx, *, message: str):
    await ctx.send(message)

@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a + b)

@bot.command()
async def subtract(ctx, a: int, b: int):
    await ctx.send(a - b)

@bot.command()
async def multiply(ctx, a: int, b: int):
    await ctx.send(a * b)

@bot.command()
async def divide(ctx, a: int, b: int):
    if b == 0:
        await ctx.send("Cannot divide by zero.")
    else:
        await ctx.send(a / b)

# Fun commands
@bot.command()
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def flip(ctx):
    outcome = random.choice(['Heads', 'Tails'])
    await ctx.send(outcome)

@bot.command()
async def joke(ctx):
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you get when you cross a snowman with a vampire? Frostbite.",
        "Why was the math book sad? Because it had too many problems."
    ]
    await ctx.send(random.choice(jokes))

@bot.command()
async def trivia(ctx):
    questions = {
        "What is the capital of France?": "Paris",
        "Who wrote 'To Kill a Mockingbird'?": "Harper Lee",
        "What is the smallest planet in our solar system?": "Mercury",
    }
    question, answer = random.choice(list(questions.items()))
    await ctx.send(question)
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        msg = await bot.wait_for('message', check=check, timeout=15)
        if msg.content.lower() == answer.lower():
            await ctx.send('Correct!')
        else:
            await ctx.send(f'Incorrect! The answer was {answer}.')
    except asyncio.TimeoutError:
        await ctx.send(f'Time is up! The answer was {answer}.')

# Information commands
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title="User Info", description=f"Info about {member}", color=discord.Color.blue())
    embed.add_field(name="Username", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Status", value=member.status, inline=True)
    embed.add_field(name="Top Role", value=member.top_role, inline=True)
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    embed = discord.Embed(title="Server Info", description=f"Info about {server.name}", color=discord.Color.green())
    embed.add_field(name="Server name", value=server.name, inline=True)
    embed.add_field(name="Server ID", value=server.id, inline=True)
    embed.add_field(name="Member count", value=server.member_count, inline=True)
    embed.set_thumbnail(url=server.icon.url)
    await ctx.send(embed=embed)

# Utility commands
@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="Poll", description=question, color=discord.Color.orange())
    message = await ctx.send(embed=embed)
    await message.add_reaction('👍')
    await message.add_reaction('👎')

@bot.command()
async def choose(ctx, *choices):
    if len(choices) < 2:
        await ctx.send('Not enough choices to choose from.')
        return
    await ctx.send(f'I choose: {random.choice(choices)}')

@bot.command()
async def weather(ctx, city: str):
    api_key = 'YOUR_OPENWEATHERMAP_API_KEY'
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url).json()
    if response["cod"] != "404":
        main = response["main"]
        weather = response["weather"][0]
        embed = discord.Embed(title=f"Weather in {city}", description=weather["description"], color=discord.Color.blue())
        embed.add_field(name="Temperature", value=f"{main['temp']}°C", inline=True)
        embed.add_field(name="Humidity", value=f"{main['humidity']}%", inline=True)
        embed.add_field(name="Pressure", value=f"{main['pressure']} hPa", inline=True)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"City {city} not found.")

@bot.command()
async def timer(ctx, seconds: int):
    if seconds > 3600:
        await ctx.send("You cannot set a timer for more than 1 hour.")
        return
    await ctx.send(f'Timer set for {seconds} seconds.')
    await asyncio.sleep(seconds)
    await ctx.send(f'{ctx.author.mention}, your timer has ended!')

@bot.command()
async def remindme(ctx, time: int, *, reminder: str):
    await ctx.send(f'Reminder set for {time} minutes.')
    await asyncio.sleep(time * 60)
    await ctx.send(f'{ctx.author.mention}, reminder: {reminder}')

# Moderation commands
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member.name} has been kicked.')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'User {member.name} has been banned.')

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member_name):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name == member_name:
            await ctx.guild.unban(user)
            await ctx.send(f'User {user.name} has been unbanned.')
            return
    await ctx.send(f'User {member_name} not found.')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{amount} messages have been deleted.')

@bot.command()
async def uptime(ctx):
    now = datetime.datetime.utcnow()
    delta = now - bot.start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    await ctx.send(f'Uptime: {hours}h {minutes}m {seconds}s')

@bot.command()
async def quote(ctx):
    quotes = [
        "The best time to plant a tree was 20 years ago. The second best time is now.",
        "An unexamined life is not worth living.",
        "Eighty percent of success is showing up.",
    ]
    await ctx.send(random.choice(quotes))

# Clear reactions command
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clearreactions(ctx, message_id: int):
    try:
        msg = await ctx.channel.fetch_message(message_id)
        await msg.clear_reactions()
        await ctx.send('Reactions cleared.')
    except discord.NotFound:
        await ctx.send('Message not found.')
    except discord.Forbidden:
        await ctx.send('Permission denied.')
    except discord.HTTPException:
        await ctx.send('Failed to clear reactions.')

# Self role commands
@bot.command()
async def addrole(ctx, role: discord.Role):
    if role not in ctx.author.roles:
        await ctx.author.add_roles(role)
        await ctx.send(f'Role {role.name} has been added.')
    else:
        await ctx.send(f'You already have the role {role.name}.')

@bot.command()
async def removerole(ctx, role: discord.Role):
    if role in ctx.author.roles:
        await ctx.author.remove_roles(role)
        await ctx.send(f'Role {role.name} has been removed.')
    else:
        await ctx.send(f'You do not have the role {role.name}.')

# Continuously adding commands
for i in range(1, 201):
    @bot.command(name=f'cmd{i}')
    async def dynamic_command(ctx, number=i):
        await ctx.send(f'This is command number {number}')

# Record the start time of the bot
bot.start_time = datetime.datetime.utcnow()

# Run the bot
bot.run(TOKEN)
