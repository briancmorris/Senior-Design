# Daniel Karamitrov
# 10/13/2018

import numpy as np
import pandas as pd
from typing import List, Dict, Any
from datetime import *
from uuid import uuid4
from action_types import ActionEnum


def generate_data_email_driven(START_DATE = datetime(2012, 1, 1), STOP_DATE = datetime(2012, 12, 1),
                               EMAIL_INTERVAL = timedelta(weeks=1), LINKS_PER_EMAIL = 5, NEW_CONTACTS_PER_EMAIL = 5,
                               MIN_ACTIONS_PER_EMAIL = 5, MAX_ACTIONS_PER_EMAIL = 10, VIEWERSHIP_SPAN = timedelta(weeks=8),
                               CONTACT_INTEREST_DROPOUT_THRESHOLD = 0.2, RANDOM_SEED = None):
    """
    Generate contact actions in an email-driven manner. Beginning at the defined starting date, emails are sent out
    on a fixed period. Upon delivery,  new contacts are added and current contacts perform actions
    such as viewing links or unsubscribing. All contacts have a declining 'interest' value and fixed 'interest rate'.

    :param START_DATE: Starting record for data generation.
    :param STOP_DATE: Stopping record for data generation.
    :param EMAIL_INTERVAL: Rate at which emails should appear.
    :param LINKS_PER_EMAIL: Number of unique links per email. Links are random IDs associated with an email via a dictionary.
    :param NEW_CONTACTS_PER_EMAIL: Maximum number of contacts to add for every new email.
    :param MIN_ACTIONS_PER_EMAIL: Minimum number of actions a contact can make per received email.
    :param MAX_ACTIONS_PER_EMAIL: Maximum number of actions a contact can make per received email.
    :param VIEWERSHIP_SPAN: Contacts lose interest in emails over this span and then unsubscribe.
    :param CONTACT_INTEREST_DROPOUT_THRESHOLD: Contacts unsubscribe when interest_ratio falls below this threshold.
    :param RANDOM_SEED: Set numpy random number generator for debugging.
    :return: file_name: relative path name of generated CSV file
    """
    # List of all recorded actions by all known contacts
    # Dict keys are: 'actionID', 'contactID', 'emailID', 'linkID', 'timestamp'
    all_actions: List[Dict[str, Any]] = []

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
        all_actions.append(email_event)

        # generate links for each email
        all_emails[CURRENT_EMAIL_ID] = ['v_' + rand_str() for i in range(LINKS_PER_EMAIL)]

        # CONTACT EVENTS
        # number of new contacts introduced in this mailing interval
        # poisson distribution is left-leaning probability distribution
        num_new_contacts = np.random.poisson(NEW_CONTACTS_PER_EMAIL)

        for i in range(num_new_contacts):
            contactID = 'c_' + rand_str()
            # vary the VIEWERSHIP_SPAN my some multiplier between [0.5 .. 1.5]
            interest_rate = np.random.rand() + 0.5
            all_contacts[contactID] = {
                'id': contactID,
                'start_date': current_date,
                'interest_rate': interest_rate
            }
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
            interest_ratio = 1 - (current_date - info['start_date']) / (VIEWERSHIP_SPAN * info['interest_rate'])
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
            for remove_me in remove_contacts:
                del all_contacts[remove_me]

    raw_df = pd.DataFrame(data=all_actions,
                          columns=['contactID', 'actionID', 'emailID', 'timestamp', 'linkID'])

    # TODO: handle potential file name collisions
    file_name = './Data/data_{:s}.csv'.format(datetime.now().strftime("%Y%m%d-%H%M%S"))

    raw_df.to_csv(file_name)

    return file_name
