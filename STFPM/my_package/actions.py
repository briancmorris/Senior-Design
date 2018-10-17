from enum import Enum


class ActionType(Enum):
    """
    Represents the types of actions a contact can perform. The first entry in the list is the description of the action.
    The second entry is the numeric ID of the action.
    """

    # Account created, can only occur once.
    ACCOUNT_CREATE = ["Account Created", 0]
    # Account deactivated, can only occur once.
    ACCOUNT_DEACTIVATE = ["Account Deactivated", 1]
    # Contact subscribed to marketing emails. Must be a non-subscriber.
    SUBSCRIBE = ["Contact Subscribed to Emails", 2]
    # Contact unsubscribed from marketing emails. Must be a subscriber.
    UNSUBSCRIBE = ["Contact Unsubscribed from Emails", 3]
    # Contact received a marketing email. Must be a subscriber.
    RECEIVED_EMAIL = ["Contact Received Email", 4]
    # Contact opened a marketing email.
    OPENED_EMAIL = ["Contact Opened Email", 5]
    # Contact deleted a marketing email.
    DELETED_EMAIL = ["Contact Deleted Email", 6]
    # Contact loaded a web page.
    LOAD_PAGE = ["Contact Loaded Web Page", 7]
    # Contact closed a web page.
    CLOSE_PAGE = ["Contact Closed Web Page", 8]
    # Contact added item(s) to their cart.
    ADD_ITEM_CART = ["Contact Added Item(s) to Cart", 9]
    # Contact removed item(s) from their cart.
    REMOVE_ITEM_CART = ["Contact Removed Item(s) from Cart", 10]
    # Contacted purchased item(s) in their cart.
    PURCHASE_COMPLETE = ["Contact Purchased Item(s)", 11]
    # Contact returned item(s) from a previous purchase.
    PURCHASE_RETURN = ["Contact Returned Item(s)", 12]


class Action(object):
    """
    Object representation of an action a contact can perform. Context relevant to the action is also maintained by
    objects of this class.
    """

    def __init__(self, action_type, timestamp, contact, context):
        """
        Initializes an action with the provided type, timestamp, contact, and context.
        :param action_type: the type of action this is
        :param timestamp: the timestamp at which this action occurred (unix epoch)
        :param contact: the contact that took this action
        :param context: a dictionary containing the context in which this action was taken, can be None
        """
        if not isinstance(action_type, ActionType):
            raise ValueError("Parameter 'action_type' is not of type ActionType.")
        self.action_type = action_type

        if not isinstance(timestamp, int):
            raise ValueError("Parameter 'timestamp' is not of type int.")
        self.timestamp = timestamp

        if not isinstance(contact, str):
            raise ValueError("Parameter 'contact' is not of type str.")
        self.contact = contact

        if context is not None and not isinstance(context, dict):
            raise ValueError("Parameter 'context' is not of type dict or None.")
        self.context = context

    def get_type(self):
        """
        Returns the type of this action.
        :return: the type of this action
        """
        return self.action_type

    def get_type_description(self):
        """
        Returns the description of the type of this action.
        :return: the description of the type of this action.
        """
        return self.action_type.value[0]

    def get_type_id(self):
        """
        Returns the id of the type of this action.
        :return: the id of the type of this action
        """
        return self.action_type.value[1]

    def get_timestamp(self):
        """
        Returns the timestamp of this action.
        :return: the timestamp of this action
        """
        return self.timestamp

    def get_contact(self):
        """
        Returns the contact of this action.
        :return: the contact of this action
        """
        return self.contact

    def get_context(self):
        """
        Returns the context of this action.
        :return: the context of this action
        """
        return self.context
