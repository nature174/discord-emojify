import requests,random,discord,json,os
os.environ["SIMPLE_SETTINGS"] = "settings"
from simple_settings import settings
from discord.ext import commands
bot = commands.Bot(command_prefix='run the command called ', description="React with the emojis in a word")

with open("all.json","r") as emojlist:
	emojidict = json.load(emojlist)

@bot.event
async def on_message(response):
	cont = response.content.split(" ")
	for y in cont:
		for z in emojidict.keys():
			if z == y and not response.author.bot:
				if response.channel.id not in settings.blockchannel and response.author.id not in settings.blockuser:
					try:
						await response.add_reaction(emojidict[z])
					except discord.errors.HTTPException:
						await response.add_reaction("⚠")
					except discord.errors.Forbidden:
						break
	await bot.process_commands(response)
@bot.command()
async def invite(reply):
	'''Gimme that invite'''
	await reply.send("https://discord.com/api/oauth2/authorize?client_id=771536822458777601&permissions=67648&scope=bot")

@bot.command()
async def reload(ctx):
	'''Reload the bot's emoji list (admins only)'''
	if ctx.message.author.guild_permissions.manage_channels:
		global emojidict
		with open("all.json","r") as emojlist:
			emojidict = json.load(emojlist)
@bot.group(invoke_without_command=True)
async def block(ctx):
	'''block user or block channel'''
	await ctx.send("Use `run the command called block ` and `user` or `channel`")

@bot.group(invoke_without_command=True)
async def unblock(ctx):
	'''Unblock a previously blocked user or channel'''
	await ctx.send("Use `run the command called unblock ` and `user` or `channel`")

@block.command()
async def user(ctx,user : discord.User):
	'''Don't autoreact to this user'''
	settings.configure(blockuser=settings.blockuser + [user.id])
	await ctx.send(f"Ignoring `{name}#{discriminator}`.")

@unblock.command()
async def user(ctx,user : discord.User):
	'''Autoreact to this user'''
	if user.id in settings.blockuser:
		settings.blockuser.remove(user.id)
	await ctx.send(f"Removing `{name}#{discriminator}` from ignore list.")
@block.command()
async def channel(ctx,channel : discord.TextChannel):
	'''Don't autoreact to messages in this channel'''
	settings.configure(blockchannel=settings.blockchannel + [channel.id])
	await ctx.send(f"Ignoring {channel.mention} ({channel.name})")
@unblock.command()
async def channel(ctx,channel : discord.TextChannel):
	'''Autoreact to messages in this channel'''
	if channel.id in settings.blockchannel:
		settings.blockchannel.remove(channel.id)
	await ctx.send(f"Un-ignoring {channel.mention} ({channel.name})")
bot.run(settings.token) #put the token in the token variable in settings.py
