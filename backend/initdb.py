import sqlite3

def init_db():
    connection = sqlite3.connect('database.db')

    with open('schema.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()


    # cur.execute("INSERT INTO cards (title, pinyin, meaning, con) VALUES (?, ?, ?, ?)",
    #             ('朋友', "péngyǒu",'means friend, pal, acquaintance', 'The character 朋友 (péngyǒu) meaning "friend" can be visually connected to its meaning by imagining the first character 朋 (péng) as people standing side by side, connecting shoulders, symbolizing friendship and togetherness. The sound "péng" also evokes a sense of warmth and closeness, like a friendly pat on the back.')
    #             )
    # cur.execute("INSERT INTO cards (title, pinyin, meaning, con) VALUES (?, ?, ?, ?)",
    #             ('书', "shū",'means "book" or "to write"', 'The character "书" looks like a person with a pen in hand, symbolizing someone writing in a book. The pronunciation "shū" can be associated with the sound of turning pages or the act of writing, mimicking the flow of a pen on paper.')
    #             )
    # cur.execute("INSERT INTO cards (title, pinyin, meaning, con) VALUES (?, ?, ?, ?)",
    #             ('馆', "guǎn",'means guest, traveller; customer', 'The character 客 (kè) means "guest." The left side of the character, 宀 (mián), means "roof," indicating a guest staying under your roof. The sound "kè" resembles the English word "care," which you should show to your guests!')
    #             )
    defaultCards =[
        ('朋友', "péngyǒu",'means friend, pal, acquaintance', 'The character 朋友 (péngyǒu) meaning "friend" can be visually connected to its meaning by imagining the first character 朋 (péng) as people standing side by side, connecting shoulders, symbolizing friendship and togetherness. The sound "péng" also evokes a sense of warmth and closeness, like a friendly pat on the back.'),
        ('书', "shū",'means "book" or "to write"', 'The character "书" looks like a person with a pen in hand, symbolizing someone writing in a book. The pronunciation "shū" can be associated with the sound of turning pages or the act of writing, mimicking the flow of a pen on paper.'),
        ('馆', "guǎn",'means guest, traveller; customer', 'The character 客 (kè) means "guest." The left side of the character, 宀 (mián), means "roof," indicating a guest staying under your roof. The sound "kè" resembles the English word "care," which you should show to your guests!')
    ]
    cur.executemany('INSERT INTO cards (title, pinyin, meaning, con) VALUES (?, ?, ?, ?)', defaultCards)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    init_db()