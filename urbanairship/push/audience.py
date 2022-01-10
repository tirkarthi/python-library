import datetime
import re
import sys
import warnings

DEVICE_TOKEN_FORMAT = re.compile(r"^[0-9a-fA-F]{64}$")
UUID_FORMAT = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}" r"-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)
SMS_SENDER_FORMAT = re.compile(r"^[0-9]*$")
SMS_MSISDN_FORMAT = re.compile(r"^[0-9]*$")

# Python coarse version differentiation
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

# Set version string type
if PY3:
    string_type = str
elif PY2:
    string_type = basestring

# Value selectors; device IDs, aliases, tags, etc.
def ios_channel(uuid):
    """Select a single iOS Channel"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError("Invalid iOS Channel")
    return {"ios_channel": uuid.lower().strip()}


def android_channel(uuid):
    """Select a single Android Channel"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError("Invalid Android Channel")
    return {"android_channel": uuid.lower().strip()}


def amazon_channel(uuid):
    """Select a single Amazon Channel"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError("Invalid Amazon Channel")
    return {"amazon_channel": uuid.lower().strip()}


def device_token(token):
    """Select a single iOS device token"""
    # Ensure the device token is valid
    if not DEVICE_TOKEN_FORMAT.match(token):
        raise ValueError("Invalid device token")
    return {"device_token": token.upper().strip()}


def apid(uuid):
    """Select a single Android APID"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError("Invalid APID")
    return {"apid": uuid.lower().strip()}


def channel(uuid):
    """Select a single channel.
    This selector may be used for any channel_id, regardless of device type"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError("Invalid Channel")
    return {"channel": uuid.lower().strip()}


def open_channel(uuid):
    """Select a single Open Channel"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError("Invalid Open Channel")
    return {"open_channel": uuid.lower().strip()}


def sms_sender(sender):
    """Select an SMS Sender"""
    if not (isinstance(sender, string_type) or SMS_SENDER_FORMAT.match(sender)):
        raise ValueError("sms_sender value must be a numeric string.")
    return {"sms_sender": sender}


def sms_id(msisdn, sender):
    """Select an SMS MSISDN"""
    if not (isinstance(msisdn, string_type) or SMS_MSISDN_FORMAT.match(msisdn)):
        raise ValueError("msisdn value must be a numeric string.")
    if not (isinstance(sender, string_type) or SMS_SENDER_FORMAT.match(sender)):
        raise ValueError("sender value must be a numeric string.")
    return {"sms_id": {"sender": sender, "msisdn": msisdn}}


def wns(uuid):
    """Select a single Windows 8 APID"""
    if not UUID_FORMAT.match(uuid):
        raise ValueError("Invalid wns")
    return {"wns": uuid.lower().strip()}


def tag(tag):
    """Select a single device tag."""
    return {"tag": tag}


def tag_group(tag_group, tag):
    """Select a tag group and a tag."""
    payload = {"group": tag_group, "tag": tag}
    return payload


def alias(alias):
    """Select a single alias."""
    return {"alias": alias}


def segment(segment):
    """Select a single segment."""
    return {"segment": segment}


def named_user(name):
    """Select a Named User ID"""
    return {"named_user": name}


def subscription_list(list_id):
    """Select a subscription list"""
    return {"subscription_lists": list_id}


def static_list(list_id):
    """Select a static list"""
    return {"static_list": list_id}


# Attribute selectors
def date_attribute(attribute, operator, precision=None, value=None):
    """
    Select an audience to send to based on an attribute object with a DATE schema type,
    including predefined and device attributes.
    Please refer to https://docs.airship.com/api/ua/?http#schemas-dateattribute for
    more information about using this selector, including information about required
    data formatting for values.
    Custom attributes must be defined in the Airship UI prior to use.
    """
    if operator not in ["is_empty", "before", "after", "range", "equals"]:
        raise ValueError(
            "operator must be one of: 'is_empty', 'before', 'after', 'range', 'equals'"
        )

    selector = {"attribute": attribute, "operator": operator}

    if operator == "range":
        if value is None:
            raise ValueError(
                "value must be included when using the '{0}' operator".format(operator)
            )

        selector["value"] = value

    if operator in ["before", "after", "equals"]:
        if value is None:
            raise ValueError(
                "value must be included when using the '{0}' operator".format(operator)
            )
        if precision is None:
            raise ValueError(
                "precision must be included when using the '{0}' operator".format(
                    operator
                )
            )

        selector["value"] = value
        selector["precision"] = precision

    return selector


def text_attribute(attribute, operator, value):
    """
    Select an audience to send to based on an attribute object with a TEXT schema type,
    including predefined and device attributes.

    Please refer to https://docs.airship.com/api/ua/?http#schemas-textattribute for
    more information about using this selector, including information about required
    data formatting for values.

    Custom attributes must be defined in the Airship UI prior to use.
    """
    if operator not in ["equals", "contains", "less", "greater", "is_empty"]:
        raise ValueError(
            "operator must be one of 'equals', 'contains', 'less', 'greater', 'is_empty'"
        )

    if type(value) is not str:
        raise ValueError("value must be a string")

    return {"attribute": attribute, "operator": operator, "value": value}


def number_attribute(attribute, operator, value):
    """
    Select an audience to send to based on an attribute object with a INTEGER schema
    type, including predefined and device attributes.

    Please refer to https://docs.airship.com/api/ua/?http#schemas-numberattribute for
    more information about using this selector, including information about required
    data formatting for values.

    Custom attributes must be defined in the Airship UI prior to use.
    """
    if operator not in ["equals", "contains", "less", "greater", "is_empty"]:
        raise ValueError(
            "operator must be one of 'equals', 'contains', 'less', 'greater', 'is_empty'"
        )

    if type(value) is not int:
        raise ValueError("value must be an integer")

    return {"attribute": attribute, "operator": operator, "value": value}


# Compound selectors
def or_(*children):
    """Select devices that match at least one of the given selectors.

    >>> or_(tag('sports'), tag('business'))
    {'or': [{'tag': 'sports'}, {'tag': 'business'}]}

    """
    return {"or": [child for child in children]}


def and_(*children):
    """Select devices that match all of the given selectors.

    >>> and_(tag('sports'), tag('business'))
    {'and': [{'tag': 'sports'}, {'tag': 'business'}]}

    """
    return {"and": [child for child in children]}


def not_(child):
    """Select devices that does not match the given selectors.

    >>> not_(and_(tag('sports'), tag('business')))
    {'not': {'and': [{'tag': 'sports'}, {'tag': 'business'}]}}

    """
    return {"not": child}
