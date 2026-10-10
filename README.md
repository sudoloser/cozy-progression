# Cozy Progression > Discord Bot

Small Discord bot for the Cozy Progression Discord server

# Usage Guide

Run this in the `./src` directory:
```bash
python3 install -r requirements.txt
```
And then create a `.env` file in the `./src` directory with you Discord Bot Token. It should look something like this:
```txt
BOT_TOKEN=MTU...
```
And finally run it!
```
python3 main.py
```

> ![NOTE]
> The changelog command defaults to my github url. you can change that by replacing the value of `"base_url"` in `./src/cogs/utils.py`.