"""
Q BRANCH
=========
Q's latest gadget: an LLM-powered engagement bait classifier.
The regex was good. This is better. Q is insufferable about it.

Uses Claude Haiku — fast, cheap, and surprisingly judgmental about
engagement farming. Like Q, but with fewer sighs.
"""

import logging
import os

log = logging.getLogger("Q_BRANCH")

_client = None


def _get_client():
    """Lazily initialize the Anthropic client. Q does not waste resources."""
    global _client
    if _client is not None:
        return _client

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    try:
        import anthropic
        _client = anthropic.Anthropic(api_key=api_key)
        log.info("Q BRANCH ONLINE — LLM classifier armed.")
        return _client
    except Exception as e:
        log.warning("Q BRANCH OFFLINE — could not initialize: %s", e)
        return None


CLASSIFIER_PROMPT = """\
You are a binary classifier. Your job: decide if this tweet is engagement bait.

Engagement bait = tweets that ask followers to perform actions (reply, comment, \
like, repost, follow, DM) in exchange for a promised reward that is almost never \
delivered. Common patterns include but are NOT limited to:

- "Reply [word] and I'll [promise]"
- "Comment [word] below and I will [promise]"
- "Like + comment + repost and I'll DM you [thing]"
- "Drop a [emoji] and I'll [promise]"
- "Follow me and reply [word] for a free [thing]"
- "Type [word] if you want [thing]"
- "Who wants [thing]? Like and repost"
- Any tweet asking for engagement in exchange for a vague promise

Be aggressive. If it smells like bait, it's bait. False positives are acceptable. \
False negatives are not.

Respond with exactly one word: YES or NO."""


def classify_tweet(text: str) -> bool | None:
    """
    Ask Claude whether this tweet is engagement bait.
    Returns True (bait), False (clean), or None (classifier unavailable).
    None means the caller should fall back to regex.
    """
    client = _get_client()
    if client is None:
        return None

    try:
        resp = client.messages.create(
            model="claude-haiku-4-20250414",
            max_tokens=4,
            system=CLASSIFIER_PROMPT,
            messages=[{"role": "user", "content": text}],
        )
        answer = resp.content[0].text.strip().upper()
        return answer == "YES"
    except Exception as e:
        log.warning("Q BRANCH MISFIRE — classification failed: %s", e)
        return None
