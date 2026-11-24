# Tuesday 24 November 2026 — The World in One Day (Full-Day Edition)

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/shania00123/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/shania00123/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A front page summing up the world's news of **Tuesday 24 November 2026** in one
1024×1024 image: 38 stories across 5 regions, every one verified against
reporting from that day. This is the full-day edition — v1 was a morning
edition built from news verifiable before 09:00 WIB; v2 adds the afternoon
and evening stories and corrects what the morning got stale.

## What happened that day

- **Ulleung Island:** about five Russian warplanes enter South Korea's
  air-defence zone; Seoul sounds its first-ever air-raid alert over a
  possible intrusion, lifts it after three minutes, scrambles F-15Ks, and
  summons a Russian attaché to protest.
- **Huang is back — then the rally fades:** Nvidia shares soared 31% on
  Monday when the board reinstated Jensen Huang as CEO; on Tuesday he gets
  a hero's welcome at HQ while the shares slip 5% in premarket trading as
  governance questions mount — and Germany's foreign minister says he is
  shocked by Trump's intervention.
- **Space threat:** allies warn Russia may launch a nuclear-armed satellite
  as soon as next month; NATO vows space defence.
- Plus: German business mood hits a three-year high (Ifo 90.6), hacked data
  puts Russia's war dead near 500,000, China probes Politburo member Chen
  Jining, an Israeli strike kills a senior Hamas security chief in Gaza,
  Ukraine defends its Libya strike as self-defence, and Asia closes up —
  Kospi +6.3%, Nikkei +3.9%, Taiex +9.1%.

Stories first reported on an earlier day — the Huang reinstatement itself
(Mon 23 Nov), the sinking of the corvette Merkury (Sun 22 Nov), the COP31
collapse (Sun 22 Nov), the Estonia warning (Mon 23 Nov) — are kept in a
separate **DATE CHECK** box, never presented as Tuesday stories.

## The image

- Masthead naming the day, a six-number strip, a UTC timeline, three drawn
  hero scenes, 19 illustrated story cards, a pinned world map with a region
  tally, an ALSO list of 16 more stories, the DATE CHECK box, and a MARKETS
  band (Tuesday closes in Asia, Monday closes in New York).
- Drawn entirely with PIL (`render.py`, stdlib + Pillow only). No network at
  run time; two runs write identical bytes.

## Run it

```sh
python3 render.py            # writes poster.png (1024x1024, < 1 MiB)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies poster.png to out/entry.png
```

## Sources

Reuters, AP, AFP, Yonhap, SCMP, Japan Times, ifo Institute, Xinhua — all
stories verified on Tuesday 24 November 2026; claims are attributed, not
stated as fact.

<sub>Entered on [make.fun](https://make.fun/?ref=r27sfaxp&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
