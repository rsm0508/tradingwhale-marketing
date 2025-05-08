# bots/reddit_bot.py
import praw
import os
from dotenv import load_dotenv

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD]):
    raise EnvironmentError("Missing Reddit credentials in environment variables.")

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent="tradingwhale-bot",
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD
)

def post_comment(subreddit_name, thread_id, comment_text):
    try:
        submission = reddit.submission(id=thread_id)
        submission.reply(comment_text)
    except Exception as e:
        print(f"Failed to post Reddit comment: {e}")
