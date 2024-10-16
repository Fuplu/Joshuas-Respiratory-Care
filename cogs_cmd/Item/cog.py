'''
Help command
'''



import discord
import logging
import os

from Database.MySQL import AsyncDatabase
from discord import app_commands
from discord.ext import commands
LOGGER = logging.getLogger()
db = AsyncDatabase(__file__)

class ItemCog(commands.Cog):
    def __init__(self, client): self.client: discord.Client = client


    @app_commands.command(name="item", description=f"Item")
    async def item(self, interaction: discord.Interaction):
        
        items = await db.execute(
            "SELECT * FROM ITEMS"
        )
        
        temp = []
        temp.append(
            "From database:\n"
            f"{items}"
        )
        
        embed = discord.Embed(
            description=''.join(temp),
            color=discord.Color.green()
        )
        
        await interaction.response.send_message(
            embed=embed
        )



    '''
    Use this to define criteria for who can use the command
    Uncomment the if statement to restrict the command to the server owner
    '''
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # if interaction.user.id != interaction.guild.owner.id: return False
        return True



async def setup(client: commands.Bot):
    await client.add_cog(ItemCog(client))