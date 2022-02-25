import json
import time
from urllib.request import Request, urlopen


def send_message(
    content: str, channel_id: str, authorization: str, with_typing: bool = True
) -> None:
    """Send a message on Discord to the given channel."""
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json",
        "User-Agent": "Autocord/1.0" if authorization.startswith("Bot ") else "Mozilla/5.0",
    }

    if with_typing:
        req = Request(
            f"https://discord.com/api/v9/channels/{channel_id}/typing",
            method="POST",
            headers=headers,
        )

        urlopen(req)

        # Emulate a person typing at 60 WPM.
        time.sleep(len(content) / 10)

    data = {"content": content}

    req = Request(
        f"https://discord.com/api/v9/channels/{channel_id}/messages",
        data=json.dumps(data).encode("utf-8"),
        method="POST",
        headers=headers,
    )

    urlopen(req)
