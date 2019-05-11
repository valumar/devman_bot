# DevMan Bot Lessons Checker 

Telegram Bot for checking lesson reviews on [DevMan](https://dvmn.org/)

### How to install

For proper use you have to get DevMan account and get [DevMan API Token](https://dvmn.org/api/docs/).
Also you need to register Telegram Bot via [@BotFather](https://telegram.me/botfather) and receive TELEGRAM_TOKEN and TELEGRAM_CHAT_ID (use [@userinfobot](https://telegram.me/userinfobot) for that)
After that rename the file `.env-example` to `.env` and paste your info.

Python3 should be already installed. 
It is strictly recommended that you use [virtual environment](https://docs.python.org/3/library/venv.html) for project isolation. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:

```
pip install -r requirements.txt
```

It's also possible to deploy this Bot on Heroku: just create new app on Heroku and connect it with your GitHub repo after forking. 

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).