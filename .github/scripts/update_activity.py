import json
import os
import re
import urllib.request

USERNAME = "UlissesCurvelloFerreira"
MAX_EVENTS = 10
README_PATH = "README.md"

# tipo do evento -> (rótulo do badge, cor "positiva")
TYPE_MAP = {
    "PushEvent": ("commit", "#1f6feb"),
    "CreateEvent": ("criação", "#2ea44f"),
    "WatchEvent": ("estrelou", "#d4a72c"),
    "ForkEvent": ("fork", "#8957e5"),
    "PullRequestEvent": ("pull request", "#1f6feb"),
    "IssuesEvent": ("issue", "#bf8700"),
    "IssueCommentEvent": ("comentário", "#bf8700"),
    "ReleaseEvent": ("release", "#2ea44f"),
    "DeleteEvent": ("remoção", "#6e7681"),
}
DEFAULT = ("atividade", "#6e7681")


def fetch_events():
    url = f"https://api.github.com/users/{USERNAME}/events/public"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {os.environ.get('GH_TOKEN', '')}",
        "Accept": "application/vnd.github+json",
        "User-Agent": USERNAME,
    })
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def build_card(event):
    etype = event.get("type", "")
    label, color = TYPE_MAP.get(etype, DEFAULT)
    text_color = "#1c1200" if etype == "WatchEvent" else "#fff"
    repo = event["repo"]["name"]
    repo_url = f"https://github.com/{repo}"
    return (
        '<div style="display:flex;align-items:center;justify-content:space-between;'
        'gap:12px;border:1px solid #30363d;border-radius:10px;padding:12px 16px;'
        'margin-bottom:10px;background:#161b22;">'
        '<div style="display:flex;align-items:center;gap:10px;">'
        f'<span style="background:{color};color:{text_color};padding:4px 10px;'
        'border-radius:20px;font-size:12px;font-weight:bold;white-space:nowrap;'
        f'min-width:150px;text-align:center;overflow:hidden;text-overflow:ellipsis;'
        f'display:inline-block;">{label}</span>'
        f'<span style="color:#c9d1d9;font-size:14px;">em '
        f'<a href="{repo_url}" style="color:#58a6ff;text-decoration:underline;">{repo}</a></span>'
        '</div>'
        f'<a href="{repo_url}"><img src="https://img.shields.io/badge/'
        'Ver_reposit%C3%B3rio-1f6feb?style=for-the-badge&logo=github&logoColor=white"/></a>'
        '</div>'
    )


def main():
    events = fetch_events()[:MAX_EVENTS]
    cards = "\n".join(build_card(e) for e in events)

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = re.sub(
        r"(<!--START_SECTION:activity-->)(.*)(<!--END_SECTION:activity-->)",
        lambda m: f"{m.group(1)}\n{cards}\n{m.group(3)}",
        content,
        flags=re.DOTALL,
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)


if __name__ == "__main__":
    main()
