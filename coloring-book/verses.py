"""Look up exact World English Bible (public domain) verse text."""
import json, re, os
HERE = os.path.dirname(__file__)
def verse(book, ch, v):
    data = json.load(open(os.path.join(HERE, "build/web", book + ".json")))
    parts = [d["value"] for d in data if d.get("chapterNumber") == ch
             and d.get("verseNumber") == v and "value" in d]
    return re.sub(r"\s+", " ", " ".join(parts)).strip()
if __name__ == "__main__":
    for ref in """genesis 1 27|psalms 139 14|jeremiah 29 11|joshua 1 9|philippians 4 13|ephesians 2 10|1samuel 16 7|isaiah 41 10|2timothy 1 7|1timothy 4 12|proverbs 3 5|psalms 118 24|matthew 19 14|isaiah 40 31|proverbs 17 17|ephesians 4 32|colossians 3 23|psalms 56 3|john 15 12|matthew 5 16|1john 3 1|zephaniah 3 17|psalms 23 1|deuteronomy 31 6|proverbs 20 11|luke 2 52|psalms 46 1|galatians 6 9|psalms 100 3|numbers 6 24|1peter 5 7|romans 8 28|psalms 121 3|matthew 10 30|psalms 34 8|john 8 12|psalms 136 1|1peter 4 10|romans 12 6|psalms 16 11""".split("|"):
        b, c, v = ref.split(); print(ref, "=>", verse(b, int(c), int(v)))
