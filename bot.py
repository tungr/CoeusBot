import discord, os
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions
from dotenv import load_dotenv

client = commands.Bot(command_prefix='-')
client.remove_command('help')
client.remove_command('reload')

# Loads a cog
@client.command()
@has_permissions(administrator=True)
@commands.is_owner()
async def load(ctx, extension):
    await ctx.channel.purge(limit=1)
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"Loaded {extension} cog", delete_after=5)

# Unloads a cog
@client.command()
@has_permissions(administrator=True)
@commands.is_owner()
async def unload(ctx, extension):
    await ctx.channel.purge(limit=1)
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f"Unloaded {extension} cog", delete_after=5)

# Reloads a cog
@client.command(aliases=['reload'])
@has_permissions(administrator=True)
@commands.is_owner()
async def _reload(ctx, extension):
    await ctx.channel.purge(limit=1)
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"Reloaded {extension} cog", delete_after=5)

load_dotenv()
# Grabs cogs from cogs directory
for fname in os.listdir(os.getenv('COGS')):
    if fname.endswith('.py'):
        client.load_extension(f'cogs.{fname[:-3]}')
    else:
        print(f'Unable to load {fname[:-3]}')

client.run(os.getenv('TOKEN'))