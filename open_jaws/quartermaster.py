"""
QUARTERMASTER (Q)
=================
Handles credentials, configuration, and client provisioning.
Every agent needs a Q. Even the ones who don't appreciate the gadgets.

Q's current mood: annoyed that this isn't written in Rust.
"""

import os
from dataclasses import dataclass

import tweepy
from dotenv import load_dotenv


@dataclass
class MissionConfig:
    """Operational parameters for the current deployment."""
    strike_threshold: int = 3
    lookback_days: int = 7
    scan_interval_minutes: int = 30
    post_kills: bool = True
    dry_run: bool = False
    max_timeline_results: int = 200


def _bool_env(key: str, default: bool) -> bool:
    val = os.getenv(key, str(default)).lower()
    return val in ("true", "1", "yes")


def load_config() -> MissionConfig:
    """Load mission parameters from environment. Q insists on sensible defaults."""
    load_dotenv()
    return MissionConfig(
        strike_threshold=int(os.getenv("STRIKE_THRESHOLD", "3")),
        lookback_days=int(os.getenv("LOOKBACK_DAYS", "7")),
        scan_interval_minutes=int(os.getenv("SCAN_INTERVAL_MINUTES", "30")),
        post_kills=_bool_env("POST_KILLS", True),
        dry_run=_bool_env("DRY_RUN", False),
        max_timeline_results=int(os.getenv("MAX_TIMELINE_RESULTS", "200")),
    )


def arm_client() -> tweepy.Client:
    """
    Provision a fully authenticated Twitter API v2 client.
    Bearer token for reading. OAuth 1.0a User Context for writing.
    Q has tested this. Twice.
    """
    load_dotenv()

    bearer = os.getenv("TWITTER_BEARER_TOKEN")
    api_key = os.getenv("TWITTER_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_secret = os.getenv("TWITTER_ACCESS_SECRET")

    if not bearer:
        raise RuntimeError(
            "TWITTER_BEARER_TOKEN not set. "
            "Q is disappointed. See .env.example."
        )

    return tweepy.Client(
        bearer_token=bearer,
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret,
        wait_on_rate_limit=True,
    )
