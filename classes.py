import discord

class Option:
    def __init__(self, emoji, option=''):
        self.emoji = emoji
        self.option = option


class Poll:
    _id = 0


    def __init__(self, title='', options=None, reactions=None):
        self.title = title
        if (options is None):
            """ Poll with no options """
            self.options = []
        else:
            """ Poll with options """
            self.options = options
        if (reactions is None):
            self.reactions = []
        else:
            self.reactions = reactions

    def add_option(self, new_option):
        for old_option in self.options:
            if (((new_option.option == old_option.option) and \
                    (new_option.emoji == old_option.emoji)) or \
                    ((new_option.option != "") and \
                    (new_option.option == old_option.option))):
                return
        self.options.append(new_option)


    def clear_options(self):
        self.options = []


    def add_reaction(self, reaction):
        self.reactions.add(reaction)


    def to_embed(self):
        embed = discord.Embed(colour=discord.Colour.from_rgb(254, 254, 254))
        if (self.title == ''):
            embed.title = ":bar_chart: Sondage"
        else:
            embed.title = ":bar_chart: {0}".format(self.title)
        if (len(self.options) == 2
                and self.options[0].option == self.options[1].option
                and self.options[0].emoji != self.options[1].emoji):
            return embed
        embed.description = ""
        for o in self.options:
            embed.description += "{0} {1}\n".format(o.emoji, o.option)
        return embed
