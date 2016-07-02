import sqlite3
import re
from collections import Counter
import pdb


def get_keyword_counter(cursor):

    query = 'SELECT tweets FROM grouptweets GROUP BY tweets'
    cursor.execute(query)
    hashtags = []
    for record in cursor:
        tags = re.findall(r"#(\w+)", record[0])
        if tags:
            hashtags.extend(tags)

    return Counter(hashtags)


def get_mentions(cursor):

    query = """
        SELECT usernames.unique_names as mentioned_username, count(*) as num_of_mentions
        FROM grouptweets
        INNER JOIN
        (
        SELECT DISTINCT (username) as unique_names
        FROM grouptweets
        ) usernames
        ON tweets LIKE '%' || usernames.unique_names || '%'
        GROUP BY usernames.unique_names
        ORDER BY num_of_mentions DESC
    """

    cursor.execute(query)
    records = [record for record in cursor]
    return records


def get_dialogue(cursor):

    query = """
        SELECT username as from_username, usernames.unique_names as mentioned_username, tweets
        FROM grouptweets
        INNER JOIN
        (
        SELECT DISTINCT (username) as unique_names
        FROM grouptweets
        ) usernames
        ON tweets LIKE '%' || usernames.unique_names || '%'
        AND usernames.unique_names = 'ThatCoffeeTho'
    """

    cursor.execute(query)
    records = [record for record in cursor]
    return records


def get_retweet_counter(cursor, limit=20):

    query = """
        SELECT tweets, count(*) as cnt
        FROM grouptweets
        WHERE tweets LIKE '%RT%'
        GROUP BY tweets
        ORDER BY cnt DESC
        LIMIT {}
    """.format(limit)

    cursor.execute(query)
    retweets = []
    for record in cursor:
        retweets.append((record[0], record[1]))

    return retweets


def get_link_counter(cursor):

    query = 'SELECT tweets FROM grouptweets'
    cursor.execute(query)
    links = []
    for record in cursor:
        if 'http' not in record[0]:
            continue

        match_obj = re.search("(?P<url>https?://[^\s]+)", record[0])

        if match_obj:
            link = match_obj.group('url')
            if link:
                links.extend([link])

    return Counter(links)


if __name__ == '__main__':

    conn = sqlite3.connect('usertweetsgroup_6-17-16.db')
    cursor = conn.cursor()

    # for line, count in sorted(get_keyword_counter(cursor).iteritems(), key=lambda x: x[1], reverse=True):
    #     print '{}: {}'.format(line, count)
    #
    # for line in get_mentions(cursor):
    #     print line
    #
    # for line in get_dialogue(cursor):
    #     print line
    #
    # for (line, count) in get_retweet_counter(cursor):
    #     print line, count

    for (line, count) in sorted(get_link_counter(cursor).iteritems(), key=lambda x: x[1], reverse=True):
        print line, count