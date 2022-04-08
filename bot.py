import os
from discord import channel
from discord.colour import Color
from discord.ext import commands
import discord
from discord import Member
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import random
import functools, operator
from deep_translator import GoogleTranslator
import requests
from bs4 import BeautifulSoup
import wikipedia
from pysherlock import web_ss
from pysherlock import qrgen
from nltk.tokenize import word_tokenize
import nltk
import openai
import wolframalpha
import randfacts
import random_topic
from keep_alive import keep_alive

nltk.download('punkt')
TOKEN = #Your Discord Bot token
bot = commands.Bot(command_prefix='.') 
bot.remove_command("help")

openai.api_key = #Open AI API key

@bot.event
async def on_ready():
    activity = discord.Game(name='Horizon Zero Dawn', type=3) #you can change from playing to watching, etc 
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Bot is ready!")
  
@bot.command()
@commands.has_permissions(ban_members=True)#bans members if admin role is true
async def ban(ctx, user: discord.Member, *, reason="No reason provided"):
        await user.ban(reason=reason)
        ban = discord.Embed(title=f":boom: Banned {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}",color=0x90EE90)
        ban.set_author(name="Gaia", icon_url="https://raw.githubusercontent.com/Sachit71/images-to-use-/main/icontest.png")
        await ctx.message.delete()
        await ctx.channel.send(embed=ban)
        await user.send(embed=ban)
  
@bot.command()
@commands.has_permissions(kick_members=True)# kicks members if admin role is true
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)
        ban = discord.Embed(title=f":boot: Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}",color=0x90EE90)
        ban.set_author(name="Gaia", icon_url="https://raw.githubusercontent.com/Sachit71/images-to-use-/main/icontest.png")
        await ctx.message.delete()
        await ctx.channel.send(embed=ban)
        await user.send(embed=ban)
  
@bot.command()
async def chat(ctx, chat):#chats with input as arg
  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=f"The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. She is Indian and loves electronic dance music, she is also a part-time historian and loves to research the napoleonic wars. The bots name is Gaia \n\nHuman: Hello, who are you?\nAI: I am an AI created by Cyber. How can I help you today?\nHuman: " + chat,
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
  )
  x = response['choices']
  z = list(map(operator.itemgetter('text'), x))
  y = ", ".join(z)

  await ctx.send(y)
  
@bot.command()
async def ask(ctx, query):
  app_id = #your wolframalpha api id
  client = wolframalpha.Client(app_id)
  res = client.query(query)
  answer = next(res.results).text
  emb = discord.Embed(title="Problem Solving", description="[Powered by Wolfram|Alpha](https://www.wolframalpha.com)", color=0x90EE90) #creates embed
  emb.set_author(name="Gaia", icon_url="https://raw.githubusercontent.com/Sachit71/images-to-use-/main/icontest.png")
  emb.add_field(name=query, value=answer, inline=False)
  emb.set_footer(text="Gaia Bot")
  await ctx.channel.send(embed=emb)
  
