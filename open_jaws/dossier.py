"""
THE DOSSIER
============
Target analysis and intelligence gathering.
Before 007 acts, 007 knows.
How many promises. How many kept. The ratio.
It's always the ratio.
"""

from dataclasses import dataclass

import tweepy

from .sentinel import scan_tweet


@dataclass
class TargetIntel:
    """Everything we know about the target. It's usually damning."""
    user_id: str
    username: str
    bait_tweets: int       # Number of "Reply X" tweets found
    total_replies_sent: int  # How many times target actually replied to others
    total_tweets_checked: int
    fulfillment_rate: float  # 0.0 to 1.0 — usually 0.0

    @property
    def promises_kept_estimate(self) -> int:
        """
        Rough estimate of follow-through.
        This is generous. Reality is worse.
        """
        return round(self.bait_tweets * self.fulfillment_rate)

    @property
    def verdict(self) -> str:
        if self.fulfillment_rate >= 0.5:
            return "STOOD DOWN — target shows signs of humanity"
        if self.fulfillment_rate >= 0.2:
            return "UNDER SURVEILLANCE — borderline case"
        if self.fulfillment_rate > 0:
            return "GUILTY — token effort does not constitute compliance"
        return "GUILTY — total dereliction of duty"


def compile_dossier(
    client: tweepy.Client,
    user_id: str,
    username: str,
    max_tweets: int = 100,
) -> TargetIntel:
    """
    Investigate a target. Pull their recent tweets.
    Count the bait. Count the actual replies. Do the math.
    The math is never in their favor.
    """
    bait_count = 0
    reply_count = 0
    total_checked = 0

    resp = client.get_users_tweets(
        id=user_id,
        max_results=min(max_tweets, 100),
        tweet_fields=["in_reply_to_user_id", "referenced_tweets", "text"],
    )

    if resp and resp.data:
        for tweet in resp.data:
            total_checked += 1

            # Is this a bait tweet?
            if scan_tweet(tweet.text) is not None:
                bait_count += 1

            # Is this an actual reply to someone else?
            # (in_reply_to_user_id is set when the tweet is a reply)
            if tweet.in_reply_to_user_id and str(tweet.in_reply_to_user_id) != user_id:
                reply_count += 1

    # Fulfillment rate: ratio of actual replies to bait tweets.
    # If they posted 20 bait tweets and replied to 2 people, that's 10%.
    # If they posted 0 bait tweets, they shouldn't be here. But just in case.
    if bait_count > 0:
        rate = min(reply_count / bait_count, 1.0)
    else:
        rate = 1.0  # Benefit of the doubt. They slipped through somehow.

    return TargetIntel(
        user_id=user_id,
        username=username,
        bait_tweets=bait_count,
        total_replies_sent=reply_count,
        total_tweets_checked=total_checked,
        fulfillment_rate=rate,
    )
