import os
import discord
from keep_alive import keep_alive
from discord.ext import commands

# ตั้งค่า Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# กำหนด Prefix เช่นใช้เครื่องหมาย .
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('-----------------------------------------')

# 1. คำสั่งแบนสมาชิก: .ban @user [เหตุผล]
@bot.command()
@commands.has_permissions(ban_members=True)
async def b(ctx, member: discord.Member, *, reason=None):
    if member == ctx.author:
        await ctx.send(">>> **คุณไม่สามารถแบนตัวเองได้!**")
        return

    await member.ban(reason=reason)
    await ctx.send(f'>>> **แบน {member.mention} เรียบร้อยแล้ว (เหตุผล: {reason})**')

@b.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("คุณไม่มีสิทธิ์ในการแบนสมาชิก (ต้องการสิทธิ์ Ban Members)")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send(">>> **ไม่พบสมาชิกที่ระบุ กรุณาแท็กหรือใส่ ID ให้ถูกต้อง**")


# 2. คำสั่งปลดแบน: .unban user_id
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    try:
        await ctx.guild.unban(user)
        await ctx.send(f'>>> **ปลดแบน {user.name} (ID: {user.id}) เรียบร้อยแล้ว**')
    except discord.NotFound:
        await ctx.send(">>> **ไม่พบรายชื่อผู้ใช้นี้ในรายการถูกแบน**")

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("คุณไม่มีสิทธิ์ในการปลดแบนสมาชิก")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("")

keep_alive()

# แทนที่ 'YOUR_BOT_TOKEN' ด้วย Token ของบอทคุณ
bot.run(os.getenv('TOKEN'))
