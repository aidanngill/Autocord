from typing import List, Optional, Tuple, TypedDict


class Action(TypedDict):
    # How many times to repeat the given messages.
    repeat: Optional[int]

    # List of messages to send.
    messages: List[str]


class Instance(TypedDict):
    # Used to keep track of when this instance was run. If one is not provided,
    # then we generate one based on the MD5 hash of the dictionary, and place
    # it back into the configuration file.
    id: Optional[str]

    # Channel to send the messages to.
    channel: str

    # Discord token to use for sending messages.
    authorization: str

    # Text to prefix each message with, typically a bot's command prefix.
    prefix: Optional[str]

    # Minimum delay between messages, not accounting for request duration.
    delay: float

    # Start and end of the period in which the instance could be started, in
    # either the format `HH`, `HH:MM`, or `HH:MM:SS` in 24 hour time.
    timing: Tuple[str, str]

    # List of messages to send, and how many times to repeat over them.
    actions: List[Action]