@bot.command()## get mentioned users avatar
async def av(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    embed = discord.Embed(title = 'User Avatar', description = avamember ,color =  0x90EE90)     
    embed.set_author(name="Gaia", icon_url="https://raw.githubusercontent.com/Sachit71/images-to-use-/main/icontest.png")
    embed.set_image(url = userAvatarUrl)
    await ctx.channel.send(embed=embed)
  
@bot.command()#english grammar and spelling checker
async def checkgrammar(ctx, textmaterial):
  response = openai.Completion.create(
  engine="text-davinci-002",
  prompt="Correct this to standard english" + "\n" + textmaterial,
  temperature=0,
  max_tokens=64,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)
  x = response['choices']
  z = list(map(operator.itemgetter('text'), x))
  y = ", ".join(z)
  emb = discord.Embed(title="Grammar Checker", description="[Powered by Open AI](https://openai.com/)", color=0x90EE90) #creates embed
  emb.set_author(name="Gaia", icon_url="https://raw.githubusercontent.com/Sachit71/images-to-use-/main/icontest.png")
  emb.add_field(name='Corrected text', value=y, inline=False)
  emb.set_footer(text="Gaia Bot")
  await ctx.channel.send(embed=emb)
  
@bot.command()#get important keypoints about any given topic
async def keypoints(ctx, keypoints):
  response = openai.Completion.create(
  engine="text-davinci-002",
  prompt="What are the 10 keypoints  I should remember when studying about " + keypoints + "?",
  temperature=0,
  max_tokens=64,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)
  x = response['choices']
  z = list(map(operator.itemgetter('text'), x))
  y = ", ".join(z)
  emb = discord.Embed(title="Keypoints maker", description="[Powered by Open AI](https://openai.com/)", color=0x90EE90) #creates embed
  emb.set_author(name="Gaia", icon_url="https://raw.githubusercontent.com/Sachit71/images-to-use-/main/icontest.png")
  emb.add_field(name='Key Points', value=y, inline=False)
  emb.set_footer(text="Gaia Bot")
  await ctx.channel.send(embed=emb)


@bot.command()#summarizes paragraph texts
async def tldr(ctx, context):
  response = openai.Completion.create(
  engine="text-davinci-002",
  prompt=context + "tl;dr" + ":" ,
  temperature=0,
  max_tokens=64,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)
  x = response['choices']
  z = list(map(operator.itemgetter('text'), x))
  y = ", ".join(z)
  emb = discord.Embed(title="Text Summary", description="[Powered by Open AI](https://openai.com/)", color=0x90EE90) #creates embed
  emb.set_author(name="Gaia", icon_url="https://raw.githubusercontent.com/Sachit71/images-to-use-/main/icontest.png")
  emb.add_field(name='TLDR', value=y, inline=False)
  emb.set_footer(text="Gaia Bot")
  await ctx.channel.send(embed=emb)


@bot.command()
async def outline(ctx, outlinetext):
  response = openai.Completion.create(
  engine="text-davinci-002",
  prompt="Create an outline for an essay about" + outlinetext,
  temperature=0,
  max_tokens=64,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)
  x = response['choices']
  z = list(map(operator.itemgetter('text'), x))
  y = ", ".join(z)
  emb = discord.Embed(title="Outline Maker", description="[Powered by Open AI](https://openai.com/)", color=0x90EE90) #creates embed
  emb.set_author(name="Gaia", icon_url="https://raw.githubusercontent.com/Sachit71/images-to-use-/main/icontest.png")
  emb.add_field(name='Makes an outline about a given topic', value=y, inline=False)
  emb.set_footer(text="Gaia Bot")
  await ctx.channel.send(embed=emb)


@bot.command()
async def interviewpoints(ctx, person):
  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt="Create a list of 10 questions to ask a " + person,
    temperature=0,
    max_tokens=64,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
  )
  x = response['choices']
  z = list(map(operator.itemgetter('text'), x))
  y = ", ".join(z)
  emb = discord.Embed(title="Interview Question Maker", description="[Powered by Open AI](https://openai.com/)", color=0x90EE90) #creates embed
  emb.set_author(name="Gaia", icon_url="https://raw.githubusercontent.com/Sachit71/images-to-use-/main/icontest.png")
  emb.add_field(name='Generate interview questions', value=y, inline=False)
  emb.set_footer(text="Gaia Bot")
  await ctx.channel.send(embed=emb)


@bot.command()
async def translate(ctx, text, language):
  translated = GoogleTranslator(source='auto', target=language).translate(text) 
  emb = discord.Embed(title="Translator", description="[Powered by Google translate](https://translate.google.co.in)", color=0x90EE90) #creates embed
  emb.set_author(name="Gaia", icon_url="https://raw.githubusercontent.com/Sachit71/images-to-use-/main/icontest.png")
  emb.add_field(name='Translation', value=translated, inline=False)
  emb.set_footer(text="Gaia Bot")
  await ctx.channel.send(embed=emb)


@bot.command()
async def translatehelp(ctx):
  emb = discord.Embed(title="Translation help", description="[Powered by Google translate](https://translate.google.co.in)", color=0x90EE90) #creates embed
  emb.set_author(name="Gaia", icon_url="https://raw.githubusercontent.com/Sachit71/images-to-use-/main/icontest.png")
  emb.add_field(name='Translation', value='[Get the language ISO-2 Values here](https://www.loc.gov/standards/iso639-2/php/code_list.ph)', inline=False)
  emb.set_footer(text="Gaia Bot")
  await ctx.channel.send(embed=emb)


@bot.command()
async def wiki(ctx):
  url = requests.get("https://en.wikipedia.org/wiki/Special:Random")
  soup = BeautifulSoup(url.content, "html.parser")
  title = soup.find(class_="firstHeading").text
  embed = discord.Embed(title="Random wikpedia content", description="[Powered by Wikipedia](https://wikipedia.com)",color=0x90EE90)
  embed.set_author(name="Gaia", icon_url="https://raw.githubusercontent.com/Sachit71/images-to-use-/main/icontest.png")
  embed.add_field(name="Your article",value=wikipedia.summary(title))
  embed.set_footer(text="Gaia Bot")
  await ctx.send(embed=embed)


