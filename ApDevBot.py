import discord
import os
from dotenv import load_dotenv
from discord.ext.commands import Bot
import smtplib

sent = ['ap.server.management@gmail.com']
text = [os.environ.get('MGMT-EMAIL-PWRD')]

load_dotenv()

TOKEN = os.environ.get('TOKEN')
client = discord.Client()
Client = Bot('!')

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

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('!members'):
        memberCount = 0
        for guild in client.guilds:
            for member in guild.members:
                memberCount += 1
            await message.channel.send('There are ' + str(memberCount) + ' people on this server')
            # await message.channel.send('\n'.join([member.name for member in guild.members]))

    if message.content.startswith('!documentation'):
        await message.channel.send(docMessage)

    if message.content.startswith('!rid'):
        comm = str(message.content).split(' ')
        try:
            lim = int(comm[1])
            await message.channel.purge(limit=lim)
        except:
            await message.channel.send('Error occurred; please try again')

    # if message.content.startswith('$senddm'):
    #


# @Client.command(pass_context = True)
# async def clear(ctx, number):
#     mgs = [] #Empty list to put all the messages in the log
#     number = int(number) #Converting the amount of messages to delete to an integer
#     async for x in Client.logs_from(ctx.message.channel, limit = number):
#         mgs.append(x)
#     await Client.delete_messages(mgs)


# @client.event
# async def on_member_join(member):

    # async for entry in guild.audit_logs(limit=1):
    #     print('{0.user} did {0.action} to {0.target}'.format(entry))


    # await member.create_dm()
    # await member.dm_channel.send(
    #     f'Hi {member.name}, welcome to my Discord server!'
    # )


@client.event
async def on_message_delete(message):
    # print(f'{message.author.name} deleted a message')
    send_to_admin(f'A message by {message.author} in {message.channel} was deleted')
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
    send_to_admin(f'New member has joined')


@client.event
async def on_member_remove(member):
    send_to_admin(f'A member has left the server')


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


def send_to_admin(txt):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(sent[0], text[0])
    # smtpObj.sendmail(sent[0], os.environ.get('ROBERT'), txt)
    smtpObj.sendmail(sent[0], 'newpydev@gmail.com', 'Subject: AP Server Management\n' + txt)
    smtpObj.quit()


client.run(TOKEN)   # TODO: ADD TOKEN
