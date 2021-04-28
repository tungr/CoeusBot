import discord, random, json, datetime as dt
from discord.ext import commands
from pymongo import MongoClient, DESCENDING

client = commands.Bot(command_prefix='-')

class ExtraCom(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @client.command(aliases=['qua'])
    async def quoteadd(self, ctx, *quote):
        now = dt.datetime.now()
        datetime = now.strftime("%m/%d/%Y, %I:%M%p")

        mclient = MongoClient(host="localhost", port=27017)
        db = mclient.coeusbot
        quotes = db.quotes
        newquote = ' '.join(quote)

        qamount = quotes.find({"guild": ctx.guild.id}) # Grab all quotes of same guild id
        qid = 1 # Starting quote ID

        # Increment qid based on # of quotes in guild
        for qnum in qamount:
            qid += 1

        mquote = {
            "datetime": datetime,
            "author": str(ctx.author),
            "quote": newquote,
            "guild": ctx.guild.id,
            "qid": qid
        }

        result = quotes.insert_one(mquote)
        mclient.close()
        await ctx.reply(f'Quote #{qid} added')
    
    @client.command()
    async def quote(self, ctx, quote_num):
        mclient = MongoClient(host="localhost", port=27017)
        db = mclient.coeusbot
        quotes = db.quotes
        aggquote = db.quotes.aggregate([{ "$match": { "guild": ctx.guild.id, "qid": int(quote_num) } }, {"$sample": { "size": 1 } }])
        if (aggquote.alive == False):
            await ctx.reply(f'No quotes found')
        else:
            for rquote in aggquote:
                qid = rquote.get('qid')
                datetime = rquote.get('datetime')
                quote = rquote.get('quote')
                newquote = quote

                quote_embed = discord.Embed(title=f'💬 Quote #{qid}', color=0x03fcce)
                quote_embed.add_field(name='\u200b', value=f'{newquote}', inline=False)
                quote_embed.set_footer(text=f'{datetime}')
                await ctx.send(embed=quote_embed)

    @client.command()
    async def quotes(self, ctx):
        mclient = MongoClient(host="localhost", port=27017)
        db = mclient.coeusbot
        quotes = db.quotes
        aggquote = db.quotes.aggregate([{ "$match": { "guild": ctx.guild.id } }, {"$sample": { "size": 1 } }])
        if (aggquote.alive == False):
            await ctx.reply(f'No quotes found')
        else:
            for rquote in aggquote:
                qid = rquote.get('qid')
                datetime = rquote.get('datetime')
                quote = rquote.get('quote')
                newquote = quote

                quote_embed = discord.Embed(title=f'💬 Quote #{qid}', color=0x03fcce)
                quote_embed.add_field(name='\u200b', value=f'{newquote}', inline=False)
                quote_embed.set_footer(text=f'{datetime}')
                await ctx.send(embed=quote_embed)
    
    # * Convention: "Reminder title" 2000/10/10 5:30
    @client.command(aliases=['remme'])
    async def remindme(self, ctx, *datetime):

        if datetime == ():
            remind_format = discord.Embed(title='📊 Commmand Usage', color=0xf54278, description='`Example: -remindme "Reminder title" 2020/5/10 5:30`')
            await ctx.reply(embed=remind_format)
            
        title, date, time = datetime
        year, month, day = date.strip().split("/")
        hour, minute = time.strip().split(":")

        with open('reminders.json', 'r') as f:
            reminders = json.load(f)

        if str(len(reminders)+1) not in reminders:
            r_amount = len(reminders) + 1
            reminders[str(r_amount)] = {}
            reminders[str(r_amount)]['title'] = title
            reminders[str(r_amount)]['reminder'] = str(dt.datetime(int(year), int(month), int(day), int(hour), int(minute)))
        
        with open('reminders.json', 'w') as f:
            json.dump(reminders, f)
        
        await ctx.reply(f'Reminder added')
    
    @remindme.error
    async def remindme_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            remind_format = discord.Embed(title='📊 Commmand Usage', color=0xf54278, description='`Example: -remindme "Reminder title" 2020/5/10 5:30`')
            await ctx.reply(embed=remind_format)
    
    @client.command(aliases=['rems'])
    async def reminders(self, ctx):
        with open('reminders.json', 'r') as f:
            reminders = json.load(f)
        
        for i in range(1, len(reminders)+1):
            reminder_title = reminders[str(i)]['title']
            reminder_time = reminders[str(i)]['reminder']
            rem_embed = discord.Embed(title=f'⏰ {reminder_title}', color=0x03fcce)
            rem_embed.add_field(name='\u200b', value=f'{reminder_time}', inline=False)
            await ctx.send(embed=rem_embed)

def setup(client):
  client.add_cog(ExtraCom(client))