import discord
from discord.ext import commands
from discord.ext.commands import Bot, guild_only
import random

client = commands.Bot(command_prefix = '?')

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.dnd, activity=discord.Game('?help'))
  print('vergil online')

#bot ping
@client.command()
async def ping(ctx):
  await ctx.send(f'{round(client.latency * 1000)} ms')

#clear chat
@client.command(aliases= ['purge','delete'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
   if amount == None:
       await ctx.channel.purge(limit=10)
   else:
       await ctx.channel.purge(limit=amount)

#errors
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('eksik bilgi girdiniz. ')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("bunun için yetkin yok.")

#kick
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason == None:
      reason = ""
    message = f"{ctx.guild.name}'dan kicklendin {reason}"
    await member.send(message)
    await member.kick(reason=reason)
    await ctx.send(f"{member} kicklendi.")

#ban
@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member :  discord.Member, *,reason=None):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("kendini banlayamazsın.")
        return
    if reason == None:
      reason = ""
    message = f"{ctx.guild.name}'dan banlandın {reason}"
    await member.send(message)
    await member.ban(reason=reason)
    await ctx.send(f"{member} banlandı.")

#unban 
@client.command()
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	
	member_name, member_discriminator = member.split('#')
	for ban_entry in banned_users:
		user = ban_entry.user
		
		if (user.name, user.discriminator) == (member_name, member_discriminator):
 			await ctx.guild.unban(user)
 			await ctx.channel.send(f"{user.mention} banı açıldı.")

@client.command()
async def vergil(ctx):
  await ctx.send('https://media.discordapp.net/attachments/899407045797765173/900147954910892072/vergil.gif')

@client.command()
async def dante(ctx):
  await ctx.send('https://media.discordapp.net/attachments/899407045797765173/900147709430874162/dante.gif')

@client.command()
async def d20(ctx):
  await ctx.send(random.choice(liste))
liste = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']

client.run('your token')
