#!/Users/kevanahlquist/Dropbox/dev/dci_notify/env/bin/python
'''
Monitor the dci.org website for new score postings.
'''

from __future__ import print_function

#Initialize Sentry before others, requires SENTRY_DSN environment variable
from raven import Client
client = Client()

# Imports
from bs4 import BeautifulSoup
from datetime import datetime
from email.mime.text import MIMEText
from requests.exceptions import ConnectionError
from socket import error as SocketError
import json
import os
import requests
import smtplib
import time


# Config directives
MAIL_SERVER = 'smtp.mailgun.org'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'postmaster@example.com')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'example_password')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'sms@example.com')
MAIL_SUPPRESS_SEND = os.environ.get('MAIL_SUPPRESS_SEND', False)
APP_SUPPRESS_POST = os.environ.get('APP_SUPPRESS_POST', False)
API_POST_URL = os.environ.get('API_POST_URL', 'http://example.com/events/') # 'http://corpscores.herokuapp.com/events/'
RECIPIENT = 'admin@example.com' # Emails message before sending to SMS.


# May be able to ignore basedir, make file wherever script is running
basedir = os.path.abspath(os.path.dirname(__file__))
OUTFILE = os.path.join(basedir, 'lastscrape.txt')
API_KEY = os.environ.get('API_KEY', 'API_KEY')

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
    '''Send the raw event to an admin.'''
    msg = MIMEText(text)
    msg['Subject'] = 'New Event posted on DCI.org'
    msg['From'] = MAIL_DEFAULT_SENDER
    msg['To'] = RECIPIENT
    if not MAIL_SUPPRESS_SEND:
        s = smtplib.SMTP(MAIL_SERVER)
        s.login(MAIL_USERNAME, MAIL_PASSWORD)
        s.sendmail(MAIL_DEFAULT_SENDER, [RECIPIENT], msg.as_string())


def post_to_app(text):
    """Post event to app, text is a string containing a json object."""
    headers = {'Content-type': 'application/json',
               'Accept':       'application/json'}
    r = requests.post(API_POST_URL, data=text, headers=headers)
    if r.status_code != 200:
        raise IOError('Unable to post event to app: %s' % text)


def process_event(event):
    '''Retrieve, parse, and send the scores for the given event UUID.'''
    params = {'event': event}
    try:
        r = requests.get('http://www.dci.org/scores/index.cfm', params=params)
    except (SocketError, ConnectionError):
        return
    if r.status_code != 200:
        return

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
    event_text = json.dumps(thisEvent,
                            sort_keys=True,
                            indent=2,
                            default=dthandler)
    #send_email(event_text)
    add_processed_event(event)
    if not APP_SUPPRESS_POST:
        post_to_app(event_text)


def set_processed_events(events):
    '''Write all processed events out to persistent storage.'''
    with open(OUTFILE, 'w') as f:
        f.writelines('%s\n' % event for event in events)


def get_processed_events():
    '''Retrieve all processed events from persistent storage.'''
    try:
        with open(OUTFILE, 'r') as f:
            ret = f.readlines()
            ret = [item.strip() for item in ret]
    except IOError:
        ret = []
    return ret


def add_processed_event(event):
    '''Add a single new event to the processed events collection.'''
    events = get_processed_events()
    if event not in events:
        events += event
        set_processed_events(events)


def scrape_func():
    '''Entry method when script is run.

    Download scores page to obtain list of event UUIDs, compare to previously
    processed events, process any new events.
    '''

    try:
        # Base /scores URL redirects to the most recent score data
        r = requests.get('http://www.dci.org/scores', allow_redirects=True)
    except (SocketError, ConnectionError):
        return
    if r.status_code != 200:
        return
    soup = BeautifulSoup(r.text)
    try:
        options = soup.find('select').findChildren()
    except AttributeError:
        return None
    current_events = [opt['value'] for opt in options]

    last_processed_events = get_processed_events()
    diff = [item for item in current_events if not eqIn(item,
                                                        last_processed_events)]
    if diff:
        for event in diff:
            process_event(event)


if __name__ == '__main__':
    while True:
        try:
            scrape_func()
        except Exception as e:
            print(e)
        time.sleep(60)
