from db import *

class Option:
    def __init__(self, emoji, option=''):
        self.emoji = emoji
        self.option = option

class Poll:
    def __init__(self, title=None, options=None, reactions=None):
        self.title = title
        if (options == None):
            self.options = []
        else:
            self.options = options
        if (reactions == None):
            self.reactions = []
        else:
            self.reactions = reactions

    def add_option(self, option):
        self.options.append(option)

    def add_reaction(self, reaction):
        self.reactions.append(reaction)

class Reaction:
    def __init__(self, option, user):
        self.option = option
        self.user = user


def get_poll(poll_id):
    t = (poll_id,)
    with DbConnection() as db:
        db.execute('SELECT question FROM polls WHERE id=?', t)
        poll = Poll(title=db.fetchone()[0])
        for row in db.execute('''SELECT option, emoji, user
                FROM polls_reactions
                JOIN polls_options ON polls_reactions.poll_option = polls_options.rowid
                WHERE polls_reactions.poll_id=?''', t):
            option = Option(option=row[0], emoji=row[1])
            poll.add_reaction(Reaction(option=option, user=row[2]))
            poll.add_option(option)
    return poll

def set_poll(msg, poll):
    with DbConnection() as db:
        db.execute('INSERT INTO polls VALUES (?, ?)', (msg, poll.title))
        for o in poll.options:
            db.execute('INSERT INTO polls_options VALUES (?, ?, ?)',
                    (msg, o.option, o.emoji))
        for r in poll.reactions:
            db.execute('''
            INSERT INTO polls_reactions VALUE (?, polls_options.rowid, ?)
            SELECT rowid FROM polls_options WHERE poll_id = ? AND option = ? AND
            emoji = ?''', (msg, r.user, msg, r.option.option, r.option.emoji))

