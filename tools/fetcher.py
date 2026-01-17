## A helper to fetch the edits from wikipedia, based on a revision ID
import requests
import re

def get_edit(rev):
    try:
        url = "https://en.wikipedia.org/w/api.php"

        agent = "BananapediaBot/1.2 (madavidcoder@hackclub.app)"
        headers = {"User-Agent": agent}

        params = {
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "rvprop": "ids|parentid",
            "revids": rev,
        }

        r = requests.get(url, params=params, headers=headers)
        pages = r.json()["query"]["pages"]
        page_id = next(iter(pages))
        revision = pages[page_id]["revisions"][0]
        parent_id = revision.get("parentid")

        diff_params = {
            "format": "json",
            "action": "compare",
            "fromrev": parent_id,
            "torev": rev,
        }
        r = requests.get(url, params=diff_params, headers=headers)
        html = r.json()["compare"]["*"]
        html = re.sub(r"\[\[[^\[\]]*?\|([^\[\]]*?)\]\]", r"\1", html)
        html = re.sub(r"\[\[([^\[\]]*?)\]\]", r"\1", html)
        html = re.sub(r"<ref[^>]*?>.*?</ref>", "", html, flags=re.DOTALL)
        html = re.sub(r"&lt;ref[^&]*?&gt;.*?&lt;\/ref&gt;", "", html, flags=re.DOTALL)
        html = re.sub(r"\s+", " ", html).strip()

        sentence = re.search(r'(?:^|[.!?]\s)([^.!?]*?<ins class="diffchange diffchange-inline">.*?<\/ins>[^.!?]*?[.!?])', html)
        sentence = sentence.group(1)
        sentence = re.sub(r"<.*?>", "", sentence).strip()

        return sentence
    except:
        return ""