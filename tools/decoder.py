## A helper to translate an edited sentence into binary, based on the encoding
import re

def decode(text):
    oxford = "1" if len(re.findall(", and", text)) >= 1 else "0"
    discourse = "1" if len(re.findall(r"\b(However|Additionally|For example|Since then|Meanwhile|Moreover|Otherwise|Later|Traditionally|For instance|Consequently|Similarly|Subsequently|Nonetheless|That is|Nationally|Previously|Eventually|Accordingly|Notably|Here|As such|Partly),\s", text)) >= 1 else "0"
    parentheses = "1" if len(re.findall(r"\(.*\)", text)) >= 1 else "0"

    return "".join([oxford, discourse, parentheses])