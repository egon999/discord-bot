
import discord
import requests
import os

DISCORD_TOKEN = os.getenv("MTM4Nzc0ODc1MDI0NzcyMzEyMg.Gk8wQ4.Efys8pQP0zb3v0zZnqs48-5dAIwkr784ic93q0
")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"🤖 ZestyBrats Like Bot is online as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!like"):
        try:
            parts = message.content.split()
            if len(parts) != 3:
                await message.channel.send("❗ Format: `!like <bd/ind> <UID>`\nExample: `!like ind 123456`")
                return

            region = parts[1].lower()
            uid = parts[2]

            if region not in ["bd", "ind"]:
                await message.channel.send("❗ Region must be `bd` or `ind` only.")
                return

            wait_msg = await message.channel.send("⏳ Sending Likes, Please Wait...")

            url = f"https://anish-likes.vercel.app/like?server_name={region}&uid={uid}&key=jex4rrr"
            response = requests.get(url)

            if response.status_code != 200:
                await wait_msg.edit(content="❌ API Request Failed. Try again.")
                return

            data = response.json()

            if data.get("status") == 2:
                await wait_msg.edit(content=(
                    f"🚫 Max Likes Reached for Today\n\n"
                    f"👤 Name: {data.get('PlayerNickname', 'N/A')}\n"
                    f"🆔 UID: {uid}\n"
                    f"🌍 Region: {region.upper()}\n"
                    f"❤️ Current Likes: {data.get('LikesNow', 'N/A')}"
                ))
                return

            await wait_msg.edit(content=(
                f"✅ Likes Sent Successfully!\n\n"
                f"👤 Name: {data.get('PlayerNickname', 'N/A')}\n"
                f"🆔 UID: {uid}\n"
                f"🌍 Server: {region.upper()}\n"
                f"❤️ Before: {data.get('LikesbeforeCommand', 'N/A')}\n"
                f"👍 After: {data.get('LikesafterCommand', 'N/A')}\n"
                f"🎯 Sent By: ZestyBrats"
            ))

        except Exception as e:
            await message.channel.send("❌ Something went wrong.")
            print(e)

client.run(DISCORD_TOKEN)
