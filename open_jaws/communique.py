"""
THE COMMUNIQUE
===============
Kill tweet composition. Every termination deserves an announcement.
The public has a right to know. The algorithm must be fed.
It is, after all, what the target would have wanted.
"""

import random

from .dossier import TargetIntel

# ---------------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------------
# Each template receives the TargetIntel as format kwargs.
# Variety is the spice of psychological warfare.
# ---------------------------------------------------------------

KILL_TEMPLATES = [
    (
        "NEUTRALIZED: @{username} promised to answer everyone who "
        'replied to their tweets. Promises made: {bait_tweets}. '
        "Promises kept: {kept}. "
        "Account muted. The timeline is secure."
    ),
    (
        "TARGET DOWN: @{username} issued {bait_tweets} "
        '"Reply X and I\'ll Y" directives in the last week. '
        "Actual follow-through rate: {rate_pct}%. "
        "Muted with extreme prejudice. Carry on."
    ),
    (
        "CONFIRMED KILL: @{username} — {bait_tweets} engagement-bait tweets. "
        "{kept} actual replies to respondents. "
        "That's a {rate_pct}% fulfillment rate. "
        "We don't negotiate with engagement farmers. Muted."
    ),
    (
        "MISSION COMPLETE: @{username} asked followers to reply "
        "{bait_tweets} times. Replied back {kept} times. "
        "The silence has been made permanent. Muted."
    ),
    (
        "DISPATCH: @{username} has been retired from active duty "
        "on this timeline. {bait_tweets} promises. {kept} deliveries. "
        "The ratio speaks for itself. Muted."
    ),
    (
        "INCIDENT REPORT: @{username} — "
        "engagement bait detected {bait_tweets} times. "
        "Response rate to actual humans: {rate_pct}%. "
        "Subject has been muted in the interest of timeline security."
    ),
]

# Closer lines. Because every communique needs a sign-off.
CLOSERS = [
    "\n\n-- 007, Open Jaws",
    "\n\n-- Agent on duty, Open Jaws",
    "\n\nThis has been an Open Jaws communique.",
    "\n\ngithub.com/method-and-apparatus/open-jaws",
]


def compose_communique(intel: TargetIntel) -> str:
    """
    Draft the kill tweet. 007 has many ways to say the same thing.
    All of them are accurate. Most of them are funny.
    """
    template = random.choice(KILL_TEMPLATES)
    closer = random.choice(CLOSERS)

    kept = intel.promises_kept_estimate
    rate_pct = f"{intel.fulfillment_rate * 100:.0f}"

    body = template.format(
        username=intel.username,
        bait_tweets=intel.bait_tweets,
        kept=kept,
        rate_pct=rate_pct,
    )

    full = body + closer

    # Twitter limit is 280 chars. Trim closer if needed.
    if len(full) > 280:
        full = body[:277] + "..."

    return full
