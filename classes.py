from db import *
import discord

class Option:
    def __init__(self, emoji, option=''):
        self.emoji = emoji
        self.option = option

class Poll:
    def __init__(self, title='', options=None, reactions=None):
        self.title = title
        if (options is None):
            self.options = []
        else:
            self.options = options
        if (reactions is None):
            self.reactions = []
        else:
            self.reactions = reactions

    def add_option(self, option):
        for o in self.options:
            if (option.option == o.option and option.emoji == o.emoji):
                return
        self.options.append(option)

    def add_reaction(self, reaction):
        self.reactions.append(reaction)

    def to_embed(self):
        embed = discord.Embed(colour=discord.Colour.from_rgb(254, 254, 254))
        if (self.title == ''):
            embed.title = ":bar_chart: Sondage"
        else:
            embed.title = self.title
        if (len(self.options) == 2
                and self.options[0].option == self.options[1].option
                and self.options[0].emoji != self.options[1].emoji):
            return embed
        embed.description = ""
        for o in self.options:
            embed.description += "{0} {1}\n".format(o.emoji, o.option)
        return embed

class Reaction:
    def __init__(self, option, user):
        self.option = option
        self.user = user

def add_new_option(msg, emoji, option):
    with DbConnection() as db:
        db.execute('''
        INSERT INTO polls_options
        VALUES (?, ?, ?)''', (msg, option, emoji))

def get_poll(poll_id=""):
    t = (poll_id,)
    poll = Poll()
    with DbConnection() as db:
        if (poll_id == ""):
            db.execute('SELECT id, question FROM polls ORDER BY rowid DESC LIMIT 1')
            res = db.fetchone()
            if (res is None):
                return None, None
            t, poll = (res[0],), Poll(title=res[1])
        else:
            db.execute('SELECT question FROM polls WHERE id=?', t)
            poll = Poll(title=db.fetchone()[0])
        db.execute('''SELECT option, emoji FROM polls_options WHERE poll_id=?''', t)
        options = db.fetchall()
        for row in options:
            option = Option(option=row[0], emoji=row[1])
            poll.add_option(option)
        #for row in db.execute('''SELECT option, emoji, user
        #        FROM polls_reactions
        #        JOIN polls_options ON polls_reactions.poll_option = polls_options.rowid
        #        WHERE polls_reactions.poll_id=?''', t):
        #    poll.add_reaction(Reaction(option=option, user=row[2]))
    return t[0], poll

def set_poll(msg, poll):
    with DbConnection() as db:
        db.execute('INSERT INTO polls VALUES (?, ?)', (msg, poll.title))
        for o in poll.options:
            db.execute('INSERT INTO polls_options VALUES (?, ?, ?)',
                    (msg, o.option, o.emoji))
        #for r in poll.reactions:
        #    db.execute('''
        #    INSERT INTO polls_reactions VALUE (?, polls_options.rowid, ?)
        #    SELECT rowid FROM polls_options WHERE poll_id = ? AND option = ? AND
        #    emoji = ?''', (msg, r.user, msg, r.option.option, r.option.emoji))
