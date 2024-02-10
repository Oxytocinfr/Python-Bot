import discord
from discord.ext import commands
import json
import requests
import random
import instaloader
from dotenv import load_dotenv
import os
from keep_alive import keep_alive



env_file_path = ".env"

if not os.path.isfile(env_file_path):
    # Check /etc/secrets/.env if not found in the current directory
    env_file_path = "/etc/secrets/.env"

load_dotenv(env_file_path)


TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().all()
client = commands.Bot(command_prefix=('-'), intents=intents,
                      help_command=None, description="Hello There")


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="Your Mom"))


abusive_words= ['chuda', 'gand', 'lund' , 'nigga', 'hoe' , 'lund', 'chut', 'chutiya', 'madarchod']
bot_abusive_words = ['maa chuda', 'gand mara', 'fuck you', 'Bitch ass nigga', 'Ur moms a hoe', 'lund lega', 'Fuck ur mommy']

welcoming_words = ['Hello', 'Hi']
bot_welcoming_words = ['Hey There', 'Hello', 'Hii !! Nice to see you here..']


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    content_lower = message.content.lower()

    # Check for abusive words
    for word in abusive_words:
        if word in content_lower:
            await message.channel.send(random.choice(bot_abusive_words))
            return
    
    # Check for welcoming words
    for word in welcoming_words:
        if word in content_lower:
            await message.channel.send(random.choice(bot_welcoming_words))
            return

    await client.process_commands(message)


@client.event
async def on_member_join(member):
    # Send a welcome message to the new member in the general channel
    # Channel id
    channel = client.get_channel(1089463512348241961)
    embed = discord.Embed(title=f"Welcome {member} to our server!")
    embed.set_image(url=member.avatar_url)
    await channel.send(embed=embed)


@client.event
async def on_member_remove(member):
    # channel = discord.utils.get(member.guild.text_channels, name="general")
    channel = client.get_channel(1089463512348241961)
    if channel is not None:
        embed = discord.Embed(title=f"{member} left our server!")
        await channel.send(embed=embed)


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

BASE_URL_WAIFU = 'https://api.waifu.im/search'
TAGS_WAIFU = ['marin-kitagawa', 'waifu', 'maid', 'mori-calliope', 'raiden-shogun', 'oppai', 'selfies', 'uniform']

def get_waifu(tag=None, previous_results=None):
    if not tag:
        tag = random.choice(TAGS_WAIFU)
    
    url = f"{BASE_URL_WAIFU}/?included_tags={tag}"
    
    response_data = requests.get(url)
    json_data = response_data.json()
    
    if 'images' in json_data and json_data['images']:
        images = [img['url'] for img in json_data['images'] if img['url'] not in previous_results]
        return images
    else:
        return None


BASE_URL = 'https://api.waifu.im/search'
TAGS = ['ass', 'hentai', 'milf', 'oral', 'paizuri', 'ecchi', 'ero']

def get_waifu_hentai(tag=None, gif=False, previous_results=None):
    if not tag:
        tag = random.choice(TAGS)
    
    url = f"{BASE_URL}/?included_tags={tag}&is_nsfw=true"
    
    if gif:
        url += "&gif=true"
    
    response_data = requests.get(url)
    json_data = response_data.json()
    
    if 'images' in json_data and json_data['images']:
        images = [img['url'] for img in json_data['images'] if img['url'] not in previous_results]
        return images
    else:
        return None

def get_normal_hentai(tag):
    url = f"{BASE_URL}/?included_tags={tag}&is_nsfw=true"
    response_data = requests.get(url)
    json_data = response_data.json()
    
    if 'images' in json_data and json_data['images']:
        image = json_data['images'][0]['url']
        return [image]
    else:
        return None

# Commands


@client.command()
async def help(ctx):
    """Shows all available commands."""
    # , color=discord.Color.blue()
    help_embed = discord.Embed(
        title="Available commands", description="List of all available commands.", color=0x351C75)
    for command in client.commands:
        help_embed.add_field(
            name=command.name, value=command.help, inline=False)
    await ctx.send(embed=help_embed)


@client.command()
async def ping(ctx):
    """
    Check the bot's latency.
    """
    latency = client.latency * 1000
    embed = discord.Embed(
        title=f"Pong! Latency: {latency:.2f}ms", color=0x351C75)
    await ctx.send(embed=embed)


