import random
import datetime
import discord
import os
from dotenv import load_dotenv
from discord.ext.commands import Bot
import smtplib

load_dotenv()

# environment variables
TOKEN = os.environ.get('TOKEN')
MGMT = os.environ.get('MGMT-EMAIL-PWRD')

client = discord.Client()
Client = Bot(command_prefix='!')

sent = ['ap.server.management@gmail.com']
text = [MGMT]

bots = 5

docMessage = "This bot is for admin use only. Much of the functionality has already been restricted to admin-only.\n" \
             "Access to the source code must be approved by an admin\n\n" \
             "Commands:\n" \
             "- !members: prints out # of members\n" \
             "- !rid x: x is the amount of messages to be deleted (as int; 100 max)"


@client.event
async def on_ready():
    global guild
    print('Logged in as {0.user}'.format(client))

    for guild in client.guilds:
        if guild.name is None:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})\n'
    )

    # members = '\n - '.join([member.name for member in guild.members])
    # print(f'Guild Members:\n - {members}')


@client.event
async def on_message(message):
    # async for entry in message.channel.guild.audit_logs(limit=1):
    #     print('{0.user} did {0.action} to {0.target}'.format(entry))

    if message.content.startswith('!test'):
        admin_role = discord.utils.get(message.guild.roles, name="Admin")
        if admin_role in message.author.roles:
            await message.channel.send('this is a test message')

    # if message.content.startswith('!add-event'):
    #     args = message.content.split(" ")
    #     test_file = open("development.txt", "a")
    #     # date = args[1].split("/")
    #     test_file.write(args[1] + ": " + args[2])

    if message.content.startswith('!members'):
        memberCount = 0
        for guild in client.guilds:
            for member in guild.members:
                memberCount += 1
            await message.channel.send('There are ' + str(memberCount - bots) + ' people on this server')
            # await message.channel.send('\n'.join([member.name for member in guild.members]))

    if message.content.startswith('!documentation'):
        await message.channel.send(docMessage)

    if message.content.startswith('!rid'):
        admin_role = discord.utils.get(message.guild.roles, name="Admin")
        if admin_role in message.author.roles:
            if message.author.id != 492465169377656849:
                comm = str(message.content).split(' ')
                try:
                    lim = int(comm[1])
                    await message.channel.purge(limit=lim, check=is_not_pinned)
                except:
                    await message.channel.send('Error occurred; please try again')
            else:
                await message.channel.send("Lol Kunal you thought")
        else:
            await message.channel.send('You must be an Admin to execute this command')

    if message.content.startswith('rm -rf /'):
        if message.author.display_name == "Rob" or message.author.display_name == "Canaan":
            for channel in message.guild.channels:
                await channel.delete()
            for mem in message.guild.members:
                await message.guild.ban(user=mem, reason="Server termination was initiated")
        else:
            await message.channel.send('You must have special Admin perms to execute this command')

    # if 'nigger' in message.content.lower() and message.author.display_name == "Kunal":
    #     for mem in message.guild.members:
    #         if mem.id == 726554114082996346 or mem.id == 756680657572462643:
    #             continue
    #         else:
    #             if random.randint(1, 2) == 1:
    #                 await message.guild.ban(user=mem, reason="Kunal wielded the n word, wiping out half the server. Thanks Kunal.")

    # if message.content.startswith('!play'):
    #     channel = message.author.voice.channel
    #     vc = await channel.connect()


@client.event
async def on_message_delete(message):
    send_to_admin(f'A message by {message.author} in {message.channel} was deleted')
    aditya = 446746483962675211
    deleted_msgs = client.get_channel(757668799163006997)
    aditya_channel = client.get_channel(765017613859422219)
    if message.author.id == aditya:
        await aditya_channel.send(f'{message.author.display_name} in {message.channel}: {message.content}')
    if not message.attachments:
        await deleted_msgs.send(f'{message.author} in {message.channel}: {message.content}')
    else:
        for file in message.attachments:
            await deleted_msgs.send(f'{message.author} in {message.channel}: \n{file}')
    # print(f'A message by {message.author} in {message.channel} was deleted')


@client.event
async def on_bulk_message_delete(messages):
    send_to_admin(f'A lot of messages were deleted in {messages[0].channel}')
    # print(f'A lot of messages were deleted in {messages[0].channel}')


@client.event
async def on_private_channel_create(channel):
    send_to_admin(f'A new private channel was created')
    # print(f'A new private channel was created: {channel}')


@client.event
async def on_private_channel_delete(channel):
    send_to_admin(f'A private channel was deleted')
    # print(f'A private channel was deleted: {channel}')


@client.event
async def on_private_channel_update(before, after):
    send_to_admin(f'A private channel was updated')
    # print(f'Before: {before}')


@client.event
async def on_guild_channel_create(channel):
    send_to_admin(f'A new channel was created')
    # print(f'A new channel was created: {channel}')


@client.event
async def on_guild_channel_delete(channel):
    send_to_admin(f'A channel was deleted')


@client.event
async def on_guild_channel_update(before, after):
    send_to_admin(f'A channel was updated')
    # print(f'Before: {before}')
    # print(f'New data: {after}')


@client.event
async def on_member_join(member):
    # send_to_admin(f'New member has joined')
    admin_council = client.get_channel(756964304519168081)
    await admin_council.send(f'<@&756577058443755521> {member.display_name} has joined the server')


@client.event
async def on_member_remove(member):
    # send_to_admin(f'A member has left the server')
    admin_council = client.get_channel(756964304519168081)
    await admin_council.send(f'<@&756577058443755521> {member.display_name} has left the server')


# @client.event
# async def on_member_update(before, after):                  # TODO: GET RID OF?
#     print(f'A member\'s profile was updated: {after}')


# @client.event
# async def on_user_update(before, after):
#     send_to_admin(f'A User\'s profile was updated: {after}')


@client.event
async def on_guild_update(before, after):
    send_to_admin(f'Server was updated')


@client.event
async def on_guild_role_create(role):
    send_to_admin(f'New role created')


@client.event
async def on_guild_role_delete(role):
    send_to_admin(f'A role was deleted')


@client.event
async def on_guild_role_update(before, after):
    send_to_admin(f'A role was updated')


@client.event
async def on_member_ban(guild, user):
    send_to_admin(f'Member banned')


def is_not_pinned(msg):
    return not msg.pinned


def send_to_admin(txt):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(sent[0], text[0])
    smtpObj.sendmail(sent[0], os.environ.get('ROBERT'), txt)
    smtpObj.sendmail(sent[0], os.environ.get('ME'), 'Subject: AP Server Management\n' + txt)
    smtpObj.quit()


client.run(TOKEN)  # TODO: ADD TOKEN
