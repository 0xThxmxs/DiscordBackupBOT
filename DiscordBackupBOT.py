import json
import os
import shutil

from discord.ext import commands

bot = commands.Bot(command_prefix=".")
bot.remove_command("help")

with open("config.json", "r") as dump:
    config = json.load(dump)


@bot.event
async def on_ready():
    print("[+] REsearchBackup")


@bot.command(pass_context=True)
async def backup(ctx):
    await ctx.message.delete()

    for guild in bot.guilds:
        for category in guild.categories:
            if category.id == config["category_to_backup_id"]:
                await ctx.send("[*] Category to backup: {} :white_check_mark:".format(category))

                for channel in category.text_channels:
                    if not os.path.exists("backup/{}".format(channel)):
                        os.makedirs("backup/{}".format(channel))

                    messages = await channel.history().flatten()

                    with open("backup/{}/messages.txt".format(channel), "a") as file:
                        for message in messages:
                            file.write("{}\n".format(message.content))

                    await ctx.send("[+] Backuping channel: {} :white_check_mark:".format(channel))

                await ctx.send("[+] Backup finished :white_check_mark:".format(category))


@bot.command(pass_context=True)
async def restore(ctx):
    await ctx.message.delete()

    for guild in bot.guilds:
        for category in guild.categories:
            if category.id == config["category_to_restore_id"]:
                await ctx.send("[*] Category to restore backup: {} :white_check_mark:".format(category))

                for directory in os.listdir("backup/"):
                    await ctx.guild.create_text_channel(directory, category=category)

                for channel in category.text_channels:
                    with open("backup/{}/messages.txt".format(channel), "r") as file:
                        for message in file.readlines():
                            await channel.send(message)


@bot.command(pass_context=True)
async def delete(ctx):
    await ctx.message.delete()

    for guild in bot.guilds:
        for category in guild.categories:
            if category.id == config["category_to_restore_id"]:
                await ctx.send("[*] Category to delete: {} :white_check_mark:".format(category))

                for channel in category.text_channels:

                    if os.path.exists("backup/{}".format(channel)):
                        shutil.rmtree("backup/{}".format(channel))

                    await channel.delete()
                    await ctx.send("[+] Deleting channel: {} :white_check_mark:".format(channel))

                await ctx.send("[+] Backup deleting finished: {} :white_check_mark:".format(category))


bot.run(config["token"])
