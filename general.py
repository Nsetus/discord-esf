""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 5.0
"""

import platform
import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="botinfo",
        description=" "Полезная" информация о боте.",
    )
    @checks.not_blacklisted()
    async def botinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the bot.
        
        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description="duuuuuuuuuude",
            color=0x9C84EF
        )
        embed.set_author(
            name="Bot Information"
        )
        embed.add_field(
            name="Холдер:",
            value="Nset#5181",
            inline=True
        )
        embed.add_field(
            name="Питон версия:",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="Префиксы:",
            value=f"/ (Слеш) или {self.bot.config['prefix']} для стандартных команд",
            inline=False
        )
        embed.set_footer(
            text=f"Запрошено было для {context.author}"
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    @checks.not_blacklisted()
    async def serverinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the server.
        
        :param context: The hybrid command context.
        """
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{context.guild}",
            color=0x9C84EF
        )
        if context.guild.icon is not None:            
            embed.set_thumbnail(
                url=context.guild.icon.url
            )
        embed.add_field(
            name="Сервер айди",
            value=context.guild.id
        )
        embed.add_field(
            name="Счетчик пользователей на сервере",
            value=context.guild.member_count
        )
        embed.add_field(
            name="Tекст/Войс каналов",
            value=f"{len(context.guild.channels)}"
        )
        embed.add_field(
            name=f"Ролей ({len(context.guild.roles)})",
            value=roles
        )
        embed.set_footer(
            text=f"Создано в: {context.guild.created_at}"
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="Чек Пинг бота, если он опять обкакался.",
    )
    @checks.not_blacklisted()
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.
        
        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            title="🏓 Понг!",
            description=f"Пинг бота составляет {round(self.bot.latency * 1000)}ms.",
            color=0x9C84EF
        )
        await context.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
