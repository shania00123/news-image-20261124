# Tuesday 24 November 2026 — The World in One Day

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/shania00123/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/shania00123/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A front page summing up the world's news of **Tuesday 24 November 2026** in one
1024×1024 image: 35 stories across 6 regions, every one verified against
reporting from that day. A morning edition — built from news verifiable
before 09:00 WIB, so the day's later stories are for the evening edition.

## What happened that day

- **Ulleung Island:** Russian warplanes enter South Korea's air-defence zone;
  Seoul issues an evacuation alert, lifted three minutes later, jets scrambled.
- **Huang is back:** Nvidia reinstates Jensen Huang as chief after Trump
  intervenes; Asian markets roar — Kospi up as much as 6.3%, Nikkei up 3%.
- **Space threat:** allies warn Russia may launch a nuclear-armed satellite as
  soon as next month; NATO vows space defence.
- Plus: hacked data puts Russia's war dead near 500,000, Trump offers the
  Philippines $2.4bn, Mexico nabs 'Chapo Isidro' with a US drone overhead,
  the GTA VI hacker gets 7 years, and Gukesh opens his world chess defence.

Stories first reported on an earlier day — the Estonia warning, the Libya
warship sinking, the India–NZ Test draw, the Quad outcomes, Verstappen's
Las Vegas win — are kept in a separate **DATE CHECK** box, never presented
as Tuesday stories.

## The image

- Masthead naming the day, a six-number strip, a MARKETS band (Monday 23 Nov
  closes: Kospi −3.31%, Hang Seng −0.12%, S&P 500 +4.73%, Nasdaq +6.51%,
  gold $3,630.30, Bitcoin $61,060, Brent $86.90), a UTC timeline, three drawn
  hero scenes, 19 illustrated story cards, a pinned world map with a region
  tally, an ALSO list of 13 more stories, and the DATE CHECK box.
- Drawn entirely with PIL (`render.py`, stdlib + Pillow only). No network at
  run time; two runs write identical bytes.

## Run it

```sh
python3 render.py            # writes poster.png (1024x1024, < 1 MiB)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies poster.png to out/entry.png
```

## Sources

Reuters, AP, Al Jazeera, SCMP, Japan Times, AFP, The Times, CNA — all stories
verified on Tuesday 24 November 2026; claims are attributed, not stated as
fact.

<sub>Entered on [make.fun](https://make.fun/?ref=r27sfaxp&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
