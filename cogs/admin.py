import discord, sys
from discord.ext import commands
from discord.ext.commands import has_permissions, bot_has_permissions

client = commands.Bot(command_prefix='-')
client.remove_command('help')

class AdminCom(commands.Cog):

    def __init__(self, client):
        self.client = client

    @client.command()
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} was banned from the server. Reason: {reason}')
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.reply(f'I have insufficient permissions')

    @client.command()
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f'Cleared {amount} messages', delete_after=5)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.reply(f'I have insufficient permissions')
    
    @client.command()
    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} was kicked from the server. Reason: {reason}')
    
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.reply(f'I have insufficient permissions')
    
    @client.command()
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    async def unban(self, ctx, member):
        banned_users = await ctx.guild.ban()
        member_name, member_discriminator = member.split('#') # name#discriminator

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator == member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return
    
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.reply(f'I have insufficient permissions')

    @client.command()
    @has_permissions(administrator=True)
    @bot_has_permissions(manage_messages=True)
    async def killthebot(self, ctx):
        channel = 790346432636518462
        if (ctx.channel.id == channel):
            await ctx.reply(f'Shutting down')
            sys.exit()

def setup(client):
  client.add_cog(AdminCom(client))