# Cron Schedule Minute-0 Congestion Analysis

**Source file:** `cron_schedule_4k_refined.tsv`  
**Analysis date:** 2026-07-18  
**Reference date used:** 2026-07-21 (Tuesday — representative weekday)

---

## Current State

| Metric | Value |
|---|---|
| Total jobs | 4,000 |
| Average jobs per minute slot | **304** |
| Jobs at minute 0 | **3,237** (+964% above average) |
| Jobs at minute 30 | **2,161** (+611% above average) |
| Jobs at minute 15 | **1,815** (+497% above average) |
| Jobs at minute 45 | **1,780** (+485% above average) |

Minutes 0, 15, 30, and 45 dominate overwhelmingly. Most other minutes sit well below average (e.g. minutes 1–13 have ~115–126 jobs each).

---

## Breakdown of the 3,237 Jobs at Minute 0

| Category | Count | Notes |
|---|---|---|
| `* * * * *` — every minute, incidentally hits 0 | 77 | Not worth changing — they run at every minute |
| Fire at **minute 0 only** (e.g. `0 * * * *`) | **1,091** | Highest priority to fix |
| Fire at 0 **plus other minutes** (e.g. `*/30`, `*/15`) | 2,069 | Also significant |

---

## Most Congested Minutes (Top 20)

| Minute | Jobs | vs Average |
|---:|---:|---:|
| 0 | 3,237 | +2,933 |
| 30 | 2,161 | +1,857 |
| 15 | 1,815 | +1,511 |
| 45 | 1,780 | +1,476 |
| 40 | 639 | +335 |
| 20 | 631 | +327 |
| 10 | 616 | +312 |
| 50 | 604 | +300 |
| 5 | 466 | +162 |
| 35 | 448 | +144 |
| 25 | 443 | +139 |
| 55 | 443 | +139 |
| 16 | 126 | -178 |
| 32 | 126 | -178 |
| 48 | 126 | -178 |
| 4 | 124 | -180 |
| 24 | 122 | -182 |
| 54 | 119 | -185 |
| 2 | 116 | -188 |
| 1 | 115 | -189 |

---

## Suggestions

### 1. Hourly jobs — `0 * * * *` (433 jobs, 24 fires/day each)
These are the single biggest lever: 433 jobs all stacking at the same second every hour.  
**Fix:** Spread them across minutes 1–59. Each job gets a unique offset, keeping the same hourly cadence with no load spike.  
Example: `0 * * * *` → `7 * * * *`

### 2. Step jobs that include minute 0

| Pattern | Jobs | Fires/day each | Fix |
|---|---:|---:|---|
| `*/2 * * * *` | 8 | 720 | Change to `1-59/2` (fires at 1, 3, 5 … 59) |
| `*/3 * * * *` | 3 | 480 | Change to `1/3` or `2/3` |
| `*/4 * * * *` | 2 | 360 | Change to `1/4`, `2/4`, or `3/4` |
| `*/5 * * * *` | many | 288 | Change to `1/5`, `2/5`, `3/5`, or `4/5` |
| `*/10 * * * *` | many | 144 | Change to `1/10`, `3/10`, `7/10`, etc. |
| `*/15 * * * *` | many | 96 | Change to `3/15`, `7/15`, `11/15` |
| `*/30 * * * *` | many | 48 | Change to `1/30` or `2/30` |

### 3. Sub-hourly jobs with fixed intervals (`*/30`, `*/15`)
These hit minute 0 and all its multiples simultaneously, creating the secondary spikes at 15, 30, and 45.  
**Fix:** Add an offset so the sequence shifts away from round numbers.  
Example: `*/15 * * * *` → `3/15 * * * *` (fires at 3, 18, 33, 48)

---

## Priority Order

1. **Hourly-only jobs (`0 * * * *`)** — 433 jobs, highest concentration, easiest fix (just change one digit)
2. **`*/5` and `*/10` jobs** — high fire rate, always land on multiples of 5 (which are already overcrowded)
3. **`*/15` and `*/30` jobs** — drive the secondary spikes at 15, 30, and 45
4. **`*/2`, `*/3`, `*/4` jobs** — very high fire rate but fewer in number

---

## Notes

- The `* * * * *` jobs (every minute) were excluded from suggestions since they already distribute load evenly across all 60 minutes.
- Weekday-restricted jobs (e.g. `1-5`, `1-6`) were evaluated on a Tuesday, which is representative of the typical workweek load.
- No files were modified during this analysis.
