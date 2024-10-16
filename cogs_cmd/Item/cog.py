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
    @app_commands.describe(
        jcode="Search for an item"
    )
    async def item(self, interaction: discord.Interaction, jcode: str):
        
        items = await db.execute(
            "SELECT name,jcode,ref,location FROM ITEMS WHERE "
            f"jcode='{jcode}' LIMIT 1"
        )
        
        temp = []
        temp.append(
            "From database:\n"
            f"**ITEM**: {items[0][1]}**/**{items[0][0]}\n"
            f"**REF**: {items[0][2]}\n"
            f"**LOCATION**: {items[0][3]}"
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