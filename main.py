import discord
import os
import requests
import json
import random
from replit import db

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]
eggID = ["eggjay"]
emID = ["emjay","mj","MJ"]
starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person!",
  "Sucks to suck I guess...",
  "Good for you 🙄",
  "What do you want me to do about it!"
]
botNRe = ["Yikes", "👀","🙄"]
botNeomu= ["is feeling"]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + " -" + json_data[0]["a"]
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
# checking message content starts
  msg = message.content
  
  if any(word in msg for word in eggID):
    await message.channel.send("What do you want!!!!")
  elif any(word in msg for word in emID):
    await message.channel.send("Leave her alone!!!!")
  elif any(word in msg for word in botNeomu):
    await message.channel.send(random.choice(botNRe))
  else:
    if msg.startswith('$'):
      if msg.startswith('$hello'):
        await message.channel.send('Hello!')
      elif msg.startswith('$help'):
        await message.channel.send('✨ Bestie only you can help yourself! ✨')
      elif msg.startswith('$whomst'):
        await message.channel.send("I'm eggjay!")
      elif msg.startswith('$vibe'):
        await message.channel.send("~stars")
        await message.channel.send("~advice")
        await message.channel.send("#vibe")
      elif msg.startswith("$inspire"):
        quote = get_quote()
        await message.channel.send(quote)
      elif msg.startswith("$new"):
        encouraging_message = msg.split("$new ",1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")
      elif msg.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():
          index = int(msg.split("$del",1)[1])
          delete_encouragment(index)
          encouragements = db["encouragements"]
        await message.channel.send(encouragements)
      elif msg.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
          encouragements = db["encouragements"]
        await message.channel.send(encouragements)
      elif msg.startswith("$responding"):
        value = msg.split("$responding ",1)[1]
        if value.lower() == "true":
          db["responding"] = True
          await message.channel.send("Responding is on.")
        else:
          db["responding"] = False
          await message.channel.send("Responding is off.")
      elif db["responding"]:
        options = starter_encouragements
        if "encouragements" in db.keys():
          options = options + list(db['encouragements'])
        if any(word in msg for word in sad_words):
          await message.channel.send(random.choice(options))
        else:
          await message.channel.send("Cash is for capitalists...")
        


    

client.run(os.getenv('TOKEN'))
