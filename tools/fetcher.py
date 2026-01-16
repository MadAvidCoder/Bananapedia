## A helper to fetch the edits from wikipedia, based on a revision ID
import requests
from bs4 import BeautifulSoup
import re

def get_edit(rev):
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
    inserted_text = [ins.get_text() for ins in soup.find_all("ins", class_="diffchange diffchange-inline")]

    added_lines = soup.find_all("td", class_="diff-addedline diff-side-added")
    text_lines = [td.get_text(separator=" ", strip=True) for td in added_lines]
    text = " ".join(text_lines)
    text = re.sub(r"<ref[^>]*?>.*?</ref>", "", text, flags=re.DOTALL)
    text = re.sub(r" ,", ",", text)

    sentences = re.split(r"(?<=[.!?])\s+", text)
    changed_sentences = [s for s in sentences if any(ins in s for ins in inserted_text)][0]

    return changed_sentences