@client.command()
async def quote(ctx):
    """
      Motivational Quotes.
    """
    quote = get_quote()
    embed = discord.Embed(title=f"{quote}", color=0x351C75)
    await ctx.send(embed=embed)


@client.command()
async def joke(ctx):
    """
      Dad Jokes.
    """
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    data = response.json()
    embed = discord.Embed(
        title=data["setup"], description=data["punchline"], color=0x351C75)
    await ctx.send(embed=embed)


@client.command()
async def meals(ctx, dish):
    """
    Meals (T_T)
    """
    url = f'https://www.themealdb.com/api/json/v1/1/search.php?s={dish}'
    response = requests.get(url)
    data = response.json()
    if data['meals'] == 'null':
        embed = discord.Embed(title=f"invalid diish {dish}")
        await ctx.send(embed=embed)
    else:
        meal = data['meals'][0]
        ingredient = []
        for i in range(20):
            i += 1
            this_ingredient = meal[f'strIngredient{i}']
            ingredient.append(this_ingredient)
        new_list = [item for item in ingredient if item]
        embed = discord.Embed(title=f"{meal['strMeal']}")
        embed.set_thumbnail(url=f"{meal['strMealThumb']}")
        embed.add_field(
            name='Youtube', value=f"{meal['strYoutube']}", inline=True)
        embed.add_field(name='Ingredients',
                        value=f"{new_list}", inline=True)
        await ctx.send(embed=embed)



@client.command()
async def meme(ctx, meme_type="random"):
    """
    Get memes for a laugh.
    
    Parameters:
      - meme_type: Type of meme (random, wholesome, memes, dankmemes, me_irl, DarkMemesPh)
    """
    meme_types = {
        "random": "https://meme-api.com/gimme",
        "wholesome": "https://meme-api.com/gimme/wholesomememes",
        "memes": "https://meme-api.com/gimme/memes",
        "dankmemes": "https://meme-api.com/gimme/dankmemes",
        "me_irl": "https://meme-api.com/gimme/me_irl",
        "darkmemesph": "https://meme-api.com/gimme/DarkMemesPh",  # Changed key to lowercase
    }

    meme_type_lower = meme_type.lower()

    if meme_type_lower == 'help':
        await ctx.send("Available types: random, wholesome, memes, dankmemes, me_irl, DarkMemesPh")
        return
    elif meme_type_lower not in meme_types:
        await ctx.send("Invalid meme type. Available types: random, wholesome, memes, dankmemes, me_irl, DarkMemesPh")
        return

    url = meme_types[meme_type_lower]
    response = requests.get(url)

    if response.status_code != 200:
        await ctx.send("Failed to fetch meme. Try again later.")
        return

    data = response.json()
    embed = discord.Embed(color=0x351C75)
    embed.set_image(url=data["url"])
    await ctx.send(embed=embed)
    

@client.command()
async def weather(ctx, location: str):
    """
      Weather..
    """
    api_key = "92076f156adf35fe2261d1ff77b24023"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if data['cod'] == '404':
        embed = discord.Embed(title=f"{data['message']}")
        await ctx.send(embed=embed)
        return
    temperature = round(data["main"]["temp"] - 273.15, 1)
    description = data["weather"][0]["description"].capitalize()
    city = data["name"]
    country = data["sys"]["country"]
    embed = discord.Embed(title=f"Weather for {city}, {country}",
                          description=f"{description}\nTemperature: {temperature}°C", color=0x351C75)
    await ctx.send(embed=embed)



@client.command()
async def waifu(ctx, tag=None, count: int = 1):
    """
    Waifu.
    :param tag: Specify a tag for waifu content (optional).
    :param count: Number of waifu images to display (default is 1) and the maximum no of images which have been set is 10 at a time.
    usecase = -waifu maid 5
    waifu [tag] [no of img]
    TAGS = marin-kitagawa, waifu, maid, mori-calliope, raiden-shogun, oppai, selfies, uniform
    """
    MAX_IMAGES = 4  # Maximum number of images allowed
    
    previous_results = set()
    
    # Limit the count to the maximum allowed value
    count = min(count, MAX_IMAGES)
    
    for _ in range(count):
        waifu_images = get_waifu(tag, previous_results)
        
        if waifu_images:
            for image_url in waifu_images:
                previous_results.add(image_url)
                embed = discord.Embed()
                embed.set_image(url=image_url)
                await ctx.send(embed=embed)
        else:
            await ctx.send(f"No waifu images found for the specified tag: {tag}")

