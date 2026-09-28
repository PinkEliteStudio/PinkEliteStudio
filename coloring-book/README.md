# Made in His Image: Bible Truth Coloring Book (ages 5-10)

30 original designs following the seasons (winter, spring, summer, fall). Each page has:
a Bible truth in hollow letters to color, a verse from the World English Bible (public
domain, so it's free to use in a book you sell), a picture area, and lines for notes.
Every design is printed on one side only, with a blank back page.

## Files
| File | What it is |
|---|---|
| `output/interior.pdf` | KDP manuscript: 68 pages, 8.5 x 11 in, no bleed |
| `output/cover.pdf` | KDP paperback cover, full wrap: 17.403 x 11.25 in (spine 0.153 in) |
| `ART_PROMPTS.md` | Ready-to-paste prompts for all 30 pictures and the cover |
| `content.py` | Title, author name, truths, verses, scenes: edit here |

## Steps
1. Open `content.py` and change `"author": "Your Name Here"` to your pen or brand name.
2. Make each picture using its prompt in `ART_PROMPTS.md`. Check hands, feet, eyes and faces.
3. Save the images as `art/01.png` ... `art/30.png` and the color cover picture as `art/cover.png`.
4. Rebuild: `python3 build_book.py`. The script converts art to pure black & white and warns
   if an image's resolution is too low for print.
5. In KDP, upload `output/interior.pdf` as the manuscript and `output/cover.pdf` as the cover.
   KDP settings: 8.5 x 11 in, **no bleed**, black & white interior, white paper, glossy cover.
6. Answer **Yes** to KDP's AI-generated content question (images).
7. Order a printed proof copy before you publish.

If you change the page count (add or remove designs), rebuild so the cover's spine width updates.
