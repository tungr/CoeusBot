import discord
from discord.ext import commands
import json

client = commands.Bot(command_prefix='-')

class LevelCom(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @client.event
    async def on_member_join(self, member):
        with open('users.json', 'r') as f:
            users = json.load(f)
        
        await self.update_exp(users, member)

        with open('users.json', 'w') as f:
            json.dump(users, f)
    
    @client.command()
    async def level(self, ctx):
        with open('users.json', 'r') as f:
            users = json.load(f)
        user = ctx.author
        curr_level = users[str(user.id)]['level']
        curr_xp = users[str(user.id)]['experience']
        xp_end = int((curr_level+1) ** 4)
        await ctx.reply(f"You are currently Level {curr_level}.\nYou need {xp_end-curr_xp} XP to reach your next level.")

    async def update_exp(self, ctx, exp):
        with open('users.json', 'r') as f:
            users = json.load(f)
        user = ctx.author

        if str(user.id) not in users:
            users[str(user.id)] = {}
            users[str(user.id)]['experience'] = exp
            users[str(user.id)]['level'] = 1
        else:
            await self.add_exp(ctx, users, exp)
            await self.level_up(ctx, users, ctx.channel)
        with open('users.json', 'w') as f:
            json.dump(users, f)

    async def add_exp(self, ctx, users, exp):
        user = ctx.author
        users[str(user.id)]['experience'] += exp
        print(f"{user} recieved {exp}XP")

    async def level_up(self, ctx, users, channel):
        user = ctx.author
        experience = users[str(user.id)]['experience']
        lvl_start = users[str(user.id)]['level']
        lvl_end = int(experience ** (1/4)) # Formula used to calculate xp for next level

        if (lvl_start < lvl_end):
            users[str(user.id)]['level'] = lvl_end
            await ctx.send(f"{user.mention} has leveled up to Level {lvl_end}")

def setup(client):
  client.add_cog(LevelCom(client))