# Daniel Karamitrov
# 10/13/2018

import numpy as np
import pandas as pd
from typing import List, Dict, Any
from datetime import *
from uuid import uuid4
from action_types import ActionEnum


# list of all recorded actions by all known contacts
# dict keys are: 'actionID', 'contactID', 'emailID', 'linkID', 'timestamp'
all_actions: List[Dict[str, Any]] = []

START_DATE = datetime(2012, 1, 1)
STOP_DATE = datetime(2012, 12, 1)
EMAIL_INTERVAL = timedelta(weeks=1)  # weekly emails

LINKS_PER_EMAIL = 5

NEW_CONTACTS_PER_EMAIL = 5

MIN_ACTIONS_PER_EMAIL = 5
MAX_ACTIONS_PER_EMAIL = 10
VIEWERSHIP_SPAN = timedelta(weeks=8)  # contacts lose interest in emails over this span and then unsubscribe

CONTACT_INTEREST_DROPOUT_THRESHOLD = 0.2  # contacts unsubscribe when interest_ratio falls below this threshold

RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)


def daterange_interval(start_date, end_date, interval):
    """ Generator for supplying a sequence of dates by a periodic interval. """
    last_date = start_date
    while last_date < end_date:
        yield last_date + interval
        last_date += interval


def rand_str(length=5) -> str:
    """ Create a random string of a given length using UUID. """
    return uuid4().hex[:length]


all_emails: Dict[str, List] = {}
all_contacts: Dict = {}
for current_date in daterange_interval(START_DATE, STOP_DATE, EMAIL_INTERVAL):
    # EMAIL EVENT
    CURRENT_EMAIL_ID = "e_" + rand_str()
    email_event = {
        'emailID': CURRENT_EMAIL_ID,
        'timestamp': current_date,
        # 'actionID': None,
        # 'contactID': None,
        # 'linkID': None,
    }
    print("EMAIL PERIOD: ID={}, DATE={}".format(CURRENT_EMAIL_ID, current_date))
    all_actions.append(email_event)

    # generate links for each email
    all_emails[CURRENT_EMAIL_ID] = ['v_' + rand_str() for i in range(LINKS_PER_EMAIL)]

    # CONTACT EVENTS
    # number of new contacts introduced in this mailing interval
    # poisson distribution is left-leaning probability distribution
    num_new_contacts = np.random.poisson(NEW_CONTACTS_PER_EMAIL)
    print("\tNEW CONTACTS={}".format(num_new_contacts))

    for i in range(num_new_contacts):
        contactID = 'c_' + rand_str()
        all_contacts[contactID] = {'id': contactID, 'start_date': current_date}
        contact_action_event = {
            'emailID': CURRENT_EMAIL_ID,
            'timestamp': current_date,
            'actionID': ActionEnum.SUBSCRIBE.value,
            'contactID': contactID,
            'linkID': None,
        }
        all_actions.append(contact_action_event)

    remove_contacts = []
    for contactID, info in all_contacts.items():
        # number of actions this contact will perform for the current email
        # TODO: num_actions depends on how long this contact has been a subscriber
        # TODO: num_actions should decrease in proportion to the length of time they have been a subscriber
        interest_ratio = 1 - (current_date - info['start_date']) / VIEWERSHIP_SPAN
        if interest_ratio < CONTACT_INTEREST_DROPOUT_THRESHOLD:
            contact_action_event = {
                'emailID': CURRENT_EMAIL_ID,
                'timestamp': current_date,
                'actionID': ActionEnum.UNSUBSCRIBE.value,
                'contactID': contactID,
                'linkID': None,
            }
            all_actions.append(contact_action_event)
            remove_contacts.append(contactID)
            continue

        num_actions = np.random.randint(
            interest_ratio * MIN_ACTIONS_PER_EMAIL,
            interest_ratio * MAX_ACTIONS_PER_EMAIL)
        link_view_offsets = np.random.poisson(lam=3, size=num_actions)
        print("\tContact={}, interest_ratio={}, num_actions={}, link_view_offsets={}"
              .format(contactID, interest_ratio, num_actions, link_view_offsets))

        for i in range(num_actions):
            # generate a series of actions offset randomly from the email arrival by some minutes
            # in this case, the user selected a link from the email
            # TODO: add some probability so that a contact occasionally forwards to a friend
            contact_action_event = {
                'emailID': CURRENT_EMAIL_ID,
                'timestamp': current_date + timedelta(minutes=int(link_view_offsets[i])),
                'actionID': ActionEnum.VIEW_LINK.value,
                'contactID': contactID,
                'linkID': np.random.choice(all_emails[CURRENT_EMAIL_ID]),
            }
            all_actions.append(contact_action_event)

    if len(remove_contacts) > 0:
        # remove contacts that lost interest after this email.
        print('Removed Contacts: {}'.format(remove_contacts))
        for remove_me in remove_contacts:
            del all_contacts[remove_me]


raw_df = pd.DataFrame(data=all_actions,
                      columns=['contactID', 'actionID', 'emailID', 'timestamp', 'linkID'])
raw_df.to_csv('./Data/not_medium_dataset_raw.csv')
