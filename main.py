import discord
import requests
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
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
                await message.channel.send(
                    "❗ **Format:** `!like <bd/ind> <UID>`\n**Example:** `!like ind 123456`"
                )
                return

            region = parts[1].lower()
            uid = parts[2]

            if region not in ["bd", "ind"]:
                await message.channel.send("❗ **Region must be** `bd` **or** `ind` **only.**")
                return

            wait_msg = await message.channel.send("⏳ **Sending Likes, Please Wait a mooment...**")

            url = f"https://anish-likes.vercel.app/like?server_name={region}&uid={uid}&key=jex4rrr"
            response = requests.get(url)

            if response.status_code != 200:
                await wait_msg.edit(content="❌ **API Request Failed. Try again.**")
                return

            data = response.json()

            if data.get("status") == 2:
                embed = discord.Embed(
                    title="🚫 Max Likes Reached for Today, Cooling Down 24Hrs...",
                    description=(
                        f"**👤 Account Name:** {data.get('PlayerNickname', 'N/A')}\n"
                        f"**🆔 UID:** {uid}\n"
                        f"**🌍 Region:** {region.upper()}\n"
                        f"**🔸 Current Likes:** {data.get('LikesNow', 'N/A')}"
                    ),
                    color=discord.Color.red()
                )
                await wait_msg.edit(content=None, embed=embed)
                return

            # ✅ Your banner image (replace this URL with your Discord-uploaded banner)
            BANNER_URL = "https://media.discordapp.net/attachments/1287445603089125573/1388447692941820076/standard_2.gif?ex=6861042e&is=685fb2ae&hm=95b5ad88d2e8bb1a81f3f9f7dedcc52897045821e3d30391d782f6e0fab2ee46&="

            # ✅ Build the success embed
            embed = discord.Embed(
                title="✅ Likes Sent Successfully!",
                description=(
                    f"**👤 Account Name:** {data.get('PlayerNickname', 'N/A')}\n"
                    f"**🆔 UID:** {uid}\n"
                    f"**🌍 Server:** {region.upper()}\n"
                    f"**🔵 Before:** {data.get('LikesbeforeCommand', 'N/A')}\n"
                    f"**🔴 After:** {data.get('LikesafterCommand', 'N/A')}\n"
                    f"**🔹 Sent By:** .gg/ZestyBrats"
                ),
                color=discord.Color.green()
            )

            embed.set_image(url=BANNER_URL)
            embed.set_footer(text=f"Requested by {message.author}")

            await wait_msg.edit(content=None, embed=embed)

        except Exception as e:
            await message.channel.send("❌ **Something went wrong.**")
            print(e)

client.run(DISCORD_TOKEN)
