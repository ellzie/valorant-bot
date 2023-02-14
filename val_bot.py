from typing import Optional
import valo_api
import discord
from discord import app_commands
import teams


MY_GUILD = discord.Object(id=open("guildID.txt", "r").read())  # replace with your guild id

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents,activity: discord.Activity):
        super().__init__(intents=intents,activity=activity)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents,activity=discord.Game(name='VALORANT'))

teamList = {}
queueList = {}

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

# ^ IMPORTS, BEHIND THE SCENES, ETC.
# ---------------------------------------------------------
# \/ BASIC COMMANDS

@client.tree.command()
@app_commands.describe(
    region='Player Region',
    name='Player Name',
    tag='Player Tag',
)
async def rank(interaction: discord.Interaction, region: str, name: str, tag: str):
    """Return Rank"""
    await interaction.response.defer()
    user_details = valo_api.get_mmr_details_by_name(region=region,name=name,tag=tag,version="v2")
    account_details = valo_api.get_account_details_by_name(region=region,name=name,tag=tag,version="v1")
    user_rank = user_details.current_data.currenttierpatched
    user_rank_int = user_details.current_data.currenttier
    user_rr = user_details.current_data.ranking_in_tier
    user_last_game = user_details.current_data.mmr_change_to_last_game
    embedVar = discord.Embed(title=name+"#"+tag,color=teams.pickColor(user_rank_int))
    embedVar.set_thumbnail(url=(account_details.card.small))
    embedVar.add_field(name="Rank",value=user_rank,inline=True)
    if (user_rank != None):
        embedVar.add_field(name="RR",value=f'`{user_rr}({user_last_game})`',inline=True)
    await interaction.followup.send(embed=embedVar)



@client.tree.command()
async def victoriabitter(interaction: discord.Interaction):
    """YAY"""
    await interaction.response.send_message(f'thanks for the wonderful profile picture, em0nky...')

# ^ BASIC COMMANDS
#---------------------------------------------------------
# \/ TEAMS

@client.tree.command()
async def createteam(interaction: discord.Interaction, teamname: str):
    """Creates Team object that will be stored in a map maybe or a list"""
    teamList[teamname] = teams.Team(teamname)
    await interaction.response.send_message(f'Team Created!')


@client.tree.command()
@app_commands.describe(
    region='Player Region',
    name='Player Name',
    tag='Player Tag',
)
async def addplayer(interaction: discord.Interaction, teamname: str, region: str, name: str, tag: str):
    """add player to a created team"""
    player = teams.Player(region=region, name=name, tag=tag)
    teamList[teamname].addPlayer(player)
    await interaction.response.send_message(f'Player Added!')

@client.tree.command()
@app_commands.describe(
    teamname='Team Name',
)
async def viewteam(interaction: discord.Interaction, teamname: str):
    """embed test"""
    embedVar = discord.Embed(title=teamname,description="Players")
    for obj in teamList[teamname].players:
        embedVar.add_field(name=obj.name+"#"+obj.tag, value=obj.rankString, inline=False)
    await interaction.response.send_message(embed=embedVar)

# ^ TEAMS
#---------------------------------------------------------
# \/ QUEUE

@client.tree.command()
@app_commands.describe(
    join='Whether to automatically join the queue (defaults to False)',
    region='Player Region (only required if join is set to True)',
    name='Player Name (only required if join is set to True)',
    tag='Player Tag (only required if join is set to True)',
)
async def postqueue(interaction: discord.Interaction, join: bool = False, region: str = None, name: str = None, tag: str = None):
    """Creates Queue object, that will"""
    if (join == True):
        if (region != None or name != None or tag != None):
            player = teams.Player(region=region, name=name, tag=tag)
            queueList[interaction.user.name] = teams.Queue(owner=interaction.user.name)
            queueList[interaction.user.name].addPlayer(player)
            output = f'Queue Created with ' + interaction.user.name + " as the name!\nYou've been added to the queue!"
        else:
            output = f'Missing information required to add you to queue! Abandoning making queue (set join to False to allow creating empty queue!)'
    else:
        queueList[interaction.user.name] = teams.Queue(owner=interaction.user.name)
        output = f'Queue Created with ' + interaction.user.name + " as the name!"
    await interaction.response.send_message(output)

@client.tree.command()
async def viewqueue(interaction: discord.Interaction, queuename: str):
    """embed test"""
    if queuename in queueList:
        embedVar = discord.Embed(title=queuename + "'s queue!")
        for obj in queueList[queuename].players:
            embedVar.add_field(name=obj.name+"#"+obj.tag, value=obj.rankString, inline=False)
        await interaction.response.send_message(embed=embedVar)
    else:
        await interaction.response.send_message(f'Error: queue with name {queuename} does not exist!')
@client.tree.command()
@app_commands.describe(
    region='Player Region',
    name='Player Name',
    tag='Player Tag',
)
async def joinqueue(interaction: discord.Interaction, queuename: str, region: str, name: str, tag: str):
    """join a created queue"""
    if queuename in queueList:
        player = teams.Player(region=region, name=name, tag=tag)
        queueList[queuename].addPlayer(player)
        output = f"You've joined {queuename}'s queue"
    else:
        output = f"Error: queue with name {queuename} does not exist!"
    await interaction.response.send_message(output)

@client.tree.command()
async def endqueue(interaction: discord.Interaction, queuename: str):
    """End a queue"""
    popAttempt = queueList.pop(queuename, None)
    if (popAttempt == None):
        output = f"Error: queue with name {queuename} does not exist!"
    else:
        output = f"{queuename}'s queue has been deleted!" 
    await interaction.response.send_message(output)
client.run(open("botToken.txt", "r").read())
