import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
# Image processing library
from PIL import Image
# Python wrapper for Tesseract OCR
import pytesseract
import io

# Set the path to the Tesseract executable, this is the default
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

load_dotenv()
token = os.getenv('TOKEN')

# Define the intents your bot needs
intents = discord.Intents.default()
intents.message_content = True # Enable bot to receive message content

# Create the bot instance with the defined intents
bot = commands.Bot(command_prefix='!', intents=intents) 
# You can change the command prefix to whatever you want

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

# Change the command here
@bot.command(name='ocr')
async def ocr_command(ctx):
    # Check if images are attached
    if len(ctx.message.attachments) == 0:
        await ctx.send("Please attach an image.")
        return

    ocr_results = []  # List to store OCR results for each image

    for attachment in ctx.message.attachments:
        image_url = attachment.url

        # Get image. don't worry, it does not save the images it's for tesseract to process them
        image_bytes = await attachment.read()
        image = Image.open(io.BytesIO(image_bytes))

        # Perform OCR using pytesseract
        text = pytesseract.image_to_string(image)
        ocr_results.append(text)

    # Combine OCR results into a single message
    combined_text = "\n\n".join(f"OCR Result for Image {i + 1}:\n{text}" for i, text in enumerate(ocr_results))

    # Send the OCR results
    await ctx.send(combined_text)

# Run the bot
bot.run(token)