@bot.command()
async def web_screenshot(ctx, website):
  web_ss(website)
  embed = discord.Embed(title="Website Screenshot", description=website, color=0x90EE90) #creates embed
  embed.set_author(name="Gaia", icon_url="https://raw.githubusercontent.com/Sachit71/images-to-use-/main/icontest.png")
  file = discord.File("screenshot.jpg", filename="screenshot.jpg")
  embed.set_image(url="attachment://screenshot.jpg")
  embed.set_footer(text="Gaia Bot")
  await ctx.send(file=file, embed=embed)

  os.remove('screenshot.jpg')

@bot.command()
async def music(ctx, entry):
  response = openai.Completion.create(
  engine="text-davinci-002",
  prompt="Decide whether the tone of the text is angry, sad, happy, overjoyed, scared, excited, anxious, uninterested, motivational, demotivated, suicidal, romantic:" + entry,
  temperature=0,
  max_tokens=60,
  top_p=1.0,
  frequency_penalty=0.5,
  presence_penalty=0.0
)
  x = response['choices']
  z = list(map(operator.itemgetter('text'), x))
  y = ", ".join(z)
  ab = word_tokenize(y)

  happy = ['https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC','https://open.spotify.com/playlist/37i9dQZF1DWZKuerrwoAGz','https://open.spotify.com/playlist/37i9dQZF1DX0UrRvztWcAU','https://open.spotify.com/playlist/37i9dQZF1DX1H4LbvY4OJi']
  angry = ['https://open.spotify.com/playlist/4t20BRvt7OXkSrUHVXOG7j','https://open.spotify.com/album/2UG4n2AvoNcS1sgynv1qW7','https://open.spotify.com/artist/1fmGBRVmYCmuUQZ7OGrMOn','https://open.spotify.com/album/6jnXzHxv9dIucU0ID5yd0t']
  sad = ['https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0','https://open.spotify.com/playlist/3Kz5KBE3Ksupz9odBGwze6','https://community.spotify.com/t5/Music-Chat/Songs-For-When-You-Are-In-A-Bad-Mood/td-p/1695720','https://open.spotify.com/playlist/3Ar6l24242VBGny7S9VxcD','https://www.pinterest.com/pin/424605071124115414/']
  calm = ['https://open.spotify.com/artist/00WqZVAC8plAECRF34lDqL','https://open.spotify.com/artist/6ow78JLrWSmpuyIq1ynex4','https://open.spotify.com/playlist/2EXP6pCDBdF4yRj2LZ6xFr','https://open.spotify.com/artist/3x8UwNjnSSgJXOLx3P2m62/','https://open.spotify.com/playlist/6EIVswdPfoE9Wac7tB6FNg']
  motivational = [
    'https://open.spotify.com/playlist/37i9dQZF1DXdxcBWuJkbcy',
    'https://open.spotify.com/playlist/6o7IK7K9wanDCWTlWFWqj9',
    'https://open.spotify.com/playlist/3QmRFEwJ5kMVE4CGUuf5C3',
    'https://open.spotify.com/playlist/3jxMoEAFkRawkZJlY9Yuke',
    'https://open.spotify.com/playlist/37i9dQZF1DX91wPVdp6ygD'
  ]
  romantic = [
    'https://open.spotify.com/artist/4yNf9wUbfht6etRreqEtLk',
    'https://open.spotify.com/playlist/0OOZzfr4olaGarfeaydGZf',
    'https://open.spotify.com/playlist/0qwA80h4eYEDSyy5JLdZKE',
    'https://open.spotify.com/artist/6vqkyboHEusslAzvaeGG9K',
    'https://open.spotify.com/album/5ouvdBI8fnK3EuoJNbx0pn',
    'https://open.spotify.com/artist/4MtOV6YePQbsQ1kxyikIP6'
  ]
  if "happy" in ab:
    
    await ctx.send("Here's your playlist based on our sentiment analysis " + random.choice(happy))

  
  if "angry" in ab:
    await ctx.send("Here's your playlist based on our sentiment analysis " + random.choice(angry))
  if "sad" in ab:
    await ctx.send("Here's your playlist based on our sentiment analysis " + random.choice(sad))

  if "overjoyed" in ab:
    await ctx.send("Here's your playlist based on our sentiment analysis " + random.choice(happy))
  if "scared" in ab:
    await ctx.send("Here's your playlist based on our sentiment analysis " + random.choice(calm))

  if "excited" in ab:
    await ctx.send("Here's your playlist based on our sentiment analysis " + random.choice(happy))
    
  if "suicidal" in ab:
    await ctx.send("Please seek help imediately  https://www.opencounseling.com/suicide-hotlines" )
    
  if "demotivated" in ab:
    await ctx.send("Here's your playlist based on our sentiment analysis " + random.choice(motivational))
  if "romantic" in ab:
    await ctx.send("Here's your playlist based on our sentiment analysis" + random.choice(romantic))
