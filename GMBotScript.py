import os
import discord
import random

from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.utils import get, find
from discord import Intents, Member, Guild

from itertools import cycle

#One line core processes the bot needs to run
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
bot = commands.Bot(command_prefix="!")
intents = discord.Intents.all()
client = discord.Client(intents=intents)

#Loads all available cogs on boot up
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

#Check for specific channel
def in_channel(*channels):
    def predicate(ctx):
        return ctx.channel.id in channels
    return commands.check(predicate)

backstage_channels = [830756387134636043, 830761159408746526, 830248428423479316, 830292096975765514]

#Prints signal message to the console when the bot is first turned on
@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready.')
        
#Sends "!Pong" when "!ping" is typed in a channel
@in_channel(backstage_channels[0], backstage_channels[1], backstage_channels[2], backstage_channels[3])
@bot.command()
async def ping(ctx):
    await ctx.channel.send(f'pong! Latency: {round(bot.latency * 1000)}ms')

#Loads cog
@in_channel(backstage_channels[0], backstage_channels[1], backstage_channels[2], backstage_channels[3])
@bot.command()
@commands.has_permissions(manage_channels=True)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.channel.send(f'{extension} has been loaded')

#Unloads cog
@in_channel(backstage_channels[0], backstage_channels[1], backstage_channels[2], backstage_channels[3])
@bot.command()
@commands.has_permissions(manage_channels=True)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.channel.send(f'{extension} has been unloaded')

#Reload cog
@in_channel(backstage_channels[0], backstage_channels[1], backstage_channels[2], backstage_channels[3])
@bot.command(aliases=["reload"])
@commands.has_permissions(manage_channels=True)
async def reloader(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.channel.send(f'{extension} has been reloaded')

#No command error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('I\'m not sure what you\'re asking. Try \"!help\" for a list of commands I understand.')

bot.run(TOKEN)