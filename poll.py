import discord
from config import POLL_CHANNEL
from classes import *

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

async def send_poll(ctx, *args, msg=""):
    if (ctx.message.channel.id != POLL_CHANNEL):
        return
    if (len(args) > 27):
        await ctx.send("Arrête d'essayer de me casser :pepecry:")
        return
    poll, embed = create_poll(args)
    msg = await ctx.send(content=msg, embed=embed)
    if (len(args) != 0):
        set_poll(msg.id, poll)
        for option in poll.options:
            await msg.add_reaction(option.emoji)

def create_poll(args):
    embed = discord.Embed(colour=discord.Colour.from_rgb(254, 254, 254))
    title = ""
    description = ""
    poll = None
    '''
    man Poll
    '''
    if (len(args) == 0):
        title = "man /poll"
        description = """
        **Sondage simple \N{Thumbs Up Sign}/\N{Thumbs Down Sign}:**
        /poll \"Suis-je un bon bot ?\"
        ou
        /poll \"Vim\" \"Emacs\"\n
        **Sondage avec plusieurs propositions**
        /poll \"Pain au chocolat ou chocolatine ?\" \"Pain au chocolat\" \"Pain au chocolat\" """
    else:
        poll = Poll(title=args[0])
        title = ":bar_chart: {0}".format(args[0])
        #Simple Poll
        if (len(args) == 1):
            poll.add_option(Option(emoji="\N{Thumbs Up Sign}"))
            poll.add_option(Option(emoji="\N{Thumbs Down Sign}"))
        #Simple Poll 2
        elif (len(args) == 2):
            poll.title = ""
            title = ""
            poll.add_option(Option(emoji=alphabet[0], option=args[0]))
            poll.add_option(Option(emoji=alphabet[1], option=args[1]))
            description += "{0} {1}\n".format(alphabet[0], args[0])
            description += "{0} {1}\n".format(alphabet[1], args[1])
        #Multiple options Poll
        else:
            for i in range (0, len(args) - 1):
                poll.add_option(Option(emoji=alphabet[i], option=args[i + 1]))
                description += "{0} {1}\n".format(alphabet[i], args[i + 1])
    embed.title, embed.description = title, description
    return poll, embed

async def poll_add_option(ctx, *args):
    if (ctx.message.channel.id != POLL_CHANNEL):
        return
    # Man
    if (len(args) > 1 or len(args) == 0):
        await ctx.send(embed=discord.Embed(
            colour=discord.Colour.from_rgb(254, 254, 254),
            title="man /poll_add",
            description="""**Pour ajouter une option au dernier sondage**
            /poll_add \"Nouvelle option\" """))
        return
    poll_id, poll = get_poll()
    if (poll is None):
        await ctx.send("Il n'y a pas de dernier sondage")
        return
    if (poll.options[0] == "" and poll.options[1] == ""):
        await ctx.send("On peut pas ajouter d'options à un poll simple")
        return
    #FIXME
    if (len(poll.options) == 26):
        await ctx.send("Arrête d'essayer de me casser :pepecry:")
    # Option exists
    for o in poll.options:
        if args[0] == o.option:
            await ctx.send("L'option existe déjà")
            return
    emoji = alphabet[len(poll.options)]
    add_new_option(poll_id, emoji, args[0])
    msg = await ctx.fetch_message(poll_id)
    embed = msg.embeds[0]
    embed.description += "\n{0} {1}\n".format(emoji, args[0])
    await msg.edit(embed=embed)
    await msg.add_reaction(emoji)
