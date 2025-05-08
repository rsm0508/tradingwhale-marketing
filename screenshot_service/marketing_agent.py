# screenshot_service/marketing_agent.py

import os
import openai

def generate_blurb(symbol: str, interval: str, signal_type: str = "buy") -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        return "[Error: OPENAI_API_KEY not set]"
    prompt = f"""
    You're a trading expert writing promotional content.
    A new {signal_type.upper()} signal just triggered for {symbol} on the {interval} chart.
    Create a short, punchy 280-character blurb for Twitter or Telegram to convert viewers into users.
    Mention: TradingWhale.io and urgency to check it out.
    Denylist words: guarantee, risk-free, 100%.
    """
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error generating blurb: {str(e)}]"

def generate_caption(symbol: str, interval: str, signal_type: str = "buy") -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        return "[Error: OPENAI_API_KEY not set]"
    prompt = f"""You're a trading influencer. A {signal_type.upper()} signal just triggered for {symbol} on the {interval} chart. \
Write a 1-sentence call-to-action to attract engagement. Mention TradingWhale.io."""
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error generating caption: {str(e)}]"
