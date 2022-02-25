# Autocord

Automatically send groups of messages at certain times on Discord.

## Requirements

- Python [<sup>3.10</sup>](https://www.python.org/downloads/release/python-3100/)
- Discord account, and a server for messages
- [`pm2`](https://www.npmjs.com/package/pm2) (optional)
- [Node.js](https://nodejs.org/en/download/) (if using pm2)

Only native modules are used in this project. No pip requirements necessary.

## Usage

Before doing anything you will need to create a configuration file using the following format. By default this file should be called `config.json`, but you may specify a different file name in the program's arguments.

```json
[
  {
    "id": "my-daily-messages",
    "channel": "1234567890",
    "authorization": "Bot super-secret-login-token",
    "prefix": "(This message is automated) ",
    "delay": 5.0,
    "timing": [
      "12:00",
      "16:00"
    ],
    "actions": [
      {
        "repeat": 1,
        "messages": [
          "Hello there! This message will send once..."
        ]
      },
      {
        "repeat": 5,
        "messages": [
          "But this message will be sent 5 times!"
        ]
      },
      {
        "repeat": 1,
        "messages": [
          "Message 1...",
          "Message 2...",
          "Message 3...",
          "Message 4...",
          "Message 5!"
        ]
      }
    ]
  }
]
```

Using this configuration you will see the following messages sent 5 seconds apart from each other at a random time between 12:00 (12pm) and 16:00 (4pm).

![Messages sent using the previous configuration.](https://i.imgur.com/Jp9Fghj.png)

The console will show something similar to the following.

```
C:\Autocord>py -m autocord config-test.json
[2022-02-25 12:16:04] [__main__] INFO: Started running instance 'my-daily-messages'...
[2022-02-25 12:18:27] [__main__] INFO: Waiting 1244.5 minutes before running the next instance.
```

### Standard

If you are using the standard `config.json` file you may type the following.

`py -m autocord`

To use a different file, simply add the name of the file after the command like so:

`py -m autocord another-config-file.json`

### pm2

*pm2* is a process manager built with Node that can run Javascript and Python scripts among other applications. To start using it, simply type the following commands.

```bash
npm install pm2 -g
pm2 start pm2.yml
```

## Notes

* If you are using a Discord bot account you will need to prefix your account token with **Bot** for it to work, such as in the example.
