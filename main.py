import datetime
from datetime import datetime
import discord
from discord.ext import commands
import sched, time
import cases
import os
import subprocess
import asyncio

s = sched.scheduler(time.time, time.sleep)
bot = commands.Bot(command_prefix='?')


@bot.event
async def on_ready():
    print("bot is ready for stuff")
    result = subprocess.check_output("git rev-parse --short HEAD", shell=True)
    await bot.change_presence(activity=discord.Game("auf Version " + str(result.decode('utf-8'))), afk=True)

class general_stuff(commands.Cog):

    @commands.command()
    async def ree(self, ctx):
        print("lol")
        await ctx.reply("ree")

    @commands.command()
    @commands.is_owner()
    async def stop(self,ctx):
        print("stopping")
        await bot.logout()

    @commands.command()
    @commands.is_owner()
    async def redeploy(self,ctx):
        await ctx.message.delete()
        await bot.logout()
        os.system("wget http://192.168.178.66:9000/hooks/redeploy")

    @commands.command()
    @commands.has_role(783432061205610527)
    async def auszeit(self, ctx, arg, arg2):
        message = ctx.message
        await message.delete()
        if len(message.mentions) == 1:
            timeoutUser = message.mentions[0]
            rolesBefore = timeoutUser.roles

            for role in rolesBefore:
               if role.id != 402193346610855946:
                   await timeoutUser.remove_roles(role)

            if not timeoutUser.voice.channel is None:
                old_channel = timeoutUser.voice.channel
                auszeitchannel = message.guild.get_channel(channel_id=841330121788227664)
                await timeoutUser.move_to(auszeitchannel)
                await asyncio.sleep(float(arg2))
                await timeoutUser.move_to(old_channel)
            for role in rolesBefore:
                if role.id != 402193346610855946:
                 await timeoutUser.add_roles(role)
                 await timeoutUser.edit(mute=False)

    @commands.command()
    async def update(self, message):

        emoji_lb = "<:lb:835461187319234570>"
        emoji_de = "🇩🇪"

        embed = discord.Embed(title="Corona-Zahlen " + emoji_lb + "/" + emoji_de, description="Loading data...", color=0xff0000)
        message_new = await message.reply(embed=embed)

        deaths_lb = cases.getValue("Tode_Gesamt")
        cases_lb = cases.getValue("Faelle_Gesamt")

        deaths_de = cases.getDeathsInGermany()
        cases_de = cases.getAllCasesInGermany()

        ratio_lb = (float(float(deaths_lb) * 100 / float(cases_lb)))
        ratio_de = (float(float(deaths_de) * 100 / float(cases_de)))

        lb_time = cases.getValue("DashTime")
        de_time = cases.getDateRKI()

        now = datetime.now()
        date_now = now.strftime("%d.%m.%Y")
        prefix = ""

        if str(date_now) == lb_time:
            prefix = "⚠️"

        embed = discord.Embed(title="Corona-Zahlen " + emoji_lb + "/" + emoji_de,
                              color=0x00ffff,
                              timestamp=datetime.datetime.utcnow())

        cases_km = prefix + cases.getCasesIn("KorntalMuenchingen")
        cases_sd = prefix + cases.getCasesIn("Schwieberdingen")
        cases_hm = prefix + cases.getCasesIn("Hemmingen")

        embed.add_field(name="Korntal-Münchingen",
                        value=cases_km + " // " + str(round(float(cases_km)*5.07150827)),
                        inline=True)

        embed.add_field(name="Schwieberdingen",
                        value=cases_sd + " // " + str(round(float(cases_sd)*8.77963126)),
                        inline=True)

        embed.add_field(name="Hemmingen",
                        value=cases_hm + " // " + str(round(float(cases_hm)*12.3777695)),
                        inline=True)

        ######################################################

        embed.add_field(name="7-Tage-Inzidenz " + emoji_lb,
                        value=prefix + cases.getValue("sieben_T_Inz"),
                        inline=True)

        embed.add_field(name="7 Tage Inzidenz " + emoji_de,
                        value=cases.getSevenDayIncidence())

        embed.add_field(name="Erhebungsdatum ⏲",
                        value=prefix + lb_time + "/" + de_time,
                        inline=False)

        ######################################################

        embed.add_field(name="Mortalität " + emoji_lb,
                        value=prefix + str(round(ratio_lb, 2)) + "%",
                        inline=True)

        embed.add_field(name="Mortalität " + emoji_de,
                        value=str(round(ratio_de, 2)) + "%",
                        inline=True)

        embed.add_field(name="Mortalität 🌍",
                        value="~2.81%",
                        inline=False)

        ######################################################

        embed.add_field(name="Neue Fälle " + emoji_lb + " (ARCGIS)",
                        value=prefix + "+" + cases.getValue("Diff_Faelle_Gesamt"),
                        inline=True)

        embed.add_field(name="Neue Fälle " + emoji_de + " (RKI)",
                        value="+" + cases.getNewCasesInGermany(),
                        inline=True)

        ######################################################

        embed.set_footer(text=message.author.name + "#" + message.author.discriminator,
                         icon_url=message.author.avatar_url)
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/464054727403896832/831636985897943080/303284178048211.png")
        await message_new.edit(embed=embed)


bot.add_cog(general_stuff())
bot.run(os.environ["BOT_TOKEN"])