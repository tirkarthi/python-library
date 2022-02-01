from typing import List, Any

from .audience import (
    alias,
    amazon_channel,
    and_,
    android_channel,
    apid,
    channel,
    date_attribute,
    device_token,
    ios_channel,
    named_user,
    not_,
    number_attribute,
    open_channel,
    or_,
    segment,
    sms_id,
    sms_sender,
    subscription_list,
    static_list,
    tag,
    tag_group,
    text_attribute,
    wns,
)
from .core import CreateAndSendPush, Push, ScheduledPush, TemplatePush
from .payload import (
    actions,
    amazon,
    android,
    campaigns,
    device_types,
    email,
    in_app,
    interactive,
    ios,
    localization,
    message,
    mms,
    notification,
    open_platform,
    options,
    public_notification,
    sms,
    style,
    wearable,
    web,
    wns_payload,
)
from .schedule import (
    ScheduledList,
    best_time,
    local_scheduled_time,
    scheduled_time,
    schedule_exclusion,
    recurring_schedule,
)
from .template import Template, TemplateList, merge_data

# Common selector for audience & device_types

all_: str = "all"
"""Select all, to do a broadcast.

Used in both ``audience`` and ``device_types``.
"""


__all__: List[Any] = [
    all_,
    Push,
    ScheduledPush,
    ScheduledList,
    TemplatePush,
    Template,
    TemplateList,
    CreateAndSendPush,
    ios_channel,
    android_channel,
    amazon_channel,
    channel,
    open_channel,
    sms_id,
    sms_sender,
    device_token,
    apid,
    wns,
    tag,
    tag_group,
    alias,
    segment,
    and_,
    or_,
    not_,
    notification,
    ios,
    android,
    amazon,
    web,
    sms,
    mms,
    wns_payload,
    open_platform,
    message,
    device_types,
    options,
    actions,
    interactive,
    scheduled_time,
    local_scheduled_time,
    in_app,
    named_user,
    date_attribute,
    email,
    campaigns,
    wearable,
    style,
    public_notification,
    best_time,
    merge_data,
    text_attribute,
    number_attribute,
    static_list,
    subscription_list,
    localization,
    recurring_schedule,
    schedule_exclusion,
]