@bot.command()
async def qrcode(ctx,data):
  qrgen(data)
  embed = discord.Embed(title="QR code generator", description=data, color=0x90EE90) #creates embed
  embed.set_author(name="Gaia", icon_url="https://raw.githubusercontent.com/Sachit71/images-to-use-/main/icontest.png")
  file = discord.File("qrcode.png", filename="qrcode.png")
  embed.set_image(url="attachment://qrcode.png")
  embed.set_footer(text="Gaia Bot")
  await ctx.send(file=file, embed=embed)
  os.remove('qrcode.png')

@bot.command()
async def facts(ctx):
  x = randfacts.get_fact()
  emb = discord.Embed(title='Random facts', description=x,color=0x90EE90)
  emb.set_author(name="Gaia", icon_url="https://raw.githubusercontent.com/Sachit71/images-to-use-/main/icontest.png")
  emb.set_footer(text="Gaia Bot")
  await ctx.send(embed=emb)

@bot.command()
async def topic(ctx):
  topic=random_topic.get_topic()
  emb = discord.Embed(title='Random topics', description=topic,color=0x90EE90)
  emb.set_author(name="Gaia", icon_url="https://raw.githubusercontent.com/Sachit71/images-to-use-/main/icontest.png")
  emb.set_footer(text="Gaia Bot")
  await ctx.send(embed=emb)

@bot.command()
async def info(ctx):
  embed = discord.Embed(title="Gaia Info",description="GitHub and other links.",color=0x90EE90)
  embed.set_author(name="Gaia", icon_url="https://raw.githubusercontent.com/Sachit71/images-to-use-/main/icontest.png")
  embed.add_field(name="All links",value="[Our Linktree](https://linktr.ee/therealcyber)")
  embed.add_field(name="About",value="The Bot is named after a character in the video game Horizon Zero Dawn, it's written in Python and is filled with tons of features for you to spice your Discord experience up, it is also my submission to the Sonoma Hackathon 2.0!")
  embed.set_footer(text="Gaia Bot")
  await ctx.send(embed=embed)
  
@bot.command()
async def help(ctx):
  embed = discord.Embed(title="Command List", description="Command List for Gaia",color=0x90EE90)
  #https://www.flaticon.com/free-icon/gaia_1598398
  embed.set_author(name="Gaia", icon_url="https://raw.githubusercontent.com/Sachit71/images-to-use-/main/icontest.png")
  embed.add_field(name="`.ban {user}`",value="Bans the user if the admin role is true.")
  embed.add_field(name="`.kick {user}`",value="Kicks the user if the admin role is true.")
  embed.add_field(name="`.av {user`}",value="Gets the users avatar.")
  embed.add_field(name="`.chat {Prompt}`",value="Chat with Gaia :wink:")
  embed.add_field(name="`.ask {query}`",value="Computes, calculus, physics, algebra, fetches open domain questions and a lot more.")
  embed.add_field(name="`.topic`",value="Gets you a random topic to have a convo about.")
  embed.add_field(name="`.facts`",value="Gets you random interrsting facts.")
  embed.add_field(name="`.music {Your text}`",value="Gets you a random Spotify playlist based on your mood.")
  embed.add_field(name="`.web_screenshot {website link}`",value="Gets you the image of the website, so that you don't have to click on suspicious links.")
  embed.add_field(name="`.wiki`",value="Gets you random Wikipedia artcles.")
  embed.add_field(name="`.translate {Text to be translated} {Target language ISO code}`",value="Translates to specified language")
  embed.add_field(name=" `.translatehelp`",value="Gets you the ISO code of the language you want to translate.")
  embed.add_field(name="`.interviewpoints {Person to interview}`",value="Gives you questions to interview the specified person.")
  embed.add_field(name="`.outline {essay topic}`",value="Gives you important outlines about a topic to include in your essay")
  embed.add_field(name="`.tldr {paragraph}`",value="Summarizes long texts for you.")
  embed.add_field(name="`.keypoints {topic}`",value="Gives you keypoints to study about the mentioned topic.")
  embed.add_field(name="`.checkgrammar {Text}`",value="Checks for grammar and spelling.")
  embed.add_field(name="`.help`",value="Shows the message.")
  embed.add_field(name="`.qrcode {Data}`",value="Generates a qr code with the given data embeded.")
  embed.add_field(name="`.info`",value="Get info about the bot.")
  embed.set_footer(text="A make in India initiative.")
  await ctx.send(embed=embed)

keep_alive()
bot.run(TOKEN)

