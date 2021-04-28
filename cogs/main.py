import discord, json, random, datetime as dt
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions
from discord.utils import get
from urllib.request import urlopen

# client = discord.Client()
client = commands.Bot(command_prefix='-')
client.remove_command('help')
botcmd = '-'
now = dt.datetime.now()
datetime = now.strftime("%m/%d/%Y, %H:%M:%S")

class MainCom(commands.Cog):

  def __init__(self, client):
    self.client = client
    self.level = client.get_cog('LevelCom')

  # When the bot starts up
  @commands.Cog.listener()
  async def on_ready(self):
    randomgame = ["with life", "with death", "with fire", "with your mind", "with your heart", "with your dog", "with your cat"]
    print(f'({datetime}) ' + 'Logged in as {0.user}'.format(self.client))
    game = discord.Game(random.choice(randomgame))
    await self.client.change_presence(status=discord.Status.online, activity=game)

  # Command: -cat
  @client.command(aliases=['cat'])
  async def cats(self, ctx):
    site = urlopen("https://api.thecatapi.com/v1/images/search")
    catFile = site.read().decode()
    catData = json.loads(catFile)
    for cat in catData:
      await ctx.reply(cat['url'], mention_author=False)

    # TODO Move this to levels file and allow different arguments for update_exp
    # Adds cat_cmd usage to JSON file
    with open('users.json', 'r') as f:
      users = json.load(f)
    user = ctx.author
    if "cat_cmd" not in users[str(user.id)]:
      users[str(user.id)]['cat_cmd'] = 1
    else:
      users[str(user.id)]['cat_cmd'] += 1
    with open('users.json', 'w') as f:
      json.dump(users, f)

    # Awards exp to user
    if self.level is not None:
      await self.level.update_exp(ctx, 5)
    else:
      print("Levels cog is not loaded. No XP given.")

  # Command: -hello
  @client.command()
  async def hello(self, ctx):
    levels = self.client.get_cog('LevelCom')
    await ctx.reply('Hello! 👋')

  # Command: -help
  @client.command(aliases=['help'])
  async def _help(self, ctx):
    embed_help = discord.Embed(title=f'❓ Command Help', color=0x09e326)
    embed_help.add_field(name='🎱 Ask the 8ball a question', value='`' + botcmd + '8ball [Question]`', inline=False)
    embed_help.add_field(name='🐈 Cat pictures', value='`' + botcmd + 'cats`', inline=False)
    embed_help.add_field(name='👋 Say hello!', value='`' + botcmd + 'hello`', inline=False)
    embed_help.add_field(name='🌐 Test your latency', value='`' + botcmd + 'ping`', inline=False)
    embed_help.add_field(name='📊 Make a poll', value='`' + botcmd + 'poll [Question/Choice1/Choice2/...]`', inline=False)
    embed_help.add_field(name='🎲 Roll dice', value='`' + botcmd + 'roll [Dice #] [Sides] (Max 5 dice)`', inline=False)
    await ctx.reply(embed=embed_help)

  @client.command(aliases=['8ball'])
  async def _8ball(self, ctx, *, question):
    responses = [ "It is certain.",
              "It is decidedly so.",
              "Without a doubt.",
              "Yes - definitely.",
              "You may rely on it.",
              "As I see it, yes.",
              "Most likely.",
              "Outlook good.",
              "Yes.",
              "Signs point to yes.",
              "Reply hazy, try again.",
              "Ask again later.",
              "Better not tell you now.",
              "Cannot predict now.",
              "Concentrate and ask again.",
              "Don't count on it.",
              "My reply is no.",
              "My sources say no.",
              "Outlook not so good.",
              "Very doubtful."]
    embed_8ball = discord.Embed(title=f'🎱 {question}', color=0x03fcce)
    embed_8ball.add_field(name='\u200b', value=f'{random.choice(responses)}', inline=False)
    await ctx.send(embed=embed_8ball)

  # Command: -8ball [Question]
  @_8ball.error
  async def _8ball_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      _8ball_format = discord.Embed(title='🎱 Commmand Usage', color=0xf54278, description='`-8ball [Question]`')
      await ctx.reply(embed=_8ball_format)

  # Command: -ping
  @client.command()
  async def ping(self, ctx):
    embed_ping = discord.Embed(title=f'🌐 Pong!', color=0x03fcce)
    embed_ping.add_field(name='\u200b', value=f'{round(self.client.latency * 1000)} ms', inline=False)
    await ctx.reply(embed=embed_ping)

  # Command: -poll [Question/Choice 1/Choice 2/Choice X...]
  @client.command()
  async def poll(self, ctx, *, poll):
    poll_emoji = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯"]
    question, *choices = poll.strip().split("/")
    embed_poll = discord.Embed(title=f'📊 {question}', color=0x03fcce)
    if (len(choices) <= 1):
      embed_poll.add_field(name='\u200b', value=f'{poll_emoji[0]} Yes', inline=False)
      embed_poll.add_field(name='\u200b', value=f'{poll_emoji[1]} No', inline=False)
      embed_poll.set_footer(text=f'Poll started by {ctx.author}')
      poll_message = await ctx.send(embed=embed_poll)
      for i in range(2):
        await poll_message.add_reaction(poll_emoji[i])
    else:
      for i, choice in zip(range(len(choices)), choices):
          embed_poll.add_field(name='\u200b', value=f'{poll_emoji[i]} {choice}', inline=False)
      embed_poll.set_footer(text=f'Poll started by {ctx.author}')
      poll_message = await ctx.send(embed=embed_poll)
      for i in range(len(choices)):
        await poll_message.add_reaction(poll_emoji[i])

  @poll.error
  async def poll_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      poll_format = discord.Embed(title='📊 Commmand Usage', color=0xf54278, description='`-poll [Question/Choice1/Choice2/...]`')
      await ctx.reply(embed=poll_format)

  # Command: -roll [Dice #] [Sides]
  @client.command()
  async def roll(self, ctx, dice, roll):
    maxRolls = 5
    embed_roll = discord.Embed(title=f'🎲 Dice Rolling', color=0x03fcce)
    if (int(dice) == 1):
      randroll = random.randint(1,int(roll))
      threshold = int(roll)/2
      embed_roll.add_field(name='\u200b', value=f'Rolled a {randroll}', inline=False)
      await ctx.send(embed=embed_roll)
      # if (randroll > threshold) and (self.level is not None):
      #   await self.level.update_exp(ctx, 5)
      # else:
      #   print("No XP given.")
    elif (int(dice) > 1 and int(dice) <= maxRolls):
      for die in range(1,int(dice)+1):
        embed_roll.add_field(name='\u200b', value=f'Dice {die} rolled a {random.randint(1,int(roll))}', inline=False)
      await ctx.send(embed=embed_roll)
    else:
      roll_error = discord.Embed(title='🎲 Command Error', color=0xf54278, description='`You can only use up to 5 dice`')
      await ctx.send(embed=roll_error)

  @roll.error
  async def roll_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      roll_format = discord.Embed(title='🎲 Commmand Usage', color=0xf54278, description='`-roll [Dice #] [Sides] (Max 5 dice)`')
      await ctx.reply(embed=roll_format)

def setup(client):
  client.add_cog(MainCom(client))