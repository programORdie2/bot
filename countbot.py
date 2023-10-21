import os, json

import discord

from py_expression_eval import Parser

parser = Parser()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def super_eval(number):
  return parser.parse(number).evaluate({})


@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord!')


next_numbers = json.loads(open('server_count.json', encoding='utf-8').read())


@client.event
async def on_message(message):
  global next_numbers
  if message.author == client.user:
    return
  server_id = str(message.guild.id)
  username = str(message.author).split("#")[0]
  channel = str(message.channel.name)
  user_message = str(message.content)
  if not 'counting' in channel:
    return
    
  if server_id in list(next_numbers):
    next_number = next_numbers[server_id]['count']
  else:
    next_number = 0
    next_numbers[server_id] = {'count': 0, 'lu': ''}
    with open('server_count.json', 'w') as f:
      f.write(json.dumps(next_numbers))


#    print(f'Message {user_message} by {username} ({str(message.author)}) on {channel}')
  try:
    msg_val = str(int(super_eval(user_message)))
  except:
    return
  if str(message.author) == next_numbers[server_id]['lu']:
    embed = discord.Embed(color=discord.Color.from_rgb(233, 184, 36), title="⚠️ Spam Warning!", description=f'You can\'t count two numbers in a row.')
    await message.add_reaction("⚠️")
    await message.reply(embed=embed)
    return
  if msg_val == str(next_number):
    await message.add_reaction("✅")
    next_number += 1
    next_numbers[server_id]['count'] = next_number
    next_numbers[server_id]['lu'] = str(message.author)
    with open('server_count.json', 'w') as f:
      f.write(json.dumps(next_numbers))
    return
  else:
    embed = discord.Embed(
        color=discord.Color.from_rgb(255, 0, 0),
        title="❌ Wrong!",
        description=
        f'That\'s not correct! The next number was **{next_number}**, count is reset to **0** :('
    )
    await message.add_reaction("❌")
    await message.reply(embed=embed)
    next_number = 0
    next_numbers[server_id]['count'] = next_number
    with open('server_count.json', 'w') as f:
      f.write(json.dumps(next_numbers))
    return

client.run(TOKEN)
