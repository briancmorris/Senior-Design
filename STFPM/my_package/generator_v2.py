import numpy as np
import numpy.random as r
import pandas as pd
from typing import List, Dict, Any
from datetime import *
from uuid import uuid4
from generatorobjects import *

# Define the value of the random seed.
np.random.seed(42)

# List dictionaries to convert to a data frame.
all_actions: List[Dict[str, Any]] = []
# List of all contacts who have ever been in the system.
all_contacts = []
# List of current contacts in the system.
current_contacts = []

# Historical data begins on January 1, 2010
start_date = datetime(2010, 1, 1)
# Historical data ends on December 31, 2018
end_date = datetime(2018, 12, 31)
current_date = None

# Bi-weekly emails are sent to contacts.
email_interval = timedelta(days=3)
# Number of links per email. Interval: [5, 11)
LINKS_PER_EMAIL = r.randint(5, 11)

# Number of contacts that are gained each day. Interval [5, 21)
NEW_CONTACTS_PER_DAY = r.randint(5, 21)



def rand_str(length=5) -> str:
    """
    Creates a random string with the specified length and returns it.
    :param length: the length of the randomly generated string, default = 5
    :return: the randomly generated string
    """
    return uuid4().hex[:length]


def contact_generator(num_contacts):
    """
    Generates random contacts with varying action probabilities and appends them to global contact arrays.
    :param num_contacts: the number of contacts to generate
    """
    if not isinstance(num_contacts, int):
        raise ValueError("Parameter 'num_contacts' is not of type int.")

    for n in range(0, num_contacts):
        c_id = "c_" + rand_str()
        dob_year = int(r.randint(1900, 2019))
        dob_month = int(r.random(1, 13))
        dob_day = int(r.random(1, 32))

        if dob_day > 30 and ((dob_month == 4) or (dob_month == 6) or (dob_month == 9) or (dob_month == 11)):
            dob_day = 30
        elif dob_day > 28 and dob_month == 2:
            dob_day = 28

        c_dob = datetime(dob_year, dob_month, dob_day)

        contact = Contact(c_id, c_dob)
    counter = 0
    num_contacts = int(num_contacts)
    while counter < num_contacts:
        contact = {}
        id = "c_" + rand_str()

        yield contact
        counter += 1