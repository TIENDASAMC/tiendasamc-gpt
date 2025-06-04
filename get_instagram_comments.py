import argparse
import requests


def get_instagram_business_account(page_id: str, access_token: str) -> str | None:
    """Return the instagram business account id for a given page."""
    url = f"https://graph.facebook.com/v17.0/{page_id}"
    params = {"fields": "instagram_business_account", "access_token": access_token}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    ig_account = data.get("instagram_business_account")
    if ig_account:
        return ig_account.get("id")
    return None


def fetch_latest_comments(ig_user_id: str, access_token: str, limit: int = 25) -> list[dict]:
    """Fetch comments from recent media and return them sorted by timestamp."""
    url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media"
    params = {"fields": "id,caption,timestamp", "access_token": access_token, "limit": limit}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    media_items = resp.json().get("data", [])

    comments: list[dict] = []
    for media in media_items:
        media_id = media["id"]
        comment_url = f"https://graph.facebook.com/v17.0/{media_id}/comments"
        comment_params = {
            "fields": "id,username,text,timestamp",
            "access_token": access_token,
        }
        com_resp = requests.get(comment_url, params=comment_params)
        if not com_resp.ok:
            continue
        for comment in com_resp.json().get("data", []):
            comment["media_id"] = media_id
            comments.append(comment)

    comments.sort(key=lambda c: c.get("timestamp", ""), reverse=True)
    return comments


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch latest Instagram comments via Graph API.")
    parser.add_argument("page_id", help="Facebook Page ID connected to the Instagram business account")
    parser.add_argument("access_token", help="Graph API access token")
    parser.add_argument(
        "--limit",
        type=int,
        default=25,
        help="Number of media items to retrieve comments from (default: 25)",
    )
    args = parser.parse_args()

    ig_user_id = get_instagram_business_account(args.page_id, args.access_token)
    if not ig_user_id:
        raise SystemExit(
            "Could not retrieve instagram business account. Ensure the page ID and token are valid."
        )

    comments = fetch_latest_comments(ig_user_id, args.access_token, args.limit)
    for com in comments:
        ts = com.get("timestamp")
        user = com.get("username")
        text = com.get("text")
        media_id = com.get("media_id")
        print(f"[{ts}] @{user}: {text} (media {media_id})")


if __name__ == "__main__":
    main()
