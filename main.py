import datetime
import discord
from discord.ext import commands
import sched, time
import cases
import os
import requests
import socket

s = sched.scheduler(time.time, time.sleep)
bot = commands.Bot(command_prefix='?')


@bot.event
async def on_ready():
    print("bot is ready for stuff")
    await bot.change_presence(activity=discord.Game("lol"),afk=True)

class general_stuff(commands.Cog):

    @commands.command()
    async def ree(self, message):
        print("lol")
        await message.reply("ree")

    @commands.command()
    @commands.is_owner()
    async def stop(self, message):
        print("stopping")
        await bot.logout()

    @commands.command()
    @commands.is_owner()
    async def redeploy(self, message):
        ip = socket.gethostbyname(socket.gethostname())
        print(ip)
        requests.get("http:/" + ip + ":9000/hooks/redeploy")

    @commands.command()
    async def update(self, message):

        emoji_lb = "<:lb:835461187319234570>"
        emoji_de = "🇩🇪"

        deaths_lb = cases.getValue("Tode_Gesamt")
        cases_lb = cases.getValue("Faelle_Gesamt")

        deaths_de = cases.getDeathsInGermany()
        cases_de = cases.getAllCasesInGermany()

        ratio_lb = (float(float(deaths_lb) * 100 / float(cases_lb)))
        ratio_de = (float(float(deaths_de) * 100 / float(cases_de)))

        embed = discord.Embed(title="Corona-Zahlen " + emoji_lb + "/" + emoji_de,
                              color=0x00ffff,
                              timestamp=datetime.datetime.utcnow())

        cases_km = cases.getCasesIn("KorntalMuenchingen")
        cases_sd = cases.getCasesIn("Schwieberdingen")
        cases_hm = cases.getCasesIn("Hemmingen")

        embed.add_field(name="Korntal-Münchingen",
                        value=cases_km + " // " + str(round(float(cases_km)*5.07150827)),
                        inline=True)

        embed.add_field(name="Schwieberdingen",
                        value=cases_sd + " // " + str(round(float(cases_hm)*8.77963126)),
                        inline=True)

        embed.add_field(name="Hemmingen",
                        value=cases_hm + " // " + str(round(float(cases_hm)*12.3777695)),
                        inline=True)

        ######################################################

        embed.add_field(name="7-Tage-Inzidenz " + emoji_lb,
                        value=cases.getValue("sieben_T_Inz"),
                        inline=True)

        embed.add_field(name="7 Tage Inzidenz " + emoji_de,
                        value=cases.getSevenDayIncidence())

        embed.add_field(name="Erhebungsdatum ⏲",
                        value=cases.getValue("DashTime") + "/" + cases.getDateRKI(),
                        inline=False)

        ######################################################

        embed.add_field(name="Mortalität " + emoji_lb,
                        value=str(round(ratio_lb, 2)) + "%",
                        inline=True)

        embed.add_field(name="Mortalität " + emoji_de,
                        value=str(round(ratio_de, 2)) + "%",
                        inline=True)

        embed.add_field(name="Mortalität 🌍",
                        value="~2.81%",
                        inline=False)

        ######################################################

        embed.add_field(name="Neue Fälle " + emoji_lb + " (ARCGIS)",
                        value="+" + cases.getValue("Diff_Faelle_Gesamt"),
                        inline=True)

        embed.add_field(name="Neue Fälle " + emoji_de + " (RKI)",
                        value="+" + cases.getNewCasesInGermany(),
                        inline=True)

        ######################################################

        embed.set_footer(text=message.author.name + "#" + message.author.discriminator,
                         icon_url=message.author.avatar_url)
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/464054727403896832/831636985897943080/303284178048211.png")
        await message.reply(embed=embed)


bot.add_cog(general_stuff())
bot.run(os.environ["BOT_TOKEN"])
