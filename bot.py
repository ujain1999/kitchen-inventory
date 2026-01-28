import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Select
from sheets import add_place, add_item, get_places, list_inventory
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))  # your server ID

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

tree = bot.tree  # App commands (slash commands)

@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"Logged in as {bot.user}")

# -------------------
# Slash Command: Add Place
# -------------------
@tree.command(name="addplace", description="Add a new storage place", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(place_name="Name of the place")
async def addplace_command(interaction: discord.Interaction, place_name: str):
    if add_place(place_name):
        await interaction.response.send_message(f"✅ Added new place: **{place_name}**")
    else:
        await interaction.response.send_message(f"⚠ Place **{place_name}** already exists.")

# -------------------
# Slash Command: Add Item
# -------------------
class PlaceDropdown(Select):
    def __init__(self, item_name, quantity, places):
        options = [discord.SelectOption(label=p) for p in places]
        super().__init__(placeholder="Select a place...", min_values=1, max_values=1, options=options)
        self.item_name = item_name
        self.quantity = quantity

    async def callback(self, interaction: discord.Interaction):
        chosen_place = self.values[0]
        add_item(self.item_name, self.quantity, chosen_place)
        await interaction.response.send_message(f"✅ Added **{self.item_name} ({self.quantity})** to **{chosen_place}**")

@tree.command(name="additem", description="Add a new item to inventory", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(item_name="Item name", quantity="Quantity of the item")
async def additem_command(interaction: discord.Interaction, item_name: str, quantity: str):
    places = get_places()
    if not places:
        await interaction.response.send_message("⚠ No places found. Add a place first with `/addplace`.")
        return

    view = View()
    view.add_item(PlaceDropdown(item_name, quantity, places))
    await interaction.response.send_message(f"Select a place for **{item_name} ({quantity})**:", view=view)

# -------------------
# Slash Command: List Inventory
# -------------------
@tree.command(name="listinventory", description="List inventory items", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(place_name="Optional: filter by place")
async def listinventory_command(interaction: discord.Interaction, place_name: str = None):
    inv = list_inventory(place_name)
    if place_name:
        if not inv:
            await interaction.response.send_message(f"No items found in **{place_name}**.")
            return
        msg = f"**Inventory for {place_name}:**\n"
        for r in inv:
            msg += f"- {r['Item']} ({r['Quantity']})\n"
    else:
        msg = "**Full Inventory:**\n"
        for p, items in inv.items():
            msg += f"__{p}__\n"
            for r in items:
                if r['Item']:
                    msg += f"- {r['Item']} ({r['Quantity']})\n"
    await interaction.response.send_message(msg)

bot.run(TOKEN)