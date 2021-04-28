#### Transfer data from JSON file to MongoDB ####
# @client.command()
# async def qupload(self, ctx):

#     mclient = MongoClient(host="localhost", port=27017)
#     db = mclient.coeusbot
#     quotesdb = db.quotes

#     with open('quotes.json', 'r') as f:
#         quotes = json.load(f)
    
#     for quotenum in range(1, len(quotes)):
#         datetime = quotes[str(quotenum)]['date_time']
#         author = quotes[str(quotenum)]['author']
#         quote = quotes[str(quotenum)]['quote']
#         guild = ctx.guild.id

#         qamount = quotesdb.find({"guild": ctx.guild.id}) # Grab all quotes of same guild id
#         qid = 1

#         # Increment qid based on # of quotes in guild
#         for qnum in qamount:
#             qid += 1

#         mquote = {
#             "datetime": datetime,
#             "author": author,
#             "quote": quote,
#             "guild": guild,
#             "qid": qid
#         }

#         result = quotesdb.insert_one(mquote)
#         mclient.close()
#     await ctx.reply(f'Quotes transferred')

#### Add quote to JSON file ####
# @client.command(aliases=['qua'])
# async def quoteadd(self, ctx, *quote):
#     with open('quotes.json', 'r') as f:
#         quotes = json.load(f)
    
#     if str(len(quotes)+1) not in quotes:
#         now = dt.datetime.now()
#         date_time = now.strftime("%m/%d/%Y, %I:%M%p")
#         q_amount = len(quotes) + 1

#         quotes[str(q_amount)] = {}
#         quotes[str(q_amount)]['quote'] = quote
#         quotes[str(q_amount)]['date_time'] = date_time
#         quotes[str(q_amount)]['author'] = str(ctx.author)

#     with open('quotes.json', 'w') as f:
#         json.dump(quotes, f)

#     await ctx.reply(f'Quote added')

#### Grab quote from JSON file ####
# @client.command()
# async def quotes(self, ctx):
#     with open('quotes.json', 'r') as f:
#         quotes = json.load(f)

#     randquote = random.randint(1,len(quotes))
#     quote = quotes[str(randquote)]['quote']
#     date_time = quotes[str(randquote)]['date_time']
#     author = quotes[str(randquote)]['author']
    
#     quote_embed = discord.Embed(title=f'💬 Quote #{randquote}', color=0x03fcce)

#     newquote = ' '.join(quote)
#     quote_embed.add_field(name='\u200b', value=f'{newquote}', inline=False)
#     quote_embed.set_footer(text=f'{date_time}')
#     await ctx.send(embed=quote_embed)