@client.command()
async def hentai(ctx, tag=None, gif: bool = False, count: int = 1):
    """
    Hentai (¬‿¬).
    :param tag: Specify a tag for hentai content (optional).
    :param gif: Include GIFs in the response (default is False).
    :param count: Number of hentai images to display (default is 1) and the maximum no of images which have been set is 10 at a time.
    usecase = -hentai ass True 5
    hentai [tag] [True/False] [no of img]
    TAGS = ass, oral, hentai, ecchi, ero, paizuri, milf
    """
    MAX_IMAGES = 10  # Maximum number of images allowed
    
    if ctx.channel.is_nsfw():
        previous_results = set()
        
        # Limit the count to the maximum allowed value
        count = min(count, MAX_IMAGES)
        
        for _ in range(count):
            hentai = get_waifu_hentai(tag, gif, previous_results)
            
            # If no results, try getting a normal hentai image
            if not hentai:
                hentai = get_normal_hentai(tag)
            
            if hentai:
                for image_url in hentai:
                    previous_results.add(image_url)
                    embed = discord.Embed(color=0x351C75)
                    embed.set_image(url=image_url)
                    await ctx.send(embed=embed)
            else:
                await ctx.send(f"No hentai found for the specified tag: {tag}")
    else:
        embed = discord.Embed(title="NSFW Channel Only", color=0xFF0000)
        await ctx.send(embed=embed)
# Socials

@client.command()
async def instagram(ctx, username):
    """
      Displays the instagram profile of a user.
    """
    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, username)
    embed = discord.Embed(
        title=f"{username}'s Instagram Details", color=0x351C75)
    embed.set_thumbnail(url=profile.profile_pic_url)
    embed.add_field(name="Followers", value=profile.followers)
    embed.add_field(name="Following", value=profile.followees)
    embed.add_field(name="Bio", value=profile.biography)
    await ctx.send(embed=embed)


@client.command()
async def discord_profile(ctx, user: discord.Member = None):
    """
      Displays the discord profile of any user in the server.
      If no user is specified then it will display your profile.
    """
    if not user:
        user = ctx.author
    embed = discord.Embed(
        title=user.name, description=user.mention, color=0x351C75)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name='Joined', value=user.joined_at.strftime(
        '%Y-%m-%d %H:%M:%S'), inline=True)
    embed.add_field(name='Registered', value=user.created_at.strftime(
        '%Y-%m-%d %H:%M:%S'), inline=True)

    await ctx.send(embed=embed)

# Moderation commands


@client.command()
# @commands.has_permissions(administrator=True)
async def purge(ctx, limit: int):
    """
      Deletes a specified number of messages in the channel.
    """
    if not ctx.author.guild_permissions.administrator:
        embed = discord.Embed(
            title='You do not have permission to use this command.', color=0xFF0000)
        await ctx.send(embed=embed)
        return
    await ctx.message.delete()
    await ctx.channel.purge(limit=limit)
    embed = discord.Embed(
        title=f'Successfully deleted {limit} messages.', color=0x351C75)
    await ctx.send(embed=embed, delete_after=5)


@client.command()
# @commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """
      Kicks the user from the server.
    """
    if not ctx.author.guild_permissions.administrator:
        embed = discord.Embed(
            title='You do not have permission to use this command.', color=0xFF0000)
        await ctx.send(embed=embed)
        return
    await member.kick(reason=reason)
    embed = discord.Embed(title=f"{member} has been kicked from the server.")
    await ctx.send(embed=embed)
    await member.send(f"You have been kick from the server beacause {reason}")


@client.command()
# @commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """
      Bans the user from the server.
    """
    if not ctx.author.guild_permissions.administrator:
        embed = discord.Embed(
            title='You do not have permission to use this command.', color=0xFF0000)
        await ctx.send(embed=embed)
        return
    await member.ban(reason=reason)
    embed = discord.Embed(
        title=f"{member} has been banned from the server.", color=0xFF0000)
    await ctx.send(embed=embed)
    await member.send(f"You have been banned from the server beacause {reason}")


if TOKEN is None:
    print("Bot token is not set. Please set the DISCORD_TOKEN environment variable.")
else:
    # Your bot code here
    keep_alive()
    client.run(TOKEN)
