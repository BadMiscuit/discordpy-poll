import sqlite3

conn = sqlite3.connect('bot.db')

c = conn.cursor()

c.execute ('DROP TABLE polls')
c.execute('''
        CREATE TABLE polls(
        id VARCHAR PRIMARY KEY,
        question VARCHAR)
        ''')

c.execute ('DROP TABLE polls_options')
c.execute('''
        CREATE TABLE polls_options(
        poll_id VARCHAR NOT NULL,
        option VARCHAR,
        emoji VARCHAR,
        FOREIGN KEY (poll_id) REFERENCES polls (id))
        ''')

c.execute ('DROP TABLE polls_reactions')
c.execute('''
        CREATE TABLE polls_reactions(
        poll_id VARCHAR NOT NULL,
        poll_option INTEGER NOT NULL,
        user VARCHAR NOT NULL,
        FOREIGN KEY (poll_id) REFERENCES polls (id),
        FOREIGN KEY (poll_option) REFERENCES polls_options (rowid))
        ''')

conn.commit()

conn.close()

