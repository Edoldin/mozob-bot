import os
import discord
import asyncio
import configparser

from bot.commands import Command
from bot.tftHiddenQuests import TFTHiddenQuestsCommands

client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as: {0} - {1}'.format(client.user.name, client.user.id))
    print('-'*20)


@client.event
@asyncio.coroutine
def on_message(message):
    command = message.content.lower()
    if message.author == client.user:
        return
    elif command == '&':
        yield from message.channel.send('<@{0}>, No command has been passed.'.format(message.author.id))
    elif command == '&help':
        yield from message.channel.send(Command.help())
    elif command == '&hello':
        yield from message.channel.send(Command.hello(message.author.id))
    elif command.startswith('&factory create'):
        parts = command.replace('&factory create', '').split('&')
        if len(parts) != 2:
            response = '''No has usado bien el comando. 
Hay que usar: `&factory create <Nombre fabrica>&<Nombre producto>`
Por ejemplo: `&factory create mi fabrica de tomates&tomate`
'''
        else:
            response = Command.createFactory(message.author.id, parts[0].strip(), parts[1].strip())
        yield from message.channel.send(response)

    elif command == '&factory delete':
        yield from message.channel.send(Command.deleteFactory(message.author.id))

    elif command == '&factory list':
        yield from message.channel.send(Command.listFactory())

    elif command == '&inventory':
        yield from message.channel.send(Command.inventory(message.author.id))

    elif command == '&tft random_classes':
        yield from message.channel.send(Command.tftRandomClasses(message.author.id))

    elif command == '&tft hidden_quest help':
        responses = Command.tftHiddenQuestHelp()
        yield from message.channel.send(responses[0])
        yield from message.channel.send(responses[1])

    elif command.startswith('&tft hidden_quest create'):
        parts = command.split(' ')
        if len(parts) == 3:
            yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.create(message.author, message.channel)))
        elif len(parts) == 4:
            yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.create(message.author, message.channel, parts[3])))
        else:
            yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.create(message.author, message.channel, parts[3], parts[4])))

    elif command.startswith('&tft hidden_quest join'):
        parts = command.split(' ')
        if len(parts) < 4:
            yield from message.channel.send('Es necesario especificar el ID de la sala a la que te quieres unir. Por ejemplo, `&tft hidden_quest join patata-18`.')
        else:
            yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.join(message.author, parts[3])))

    elif command.startswith('&tft hidden_quest destroy'):
        yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.destroy(message.author)))

    elif command.startswith('&tft hidden_quest leave'):
        yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.leave(message.author)))

    elif command.startswith('&tft hidden_quest reroll'):
        yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.reroll(message.author)))

    elif command.startswith('&tft hidden_quest ready'):
        yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.ready(message.author)))

    elif command.startswith('&tft hidden_quest start'):
        yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.start(message.author)))

    elif command.startswith('&tft hidden_quest end'):
        parts = command.split(' ')
        if len(parts) < 5:
            yield from message.channel.send('Es necesario especificar la posición en la que has quedado y si has cumplido tu misión (y) o no (n). Por ejemplo, si has quedado 5º y has fracasado en tu misión secreta, deberías poner: `&tft hidden_quest end 3 n`.')
        else:
            yield from message.channel.send('{0}'.format(TFTHiddenQuestsCommands.end(message.author, parts[3], parts[4])))

    elif command.startswith('&tft hidden_quest status'):
        response = TFTHiddenQuestsCommands.status(message.author)
        if response is not None:
            yield from message.channel.send('{0}'.format(response))

    elif command.startswith('&leet'):
        response = Command.leet_speak(command.replace('&leet', ''))
        yield from message.channel.send('{0}'.format(response))

# Set up the base bot
class DiscordBot(object):
    def __init__(self):
        self.token = None
        self.configPath = os.path.join(os.getcwd(), 'config.ini')
        self.config = configparser.ConfigParser()

    def exists_config(self):
        return os.path.exists(self.configPath)

    def create_config(self):
        # Ask user for bot token
        self.token = input('Bot Token:')
        # Creates base config file
        self.config.add_section('DiscordBot')
        self.config.set('DiscordBot', 'token', self.token)
        with open(self.configPath, 'w') as configfile:
            self.config.write(configfile)

    def get_token(self):
        self.config.read(self.configPath)
        self.token = self.config.get('DiscordBot', 'token')

    def set_token(self, token):
        self.config.read(self.configPath)
        self.config.set('DiscordBot', 'token', token)
        with open(self.configPath, 'w') as configfile:
            self.config.write(configfile)

    def run(self):
        client.run(self.token)
