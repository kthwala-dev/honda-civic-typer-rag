import re

HEADER = re.compile(r"26 CIVIC HATCHBACK TYPE R-\S+\.book\s+\d+\s+ページ\s+\S+\s+\S+\s+\S+")
STRAY_TIME = re.compile(r"午後[０-９]+時[０-９]+分")


def clean(text):
    text = HEADER.sub(" ", text)
    text = STRAY_TIME.sub(" ", text)
    return re.sub(r"[ \t]+", " ", text).strip()