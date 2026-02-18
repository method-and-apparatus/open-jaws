# OPEN JAWS

**Licensed to Unfollow.**

> *"The name is Agent. Subagent."*

An autonomous Twitter/X agent that identifies engagement-bait accounts -- the ones who tweet "Reply BOLD and I'll review your startup" then review absolutely nothing -- and terminates them with extreme prejudice.

By which we mean it mutes them. Then tweets about it.

---

## THREAT ASSESSMENT

Your timeline is under attack. The enemy doesn't use malware or zero-days. They use something far more insidious:

**"Reply [WORD] and I'll [THING]"**

They won't do the thing. They never do the thing. You know this. I know this. And yet 400 people reply "BOLD" every single time, and the algorithm rewards the engagement, and your feed becomes a wasteland of broken promises and growth-hacking sociopathy.

This ends now.

---

## HOW IT WORKS

Open Jaws deploys two agents:

### Q Branch (intelligence)

The Sentinel's new toy. An LLM classifier (Claude Haiku) that reads every tweet and asks one question: *is this engagement bait?* Catches the creative ones that regex can't — the multi-action requests, the conditional follows, the "like + comment + repost and I'll DM you" mutations. Biased toward flagging. False positives are acceptable. False negatives are not.

Set `ANTHROPIC_API_KEY` in `.env` to activate. Without it, the Sentinel falls back to regex. Which still works. Q is just disappointed in you.

### The Sentinel (surveillance)

Monitors your timeline for the pattern. Regex-based detection (now the fallback) with variant matching for the creative ones who think writing "Drop a fire emoji and I'll..." makes it different. It doesn't.

Detection covers:
- `Reply [X] and I'll [Y]`
- `Comment [X] and I will [Y]`
- `Drop a [X] and I'll [Y]`
- `Type [X] below and I'll [Y]`
- And 14 other mutations of the same grift

### 007 (wetwork)

When the Sentinel flags a repeat offender (configurable threshold, default: 3 strikes in 7 days), 007 is activated.

007's mission:

1. **Compile the dossier** -- Scan the target's recent tweet history. Count the promises. Count the deliveries. Calculate the ratio. It's always the ratio.
2. **Terminate** -- Mute the account. Not block. Block implies respect. Block implies they mattered enough to cut off. Mute is the quiet room. Mute is the void. Mute is 007 walking away from the explosion without looking back.
3. **File the communique** -- Tweet the kill confirmation. Every. Single. Time.

### The Communique

Every kill generates a tweet. The world must know.

Examples from the field:

> NEUTRALIZED: @growth_guru_97 promised to "review your landing page" 23 times this month. Actual reviews delivered: 0. Account muted. The timeline is secure.

> TARGET DOWN: @hustleceo asked followers to "Reply ALPHA" 14 times in 7 days. Reply rate to respondents: 0%. Subject has been muted with extreme prejudice. Carry on.

> CONFIRMED KILL: @10x_mentor_ai offered to "rate your profile" if you commented a flag emoji. 312 people commented. 0 profiles rated. We don't negotiate with engagement farmers. Muted.

---

## QUARTERMASTER'S KIT

### Requirements

- Python 3.10+
- A Twitter/X API developer account (Bearer Token + OAuth 1.0a for posting)
- An Anthropic API key (optional — enables LLM-powered detection via Q Branch)
- A deep, abiding hatred of engagement farming

### Installation

```bash
git clone https://github.com/method-and-apparatus/open-jaws.git
cd open-jaws
pip install -r requirements.txt
cp .env.example .env
# Fill in your API credentials. Q has prepared the template.
```

---

## MISSION PARAMETERS

Edit `.env` to configure the operation:

```env
# Strike threshold — offenses before termination
STRIKE_THRESHOLD=3

# Rolling window for counting strikes (days)
LOOKBACK_DAYS=7

# How often Sentinel sweeps the timeline (minutes)
SCAN_INTERVAL_MINUTES=30

# Post kill confirmations to your timeline
POST_KILLS=true

# Reconnaissance only — observe, don't mute
DRY_RUN=false
```

`STRIKE_THRESHOLD=1` — License to kill on sight.
`STRIKE_THRESHOLD=10` — Diplomatic immunity. For now.

---

## DEPLOYMENT

### Single sweep

```bash
python run_mission.py
```

### Continuous operation

```bash
python run_mission.py --daemon
```

### Dry run (reconnaissance only)

```bash
python run_mission.py --dry-run
```

007 will identify all targets but take no action. For when you want to count the bodies without pulling the trigger.

---

## THE KILL FEED

All operations are logged to `dossier/mission_log.jsonl`:

```json
{
  "timestamp": "2026-02-11T09:14:33Z",
  "target": "crypto_alpha_mike",
  "target_id": "1234567890",
  "offense_count": 7,
  "promises_made": 34,
  "promises_kept": 1,
  "fulfillment_rate": "2.9%",
  "action": "MUTED",
  "communique_tweet_id": "1889012345678901234",
  "status": "NEUTRALIZED"
}
```

---

## Q BRANCH (Contributing)

PRs welcome. Especially from Q, who is already working on a complete rewrite in Rust because "Python is not befitting an agent of the Crown."

The Rust rewrite will be 47x faster at muting people. The muting will happen at compile time. The borrow checker will ensure we never accidentally unmute a target. Q is very excited about this. Nobody else is.

### Contributing guidelines

1. Fork the repo
2. Create a branch (`git checkout -b mission/your-feature`)
3. Commit with an appropriate message (`git commit -m "DEBRIEF: added support for LinkedIn engagement farmers"`)
4. Push and open a PR
5. Wait for 007's code review. 007 is thorough.

---

## KNOWN TARGETS

*This section is automatically updated by the kill feed.*

*Last sweep: `--:--`*

| Handle | Promises | Delivered | Rate | Status |
|--------|----------|-----------|------|--------|
| *Awaiting first deployment* | | | | |

---

## FAQ

**Isn't this mean?**
We're muting spam accounts. The single most nonviolent action available on the platform. 007 is, by spy standards, a pacifist.

**What if someone actually follows through?**
Then they won't hit the strike threshold. The dossier checks delivery rate. If you actually reply to people, 007 respects you. 007 might even follow you.

**Will this get my account banned?**
Muting is not a TOS violation. Tweeting about muting is not a TOS violation. Being funny about muting is not a TOS violation. Yet.

**What counts as "following through"?**
007 checks whether the target actually replied to people who responded to their "Reply X" tweets. Saying "great question, DM me" does not count. That's just a second trap.

**Can I add my own detection patterns?**
Yes. Edit the patterns in `open_jaws/sentinel.py`. The engagement farmers are evolving. So must we.

---

## LICENSE

MIT. See [LICENSE](LICENSE).

Or as we call it around here: **License to Kill.**

---

*Open Jaws is a [Method & Apparatus](https://github.com/method-and-apparatus) production.*

*No engagement farmers were harmed in the making of this agent. They were muted. Which is worse.*
