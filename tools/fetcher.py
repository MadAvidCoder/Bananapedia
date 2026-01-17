## A helper to fetch the edits from wikipedia, based on a revision ID
import requests
from bs4 import BeautifulSoup
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

        soup = BeautifulSoup(html, "html.parser")
        inserted_text = soup.find_all("ins", class_="diffchange diffchange-inline")

        sentences = []
        for tag in inserted_text:
            text = tag.get_text(separator=" ", strip=True)
            parent_text = tag.parent.get_text(separator=" ", strip=True)
            parent_text = re.sub(r"<ref[^>]*?>.*?</ref>", "", parent_text, flags=re.DOTALL)
            parent_text = re.sub(r"\[\[.*?\|(.*?)\]\]", r"\1", parent_text)
            parent_text = re.sub(r"\[\[(.*?)\]\]", r"\1", parent_text)
            parent_sentences = re.split(r"(?<=[.!?])\s+", parent_text)
            for s in parent_sentences:
                if text in s:
                    sentences.append(s)

        return sentences[0] if sentences else ""
    except:
        return ""