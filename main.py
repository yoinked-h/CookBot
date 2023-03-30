# -*- coding: utf-8 -*-
import discord
from discord.ext import commands, tasks
import time
import os
import loadhandler as lh
bot = commands.Bot(command_prefix='>.<')
rateLimit = {}
#unicode
THUMBSUP = u'\U0001F44D'
THUMBSDOWN = u'\U0001F44E'
#check if chars.json exists
if not os.path.exists('./chars.json'):
    #setup
    with open('./chars.json', 'w') as f:
        f.write('{}')
    os.mkdir('./data')
    with open('./data/0.json', "w") as f:
        f.write('{}')

def areRateLimited(usrID):
    if usrID in rateLimit:
        if rateLimit[usrID] < time.time():
            del rateLimit[usrID]
            return False 
        else:
            return True 
    return False
def rateLimitf(usrID, delta):
    rateLimit[usrID] = time.time() + delta
@bot.slash_command()
async def createcharacter(ctx, 
                          character: discord.Option(str,'Name of the character (preferibly no special characters)', required=True), 
                          prompt: discord.Option(str,'Prompt used to generate this character', required=True), 
                          imageurl:discord.Option(str,'Image url (can be a discord one) with an image of the generation', required=True)):
    """
    Create a character in the database.
    """
    #ratelimit check
    if areRateLimited(ctx.author.id):
        await ctx.respond(f"You are rate limited. Please wait {round(rateLimit[ctx.author.id] - time.time())} more seconds.")
        return
    rateLimitf(ctx.author.id, 25)
    if lh.addchar(character, prompt, imageurl):
        await ctx.respond(embed=betterRespond("Character created!", f"{character} has been created with the prompt `{prompt}`.", imageurl), ephemeral=True)
    else:
        await ctx.respond(embed=betterRespond("Character creation failed!", f"{character} could not be created with the prompt `{prompt}`; maybe it's already been made?"), ephemeral=True)
#vote view
class voteview(discord.ui.View):
    def __init__(self, charname):
        super().__init__()
        self.charname = charname
    @discord.ui.button(style=discord.ButtonStyle.green, emoji=THUMBSUP) 
    async def upvote(self, button, interaction: discord.Interaction):
        if areRateLimited(interaction.user.id):
            await interaction.response.send_message("You have been rate limited, please try again later.", ephemeral=True)
            return
        #rate limit by 1 minute
        rateLimitf(interaction.user.id, 60)
        lh.vote(self.charname, True)
        await interaction.response.send_message("Your vote has been updated.", ephemeral=True)
    @discord.ui.button(style=discord.ButtonStyle.red, emoji=THUMBSDOWN) 
    async def downvote(self, button, interaction: discord.Interaction):
        if areRateLimited(interaction.user.id):
            await interaction.response.send_message("You have been rate limited, please try again later.", ephemeral=True)
            return
        rateLimitf(interaction.user.id, 60)
        lh.vote(self.charname, False)
        await interaction.response.send_message("Your vote has been updated.", ephemeral=True)
        #disable all buttons
        

def betterRespond(title:str, info:str, image:str=None, footer:str=None):
    embed=discord.Embed(title=title, description=info)
    #set the color to a random color
    embed.color = discord.Color.random()
    if footer:
        embed.set_footer(text=footer)
    if image != None:
        embed.set_image(url=image)
    return embed
@bot.slash_command()
async def search(ctx, 
                 character: discord.Option(str,'Name of the character to search for', required=True), 
                 sendtochannel: discord.Option(bool,'Send the message to everyone in the channel (default: True)', default=True)):
    """
    Search for a character in the database.
    """
    char = lh.search(character)
    chardata = lh.getReal(char)
    lh.searchForBad()
    if char == None:
        await ctx.respond(embed=betterRespond("Character not found!", f"A prompt for {character} could not be found. Consider adding one using /createcharacter"), ephemeral=True)
    else:
        #format the embed
        tosend = betterRespond(char['name'], f"`{chardata['prompt']}`", chardata['imageurl'], f"Use the UI below to vote! Total votes: {chardata['totalvotes']}")
        await ctx.respond(embed=tosend, ephemeral=not sendtochannel, view=voteview(char['name']))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-' * max(len(str(bot.user.name)), len(str(bot.user.id)), 12))

#run the bot using environment variables
bot.run(os.getenv('DISCORD_TOKEN'))