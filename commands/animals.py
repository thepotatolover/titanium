import discord
from discord import app_commands, Color
from discord.ext import commands
import random
import aiohttp
import os
from pathlib import Path

class animals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sandcat_files = os.listdir(f"{self.bot.path}{self.bot.pathtype}content{self.bot.pathtype}sand-cat{self.bot.pathtype}")

    global cat_titles, dog_titles
    
    animalGroup = app_commands.Group(name="animals", description="See cute animals.")
    
    # Cat / Dog Embed Titles
    cat_titles = ["Aww!", "Cute cat!", "Adorable!", "Meow!", "Purrfect!", "Cat!", ":3"]
    dog_titles = ["Aww!", "Cute dog!", "Adorable!", "Woof!", "Woof woof!", "Dog!", "Bark!"]
    
    # Cat command
    @animalGroup.command(name = "cat", description = "Get a random cat picture.")
    @app_commands.checks.cooldown(1, 5)
    async def cat(self, interaction: discord.Interaction):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thecatapi.com/v1/images/search") as request:
                request_data = await request.json()
                embed_title = random.choice(cat_titles)
                embed = discord.Embed(title = embed_title, color = Color.random())
                embed.set_image(url = request_data[0]["url"])
                embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
                await interaction.followup.send(embed = embed)

    # Dog command
    @animalGroup.command(name = "dog", description = "Get a random dog picture.")
    @app_commands.checks.cooldown(1, 5)
    async def dog(self, interaction: discord.Interaction):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://dog.ceo/api/breeds/image/random") as request:
                request_data = await request.json()
                embed_title = random.choice(dog_titles)
                embed = discord.Embed(title = embed_title, color = Color.random())
                embed.set_image(url = request_data["message"])
                embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
                await interaction.followup.send(embed = embed)
    
    # Sand Cat command
    @animalGroup.command(name = "sand-cat", description = "Get a random sand cat picture.")
    @app_commands.checks.cooldown(1, 5)
    async def sand_cat(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        try:
            target_file = random.choice(self.sandcat_files)
            
            # Make embed, send it
            embed = discord.Embed(title = random.choice(cat_titles), description = "Image credit: https://display-a.sand.cat/", color = Color.random())
            file = discord.File(f"{self.bot.path}{self.bot.pathtype}content{self.bot.pathtype}sand-cat{self.bot.pathtype}{target_file}", filename = target_file)
            embed.set_image(url = f"attachment://{target_file}")
            embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
            await interaction.followup.send(file=file, embed = embed)
        except Exception:
            embed = discord.Embed(title = "Unexpected Error", description = "Please try again later or message <@563372552643149825> for assistance.", color = Color.red())
            await interaction.edit_original_response(embed = embed, view = None)

async def setup(bot):
    await bot.add_cog(animals(bot))