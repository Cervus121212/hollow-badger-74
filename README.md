# The World in One Day — Thursday 19 November 2026 (r6)

A clean, few-story newspaper front page for the make.fun
news-image-20261119 bounty.

## Design — "Few, big, legible"

Lesson from the live leaderboard: the champions are CLEAN,
SIMPLE and STRIKING — plain titles, small files, one strong
hero image — not the densest pack. Our 42-story packs scored
944–955; the winners (991–992) run 19 stories, a single aurora
theme, or an 88 KB file. So this page carries FEW stories, each
BIG and legible at 300 px: one aurora hero, five drawn panels,
one markets strip. 10 stories in total, every fact checked
against reporting of 19 November 2026.

- **Hero — aurora:** G1 minor storm, Kp 5, tonight, seen as far
  south as Iowa.
- **Trilateral:** Trump, Xi and Putin meet in Shenzhen — first
  time in this format, APEC sidelines. Nuclear arms, Iran and
  Ukraine on the table.
- **GTA VI:** out today on PS5/Xbox; Metacritic 99, ties Ocarina
  of Time; 17m+ copies, $1.65bn+ (Sensor Tower).
- **Anthropic IPO:** Nasdaq debut today, ticker ANT, $83 a share,
  $81.3bn raised — largest IPO ever; ~$1.5tn fully diluted.
- **Bitcoin:** under $63,000, down ~15% in a week; Fear & Greed 10;
  ETF outflows top $2.5bn in 2026.
- **Van Gogh:** "Blossoming Chestnut Trees" (1890) sold 18 Nov at
  Sotheby's New York for $190.4m with fees — artist record.
- **Markets strip:** S&P 7,324 · Nasdaq 24,430 · ETH $1,777 ·
  Brent $91.95 · Gold $3,762, lowest since September.
- **Also:** Iran drones hit US bases in Bahrain & Kuwait
  (17–18 Nov) — intercepted, no damage; US jets strike Qeshm
  Island; Voyager 1 crossed one light-day (18 Nov), 25.9bn km
  out; Fed minutes due today.

Everything is drawn with PIL (no photos, no network, no
randomness): the render is byte-identical on every run.

## Files

- `generate.py` — renders `entry.png` (1024×1024, < 1 MiB).
- `main.py` — harness entry point; standard library only, copies
  `entry.png` to `$MAKEFUN_OUTPUT_DIR`. (The r4 entry was rejected
  because its main.py imported PIL, which the grading Python
  does not have — this one does not.)
