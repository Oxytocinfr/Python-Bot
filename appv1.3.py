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


def get_waifu(tag=None):
    base_url = 'https://api.waifu.im/search/'
    base_url_all = ['https://api.waifu.im/search',
                    'https://api.waifu.im/search/?included_tags=marin-kitagawa',
                    'https://api.waifu.im/search/?included_tags=waifu',
                    'https://api.waifu.im/search/?included_tags=maid',
                    'https://api.waifu.im/search/?included_tags=mori-calliope',
                    'https://api.waifu.im/search/?included_tags=raiden-shogun',
                    'https://api.waifu.im/search/?included_tags=oppai',
                    'https://api.waifu.im/search/?included_tags=selfies',
                    'https://api.waifu.im/search/?included_tags=uniform']
    if tag:
        url = f"{base_url}?included_tags={tag}&nsfw=false"
    else:
        url = random.choice(base_url_all)
    response_data = requests.get(url)
    json_data = response_data.json()

    if "detail" in json_data and json_data['detail']:
        return json_data['detail']
    else:
        image = json_data['images'][0]['url']
        return image

# Old Random

# def get_waifu_hentai():
#     url = ['https://api.waifu.im/search/?is_nsfw=true&gif=true',
#            'https://api.waifu.im/search/?is_nsfw=true',
#            'https://api.waifu.im/search/?included_tags=ass',
#            'https://api.waifu.im/search/?included_tags=hentai',
#            'https://api.waifu.im/search/?included_tags=milf',
#            'https://api.waifu.im/search/?included_tags=oral',
#            'https://api.waifu.im/search/?included_tags=paizuri',
#            'https://api.waifu.im/search/?included_tags=ecchi',
#            'https://api.waifu.im/search/?included_tags=ero']
#     hentai = random.choice(url)
#     response_data = requests.get(hentai)
#     json_data = response_data.json()
#     image = json_data['images'][0]['url']
#     return image

# Complete random mk1


BASE_URL = 'https://api.waifu.im/search'
TAGS = ['ass', 'hentai', 'milf', 'oral', 'paizuri', 'ecchi', 'ero']


def get_waifu_hentai():
    tag = random.choice(TAGS)
    url_no_gif = f"{BASE_URL}/?included_tags={tag}&is_nsfw=true"
    url_gif = f"{BASE_URL}/?included_tags={tag}&is_nsfw=true&gif=true"
    urls = [url_no_gif, url_gif]
    url = random.choice(urls)
    response_data = requests.get(url)
    json_data = response_data.json()
    image = json_data['images'][0]['url']
    return image

# Random mk2

# def get_waifu_hentai(tag=None, is_gif=None):
#     base_url = 'https://api.waifu.im/search/'
#     tag_list = ['ass', 'hentai', 'milf', 'oral', 'paizuri', 'ecchi', 'ero']

#     if tag:
#         url_tag = random.choice(tag_list) if tag == 'random' else tag
#         url = f"{base_url}?included_tags={url_tag}"
#     else:
#         url_tag = random.choice(tag_list)
#         url = f"{base_url}?included_tags={url_tag}"

#     if is_gif is not None:
#         url += '&gif=true' if is_gif else ''

#     response_data = requests.get(url)
#     json_data = response_data.json()

#     if not json_data['images']:
#         return 'error'

#     image_url = random.choice(json_data['images'])['url']

#     return image_url

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
async def meme(ctx):
    """
      Memes to have a laugh.
    """
    link = ["https://meme-api.com/gimme",
            'https://meme-api.com/gimme/wholesomememes',
            'https://meme-api.com/gimme/memes',
            'https://meme-api.com/gimme/dankmemes',
            'https://meme-api.com/gimme/me_irl']
    url = random.choice(link)
    response = requests.get(url)
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
async def waifu(ctx, tag=None):
    """
    Waifu.
    """
    waifu = get_waifu(tag)
    if 'error' in waifu or 'bad' in waifu:
        embed = discord.Embed(title=waifu)
        await ctx.send(embed=embed)
    elif waifu.startswith('http'):
        embed = discord.Embed()
        embed.set_image(url=waifu)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=waifu)
        await ctx.send(embed=embed)


@client.command()
async def hentai(ctx):
    """
      Hentai (¬‿¬).
    """
    if ctx.channel.is_nsfw():
        hentai = get_waifu_hentai()
        embed = discord.Embed(color=0x351C75)
        embed.set_image(url=hentai)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="NSFW Channel Only", color=0xFF0000)
        await ctx.send(embed=embed)

# @client.command()
# async def hentai(ctx, tag='random', is_gif=False):
#     """
#     hentai.
#     """
#     image_url = get_waifu_hentai(tag, is_gif)

#     if image_url == 'error':
#         embed = discord.Embed(description='No results found.')
#     elif is_gif:
#         embed = discord.Embed()
#         embed.set_image(url=image_url)
#     else:
#         embed = discord.Embed(title=f"{tag.capitalize()} waifu")
#         embed.set_image(url=image_url)

#     await ctx.send(embed=embed)


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
