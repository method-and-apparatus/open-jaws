"""
THE SENTINEL
=============
Feed surveillance. Pattern detection. Early warning.
The Sentinel sees everything. The Sentinel judges silently.
The Sentinel passes targets to 007.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

import tweepy

from .quartermaster import MissionConfig

# ---------------------------------------------------------------
# THE PATTERNS
# ---------------------------------------------------------------
# Every mutation of "Reply X and I'll Y" that the engagement
# farmers have invented. They think they're clever. They aren't.
# ---------------------------------------------------------------

BAIT_PATTERNS = [
    # Core pattern: Reply/Comment/Drop/Type [X] and I'll/I will [Y]
    re.compile(
        r"(?:reply|comment|drop|type|send|post|put|write|leave)"
        r"[\s:]+(?:with\s+)?"
        r"(?:[\"'\u201c\u201d]?.{1,30}[\"'\u201c\u201d]?|(?:a\s+)?\S+(?:\s+emoji)?)"
        r"\s+(?:and|&|,)\s+"
        r"I(?:'ll|\s+will)\s+",
        re.IGNORECASE,
    ),
    # "Want me to [Y]? Reply [X]" (inverted form)
    re.compile(
        r"want\s+me\s+to\s+.{5,50}\?\s*"
        r"(?:reply|comment|drop|type)",
        re.IGNORECASE,
    ),
    # "I'll [Y] everyone who replies [X]"
    re.compile(
        r"I(?:'ll|\s+will)\s+\w+\s+(?:everyone|every\s+person|anybody|anyone)"
        r"\s+who\s+(?:replies|comments|drops|types)",
        re.IGNORECASE,
    ),
    # "[Y] for everyone who [replies X]"
    re.compile(
        r"(?:free|honest)\s+\w+\s+for\s+(?:everyone|anyone|anybody)"
        r"\s+who\s+(?:replies|comments|drops|types)",
        re.IGNORECASE,
    ),
]


@dataclass
class Suspect:
    """A flagged tweet and its author. Innocent until proven guilty. Briefly."""
    author_id: str
    author_username: str
    tweet_id: str
    tweet_text: str
    detected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    pattern_index: int = 0


def scan_tweet(text: str) -> int | None:
    """
    Check a single tweet against all known bait patterns.
    Returns the pattern index if matched, None if clean.
    """
    for i, pattern in enumerate(BAIT_PATTERNS):
        if pattern.search(text):
            return i
    return None


def sweep_timeline(
    client: tweepy.Client,
    config: MissionConfig,
) -> list[Suspect]:
    """
    Sweep the authenticated user's home timeline.
    Flag anything that matches the bait patterns.
    The Sentinel does not look away.
    """
    suspects: list[Suspect] = []

    since = datetime.now(timezone.utc) - timedelta(days=config.lookback_days)

    # Reverse chronological timeline via v2
    resp = client.get_home_timeline(
        max_results=min(config.max_timeline_results, 100),
        tweet_fields=["author_id", "created_at", "text", "conversation_id"],
        user_fields=["username"],
        expansions=["author_id"],
        start_time=since,
    )

    if not resp or not resp.data:
        return suspects

    # Build author lookup from includes
    users_by_id: dict[str, str] = {}
    if resp.includes and "users" in resp.includes:
        for user in resp.includes["users"]:
            users_by_id[str(user.id)] = user.username

    for tweet in resp.data:
        pattern_idx = scan_tweet(tweet.text)
        if pattern_idx is not None:
            author_id = str(tweet.author_id)
            suspects.append(Suspect(
                author_id=author_id,
                author_username=users_by_id.get(author_id, "unknown"),
                tweet_id=str(tweet.id),
                tweet_text=tweet.text,
                pattern_index=pattern_idx,
            ))

    return suspects


def identify_repeat_offenders(
    suspects: list[Suspect],
    threshold: int,
) -> dict[str, list[Suspect]]:
    """
    Group suspects by author. Return only those who crossed the strike threshold.
    Three strikes. That's the deal. Unless you set it to one. Then one strike.
    """
    by_author: dict[str, list[Suspect]] = {}
    for s in suspects:
        by_author.setdefault(s.author_id, []).append(s)

    return {
        author_id: tweets
        for author_id, tweets in by_author.items()
        if len(tweets) >= threshold
    }
