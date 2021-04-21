import datetime
import discord
from discord.ext import commands
import sched, time
import cases
import os

s = sched.scheduler(time.time, time.sleep)
bot = commands.Bot(command_prefix='?')


@bot.event
async def on_ready():
    print("bot is ready for stuff")

class general_stuff(commands.Cog):

    @commands.command()
    async def update(self, message):
        cases.updateData()
        embed = discord.Embed(title="Corona-Zahlen Landkreis Ludwigsburg",color=0x00ffff,timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Korntal-Münchingen", value="Aktive Fälle: " + cases.getCasesIn("KorntalMuenchingen"),
                        inline=True)
        embed.add_field(name="Schwieberdingen", value="Aktive Fälle: " + cases.getCasesIn("Schwieberdingen"),
                        inline=True)
        embed.add_field(name="Hemmingen", value="Aktive Fälle: " + cases.getCasesIn("Hemmingen"), inline=True)
        ratio = (float(cases.getValue("Tode_Gesamt"))*100 / int(cases.getValue("Faelle_Gesamt")))
        embed.add_field(name="Todesrate Ludwigsburg",
                        value=str(round(ratio, 2)) + "%",
                        inline=False)
        embed.add_field(name="Neue Fälle Deutschland (RKI)", value="+" + cases.getNewCasesInGermany(), inline=False)
        embed.add_field(name="Datenerhebungsdatum", value=cases.getValue("DashTime"), inline=False)
        embed.set_footer(text=message.author.name + "#" + message.author.discriminator,icon_url=message.author.avatar_url)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/464054727403896832/831636985897943080/303284178048211.png")
        await message.reply(embed=embed)

bot.add_cog(general_stuff())
bot.run(os.environ["BOT_TOKEN"])
