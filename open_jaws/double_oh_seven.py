"""
DOUBLE-OH-SEVEN
================
The agent. The closer. The muter of men.

007 does not reply "BOLD."
007 does not drop a fire emoji.
007 has seen things.
007 remembers.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import tweepy

from .communique import compose_communique
from .dossier import TargetIntel, compile_dossier
from .quartermaster import MissionConfig
from .sentinel import Suspect

log = logging.getLogger("007")

MISSION_LOG = Path("dossier/mission_log.jsonl")


def _log_kill(record: dict) -> None:
    """Append to the mission log. Every operation is documented."""
    MISSION_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(MISSION_LOG, "a") as f:
        f.write(json.dumps(record) + "\n")


def execute_termination(
    client: tweepy.Client,
    config: MissionConfig,
    suspects: list[Suspect],
) -> list[dict]:
    """
    The main event.
    For each target: compile dossier, evaluate, terminate if guilty, file communique.
    Returns mission reports for all actions taken.
    """
    reports: list[dict] = []

    user_id = suspects[0].author_id
    username = suspects[0].author_username

    log.info("MISSION BRIEFING: target @%s — %d strikes", username, len(suspects))

    # Phase 1: Intelligence gathering
    intel = compile_dossier(client, user_id, username)
    log.info(
        "DOSSIER: @%s — %d bait tweets, fulfillment rate: %.1f%%",
        username, intel.bait_tweets, intel.fulfillment_rate * 100,
    )

    # Phase 2: Evaluate — even 007 has standards
    if intel.fulfillment_rate >= 0.5:
        log.info(
            "STOOD DOWN: @%s shows acceptable follow-through (%.0f%%). Spared.",
            username, intel.fulfillment_rate * 100,
        )
        report = _build_report(intel, action="SPARED", tweet_id=None)
        _log_kill(report)
        reports.append(report)
        return reports

    # Phase 3: Terminate
    if config.dry_run:
        log.info("DRY RUN: @%s would be muted. 007 stays the hand.", username)
        action = "DRY_RUN"
    else:
        try:
            client.mute(target_user_id=int(user_id))
            log.info("TERMINATED: @%s has been muted.", username)
            action = "MUTED"
        except tweepy.errors.TweepyException as e:
            log.error("MISSION FAILURE: could not mute @%s — %s", username, e)
            action = "FAILED"

    # Phase 4: File the communique
    communique_id = None
    if action == "MUTED" and config.post_kills:
        communique_id = _post_communique(client, intel)

    report = _build_report(intel, action=action, tweet_id=communique_id)
    _log_kill(report)
    reports.append(report)

    return reports


def _post_communique(client: tweepy.Client, intel: TargetIntel) -> str | None:
    """Tweet the kill confirmation. The world must know."""
    text = compose_communique(intel)
    try:
        resp = client.create_tweet(text=text)
        tweet_id = str(resp.data["id"])
        log.info("COMMUNIQUE FILED: tweet %s", tweet_id)
        return tweet_id
    except tweepy.errors.TweepyException as e:
        log.error("COMMUNIQUE FAILED: %s", e)
        return None


def _build_report(
    intel: TargetIntel,
    action: str,
    tweet_id: str | None,
) -> dict:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "target": intel.username,
        "target_id": intel.user_id,
        "offense_count": intel.bait_tweets,
        "promises_made": intel.bait_tweets,
        "promises_kept": intel.promises_kept_estimate,
        "fulfillment_rate": f"{intel.fulfillment_rate * 100:.1f}%",
        "verdict": intel.verdict,
        "action": action,
        "communique_tweet_id": tweet_id,
        "status": "NEUTRALIZED" if action == "MUTED" else action,
    }
