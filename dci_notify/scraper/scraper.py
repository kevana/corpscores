#!/Users/kevanahlquist/Dropbox/dev/dci_notify/env/bin/python
'''
Monitor the dci.org website for new score postings.
'''
from __future__ import print_function

# Imports
from bs4 import BeautifulSoup
from datetime import datetime
from email.mime.text import MIMEText
import json
import os
import requests
import smtplib
import sys
from time import sleep


# Config directives
MAIL_SERVER = 'smtp.mailgun.org'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'postmaster@kevanahlquist.com'
MAIL_PASSWORD = '7wo5fqm8u7n9'
MAIL_DEFAULT_SENDER = 'sms@kevanahlquist.com'
MAIL_SUPPRESS_SEND = False
APP_SUPPRESS_POST = False
RECIPIENT = 'ahlqu039@umn.edu'


# Could probably ignore basedir, make file wherever script is running
basedir = os.path.abspath(os.path.dirname(__file__))
OUTFILE = os.path.join(basedir, 'lastscrape.txt')
API_KEY = 'password'

# JSONify dates in ISO 8601 format
dthandler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime)
    else json.JSONEncoder().default(obj))


def eqIn(item, iterable):
    '''Quick in operator to test for equality instead of identity'''
    for thing in iterable:
        if item == thing:
            return True
    return False


def send_email(text):
    msg = MIMEText(text)
    msg['Subject'] = 'New Event posted on DCI.org'
    msg['From'] = MAIL_DEFAULT_SENDER
    msg['To'] = RECIPIENT
    #TODO: Get rid of this
    print(msg['Subject'])
    print(msg.as_string())
    if not MAIL_SUPPRESS_SEND:
        s = smtplib.SMTP(MAIL_SERVER)
        s.login(MAIL_USERNAME, MAIL_PASSWORD)
        s.sendmail(MAIL_DEFAULT_SENDER, [RECIPIENT], msg.as_string())


def post_to_app(text):
    'Post event to app, text is a string containing a json object.'
    url = 'http://localhost:5000/events/'
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    r = requests.post(url, data=text, headers=headers)
    if r.status_code != 200:
        raise IOError('Unable to post event to app: %s' % text)


def process_event(event):
    params = {'event': event}
    r = requests.get('http://www.dci.org/scores/index.cfm', params=params)
    if r.status_code != 200:
        raise IOError('Unable to load event: %s' % event)
    # Get coarse info out of page
    soup = BeautifulSoup(r.text)
    scoresTable = (soup.find_all('table')[5].
                   find_all('table')[1])
    infoHeader = (soup.find_all('table')[5].
                  find('h3'))
    infoList = list(infoHeader.strings)
    # Build a new event structure
    thisEvent = {}
    thisEvent['date'] = datetime.strptime(infoList[0], '%A, %B %d, %Y')
    thisEvent['name'] = infoList[2]
    loc = infoList[1].rsplit(' ', 1)
    thisEvent['city'] = loc[0].rstrip(',\n\r\t ')
    thisEvent['state'] = loc[1]
    # Parse scores
    rows = scoresTable.findChildren('tr')[2:-2]
    eventResults = []
    for row in rows:
        columns = row.findChildren('td')
        cleanColumns = [col.text.strip() for col in columns]

        if len(cleanColumns) < 3:
            break  # Some events have Exhibition/International class labels

        result = {}
        result['place'] = cleanColumns[0]
        result['corps'] = cleanColumns[1]
        result['score'] = cleanColumns[2]
        eventResults.append(result)
    thisEvent['results'] = eventResults
    thisEvent['api_key'] = API_KEY
    event_text = json.dumps(thisEvent, sort_keys=True, indent=2, default=dthandler)
    send_email(event_text)
    if not APP_SUPPRESS_POST:
        post_to_app(event_text)


def set_processed_events(events):
    with open(OUTFILE, 'w') as f:
        f.writelines('%s\n' % event for event in events)


def get_processed_events():
    try:
        with open(OUTFILE, 'r') as f:
            ret = f.readlines()
            ret = [item.strip() for item in ret]
    except IOError:
        ret = []
    return ret


def scrape_func():
    # Download scores page, compare list of UUIDs to the last one we saw
    # URL redirects to the most recent score data
    r = requests.get('http://www.dci.org/scores', allow_redirects=True)
    if r.status_code != 200:
        raise IOError('Unable to load dci.org/scores')
    soup = BeautifulSoup(r.text)
    try:
        options = soup.find('select').findChildren()
    except AttributeError:
        return None
    current_events = [opt['value'] for opt in options]
    # If new event, send notification to my cell phone
    last_processed_events = get_processed_events()
    diff = [item for item in current_events if not eqIn(item, last_processed_events)]
    if diff:
        print('Diff:')
        print(diff)
        for event in diff:
            print('Processing event_id:  %s' % event)
            process_event(event)
        # Update file with latest event uuid
        set_processed_events(current_events)


if __name__ == '__main__':

    scrape_func()
