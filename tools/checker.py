from fetcher import get_edit
from decoder import decode
import json
from rich.console import Console
from rich.progress import (
    Progress,
    BarColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    SpinnerColumn,
    TextColumn,
)

console = Console()

with open("../encoded.json", "r") as f:
    data = json.load(f)

bitstream = data['bitstream']
chunks = [bitstream[i:i+3] for i in range(0, len(bitstream), 3)]

with open("../revisions.txt", "r") as f:
    revisions = [s.rstrip() for s in f.readlines()]

progress_bar = Progress(
    SpinnerColumn(),
    TextColumn("[bold cyan]Decoding revisions"),
    BarColumn(bar_width=None),
    TextColumn("{task.completed}/{task.total}"),
    TimeElapsedColumn(),
    TimeRemainingColumn(),
    console=console,
)

fails = 0

with progress_bar:
    task = progress_bar.add_task("decode", total=len(revisions))
    for i, revision in enumerate(revisions):
        decoded = decode(get_edit(revision))
        original = chunks[i]
        if original != decoded:
            fails += 1
            console.print(f"[bold][red] FAIL[/red][/bold]: [italic][cyan]line {i+1}[/cyan][/italic]: [white]{original} != {decoded}[/white]")
        progress_bar.advance(task)
        progress_bar.update(task, description=f"[bold cyan]Decoding (fails={fails})")