from doctest import debug_script
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks
from helpers import db_manager


class Moderation(commands.Cog, name="moderation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="kick",
        description="Кикает участника из сервера",
    )
    @commands.has_permissions(kick_members=True)
    @checks.not_blacklisted()
    @app_commands.describe(user="Никнейм юзера.", reason="Причина.")
    async def kick(self, context: Context, user: discord.User, reason: str = "Причина неизвестна.") -> None:
        """
        Kick a user out of the server.

        :param context: The hybrid command context.
        :param user: The user that should be kicked from the server.
        :param reason: The reason for the kick. Default is "Not specified".
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                title="Error!",
                description="User has Admin permissions.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        else:
            try:
                embed = discord.Embed(
                    title="Участник кикнут!",
                    description=f"**{member}** был кикнут за **{context.author}**.",
                    color=0x9C84EF
                )
                embed.add_field(
                    name="Причина:",
                    value=reason
                )
                await context.send(embed=embed)
                try:
                    await member.send(
                        f"Вы были кикнуты за:**{context.author}**!\nПричина: {reason}"
                    )
                except:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.kick(reason=reason)
            except:
                embed = discord.Embed(
                    title="Ошибка!(099)",
                    description=" Я не имею право кикнуть участника, обновите мои роли чтобы система имело право кикать.",
                    color=0xE02B2B
                )
                await context.send(embed=embed)

    @commands.hybrid_command(
        name="nick",
        description="Менять никнейм у юзера на сервере.",
    )
    @commands.has_permissions(manage_nicknames=True)
    @checks.not_blacklisted()
    @app_commands.describe(user="Юзер", nickname="Новый никнейм юзера который должен стоять.")
    async def nick(self, context: Context, user: discord.User, nickname: str = None) -> None:
        """
        Change the nickname of a user on a server.

        :param context: The hybrid command context.
        :param user: The user that should have its nickname changed.
        :param nickname: The new nickname of the user. Default is None, which will reset the nickname.
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
        try:
            await member.edit(nick=nickname)
            embed = discord.Embed(
                title="Никнейм изменен!",
                description=f"**{member}'s** имеет новый никнейм **{nickname}**!",
                color=0x9C84EF
            )
            await context.send(embed=embed)
        except:
            embed = discord.Embed(
                title="Ошибка!(099)",
                description="Я не имею право изменять никнейм участникам.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="ban",
        description="Забанить анчоуса на сервере.",
    )
    @commands.has_permissions(ban_members=True)
    @checks.not_blacklisted()
    @app_commands.describe(user="Никнейм анчоуса.", reason="Причина.")
    async def ban(self, context: Context, user: discord.User, reason: str = "Не указана.") -> None:
        """
        Bans a user from the server.
        
        :param context: The hybrid command context.
        :param user: The user that should be banned from the server.
        :param reason: The reason for the ban. Default is "Not specified".
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
        try:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    title="Ошибка!(098)",
                    description="Юзер имеет админ права.",
                    color=0xE02B2B
                )
                await context.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Участник забанен!",
                    description=f"**{member}** был забанен за **{context.author}**!",
                    color=0x9C84EF
                )
                embed.add_field(
                    name="Причина:",
                    value=reason
                )
                await context.send(embed=embed)
                try:
                    await member.send(f"Вы были забанены**{context.author}**!\nПричина: {reason}")
                except:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.ban(reason=reason)
        except:
            embed = discord.Embed(
                title="Ошибка!(099)",
                description="Я не имею право банить.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="warn",
        description="Выдает Варны участнику.",
    )
    @commands.has_permissions(manage_messages=True)
    @checks.not_blacklisted()
    @app_commands.describe(user="Никнейм.", reason="Причина.")
    async def warn(self, context: Context, user: discord.User, reason: str = "Не указана") -> None:
        """
        Warns a user in his private messages.

        :param context: The hybrid command context.
        :param user: The user that should be warned.
        :param reason: The reason for the warn. Default is "Not specified".
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
        total = db_manager.add_warn(user.id, context.guild.id, context.author.id, reason)
        embed = discord.Embed(
            title="Участник заработал предупреждение!",
            description=f"**{member}** получил предупреждение за **{context.author}**!\nВ итоге предупреждений: {total}",
            color=0x9C84EF
        )
        embed.add_field(
            name="Причина:",
            value=reason
        )
        await context.send(embed=embed)
        try:
            await member.send(f"** Вы получили варн:{context.author}**!\nПричина: {reason}")
        except:
            # Couldn't send a message in the private messages of the user
            await context.send(f"{member.mention}, вы получили предупреждение **{context.author}**!\nПричина: {reason}")

    @commands.hybrid_command(
        name="warnings",
        description="Показ листа варнов у участника.",
    )
    @commands.has_guild_permissions(manage_messages=True)
    @checks.not_blacklisted()
    @app_commands.describe(user="Никнейм.")
    async def warnings(self, context: Context, user: discord.User):
        """
        Shows the warnings of a user in the server.
        
        :param context: The hybrid command context.
        :param user: The user you want to get the warnings of.
        """
        warnings_list = db_manager.get_warnings(user.id, context.guild.id)
        embed = discord.Embed(
            title = f"Предупреждения у {user}",
            color=0x9C84EF
        )
        description = ""
        if len(warnings_list) == 0:
            description = "Участник не имеет предупреждений."
        else:
            for warning in warnings_list:
                description += f"• Заварнен <@{warning[2]}>: **{warning[3]}** (<t:{warning[4]}>)\n"
        embed.description = description
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="purge",
        description="Удаляет сообщения.",
    )
    @commands.has_guild_permissions(manage_messages=True)
    @checks.not_blacklisted()
    @app_commands.describe(amount="Кол-во сколько нужно удалить сообщений.")
    async def purge(self, context: Context, amount: int) -> None:
        """
        Delete a number of messages.

        :param context: The hybrid command context.
        :param amount: The number of messages that should be deleted.
        """
        purged_messages = await context.channel.purge(limit=amount)
        embed = discord.Embed(
            title="Чат очищен!",
            description=f"**{context.author}** очистил чат от **{len(purged_messages)}** сообщений!",
            color=0x9C84EF
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="hackban",
        description="Bans a user without the user having to be in the server.",
    )
    @commands.has_permissions(ban_members=True)
    @checks.not_blacklisted()
    @app_commands.describe(user_id="The user ID that should be banned.", reason="The reason why the user should be banned.")
    async def hackban(self, context: Context, user_id: str, reason: str = "Not specified") -> None:
        """
        Bans a user without the user having to be in the server.

        :param context: The hybrid command context.
        :param user_id: The ID of the user that should be banned.
        :param reason: The reason for the ban. Default is "Not specified".
        """
        try:
            await self.bot.http.ban(user_id, context.guild.id, reason=reason)
            user = self.bot.get_user(int(user_id)) or await self.bot.fetch_user(int(user_id))
            embed = discord.Embed(
                title="User Banned!",
                description=f"**{user} (ID: {user_id}) ** was banned by **{context.author}**!",
                color=0x9C84EF
            )
            embed.add_field(
                name="Reason:",
                value=reason
            )
            await context.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user. Make sure ID is an existing ID that belongs to a user.",
                color=0xE02B2B
            )
            await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
