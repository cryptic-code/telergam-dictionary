## A Dictionary Bot for Telegram 🤖

This is just an afternoon-project born out of boredom. The code hasn't been cleaned in any way.

However, the bot is functional and can deployed to Heroku.

## Configuration

#### Procfile
```py
web: python3 bot.py
```
#### Environment Variables
Your Telegram token needs to go as an environment variable.
If running locally, place the token string in a `.env` file.
```
TOKEN=<your token goes here>
```

#### Web-Hook vs Polling
Use polling when running locally, else register a web-hook with your Heroku project's address.