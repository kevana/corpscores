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


# Could probably ignore basedir, make file wherever script is running
basedir = os.path.abspath(os.path.dirname(__file__))
OUTFILE = os.path.join(basedir, 'lastscrape.txt')
API_KEY = 'password'

# JSONify dates in ISO 8601 format
dthandler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime)
    else json.JSONEncoder().default(obj))


def send_email(text):
    msg = MIMEText(text)
    msg['Subject'] = 'New Event posted on DCI.org'
    msg['From'] = MAIL_DEFAULT_SENDER
    msg['To'] = RECIPIENT
    #TODO: Get rid of this
    print(msg['Subject'])
    print(msg.as_string())
    #s = smtplib.SMTP(MAIL_SERVER)
    #s.login(MAIL_USERNAME, MAIL_PASSWORD)
    #s.sendmail(MAIL_DEFAULT_SENDER, [RECIPIENT], msg.as_string())


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
    post_to_app(event_text)
    print('Processed Event:')
    pprint(thisEvent)


def set_latest_uuid(uuid):
    with open(OUTFILE, 'w') as f:
        f.write(uuid)


def get_latest_uuid():
    try:
        with open(OUTFILE, 'r') as f:
            ret = f.read()
    except IOError:
        ret = None
    return ret


def scrape_func():
    print('.', end='')
    sys.stdout.flush()
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
    event_ids = [opt['value'] for opt in options]
    # If new event, send notification to my cell phone
    latest_event = event_ids[0]
    last_procd_event = get_latest_uuid()
    if latest_event != last_procd_event:
        if last_procd_event:
            # Subtract 1 to exclude last processed event
            idx = event_ids.index(last_procd_event) - 1
        else:
            idx = len(event_ids)
        for event in event_ids[idx::-1]:
            print('Processing event_id:  %s' % event)
            process_event(event)
        print('New Event Scores available!')
        # Update file with latest event uuid
        set_latest_uuid(latest_event)

if __name__ == '__main__':
    # While True loop
    print('Entering check loop')
    while True:
        scrape_func()
        sleep(300)
