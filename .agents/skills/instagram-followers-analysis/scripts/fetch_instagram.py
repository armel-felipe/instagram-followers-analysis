#!/usr/bin/env python3
"""
Fetch Instagram followers/following lists directly (no export needed)
using Instaloader, then generate the same HTML dashboard.

Usage:
    python3 fetch_instagram.py --username YOUR_IG_USERNAME [-o output.html]
    IG_PASSWORD=xxx python3 fetch_instagram.py --username YOUR_IG_USERNAME

Session file is cached in ~/.config/instaloader/session-YOUR_IG_USERNAME
so you only enter the password once.

Requires: pip install instaloader
"""
import argparse, json, os, sys, getpass

# Make parse_instagram.py importable regardless of cwd
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

try:
    import instaloader
except ImportError:
    sys.exit("Instaloader not installed. Run: pip install instaloader")

from parse_instagram import generate_html, build_data

SESSION_DIR = os.path.join(os.path.expanduser("~"), ".config", "instaloader")


def fetch(username, password=None):
    L = instaloader.Instaloader(
        quiet=True,
        download_comments=False,
        download_geotags=False,
        download_tagged=False,
        download_pictures=False,
        download_videos=False,
        save_metadata=False,
        compress_json=False,
        post_metadata_txt_pattern="",
        max_connection_attempts=3,
    )
    os.makedirs(SESSION_DIR, exist_ok=True)
    sessionfile = os.path.join(SESSION_DIR, f"session-{username}")

    if os.path.isfile(sessionfile):
        try:
            L.load_session_from_file(username, sessionfile)
            print(f"Session loaded from {sessionfile}")
        except Exception:
            pass

    if not L.context.is_logged_in:
        if not password:
            password = os.environ.get("IG_PASSWORD") or getpass.getpass(f"Password for {username}: ")
        try:
            L.login(username, password)
        except Exception as e:
            sys.exit(f"Login failed: {e}")
        L.save_session_to_file(sessionfile)

    profile = instaloader.Profile.from_username(L.context, username)

    print(f"Fetching followers of @{username} ...")
    followers = []
    for f in profile.get_followers():
        followers.append({"username": f.username, "date": None})
    print(f"  -> {len(followers)} followers")

    print(f"Fetching following of @{username} ...")
    following = []
    for f in profile.get_followees():
        following.append({"username": f.username, "date": None})
    print(f"  -> {len(following)} following")

    L.close()
    return followers, following


def main():
    ap = argparse.ArgumentParser(description="Fetch Instagram followers/following and generate HTML dashboard")
    ap.add_argument("--username", required=True, help="Instagram username")
    ap.add_argument("-o", "--output", default="instagram_followers_following.html", help="Output HTML filename")
    args = ap.parse_args()

    followers, following = fetch(args.username)
    rows = build_data(followers, following)
    from collections import Counter
    cats = Counter()
    for r in rows:
        if r["following"] and r["follower"]:
            cats["mutual"] += 1
        elif r["following"]:
            cats["churner"] += 1
        else:
            cats["onboarding"] += 1

    data_js = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    total = len(rows)
    out = generate_html(data_js, cats, total)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(out)

    print(f"Total unique: {total} | Mutual: {cats['mutual']} | Churners: {cats['churner']} | Onboarding: {cats['onboarding']}")
    print(f"Wrote {args.output} ({len(out)} bytes)")


if __name__ == "__main__":
    main()
