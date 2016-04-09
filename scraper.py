import os
import sys
import re

import BeautifulSoup
from googlevoice import Voice
from pymongo import MongoClient


def extractsms(htmlsms) :
    """
    extractsms  --  extract SMS messages from BeautifulSoup tree of Google Voice SMS HTML.

    Output is a list of dictionaries, one per message.
    """
    msgitems = []
    # extract all conversations by searching for a DIV with an ID at top level.
    tree = BeautifulSoup.BeautifulSoup(htmlsms)
    conversations = tree.findAll('div', attrs={'id' : True}, recursive=False)
    for conversation in conversations:
        # Get phone number
        phone_text = conversation.findAll(attrs={'class' : 'gc-quickcall-calldesc-phone'})[0]
        phone = extractphone(phone_text.text)

        # Get date time of most recent message in conversation
        datetime_ = conversation.findAll(attrs={'class' : 'gc-message-time-row'})[0].text

        # for each conversation, extract each row, which is one SMS message.
        rows = conversation.findAll(attrs={'class' : 'gc-message-sms-row'})
        for row in rows:
            # for each row, which is one message, extract all the fields.
            msgitem = {
                u'conversation_id' : conversation['id'],
                u'phone': phone
            }
            spans = row.findAll('span',attrs={'class' : True}, recursive=False)
            for span in spans:
                cl = span['class'].replace('gc-message-sms-', '')
                # put text in dict
                msgitem[cl] = (' '.join(span.findAll(text=True))).strip()
            # add msg dictionary to list
            msgitems.append(msgitem)

        # add datetime_ to last msgitem of conversation
        msgitems[-1]['datetime'] = datetime_
    return msgitems


def extractphone(text):
    """
    Given 'Google will call your phone and connect you to(510) 315-1225.'
    return (510) 315-1225
    """
    match = re.search(r'(\([0-9]{3}\)\s[0-9]{3}-[0-9]{4})', text)

    try:
        return match.groups(0)[0]
    except AttributeError as ex:
        pass

    return None


if __name__ == '__main__':
    # Get sms
    voice = Voice()
    voice.login()
    voice.sms()

    # Connect to mongo
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/sms')
    client = MongoClient(mongo_uri)
    db = client.get_default_database()

    # Insert messages to mongo
    messages = extractsms(voice.sms.html)
    coll_result = db.messages.insert_many(messages)
    print('Records inserted: %s' % len(coll_result.inserted_ids))

    client.close()
