## A helper to fetch the edits from wikipedia, based on a revision ID
import asyncio
import httpx
import re
import time
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

class RateLimit:
    def __init__(self, interval_seconds):
        self.interval = interval_seconds
        self._lock = asyncio.Lock()
        self._last = 0.0

    async def wait(self):
        async with self._lock:
            now = time.monotonic()
            wait_for = self.interval - (now - self._last)
            if wait_for > 0:
                await asyncio.sleep(wait_for)
            self._last = time.monotonic()

WIKI_API = "https://en.wikipedia.org/w/api.php"
HEADERS = {
    "User-Agent": "BananapediaBot/1.2 (madavidcoder@hackclub.app)"
}

limiter = RateLimit(0.1)

async def fetch(client, params):
    await limiter.wait()
    r = await client.get(WIKI_API, params=params, timeout=10)

    if r.status_code == 429:
        print("Received 429; pausing for 15s")
        await asyncio.sleep(15)
        return None

    r.raise_for_status()
    return r.json()

async def get_edit(rev, client):
    try:
        params = {
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "rvprop": "ids|parentid",
            "revids": rev,
        }

        data = await fetch(client, params)

        pages = data["query"]["pages"]
        page_id = next(iter(pages))
        revision = pages[page_id]["revisions"][0]
        parent_id = revision.get("parentid")

        if not parent_id:
            return ""

        diff_params = {
            "format": "json",
            "action": "compare",
            "fromrev": parent_id,
            "torev": rev,
        }
        diff = await fetch(client, diff_params)

        html = diff["compare"]["*"]
        html = re.sub(r"\[\[[^\[\]]*?\|([^\[\]]*?)\]\]", r"\1", html)
        html = re.sub(r"\[\[([^\[\]]*?)\]\]", r"\1", html)
        html = re.sub(r"<ref[^>]*?>.*?</ref>", "", html, flags=re.DOTALL)
        html = re.sub(r"{{.*?}}", "", html, flags=re.DOTALL)
        html = re.sub(r"\s+", " ", html).strip()

        sentence = re.search(r'(?:^|[.!?]\s?)([^.!?]*?<ins class="diffchange diffchange-inline">.*?<\/ins>[^.!?]*?[.!?])', html)

        if sentence:
            sentence = sentence.group(1)
            sentence = re.sub(r"<.*?>", "", sentence).strip()
            sentence = re.sub(r"\s+", " ", sentence).strip()
            return sentence
        else:
            sentence = re.search(r'(?:^|[.!?]\s?)([^.!?]*?<del class="diffchange diffchange-inline">.*?<\/del>[^.!?]*?[.!?])', html)
            sentence = sentence.group(1)
            sentence = re.sub(r'<del.*<\/del>', "", sentence).strip()
            sentence = re.sub(r"<.*?>", "", sentence).strip()
            sentence = re.sub(r"\s+", " ", sentence).strip()
        return sentence
    except:
        return ""

async def get_async_sentences(revs):
    async with httpx.AsyncClient(headers=HEADERS) as client:
        results = []
        with Progress(
            SpinnerColumn(),
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn()
        ) as progress:
            task = progress.add_task("Fetching edits...", total=len(revs))
            for rev in revs:
                res = await get_edit(rev, client)
                results.append(res)
                progress.advance(task)
        return results

def get_sentences(revs):
    return asyncio.run(get_async_sentences(revs))