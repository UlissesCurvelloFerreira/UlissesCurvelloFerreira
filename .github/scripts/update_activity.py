import json
import os
import re
import urllib.parse
import urllib.request

USERNAME = "UlissesCurvelloFerreira"
MAX_EVENTS = 10
README_PATH = "README.md"

# tipo do evento -> (rótulo, cor hex sem #)
TYPE_MAP = {
    "PushEvent": ("commit", "1f6feb"),
    "CreateEvent": ("criação", "2ea44f"),
    "WatchEvent": ("estrelou", "d4a72c"),
    "ForkEvent": ("fork", "8957e5"),
    "PullRequestEvent": ("pull request", "1f6feb"),
    "IssuesEvent": ("issue", "bf8700"),
    "IssueCommentEvent": ("comentário", "bf8700"),
    "ReleaseEvent": ("release", "2ea44f"),
    "DeleteEvent": ("remoção", "6e7681"),
}
DEFAULT = ("atividade", "6e7681")


def fetch_events():
    url = f"https://api.github.com/users/{USERNAME}/events/public"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {os.environ.get('GH_TOKEN', '')}",
        "Accept": "application/vnd.github+json",
        "User-Agent": USERNAME,
    })
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def badge_url(label, color, logo=None):
    text = urllib.parse.quote(label.replace(" ", "_"))
    url = f"https://img.shields.io/badge/{text}-{color}?style=flat-square"
    if logo:
        url += f"&logo={logo}&logoColor=white"
    return url


def build_row(event):
    etype = event.get("type", "")
    label, color = TYPE_MAP.get(etype, DEFAULT)
    repo = event["repo"]["name"]
    repo_url = f"https://github.com/{repo}"

    label_badge = badge_url(label, color)
    repo_badge = badge_url("Ver repositório", "1f6feb", logo="github")

    return (
        "<tr>"
        f'<td><img src="{label_badge}"/> em {repo}</td>'
        f'<td align="right" nowrap><a href="{repo_url}"><img src="{repo_badge}"/></a></td>'
        "</tr>"
    )


def main():
    events = fetch_events()[:MAX_EVENTS]
    rows = "\n".join(build_row(e) for e in events)

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = re.sub(
        r"(<!--START_SECTION:activity-->)(.*)(<!--END_SECTION:activity-->)",
        lambda m: f"{m.group(1)}\n{rows}\n{m.group(3)}",
        content,
        flags=re.DOTALL,
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)


if __name__ == "__main__":
    main()
