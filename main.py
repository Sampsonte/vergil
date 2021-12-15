import discord
from discord.ext import commands
import random

intents = discord.Intents().all()
client = commands.Bot(command_prefix = '?', intents=intents)

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.dnd, activity=discord.Game('?help'))
  print('vergil online')

#welcome
@client.event
async def on_member_join(member):
  await client.get_channel(873600121793814568).send(f"{member.mention} geldi")
  role = discord.utils.get(member.guild.roles, name='unv')
  await member.add_roles(role)

#leave
@client.event
async def on_member_remove(member):
  await client.get_channel(873600121793814568).send(f"{member.mention} gitti")

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
    await ctx.send("https://media.discordapp.net/attachments/735836120746557482/903365427843956756/ezgif.com-gif-maker_16.gif")

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

@client.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)

@client.command()
@commands.has_permissions(administrator=True)
async def rol(ctx, user : discord.Member, *, role : discord.Role):
  if role.position > ctx.author.top_role.position:
    return await ctx.send('bu rolü vermek için yetkin yok.') 
  if role in user.roles:
      await user.remove_roles(role)
      await ctx.send(f"{role} rolü {user.mention}'dan alındı.")
  else:
      await user.add_roles(role)
      await ctx.send(f"{role} rolü {user.mention}'a verildi.")

@client.command(description="mute atmak")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="muted", description=f"{member.mention} mutelendi ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f"{guild.name}'den mutelendin")

@client.command(description="mutesi açmak.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await member.send(f"{ctx.guild.name}'dan muten açıldı")
   embed = discord.Embed(title="unmute", description=f"{member.mention} unmuted ",colour=discord.Colour.light_gray())
   await ctx.send(embed=embed)
  
client.run('your token here')
