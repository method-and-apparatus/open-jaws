#!/usr/bin/env python3
"""
RUN MISSION
============
Entry point. The red button. The thing you press.

Usage:
    python run_mission.py              # Single sweep
    python run_mission.py --daemon     # Continuous operation
    python run_mission.py --dry-run    # Reconnaissance only

007 is ready. Are you?
"""

import argparse
import logging
import sys
import time

from open_jaws.quartermaster import arm_client, load_config
from open_jaws.sentinel import sweep_timeline, identify_repeat_offenders
from open_jaws.double_oh_seven import execute_termination

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("CONTROL")


def run_sweep(dry_run_override: bool | None = None) -> int:
    """
    Execute a single sweep of the timeline.
    Returns the number of targets neutralized.
    """
    config = load_config()
    if dry_run_override is not None:
        config.dry_run = dry_run_override

    client = arm_client()

    mode = "RECONNAISSANCE" if config.dry_run else "LIVE"
    log.info("SWEEP INITIATED — mode: %s, threshold: %d strikes", mode, config.strike_threshold)

    # Phase 1: Surveillance
    suspects = sweep_timeline(client, config)
    log.info("SENTINEL REPORT: %d suspect tweets identified", len(suspects))

    if not suspects:
        log.info("TIMELINE CLEAR. No engagement bait detected. Rare, but welcome.")
        return 0

    # Phase 2: Identify repeat offenders
    targets = identify_repeat_offenders(suspects, config.strike_threshold)
    log.info("REPEAT OFFENDERS: %d targets above strike threshold", len(targets))

    if not targets:
        log.info("No targets exceeded %d strikes. Watching.", config.strike_threshold)
        return 0

    # Phase 3: Execute
    kill_count = 0
    for author_id, author_suspects in targets.items():
        reports = execute_termination(client, config, author_suspects)
        for r in reports:
            if r["status"] == "NEUTRALIZED":
                kill_count += 1

    log.info("SWEEP COMPLETE — %d targets neutralized", kill_count)
    return kill_count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Open Jaws — Licensed to Unfollow",
        epilog="The timeline will be secured.",
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Run continuous sweeps at the configured interval",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Reconnaissance only — observe, don't mute",
    )
    args = parser.parse_args()

    log.info("=" * 50)
    log.info("OPEN JAWS v0.0.7 — MISSION CONTROL ONLINE")
    log.info("=" * 50)

    if args.daemon:
        config = load_config()
        interval = config.scan_interval_minutes * 60
        log.info("DAEMON MODE — sweeping every %d minutes", config.scan_interval_minutes)
        log.info("007 is on station. Ctrl+C to recall.")
        try:
            while True:
                run_sweep(dry_run_override=args.dry_run or None)
                log.info("Next sweep in %d minutes. 007 waits.", config.scan_interval_minutes)
                time.sleep(interval)
        except KeyboardInterrupt:
            log.info("MISSION RECALLED. 007 stands down.")
            sys.exit(0)
    else:
        kills = run_sweep(dry_run_override=args.dry_run or None)
        log.info("Single sweep complete. %d neutralized. Exiting.", kills)


if __name__ == "__main__":
    main()
