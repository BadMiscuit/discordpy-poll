import discord

from discord.ext import commands
from utils.util import guild_only, poll_only, logtrace
from utils.emojis import alphabet, pepeangry, pepecry
from .classes import Poll, Option


class PollCog(commands.Cog):
    """
    Simple poll.
    Commands:
      * /poll "Question?"
      * /poll "Question?" "Value 1" "Value 2"
      * /poll_add "New value"
    """
    last_poll = Poll()


    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='poll')
    @guild_only()
    @poll_only()
    async def poll(self, ctx, *args):
        try:
            await self.send_poll(ctx, *args)
        except Exception as e:
            await logtrace(ctx, e)
            await ctx.message.add_reaction(self.bot.get_emoji(pepeangry[1]))


    @commands.command(name='poll_all')
    @guild_only()
    @poll_only()
    async def poll_all(self, ctx, *args):
        try:
            if (len(args) != 0):
                await self.send_poll(ctx, *args, msg="@here")
            else:
                await self.send_poll(ctx, *args)
        except Exception as e:
            await logtrace(ctx, e)
            await ctx.message.add_reaction(self.bot.get_emoji(pepeangry[1]))


    @commands.command(name='poll_add')
    @guild_only()
    @poll_only()
    async def poll_add(self, ctx, *args):
        try:
            await self.add_option_poll(ctx, *args)
        except Exception as e:
            await logtrace(ctx, e)
            await ctx.message.add_reaction("\N{Cross Mark}")
            await ctx.send("Arrête d'essayer de me casser <:{0}:{1}>".format(pepecry[0], pepecry[1]))


    async def send_poll(self, ctx, *args, msg=""):
        """ Args parser and dispatch method for /poll and /poll_all """
        if (len(args) == 0):
            await ctx.send(embed=self._help())
        elif (len(args) > 20):
            await ctx.send("Pas plus de 20 options <:{0}:{1}>".format(pepecry[0], pepecry[1]))
        else:
            if (len(args) == 1):
                self.last_poll = self.create_poll(title=args[0], options=args)
            elif (len(args) == 2):
                self.last_poll = self.create_poll(title="", options=args)
            else:
                self.last_poll = self.create_poll(title=args[0], options=args[1:])
            msg = await ctx.send(content=msg, embed=self.last_poll.to_embed())
            self.last_poll._id = msg.id
            for option in self.last_poll.options:
                await msg.add_reaction(option.emoji)


    def create_poll(self, title="", options=set()):
        poll = Poll(title=title)
        #Simple Poll
        if (len(options) <= 1):
            poll.add_option(Option(emoji="\N{Thumbs Up Sign}"))
            poll.add_option(Option(emoji="\N{Thumbs Down Sign}"))
        #Simple Poll 2
        elif (len(options) == 2):
            poll.add_option(Option(emoji=alphabet[0], option=options[0]))
            poll.add_option(Option(emoji=alphabet[1], option=options[1]))
        #Multiple options Poll
        else:
            for i in range (0, len(options)):
                poll.add_option(Option(emoji=alphabet[i], option=options[i]))
        return poll


    async def add_option_poll(self, ctx, *args):
        if (len(args) == 0):
            await ctx.send(embed=self._help_add())
        elif (self.last_poll is None):
            await ctx.send("Il n'y a pas de dernier sondage")
        else:
            msg = await ctx.fetch_message(self.last_poll._id)
            if (msg == None):
                await ctx.send("Je ne trouve pas le dernier sondage")
            elif (self.last_poll.options[0].option == "" and \
                    self.last_poll.options[1].option == ""):
                self.last_poll.clear_options()
                for reaction in msg.reactions:
                    await reaction.clear()
            options = [x.option for x in self.last_poll.options]
            new_options = [x for x in args if x not in options]
            if (len(self.last_poll.options) + len(new_options) > 20):
                await ctx.send("Arrête d'essayer de me casser <:{0}:{1}>".format(\
                        pepecry[0], pepecry[1]))
                return
            # Option exists
            if (len(new_options) == 0):
                await ctx.send("Rien à ajouter")
                return
            for opt in new_options:
                emoji = alphabet[len(self.last_poll.options)]
                self.last_poll.add_option(Option(option=opt, emoji=emoji))
                await msg.add_reaction(emoji)
            await msg.edit(embed=self.last_poll.to_embed())
            await ctx.message.add_reaction("\N{White Heavy Check Mark}")


    def _help(self):
        return discord.Embed(colour=discord.Colour.from_rgb(254, 254, 254),
            title="Manuel d'utilisation",
            description="""
            **Sondage simple \N{Thumbs Up Sign}/\N{Thumbs Down Sign}:**
            /poll \"Suis-je un bon bot ?\"
            ou
            /poll \"Vim\" \"Emacs\"\n
            **Sondage avec plusieurs propositions**
            /poll \"Pain au chocolat ou chocolatine ?\" \"Pain au chocolat\" \"Pain au chocolat\"
            """)

    def _help_add(self):
        return discord.Embed(colour=discord.Colour.from_rgb(254, 254, 254),
            title="Manuel d'utilisation",
            description="""**Pour ajouter une option au dernier sondage**
            /poll_add \"Option 1\" \"Option 2\" \"Option 3\" ... """)


def setup(bot):
    bot.add_cog(PollCog(bot))
