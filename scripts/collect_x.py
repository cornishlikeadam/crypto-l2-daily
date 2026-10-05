#!/usr/bin/env python3
"""Collect the last 24h of X posts for the daily crypto L2 slideshow.

Source of truth is X recent search (api.x.com /2/tweets/search/recent).
Nothing here is written from memory: every item carries the handle, post url
and timestamp returned by X. A home coin with no surviving post gets a
"Quiet today." entry instead of an invented one.

Usage:
  python3 scripts/collect_x.py                 # today (America/New_York)
  python3 scripts/collect_x.py --date 2026-10-05
  python3 scripts/collect_x.py --from-raw data/raw/2026-10-05.json   # re-filter a saved pull

Two ways in, set in .env at the repo root:
  X_AUTH_TOKEN + X_CT0   free: browser session cookies of an X account, searched with
                         the open-source twikit library (run with this repo's .venv python)
  X_BEARER_TOKEN         paid: official X API v2 recent search (~$0.005 per post read)
If both are set, the free cookie route is used.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
ET = ZoneInfo("America/New_York")
SEARCH_URL = "https://api.x.com/2/tweets/search/recent"

# Home coins, their X queries, and the keywords used to label a card.
# Query operators appended to every query keep reposts, replies and promos out.
QUERY_SUFFIX = " -is:retweet -is:reply -is:nullcast lang:en"
COINS = [
    {
        "coin": "Bitcoin",
        "short": "BTC",
        "query": '(Bitcoin OR BTC) (Lightning OR Ark OR "layer 2" OR L2)',
        "topics": [("Lightning", r"\blightning\b|\bLN\b|\bLSP\b|\bBOLT\s?12\b"),
                   ("Ark", r"\bArk\b|\bArk protocol\b|\bArkade\b|\bSecond\.tech\b"),
                   ("Sidechains", r"\bsidechain|\bLiquid\b|\bRootstock\b|\bRSK\b|\bStacks\b|\bSTX\b|\bBotanix\b|\bdrivechain"),
                   ("Layer 2", r"layer[\s-]?2|\bL2s?\b")],
        "home": ["bitcoin", "lightning"],
    },
    {
        "coin": "Dogecoin",
        "short": "DOGE",
        "query": '(Dogecoin OR DOGE) ("layer 2" OR L2 OR Dogechain OR community)',
        "topics": [("Dogechain", r"\bDogechain\b"),
                   ("Layer 2", r"layer[\s-]?2|\bL2s?\b"),
                   ("Community", r"\bcommunity\b")],
        "home": ["dogecoin"],
    },
    {
        "coin": "Monero",
        "short": "XMR",
        "query": "(Monero OR XMR) (FCMP OR CARROT OR hardfork OR upgrade)",
        "topics": [("FCMP++", r"\bFCMP"),
                   ("CARROT", r"\bCARROT\b"),
                   ("Hard fork", r"hard\s?fork"),
                   ("Upgrade", r"\bupgrade")],
        "home": ["monero"],
    },
    {
        "coin": "Litecoin",
        "short": "LTC",
        "query": '(Litecoin OR LTC) (Lightning OR MWEB OR "layer 2")',
        "topics": [("MWEB", r"\bMWEB\b|mimblewimble"),
                   ("Lightning", r"\blightning\b"),
                   ("Layer 2", r"layer[\s-]?2|\bL2s?\b")],
        "home": ["litecoin"],
    },
]

# Other chains a community might actually be talking about. Name -> pattern.
OTHER_CHAINS = {
    "Bitcoin": r"\bbitcoin\b|\bBTC\b",
    "Lightning": r"\blightning network\b",
    "Dogecoin": r"\bdogecoin\b|\bDOGE\b",
    "Monero": r"\bmonero\b|\bXMR\b",
    "Litecoin": r"\blitecoin\b|\bLTC\b",
    "Ethereum": r"\bethereum\b|\bETH\b",
    "Solana": r"\bsolana\b|\bSOL\b",
    "Zcash": r"\bzcash\b|\bZEC\b",
    "Bitcoin Cash": r"\bbitcoin cash\b|\bBCH\b",
    "Kaspa": r"\bkaspa\b|\bKAS\b",
    "Stacks": r"\bstacks\b|\bSTX\b",
    "Liquid": r"\bliquid network\b|\bL-BTC\b",
    "Rootstock": r"\brootstock\b|\bRSK\b",
    "Base": r"\bon base\b|\bbase chain\b|\bcoinbase'?s base\b",
    "Arbitrum": r"\barbitrum\b",
    "Starknet": r"\bstarknet\b",
    "Tron": r"\btron\b|\bTRX\b",
    "XRP": r"\bXRP\b|\bXRPL\b",
    "Cardano": r"\bcardano\b|\bADA\b",
    "Sui": r"\bsui network\b|\b\$SUI\b",
    "TON": r"\btoncoin\b|\bTON blockchain\b",
}
OTHER_CHAIN_MIN_AUTHORS = 3   # distinct authors needed before a guest chain gets a card
OTHER_CHAIN_MIN_SHARE = 0.25  # ...and at least this share of the coin's kept posts

# Drop rules. Matching any of these removes the post.
DROP_RULES = {
    "price_call": re.compile(
        r"price target|\bPT\b|\bto the moon\b|\bmoon(ing)?\b|\bpump(ing|ed)?\b|\bdump(ing|ed)?\b|"
        r"\bbreakout\b|\bresistance\b|\bsupport (level|zone)\b|\bchart\b|\bTA\b|\bbullish\b|\bbearish\b|"
        r"\bbuy (now|the dip)\b|\bentry\b|\btake profit\b|\bstop loss\b|\bleverage\b|\b\d+x\b|"
        r"\$\s?\d|\b\d+(\.\d+)?\s?(k|K)\s+(soon|next|incoming)\b|\bATH\b|\bprice\b|"
        r"market ?cap|\bmcap\b|\bmc\b|\b(to|hit|reach|go to) (a |the )?\$?\d*\s?(billion|bill|million|mil|trillion)\b|"
        r"\b\d+x\b|\bgem\b|\bape in\b|\bnot financial advice\b|\bNFA\b|\bDYOR\b|\bpricing\b|\bnext move\b",
        re.I,
    ),
    "giveaway": re.compile(
        r"giveaway|give away|airdrop|\bto win\b|\bwin \d|\bRT\s*(&|and|\+)|retweet (and|&|to)|"
        r"follow (and|&|\+) (rt|retweet|like)|claim (your|now)|whitelist|\bfree \$?\d|presale|"
        r"\bdrop your (wallet|address)\b|tag \d+ friends|\bwin (the |some )?tokens?\b|\bprize\b",
        re.I,
    ),
    "rumor": re.compile(
        r"\brumou?r|\bunconfirmed\b|\ballegedly\b|\breportedly\b|\bhearing (that|rumors)\b|"
        r"\bsources (say|tell)\b|\bleaked (docs?|news|roadmap|plans?)\b|\bsoon™|\binsiders? (say|claim)\b|\bspeculat",
        re.I,
    ),
}
MIN_TEXT_CHARS = 40
MIN_FOLLOWERS = 500
MIN_LIKES = 5  # a card should be something at least a few people engaged with
# Bios that announce promotion. These accounts are shilling, not reporting.
SHILL_BIO = re.compile(r"shill|\bNFA\b|\bDYOR\b|not financial advice|\b100x\b|\bgems?\b|\bcalls?\b|alpha group|"
                       r"\bpromo(tion)?s?\b|\bDM for\b", re.I)
# Cashtags that are fine to mention; any other $TICKER means the post is pushing some other token.
OK_TICKERS = {"BTC", "DOGE", "XMR", "LTC", "ETH", "SOL", "ZEC", "BCH", "KAS", "STX", "RBTC", "LBTC", "ARB",
              "STRK", "TRX", "XRP", "ADA", "SUI", "TON", "USDT", "USDC", "MWEB"}
MAX_CASHTAGS = 2
MAX_ITEMS_PER_COIN = 3
MIDDLE_CARDS_MAX = 8  # cards between title and close (8-10 total)


# ---------------------------------------------------------------------------
# X API
# ---------------------------------------------------------------------------

def load_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def x_search(query: str, start_time: datetime, end_time: datetime, token: str, pages: int,
             max_results: int) -> dict:
    params = {
        "query": query + QUERY_SUFFIX,
        "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end_time": end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "max_results": str(max_results),
        "sort_order": "relevancy",
        "tweet.fields": "created_at,public_metrics,lang,author_id,note_tweet,entities",
        "expansions": "author_id",
        "user.fields": "username,name,description,public_metrics,verified",
    }
    tweets: list[dict] = []
    users: dict[str, dict] = {}
    next_token = None
    for _ in range(pages):
        if next_token:
            params["next_token"] = next_token
        url = SEARCH_URL + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}",
                                                   "User-Agent": "crypto-l2-daily/1.0"})
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    body = json.load(resp)
                break
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", "replace")[:500]
                if exc.code == 429 and attempt < 2:
                    reset = exc.headers.get("x-rate-limit-reset")
                    wait = max(5, int(reset) - int(time.time())) if reset else 60
                    print(f"[collect] 429 rate limited, waiting {min(wait, 900)}s", file=sys.stderr)
                    time.sleep(min(wait, 900))
                    continue
                raise SystemExit(f"[collect] X API error {exc.code} for query {query!r}: {detail}")
            except urllib.error.URLError as exc:
                if attempt < 2:
                    time.sleep(10)
                    continue
                raise SystemExit(f"[collect] network error reaching X API: {exc}")
        tweets.extend(body.get("data", []))
        for u in body.get("includes", {}).get("users", []):
            users[u["id"]] = u
        next_token = body.get("meta", {}).get("next_token")
        if not next_token:
            break
    return {"query": query + QUERY_SUFFIX, "tweets": tweets, "users": users}


def cookie_search_all(coins: list[dict], start_time: datetime, end_time: datetime, auth_token: str,
                      ct0: str, max_results: int) -> dict:
    """All coin queries through ONE twikit session (X's session cookies, no API key, $0).

    Returns {coin: pull} in the same shape as x_search. One shared client matters:
    a fresh client per query made X answer 404 on the second search.
    """
    import asyncio
    try:
        from twikit import Client
        from twikit.errors import Forbidden, NotFound, TooManyRequests, Unauthorized
    except ImportError:
        raise SystemExit("[collect] twikit missing. Run with the repo venv: .venv/bin/python scripts/collect_x.py")

    day_after = (end_time + timedelta(days=1)).strftime("%Y-%m-%d")
    window = (f" -filter:replies -filter:retweets -filter:nativeretweets lang:en "
              f"since:{start_time.strftime('%Y-%m-%d')} until:{day_after} "
              f"since_time:{int(start_time.timestamp())} until_time:{int(end_time.timestamp())}")

    def new_client() -> "Client":
        client = Client("en-US")
        client.set_cookies({"auth_token": auth_token, "ct0": ct0})
        return client

    async def one(client, query: str) -> dict:
        full_query = query + window
        tweets: list[dict] = []
        users: dict[str, dict] = {}
        page = await client.search_tweet(full_query, "Top", count=20)
        while page and len(tweets) < max_results:
            for t in page:
                if t.retweeted_tweet is not None or t.in_reply_to:
                    continue
                u = t.user
                users[u.id] = {"id": u.id, "username": u.screen_name, "name": u.name,
                               "description": u.description or "",
                               "public_metrics": {"followers_count": u.followers_count}}
                tweets.append({
                    "id": t.id, "author_id": u.id, "lang": t.lang,
                    "created_at": t.created_at_datetime.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                    "text": t.full_text or t.text,
                    "public_metrics": {"like_count": t.favorite_count or 0, "retweet_count": t.retweet_count or 0,
                                       "quote_count": t.quote_count or 0, "reply_count": t.reply_count or 0},
                })
                if len(tweets) >= max_results:
                    break
            if len(tweets) >= max_results or len(page) == 0:
                break
            await asyncio.sleep(2)
            try:
                page = await page.next()
            except (KeyError, IndexError, TypeError):
                break  # X sent no "next page" cursor: that's the end of the results
        return {"query": full_query, "tweets": tweets, "users": users}

    async def run() -> dict:
        client = new_client()
        pulls: dict[str, dict] = {}
        for coin_cfg in coins:
            for attempt in range(3):
                try:
                    pulls[coin_cfg["coin"]] = await one(client, coin_cfg["query"])
                    break
                except (Unauthorized, Forbidden) as exc:
                    raise SystemExit("[collect] X rejected the session cookies (logged out or expired). "
                                     "Run scripts/set_x_cookies.sh with fresh auth_token and ct0. "
                                     f"Detail: {exc}")
                except NotFound:
                    # X refused the request signature; rebuild the session and retry.
                    if attempt == 2:
                        raise SystemExit(f"[collect] X kept refusing the {coin_cfg['coin']} search (404). "
                                         "The scraper may need an update for X's latest site change.")
                    await asyncio.sleep(10)
                    client = new_client()
                except TooManyRequests:
                    if attempt == 2:
                        raise SystemExit("[collect] X rate limit hit repeatedly; giving up for today")
                    print("[collect] X rate limit hit; waiting 15 min", file=sys.stderr)
                    await asyncio.sleep(900)
            print(f"[collect] {coin_cfg['coin']}: {len(pulls[coin_cfg['coin']]['tweets'])} posts (cookies)",
                  file=sys.stderr)
            await asyncio.sleep(4)
        return pulls

    return asyncio.run(run())


# ---------------------------------------------------------------------------
# Filtering and selection
# ---------------------------------------------------------------------------

URL_RE = re.compile(r"https?://\S+")
LEADING_MENTIONS_RE = re.compile(r"^(?:@\w+\s*)+")
TRAILING_TAGS_RE = re.compile(r"(?:\s*[#$]\w+)+\s*$")
EMOJI_RE = re.compile("[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0000FE0F\U0001F1E6-\U0001F1FF]+")


def full_text(tweet: dict) -> str:
    return (tweet.get("note_tweet") or {}).get("text") or tweet.get("text", "")


def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)  # 𝑻𝒉𝒆 -> The
    text = URL_RE.sub("", text)
    text = LEADING_MENTIONS_RE.sub("", text.strip())
    text = EMOJI_RE.sub("", text)
    text = re.sub(r":[a-z0-9_]+:", "", text)  # leftover emoji shortcodes like :native:
    text = TRAILING_TAGS_RE.sub("", text)
    text = re.sub(r"\s+", " ", text).strip(" -–—:|")
    return text


def first_sentence(text: str, max_words: int = 22, prefer: str | None = None) -> str:
    """One of the post's own sentences, clipped. No rewording.

    Uses the first sentence that mentions the coin or topic (`prefer` regex), else the opening one.
    """
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", text) if p.strip()]
    if not parts:
        return ""
    sentence = parts[0]
    if prefer:
        sentence = next((p for p in parts if re.search(prefer, p, re.I) and len(p.split()) >= 5), parts[0])
    words = sentence.split()
    if len(words) > max_words:
        sentence = " ".join(words[:max_words]).rstrip(",;:") + "…"
    elif sentence and sentence[-1] not in ".!?…":
        sentence += "."
    return sentence


def drop_reason(text: str, tweet: dict, user: dict | None, window: tuple | None = None) -> str | None:
    if not user or not user.get("username"):
        return "no_handle"
    if not tweet.get("created_at"):
        return "no_date"
    if window:
        created = datetime.fromisoformat(tweet["created_at"].replace("Z", "+00:00"))
        if not (window[0] <= created <= window[1]):
            return "outside_24h_window"
    if re.search(r"government efficiency|\bD\.O\.G\.E\b", text, re.I):
        return "not_dogecoin"
    if re.search(r"\balpha drop\b|\bdaily alpha\b", text, re.I):
        return "promo_post"
    if len(clean_text(text)) < MIN_TEXT_CHARS:
        return "too_short"
    if tweet.get("public_metrics", {}).get("like_count", 0) < MIN_LIKES:
        return "under_5_likes"
    if user.get("public_metrics", {}).get("followers_count", 0) < MIN_FOLLOWERS:
        return "low_follower_account"
    tags = [t.upper() for t in re.findall(r"\$([A-Za-z]{2,10})\b", text)]
    if len(tags) > MAX_CASHTAGS:
        return "cashtag_spam"
    if any(t not in OK_TICKERS for t in tags):
        return "other_token_shill"
    bio = user.get("description") or ""
    if SHILL_BIO.search(bio) or any(t.upper() not in OK_TICKERS for t in re.findall(r"\$([A-Za-z]{2,10})\b", bio)):
        return "promo_account"
    for reason, pattern in DROP_RULES.items():
        if pattern.search(text):
            return reason
    return None


def engagement(tweet: dict) -> int:
    m = tweet.get("public_metrics", {})
    return (m.get("like_count", 0) + 2 * m.get("retweet_count", 0)
            + 2 * m.get("quote_count", 0) + m.get("reply_count", 0))


def topic_label(coin_cfg: dict, text: str) -> str:
    for label, pattern in coin_cfg["topics"]:
        if re.search(pattern, text, re.I):
            return label
    return coin_cfg["topics"][-1][0]


def why_this_account(user: dict, coin: str) -> str:
    followers = user.get("public_metrics", {}).get("followers_count", 0)
    bio = re.sub(r"\s+", " ", URL_RE.sub("", user.get("description") or "")).strip()
    if bio:
        if len(bio) > 110:
            bio = bio[:107].rsplit(" ", 1)[0] + "…"
        return f"Bio: “{bio}” · {followers:,} followers"
    return f"No bio; posting in the {coin} conversation · {followers:,} followers"


def chains_mentioned(text: str, home: list[str]) -> list[str]:
    found = []
    for name, pattern in OTHER_CHAINS.items():
        if name.lower() in home:
            continue
        if re.search(pattern, text, re.I):
            found.append(name)
    return found


def coin_pattern(coin_cfg: dict) -> str:
    names = [coin_cfg["coin"], coin_cfg["short"]] + [pat for _, pat in coin_cfg["topics"]]
    return "|".join(f"(?:{n})" for n in names)


def to_item(coin_cfg: dict, tweet: dict, user: dict, other_chain: str | None = None) -> dict:
    text = full_text(tweet)
    created = datetime.fromisoformat(tweet["created_at"].replace("Z", "+00:00"))
    handle = user["username"]
    return {
        "coin": coin_cfg["coin"],
        "topic": other_chain or topic_label(coin_cfg, text),
        "claim": first_sentence(clean_text(text), prefer=coin_pattern(coin_cfg)),
        "handle": "@" + handle,
        "display_name": user.get("name", ""),
        "why_this_account": why_this_account(user, coin_cfg["coin"]),
        "post_url": f"https://x.com/{handle}/status/{tweet['id']}",
        "date": created.isoformat().replace("+00:00", "Z"),
        "date_et": created.astimezone(ET).strftime("%b %-d, %-I:%M %p ET"),
        "engagement": engagement(tweet),
        "likes": tweet.get("public_metrics", {}).get("like_count", 0),
        "reposts": tweet.get("public_metrics", {}).get("retweet_count", 0),
        "replies": tweet.get("public_metrics", {}).get("reply_count", 0),
        "other_chain_if_any": other_chain,
        "quiet": False,
    }


def select(raw: dict) -> tuple[list[dict], dict]:
    """Return (items, stats). Items are in card order."""
    per_coin: dict[str, list[dict]] = {}
    stats: dict = {"dropped": {}, "kept": {}, "other_chains": {}}
    window = None
    if raw.get("window_start") and raw.get("window_end"):
        window = (datetime.fromisoformat(raw["window_start"].replace("Z", "+00:00")),
                  datetime.fromisoformat(raw["window_end"].replace("Z", "+00:00")))
    for coin_cfg in COINS:
        pull = raw["pulls"][coin_cfg["coin"]]
        users = pull["users"]
        kept: list[tuple[dict, dict]] = []
        drops: Counter = Counter()
        for tweet in pull["tweets"]:
            user = users.get(tweet.get("author_id", ""))
            reason = drop_reason(full_text(tweet), tweet, user, window)
            if reason:
                drops[reason] += 1
                continue
            kept.append((tweet, user))
        kept.sort(key=lambda tu: engagement(tu[0]), reverse=True)
        stats["dropped"][coin_cfg["coin"]] = dict(drops)
        stats["kept"][coin_cfg["coin"]] = len(kept)

        # Guest chain: what this community is actually posting about, if not itself.
        authors_by_chain: dict[str, set] = defaultdict(set)
        for tweet, user in kept:
            for chain in chains_mentioned(full_text(tweet), coin_cfg["home"]):
                authors_by_chain[chain].add(user["id"])
        guest = None
        if authors_by_chain:
            chain, authors = max(authors_by_chain.items(), key=lambda kv: len(kv[1]))
            if (len(authors) >= OTHER_CHAIN_MIN_AUTHORS
                    and len(authors) >= OTHER_CHAIN_MIN_SHARE * len(kept)):
                guest = chain
                stats["other_chains"][coin_cfg["coin"]] = {"chain": chain, "authors": len(authors)}

        items: list[dict] = []
        seen_authors: set = set()
        seen_claims: set = set()
        for tweet, user in kept:
            if user["id"] in seen_authors:
                continue
            text = full_text(tweet)
            mentions_guest = guest is not None and guest in chains_mentioned(text, coin_cfg["home"])
            item = to_item(coin_cfg, tweet, user, guest if mentions_guest else None)
            if len(item["claim"].split()) < 5 or not re.match(r"[A-Z0-9@$#“\"'(]", item["claim"]):
                continue  # too short, or starts mid-thought
            key = re.sub(r"[^a-z0-9]", "", item["claim"].lower())[:80]
            if key in seen_claims:
                continue  # same words already on a card (copy-paste announcements)
            seen_claims.add(key)
            seen_authors.add(user["id"])
            items.append(item)
            if len(items) >= MAX_ITEMS_PER_COIN:
                break
        # Make sure a guest chain that cleared the bar has its card.
        if guest and not any(i["other_chain_if_any"] for i in items):
            for tweet, user in kept:
                if user["id"] in seen_authors:
                    continue
                if guest in chains_mentioned(full_text(tweet), coin_cfg["home"]):
                    item = to_item(coin_cfg, tweet, user, guest)
                    if len(item["claim"].split()) >= 5:
                        items.append(item)
                        break
        per_coin[coin_cfg["coin"]] = items

    # Fit 6-8 middle cards: quiet coins take one card each; trim lowest-engagement
    # extras (never a coin's only item) until it fits. Short days stay short.
    quiet = [c["coin"] for c in COINS if not per_coin[c["coin"]]]
    def middle_count() -> int:
        return len(quiet) + sum(len(v) for v in per_coin.values())
    while middle_count() > MIDDLE_CARDS_MAX:
        candidates = [(i, coin) for coin, items in per_coin.items() if len(items) > 1
                      for i in items[1:]]
        if not candidates:
            break
        victim, coin = min(candidates, key=lambda ic: ic[0]["engagement"])
        per_coin[coin].remove(victim)

    ordered: list[dict] = []
    for coin_cfg in COINS:
        items = per_coin[coin_cfg["coin"]]
        if items:
            ordered.extend(items)
        else:
            ordered.append({
                "coin": coin_cfg["coin"],
                "topic": None,
                "claim": "Quiet today.",
                "handle": None,
                "display_name": None,
                "why_this_account": None,
                "post_url": None,
                "date": None,
                "date_et": None,
                "engagement": 0, "likes": 0, "reposts": 0, "replies": 0,
                "other_chain_if_any": None,
                "quiet": True,
            })
    return ordered, stats


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYY-MM-DD (America/New_York); default today")
    ap.add_argument("--from-raw", help="re-filter a saved raw pull instead of calling X")
    ap.add_argument("--pages", type=int, default=1, help="pages per query (default 1)")
    ap.add_argument("--backfill", action="store_true",
                    help="archive a past day: window is the 24h ending at 18:00 ET on --date")
    ap.add_argument("--max-results", type=int, default=None,
                    help="posts per query page, 10-100 (default X_MAX_RESULTS or 25). "
                         "X bills each post read, so this sets the daily cost.")
    args = ap.parse_args()

    now_et = datetime.now(ET)
    day = args.date or now_et.strftime("%Y-%m-%d")

    if args.from_raw:
        raw = json.loads(Path(args.from_raw).read_text())
    else:
        load_env()
        auth_token = os.environ.get("X_AUTH_TOKEN", "").strip()
        ct0 = os.environ.get("X_CT0", "").strip()
        token = os.environ.get("X_BEARER_TOKEN", "").strip()
        if not (auth_token and ct0) and not token:
            print("[collect] No X access configured. Put X_AUTH_TOKEN and X_CT0 (free, browser cookies) "
                  f"or X_BEARER_TOKEN (paid API) in {ROOT / '.env'} and re-run.", file=sys.stderr)
            return 2
        source = "cookies" if auth_token and ct0 else "api"
        if args.backfill:
            if not args.date:
                raise SystemExit("[collect] --backfill needs --date")
            if not (auth_token and ct0):
                raise SystemExit("[collect] --backfill needs the cookie route; the paid API only covers 7 days")
            end = datetime.strptime(args.date, "%Y-%m-%d").replace(hour=18, tzinfo=ET).astimezone(timezone.utc)
        else:
            # recent search needs end_time >= 10s in the past
            end = datetime.now(timezone.utc) - timedelta(seconds=30)
        start = end - timedelta(hours=24)
        max_results = max(10, min(100, args.max_results or int(os.environ.get("X_MAX_RESULTS", "25"))))
        raw = {"collected_at": end.isoformat(), "window_start": start.isoformat(),
               "window_end": end.isoformat(), "source": source, "backfill": bool(args.backfill), "pulls": {}}
        if source == "cookies":
            raw["pulls"] = cookie_search_all(COINS, start, end, auth_token, ct0, max_results)
        else:
            for coin_cfg in COINS:
                pull = x_search(coin_cfg["query"], start, end, token, args.pages, max_results)
                raw["pulls"][coin_cfg["coin"]] = pull
                print(f"[collect] {coin_cfg['coin']}: {len(pull['tweets'])} posts (api)", file=sys.stderr)
        reads = sum(len(p["tweets"]) for p in raw["pulls"].values())
        raw["post_reads"] = reads
        if source == "api":
            print(f"[collect] {reads} post reads billed (~${reads * 0.005:.2f} at $0.005/read)", file=sys.stderr)
        raw_dir = ROOT / "data" / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        (raw_dir / f"{day}.json").write_text(json.dumps(raw, indent=1))

    items, stats = select(raw)
    out = {
        "date": day,
        "window_start": raw.get("window_start"),
        "window_end": raw.get("window_end"),
        "source": {"cookies": "X search (twikit, session cookies)",
                   "api": "X API v2 recent search"}.get(raw.get("source", "api"), "X search"),
        "queries": {c["coin"]: raw["pulls"][c["coin"]]["query"] for c in COINS},
        "items": items,
        "stats": stats,
    }
    out_path = ROOT / "data" / f"{day}.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    real = [i for i in items if not i["quiet"]]
    print(f"[collect] wrote {out_path.relative_to(ROOT)}: {len(real)} items, "
          f"{len(items) - len(real)} quiet coins")
    return 0


if __name__ == "__main__":
    sys.exit(main())
