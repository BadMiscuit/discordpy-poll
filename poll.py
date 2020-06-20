import discord
from config import POLL_CHANNEL

alphabet = ['\N{REGIONAL INDICATOR SYMBOL LETTER A}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER B}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER C}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER D}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER E}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER F}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER G}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER H}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER I}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER J}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER K}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER L}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER M}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER N}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER O}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER P}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER Q}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER R}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER S}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER T}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER U}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER V}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER W}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER X}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER Y}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER Z}']

async def send_poll(ctx, *args):
    if (ctx.message.channel.id != POLL_CHANNEL):
        return
    embed = create_poll(args)
    msg = await ctx.send(embed=embed)
    if (len(args) - 1 == 0):
        await msg.add_reaction("\N{Thumbs Up Sign}")
        await msg.add_reaction("\N{Thumbs Down Sign}")
    elif (len(args) - 1 >= 2):
        for i in range (0, len(args) - 1):
            await msg.add_reaction(alphabet[i])

def create_poll(args):
    embed = discord.Embed(colour=discord.Colour.from_rgb(254, 254, 254))
    title = ""
    description = ""
    if (len(args) == 2 or len(args) == 0):
        title = "man /poll"
        description = """
        **Sondage simple \N{Thumbs Up Sign}/\N{Thumbs Down Sign}:**
        /poll \"Suis-je un bon bot ?\"\n
        **Sondage avec plusieurs propositions**
        /poll \"Pain au chocolat ou chocolatine ?\" \"Pain au chocolat\" \"Pain au chocolat\" """
    else:
        title = ":bar_chart: {0}".format(args[0])
        for i in range (0, len(args) - 1):
            description += "{0} {1}\n".format(alphabet[i], args[i + 1])
    embed.title, embed.description = title, description
    return embed
