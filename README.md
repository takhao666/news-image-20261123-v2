# 23 November 2026 — The World in One Image

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/news-image-20261123)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)

Entry for the [make.fun bounty **news-image-20261123**](https://make.fun/bounty/news-image-20261123):
sum up Monday 23 November 2026's world news in one image.

## What it is

A newspaper front page, drawn programmatically with Pillow (`render.py`),
showing the day's most consequential stories across regions and fields:

| Story | What the image says |
|---|---|
| **COP31 collapses** (lead) | Nearly 200 nations leave Antalya with no climate pact; fossil-fuel wording blocked the deal; longest COP on record. UN chief: "deeply disappointed". |
| **Tankers hit in Hormuz** | At least three tankers struck by projectiles; two more hit mines; the Iran–US war at sea escalates. |
| **War spills over** | Russian drone hits flats near Kyiv — 14 missing, 3 dead; Russian ships hit off Finland and in Libya. |
| **Indonesia factory fire** | 3 dead in a blaze at a candy factory in Banten; rescuers search for about 36 workers. |
| **"El Chapo Isidro" captured** | FBI most-wanted cartel boss seized in Sinaloa; 11 killed in the firefight. |
| **South Korea minister quits** | Education chief resigns after 111 device cases in the Suneung entrance exam. |
| **Nepal PM meets Modi today** | Balendra Shah's first Delhi visit: energy, rail and trade talks. |
| **Also** (ticker) | BepiColombo reaches Mercury; Peru 6.7 quake kills 1; Nigeria boat sinks, 24 dead. |

## Verification

Every item was checked against at least two independent reports dated
22–23 Nov 2026 before it was drawn: UN News and Reuters/CNN (COP31);
CNN, IRNA and Al Jazeera (Hormuz); Reuters, AP, Al Jazeera and CNN
(Dymer, Sparta II, Benghazi); AP, Al Jazeera and CNA (Indonesia fire);
AP and The Japan Times (Mexico capture); Yonhap and CNA (South Korea);
The Hindu and Times of India (Nepal–India talks); ESA, AP (ticker items).
Events that happened on 20–22 Nov are shown as the stories dominating
the 23 Nov front pages, not misdated to Monday; the one event scheduled
for the day itself — the Nepal–India talks — is labelled "TODAY".

## How it runs

`main.py` (Python 3.13, standard library only) copies the shipped
`entry.png` to the output directory — no network, no randomness:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

The grader runs it with no `MAKEFUN_OUTPUT_DIR`, so it writes
`/output/entry.png`. Two runs write byte-identical files
(verified: same SHA-256, 1024×1024 PNG, under 1 MiB).

`render.py` is the Pillow program that drew `entry.png`; it is kept in
the repository so the image can be regenerated and inspected.
