# BQ: Game Specification

**Working title:** BQ · **Version:** draft 0.2 · **Date:** 2026-10-11 · **Status:** awaiting your review

> **What this is.** The plan for a mobile game that takes the player on a journey across a 3D map of the UK, from before the Romans to today, to prepare for the *Life in the UK* test.
> **What it teaches.** The whole official handbook, *Life in the United Kingdom: A Guide for New Residents* (3rd edition), as supplied in PDF form. It is broken down into 1,046 testable facts, all written in our own words.
> **What gets built first.** Only **Milestone 1 (M1)**, the *journey skeleton*: the 3D map, travelling between 78 stops, and chapters, as a test build for your Android phone.
> **Not built in M1.** No lessons, quizzes, tests or Passport. M1 only leaves room for them.

**Companion documents:**
- [`docs/LEARNING_DESIGN.md`](LEARNING_DESIGN.md): how the game teaches, in full.
- [`content-src/`](../content-src/): the fact inventory, the lesson list and the journey data.

**How to review:** Part A is about the game, so read it first; section 7 is the learning design in brief. Part B covers how it's built and tested. Part C is the plan. Section 15 lists the questions that are still open. None of them block M1.

**New in 0.2:** the content now follows the handbook PDF you supplied. A learning designer (a subagent) broke it into facts and structured the game for learning:
- 78 journey stops, with an optional prologue;
- a Passport for everything that isn't history;
- five-minute lessons;
- spaced reviews on the map;
- mock tests in the official format.

---

## Decisions

Decided in the interview on 2026-10-10, plus the rows marked **(11 Oct)**, decided on 2026-10-11.

| Topic | Decision |
|---|---|
| Engine | **Godot 4.7** (4.7.2 pinned; GDScript; *Compatibility* renderer for low-end phones) |
| Core journey | **Tap-to-travel diorama**: the whole UK as a tilted 3D tabletop map. Tap the next stop and your piece travels there |
| Orientation | **Portrait** only |
| Test device | **Budget Android phone, Android 11+** (exact model to confirm, see section 15) |
| Chapters | **7**, following the history chapter of the official handbook, Romans → today, **plus an optional prologue, "Before the Romans"** (11 Oct) |
| Progression | **Guided**: one stop at a time, in date order |
| Stops in M1 | **78** real places in legs of at most 7 (11 Oct; was 35). **Name + year only**, no learning text |
| Art direction | **Smooth stylised** terrain built from real elevation data |
| Test builds | **One command in WSL** builds and installs on the phone over Wi-Fi. No CI needed |
| Repo / CI | Repo **stays public**. CI only runs **manually or for releases** |
| iOS | Planned but not built in M1. No Apple hardware or account yet |
| Process | Spec → your review → M1 skeleton, on branch `claude/upbeat-cray-2adgy3` |
| **Content source** (11 Oct) | The handbook PDF you supplied (3rd edition). Facts are in our own words. Facts that may be outdated are checked against the latest official reprint |
| **Learning layers** (11 Oct) | **Journey**: 78 map stops, mostly history. **Passport**: 72 lessons for everything else, on 10 themed pages, with **no pins**. There is no separate map layer for modern topics |
| **Gating** (11 Oct) | **Soft**: a 70% chapter checkpoint earns a flourish but never blocks |
| **Remembering** (11 Oct) | Spaced repetition (6-box Leitner), shown as glowing pins and short review runs |
| **Test practice** (11 Oct) | Mock tests in the official format (24 questions, 45 minutes, 75% to pass) and a readiness score |
| **Other learning defaults** (11 Oct) | The journey stays inside the UK. Full study mode, with a one-tap Express mode (core facts only). Plain English (level B1) with a tap glossary. No phone notifications |

---

# Part A: The game

## 1. Vision

The player travels across a 3D diorama of the United Kingdom **and through time**, from the Stone Age and the Roman invasion to the present day. Every stop is a real place at a real moment. From M3:
- each journey stop teaches the history that happened there;
- a **Passport** teaches the rest of the official handbook: values, the UK and its nations, government and law, money, faith and customs, culture and sport;
- short lessons, spaced reviews on the map and mock tests in the official format get the player ready to pass the Life in the UK test.

**Pillars**
1. **The journey is the menu.** Progress is a route you can see across the map, not a list of lessons.
2. **Place + time = memory.** Every fact is pinned to where and when it happened.
3. **Runs on cheap phones.** It's designed for a budget Android phone first.
4. **Short sessions.** A lesson takes about five minutes and the game always resumes where you left off.
5. **Accurate.** Content follows the official handbook, in our own words. Every time-sensitive fact is checked against the latest official reprint.
6. **Remembered.** Every lesson ends with recall, and places come back as review visits until the facts stick.

**Audience:** adults preparing for the test, many with English as a second language. That means plain English at reading level B1, a tap-for-meaning glossary, large touch targets and high-legibility text.

## 2. Milestone 1 scope: the journey skeleton

| In M1 | Not in M1 (later milestones) |
|---|---|
| Whole-UK 3D map with smooth stylised terrain from real elevation data | Lessons, quizzes, spaced reviews, mock tests, scoring |
| An optional prologue plus 7 chapters: **78 stops** in legs of at most 7, guided progression | The Passport (its data exists, but nothing of it is shown) |
| Travel animation along routes, including sea crossings | Audio and music |
| Arrival card with an **empty content slot** | Final art (avatar, era vehicles, landmark models, era-specific towns and roads) |
| Time-jump transitions between chapters, then end of journey and free roam | Accounts, cloud save, analytics, ads, purchases |
| Camera: pan, pinch-zoom, double-tap recentre, follow during travel | iOS build; store release |
| Save/resume; Settings; About (build info, credits) | Languages other than English |
| **Developer menu** (test builds only): stats, jump to any stop, live tuning, benchmark | Tablet-specific layouts (they will work, but won't be tuned) |
| One-command WSL build/install; headless tests; one manual-only CI fallback | |

## 3. Player experience (M1)

### 3.1 Core loop

```
 look at the map ──► tap the glowing next stop (or "Travel")
        ▲                         │
        │                         ▼
  next stop glows ◄── Continue ◄── arrive: card shows place + year
        │                          (empty slot for the future lesson)
        └── after a chapter's last stop: TIME-JUMP to the next chapter
```

- **First launch:** title screen (placeholder) → **Start journey**. The camera sweeps from the whole-UK view to the North Sea, and the optional prologue begins. Your piece starts on **Dogger Bank**, the old land bridge to the continent (the handbook explains Britain was joined to Europe until about 10,000 years ago), and the first stop, Skara Brae on Orkney, glows.
- **Skip to the Romans:** a button in the bottom sheet on the prologue's first stop. The piece then starts **at sea off the Kent coast**, "arriving from Gaul", and Richborough glows. Skipped prologue stops stay on the map as optional side stops.
- **Later launches:** the game resumes exactly where you left off.

### 3.2 Screen layout (portrait)

```
┌──────────────────────────────────┐
│ I · ROMAN BRITAIN        AD 60   │ ← chapter + current year (rolls during travel)
│ ● ● ◉                        ⚙  │ ← progress in this leg · settings  [DEV in test builds]
│                                  │
│              (3D map)            │
│          ✦ Hadrian's Wall        │ ← next stop: glowing pin + label
│                                  │
│                                  │
│      @ ✓ Roman London            │ ← your piece (on the last stop visited)
│                    ✓ Richborough │ ← ✓ = visited
│                             [◎]  │ ← recentre
├──────────────────────────────────┤
│ NEXT STOP                        │ ← bottom sheet
│ Hadrian's Wall · AD 122          │
│ [          Travel  ▶          ]  │
└──────────────────────────────────┘
```

- The chapter shows the numeral **0** in the prologue. There the top bar shows the era (*Stone Age*, *Iron Age*) instead of a year.
- From M3b a **briefcase** button joins the settings button, to open the Passport. It is not shown in M1.

### 3.3 Controls

| Gesture | Result |
|---|---|
| Drag (one finger) | Pan the map, with inertia, kept inside the map edges |
| Pinch | Zoom between the whole-UK view and a ~60 km close view |
| Tap the next stop, or **Travel** | Travel there |
| Tap a visited stop | Camera flies there and re-opens its card (your piece doesn't move) |
| Tap a locked stop | Hint: "Visit *Roman London* first" |
| Double-tap the map | Recentre on your piece |
| Tap during travel / time-jump | Skip to the end of it |
| Android **Back** | Close the card or menu that's open. On the map, it asks whether to leave |

The map is always **north-up with no rotation**, which keeps the geography consistent for learning. Camera tilt is fixed but tunable in the developer menu.

### 3.4 Chapters, legs and stops

- A **chapter** is an era. It has a title, a year range, a mood (lighting and colour) and an ordered list of stops.
- A chapter is cut into **legs of at most 7 stops**. Only the current leg's pins are labelled; earlier legs shrink to small faded dots, so the map stays readable on a small screen.
- Stops unlock **strictly in list order** (date order), and exactly one stop is "next" at any time.
- **Stop states:**
  - *Locked:* dim pin, label only when zoomed in.
  - *Next:* glowing, pulsing pin with label.
  - *Visited:* tick pin with label.
  - *Here:* your piece is standing on it.
- States differ by **shape as well as colour** (colour-blind safe).
- **Shared places:** several stops share a place (Westminster has five, at different dates; Belfast and Liverpool three each). Their pins fan out slightly around the spot, so each can be tapped.

### 3.5 Travel

- **Route:** a path from your current position to the next stop, draped over the terrain and drawn as a dashed line that reveals itself just ahead of the piece. A route can bend through optional waypoints set in the data.
- **Sea crossings:** where a route crosses at least ~6 km of sea, the piece turns into a **boat** for that stretch, for example to Iona, Belfast or Stormont. Shorter water gaps such as estuaries are simply crossed, with no boat.
- **Timing:** duration = distance ÷ speed, clamped between about 1.5 s and 6 s, with ease-in/ease-out. Every number is tunable (section 6).
- **Camera:** frames the start and end, then follows the piece.
- **Year counter:** the year in the top bar **rolls forward** during travel (e.g. AD 60 → AD 122), so the piece moves through time as well as space.

### 3.6 Arrival card

On arrival the camera eases into a close regional view and the pin pops. A card slides up showing:

```
  CHAPTER I · ROMAN BRITAIN
  Hadrian's Wall
  AD 122
  ┌──────────────────────────────────────┐
  │  Lessons for this stop will appear   │ ← content slot (M3 fills this)
  │  here in a later version.            │
  └──────────────────────────────────────┘
  [            Continue            ]
```

- **Continue** closes the card and the next stop starts glowing.
- After a chapter's last stop, **Continue** starts the time-jump.
- From M3 the content slot holds the lesson (section 7.4), with a **Start** button.

### 3.7 Time-jump between chapters (~3 s, skippable)

1. The camera pulls back to the whole-UK view.
2. The year counter rolls quickly from the last stop's year to the next chapter's start year (e.g. AD 122 → 410). It keeps rolling during the next leg.
3. The lighting and colour **mood crossfades** to the new era.
4. A title card fades in and out: *"Chapter II · Anglo-Saxons & Vikings · 410–1066"*.
5. Your piece changes to the new chapter's colour, and the new chapter's first stop glows.

- The journey stays **continuous**: chapter II's first leg runs from wherever chapter I ended.
- From M4 the title card can add a "chapter mastered" flourish after a good checkpoint (section 7.5).

### 3.8 End of journey

After the final stop (Westminster, *Today*), a **Journey complete** card shows the stops visited (78/78), the distance travelled and the time played. It has two buttons:
- **Free roam:** every stop is unlocked. Tap any stop to fly there, and the mood follows that stop's chapter.
- **Start again:** asks for confirmation, then resets progress.

### 3.9 Settings and About

- **Graphics:** Low / Medium / High. The game picks one automatically on first launch, based on the phone's memory.
- **Reduce motion:** shorter, gentler camera moves and no pulsing.
- **Reset journey** (with confirmation).
- **About:** version and **build id** (git commit), plus credits and data licences, and the line "Based on the official *Life in the United Kingdom* handbook. BQ is an independent app, not published or endorsed by the Home Office."

### 3.10 Save and resume

- The game **autosaves** after each arrival, chapter change and settings change, and whenever it goes into the background.
- **The save holds:**
  - current chapter and next stop, and the visited stops;
  - piece and camera position;
  - settings, distance and play time;
  - the save format version;
  - two fields that stay empty in M1: per-stop `lesson_done` and `best_quiz_score`, and an empty `learn` object with a `learn_schema` number, where M3 and M4 keep lesson and review progress.
- An unreadable or unknown save is backed up and the game starts fresh. It must never crash because of a bad save.

## 4. Journey data

> **Draft for M1, from the learning design.** Every stop is chosen to anchor part of the handbook. Each chapter is split into legs of at most 7 stops.
> - **†** = a year chosen by BQ, because the handbook gives none. It only orders the stops and drives the rolling counter, and is never quizzed.
> - **‡** = a place chosen by BQ, because the handbook doesn't name a place for that story. It is never used in a map question.
>
> Coordinates live in `content-src/journey_draft.json`, which becomes `game/data/journey.json` in M1. Editing a stop is a one-line change.

| Chapter | Leg | Stops: place, year |
|---|---|---|
| **0 · Before the Romans** (Stone Age – 55 BC) *optional* | 1 | Skara Brae, Stone Age † · Stonehenge, Stone Age † · Maiden Castle, Iron Age † |
| **I · Roman Britain** (55 BC – AD 410) | 1 | Richborough ‡, 55 BC / AD 43 · Roman London, AD 60 † · Hadrian's Wall, AD 122 † |
| **II · Anglo-Saxons & Vikings** (AD 410 – 1066) | 1 | Sutton Hoo, AD 410–600 · Iona, c. AD 563 † · Canterbury, c. AD 597 † · York ‡, from AD 789 · Winchester ‡, c. AD 880 † |
| **III · The Middle Ages** (1066 – 1485) | 1 | Hastings, 1066 · Tower of London (Normans), c. 1080 † · Runnymede ‡, 1215 · Caernarfon, 1284 · Westminster Hall, c. 1295 † |
|  | 2 | Bannockburn, 1314 · Weymouth ‡, 1348 · Lincoln, c. 1400 · Southampton ‡, 1415 · Bosworth, 1485 |
| **IV · Tudors & Stuarts** (1485 – 1714) | 1 | Hampton Court ‡, 1530s · Canterbury (Church of England), 1530s · Greenwich ‡, 1547–1603 † · Stirling Castle ‡, 1560 · Stratford-upon-Avon, 1564 · Plymouth ‡, 1588 |
|  | 2 | Westminster, 1605–1642 · Derry/Londonderry ‡, c. 1609 † · Newcastle ‡, 1640 · Naseby, 1642–1649 · Worcester, 1651 † · Dover ‡, 1660 |
|  | 3 | London 1666, 1665–1666 · Cambridge (Newton), 1660s † · Torbay ‡, 1688 · Westminster, 1689 · Glencoe, 1690–1692 † · Edinburgh (Union) ‡, 1707 |
| **V · A Global Power** (1714 – 1900) | 1 | 10 Downing Street, 1714–1742 · Culloden, 1746 · Glasgow (Enlightenment) ‡, 18th century · Whitby ‡, 1770 † · Cromford ‡, 1771 † · Portsmouth (HMS Victory), 1776–1815 |
|  | 2 | Ironbridge ‡, 1779 † · Belfast ‡, 1801 · Liverpool ‡, 1807 · Manchester ‡, 1832 · Bristol ‡, c. 1835 † |
|  | 3 | Windsor ‡, 1837 · Newport (Chartists) ‡, c. 1839 † · Liverpool (Irish arrivals), c. 1850 · Hyde Park, 1851 · St Thomas' Hospital, 1854–1860 · Burwash (Kipling) ‡, 1899–1902 |
| **VI · The 20th Century** (1900 – 1945) | 1 | Manchester, 1903 · Belfast ‡, 1913–1922 · Brighton ‡, 1914 · The Cenotaph, 1916–1918 · Westminster, 1918 · Glasgow, 1929 |
|  | 2 | Cambridge, 1930s · Dover ‡, 1939–1940 · Blenheim ‡, 1940 † · Coventry, 1940 · Portsmouth ‡, 1944–1945 |
| **VII · Britain since 1945** (1945 – today) | 1 | Tredegar ‡, 1945–1948 · Tilbury ‡, 1948 · Jodrell Bank, 1950s · Liverpool ‡, 1960s · Enfield, 1967–1996 · Belfast ‡, 1969–1973 |
|  | 2 | Grantham, 1979–1990 · Stormont, 1998 · Holyrood, 1997–1999 · Senedd, 1999 · Westminster, Today |

**78 stops:** prologue 3 · I 3 · II 5 · III 10 · IV 18 · V 17 · VI 11 · VII 11. England has 59, Scotland 10, Northern Ireland 5 and Wales 4. Wales gets more in the Passport (Cardiff, Swansea). Events abroad (Agincourt, the Boyne, Waterloo, the Somme, Dunkirk, D-Day) are told from UK places, so the journey never leaves the UK.

**File format** (`game/data/journey.json`, human-editable):

```json
{
  "version": 1,
  "chapters": [
    { "id": "roman", "numeral": "I", "title": "Roman Britain", "years": "55 BC - AD 410",
      "mood": "roman", "end_year": 410,
      "start": { "lat": 51.10, "lon": 1.60, "name": "The Channel" },
      "legs": [["rom-richborough", "rom-london", "rom-housesteads"]],
      "stops": [
        { "id": "rom-richborough", "name": "Richborough", "place": "Richborough, Kent",
          "year": "55 BC / AD 43", "sort": -55, "lat": 51.293, "lon": 1.332,
          "year_src": "HB", "place_in_handbook": false, "content": "rom-richborough" }
      ] }
  ]
}
```

**Fields:**
- `year` is the text that's displayed. `sort` is the numeric year used for ordering and the rolling counter (BC years are negative).
- `year_src`: `HB` means the year is in the handbook; `EXT` means BQ chose it (†).
- `place_in_handbook: false` is the ‡ mark.
- `start` (optional) is where the piece begins when the journey starts at that chapter: Dogger Bank for the prologue, the Channel for chapter I.
- `via` (optional) is a list of waypoints that bend a route.
- `content` is the lesson id for M3. It equals the stop id and is unused in M1.

**Automated checks:**
- Ids are unique, and **frozen once released**: saves refer to them.
- Every leg has at most 7 stops.
- `sort` never decreases across the whole journey.
- Every stop is inside the map and within 3 km of land, which catches typos in coordinates.

## 5. The map and the look

### 5.1 Extent and projection

- **Area:** 49.0–61.0°N, 11.0°W–2.5°E. That covers all of the UK (Great Britain, Northern Ireland, Orkney, Shetland, the Isles of Scilly), plus the rest of the island of Ireland, the Isle of Man, the Channel Islands and the nearest strip of continental coast.
- **What's highlighted:** only **UK land** is in full colour. Everything else, including the Isle of Man and the Channel Islands (Crown Dependencies, not part of the UK), is shown **muted** and unlabelled. This later helps teach "what is the UK" at a glance.
- **Labels:** the four UK nations are labelled flat on the land: ENGLAND, SCOTLAND, WALES, NORTHERN IRELAND.
- **Projection:** spherical transverse Mercator, central meridian 4°W, origin 55°N. 1 map unit = 1 km, so the map is about **930 × 1,340 km**, which suits a portrait screen.
- **Edges:** the map fades into sea and haze at its edges, like a diorama sitting on a table.

### 5.2 Terrain: smooth stylised

- **Shading:** soft and smooth. Colour comes from **height and slope gradients**: shallow sea → beach → lowland green → upland olive → moorland brown → rock grey → a dusting of snow on the highest peaks.
- **No textures** on the terrain. Colour is computed in a shader, which is cheap on budget GPUs and lets each chapter retint the whole map.
- **Vertical exaggeration** is about ×20 (tunable) so that hills and mountains read from above.
- **Sea:** opaque, coloured by depth (turquoise shallows → deep blue), with a lighter coastal band and a gentle shimmer.

### 5.3 Chapter moods

| Ch | Mood |
|---|---|
| 0 · Before the Romans | Pale dawn; chalk grey and heather |
| I · Roman Britain | Warm golden afternoon; terracotta route line |
| II · Anglo-Saxons & Vikings | Cool misty morning; grey-blue haze, sea-green |
| III · The Middle Ages | Earthy, parchment-tinted |
| IV · Tudors & Stuarts | Rich and warm; deep red and gold accents |
| V · A Global Power | Smoky amber haze (industry) |
| VI · The 20th Century | Desaturated, cool grey-blue |
| VII · Britain since 1945 | Bright, clean, full-colour daylight |

### 5.4 Placeholders in M1

- **Player piece:** a simple pawn, tinted per chapter.
- **Boat:** a simple hull.
- **Stop markers:** simple pins.
- **UI font:** *Atkinson Hyperlegible Next*, designed for legibility (SIL Open Font License; ~114 KB).
- **Final look:** the avatar, vehicles and landmark models are open questions for M2 (section 15).

## 6. Tuning and the developer menu: how we nail down the gameplay

Every number that affects *feel* lives in `game/data/tuning.json`, not in code. In test builds you can change these numbers live **on your phone**:

1. Open **DEV → Tuning**, move the sliders and play. Changes apply instantly.
2. **Save on phone** keeps your values between launches.
3. To send them back, either tap **Copy tuning** and paste it into a chat with Claude, or run `./tools/phone.sh pull-tuning` to copy the phone's values into the repo. Either way they become the new defaults.

**Starting tunables** (defaults are first guesses, meant to be tuned on your phone):

| Group | Key | Default | Range | Effect |
|---|---|---|---|---|
| Camera | `cam.pitch_deg` | 55 | 30–80 | Tilt of the view (90 = straight down) |
| | `cam.fov_deg` | 40 | 25–70 | Lens width |
| | `cam.view_min_km` | 60 | 20–200 | Closest zoom (map width on screen) |
| | `cam.view_max_km` | 1100 | 600–1600 | Furthest zoom |
| | `cam.arrival_view_km` | 140 | 40–400 | Zoom on arrival at a stop |
| | `cam.pan_inertia` | 0.90 | 0–0.98 | How far a flick glides |
| | `cam.zoom_smooth` | 12 | 1–30 | Zoom smoothing |
| | `cam.follow_smooth` | 6 | 1–20 | How tightly the camera follows the piece |
| | `cam.travel_fit_pad` | 1.3 | 1.0–2.0 | Margin when framing a route |
| Travel | `travel.speed_kmps` | 160 | 40–600 | Piece speed (map km per second) |
| | `travel.min_s` / `max_s` | 1.5 / 6.0 | 0.5–15 | Duration limits per leg |
| | `travel.ease` | in-out | linear / out / in-out | Acceleration curve |
| | `travel.boat_min_water_km` | 6 | 0–30 | Minimum stretch of water before switching to the boat |
| | `travel.year_roll` | on | on/off | Year counter rolls during travel |
| | `travel.tap_to_skip` | on | on/off | Tap to finish travel instantly |
| Map | `map.height_exaggeration` | 20 | 5–60 | How tall hills look |
| | `map.sea_shimmer` | 0.3 | 0–1 | Sea animation strength |
| | `map.haze` | 0.5 | 0–1 | Distance haze |
| | `map.lod_bias` | 1.0 | 0.25–4 | Terrain detail vs. speed |
| | `map.shared_pin_spread_km` | 3 | 0–15 | How far pins that share a place fan out |
| Time-jump | `jump.duration_s` | 3.0 | 0.5–8 | Length of the chapter transition |
| | `jump.title_hold_s` | 1.5 | 0.5–4 | How long the chapter title stays |
| UI | `ui.marker_scale` | 1.0 | 0.5–2 | Pin and label size |
| | `ui.tap_slop_px` | 12 | 4–40 | Finger movement allowed before a tap becomes a drag |
| Perf | `perf.fps_cap` | 30 | 30/60 | Frame-rate cap |
| | `perf.idle_fps` | 15 | 5–30 | Frame-rate cap after a few seconds without input (saves battery) |

**Developer menu** (test builds only, opened with a small **DEV** button):

| Section | Contents |
|---|---|
| Overlay | Live FPS, frame time (average and worst), draw calls, triangles, video memory, quality tier |
| Journey | Jump to any chapter, leg or stop; unlock all; reset progress; replay a time-jump; start with or without the prologue |
| Tuning | The sliders above, plus save, reset and copy |
| Performance | Quality tier, render scale, FPS cap, a **simulate low-end** preset |
| Benchmark | 60-second automatic run (pans, zooms, 3 journeys, 1 time-jump). Reports average FPS, 1% low, worst frame, peak draw calls, triangles and memory, and also writes a `BQ_BENCH {...}` line to the phone log |
| Build | Version, commit, build time |

## 7. Learning design (built in M3 and M4)

> This is the summary. The full design, with every stop, Passport page, rule and number, is in [`docs/LEARNING_DESIGN.md`](LEARNING_DESIGN.md). **Nothing in this section is built in M1**; M1 only gets the journey data (section 4) and the extension points (section 8.6).

### 7.1 Content source

- **Source:** the handbook you supplied, *Life in the United Kingdom: A Guide for New Residents*, 3rd edition (a PDF version by "Britizen", Crown copyright). The test can ask about **any part** of it, including the introduction.
- **The breakdown:** **1,046 testable facts**, each with its handbook section and page, in `content-src/syllabus.csv`:
  - **474 core (A):** dates, firsts, key people, numbers, rules.
  - **430 secondary (B).**
  - **142 context (C):** story colour, never asked on its own.
- **History is only 44%** of what can be asked. Society and culture is 30%, government, law and your role 22%, and values plus "What is the UK" 4%. A history-only game would leave over half the test uncovered.
- **87 facts are flagged:** time-sensitive, inconsistent or ambiguous (for example the monarch, the Senedd, the EU, renamed bodies). They stay **pending** until a person checks them against the latest official reprint (open question 9). Until then they can appear as story at most, never in a quiz or mock test.

### 7.2 Two layers: the journey and the Passport

| Layer | Teaches | Organised as | Lessons |
|---|---|---|---:|
| **Journey** | History, plus the institutions history created (the first Parliaments, the Church of England, Remembrance Day, the devolved parliaments) | The map: guided, in date order; optional prologue + 7 chapters; legs of at most 7 stops | **78** |
| **Passport** | Everything else: the test and values, the UK and its nations, government, law and courts, voting and the world, money and everyday life, faith and customs, music and the arts, books, film and media, sport | **10 themed pages** of "stamps", opened at the **Citizenship Desk** (a landmark at Dover) or from a **briefcase** button anywhere. **No pins** | **72** |

- **Lessons about a place** (45 of the 72 stamps, e.g. Wimbledon, the Old Bailey, Edinburgh) show the place with a **temporary highlight** on the map while the lesson runs, and can use map-tap questions ("Where is Bradford?"). They leave no pin behind, so the map stays a single 78-pin route.
- **Echo unlocks:** stamps unlock in small batches after each history chapter, so modern topics meet the history that explains them. For example, finishing the Middle Ages (Magna Carta, the first Parliaments) unlocks the stamps on Parliament and the criminal courts. A welcome batch (the test, values, the UK and its nations) is open from day 1. **Test-date mode** opens everything at once.

### 7.3 Learning principles, applied

| Principle | How BQ applies it |
|---|---|
| Retrieval practice | Every lesson ends with questions; wrong answers get the right answer and a one-line reason at once |
| Spaced repetition | Facts come back just before they'd be forgotten, as glowing pins (section 7.5) |
| Memory palace | Pins are the "rooms", the guided route is the fixed walk, the rolling year is the time spine |
| Chunking | At most **9** core and secondary facts per lesson (average 6) |
| Interleaving | Review runs, echo stamps, checkpoints and mocks mix chapters on purpose |
| Elaboration | Each lesson has a hook, a cause-and-effect card and one "why / what next" question |
| Dual coding | Every core fact has a picture key: an icon, flag, coin, timeline marker or the map itself |
| Mastery | Per lesson: Learned → Solid → Mastered; per chapter: a soft checkpoint |
| Exam simulation | Mock tests in the official format, with a readiness score |

### 7.4 A lesson (about 5 minutes)

| Step | What happens |
|---|---|
| 1. Arrive | Journey: the arrival card (section 3.6) shows **Start**. Passport: tap a stamp on its page |
| 2. Story cards | 3 cards of 25–40 words: the hook, the cause and effect, a "remember" card (year, person, rule). Tap any word for its meaning |
| 3. Recall | 3 questions with instant feedback. One asks "why" or "what next"; one in four calls back to an earlier lesson |
| 4. Retry | A missed question is asked once more |
| 5. Result | 1–3 stars and the facts learned; the next place or stamp glows |

- A lesson counts as done after any attempt. Stars measure the first try; mastery measures the long term.
- **Express mode** shows only core (A) facts and skips travel animations, at about 2–3 minutes per lesson.

### 7.5 Remembering: reviews on the map

- **Schedule:** each fact sits in one of 6 **Leitner boxes**. A right answer moves it up and a wrong one drops it to the start. Reviews come after 1, 3, 7, 16 and 35 days, then the fact rests for 60.
- **Glowing pins:** a journey stop with facts due shows a small amber badge with the count. The **Citizenship Desk** glows the same way for Passport facts.
- **Review run:** tap **Review** and the piece flies a short route through up to 5 glowing places, asking 2–4 questions at each (3–6 at the Desk), mixed across chapters.
- **Quick review:** the same questions without travel, for low battery or a train ride.
- **Limits:** a daily cap of 30 questions. A friendly "review first" banner appears if more than 80 facts are overdue, and you can override it. With a test date set, intervals shrink automatically.
- **Checkpoints:** after a chapter's last stop, 10 mixed questions. **70%** earns a "chapter mastered" flourish. Below that, the game suggests the weak stops and offers a fix-it run, but **never blocks** (soft gate). The chapter's echo stamps unlock either way.

### 7.6 Mock tests and readiness

- **Full mock:** exactly like the real test, **24 questions in 45 minutes, pass at 18 (75%)**, with no feedback until the end. Also a **mini mock** (12 questions, 20 minutes) and a **fix-it mock** built from your weakest topics.
- **Blueprint:** 2 / 1 / 8 / 6 / 7 questions from handbook chapters 1–5. This is an assumption, kept as data so it can be tuned; the Home Office doesn't publish the split.
- **Fact selection:** 70% core and 30% secondary, never a pending fact, and no repeats from your last two mocks.
- **Readiness score:** your estimated chance of passing, computed from how well you know each fact. It is never higher than your recent mock results. Shown as a number with chapter bars, e.g. "Nearly ready: 82%".

### 7.7 Questions

- **Four types, as in the real test:** single answer (pick 1 of 4), true/false pair, choose two, and "which statement is correct".
- **Learning-only types, never in mocks:** map tap, put in order, match, number dial, "what happens next".
- **Writing rules:**
  - plain B1 English with positive wording (no "NOT" or "EXCEPT");
  - four options of similar length;
  - believable wrong answers taken from the handbook itself;
  - every question linked to its fact ids;
  - every question checked by a person against the handbook.
- **Bank size:** about 2,300 questions in time (3 per core fact, 2 per secondary), and at least 1,400 for M4.

### 7.8 Study time

- **Full mode:** about **28.5 hours** in total (lessons ~12.5 h, reviews ~10 h, mocks ~5.5 h, checkpoints ~0.5 h).
- **Express mode:** about **15 hours**.
- **With a test date:** test-date mode turns this into a daily plan and shows "on track" or "behind by N lessons". For example: 8 weeks at ~30 min a day; 4 weeks at ~1 hour a day; 2 weeks in Express at ~1 hour a day.

### 7.9 Accuracy and copyright rules

- **Teach what the handbook says,** because the test is written from it. For flagged facts the **latest official reprint** wins, and a flagged fact that the reprint doesn't contain becomes story only.
- **Our own words only.** No text in the game (facts, cards, questions, feedback) may share a run of **8 or more consecutive words** with the handbook. `tools/content/copyright_guard.py` checks this locally. The only exception is a short quotation of out-of-copyright or statutory text, flagged `quote`; one fact today is a poem title.
- **Never commit** the handbook PDF or its text (the repo is public; `.gitignore` blocks `content-src/private/` and PDFs). No images from the handbook.
- **Edition swap:** every fact, lesson and question records the **handbook edition** it was checked against. When a revised handbook appears, a diff script lists each fact as the same, changed, removed or new. Changed facts go back to pending and their questions back to draft. Players see a one-time "what's new" card, and affected facts return to the start of the review schedule.

---

# Part B: How it's built and tested

## 8. Technical design

### 8.1 Engine and project settings

- **Godot 4.7.2**, the latest stable release (18 Aug 2026). The exact version is pinned in `tools/godot-version`, with download checksums. Maintenance releases such as 4.7.3 are adopted deliberately, never automatically.
- **GDScript** with static typing everywhere. No C#: it adds a runtime, APK size and toolchain weight for no M1 benefit.
- **Compatibility renderer** (OpenGL ES 3.0), the Godot renderer intended for low-end mobile. It also avoids Vulkan driver crashes known on budget GPUs such as the PowerVR GE8320.
- **Display:** portrait locked; stretch mode `canvas_items` with `expand` aspect; UI respects the safe area (notches, rounded corners).
- **Android:**
  - **Minimum Android 7.0** (API 24) and **target API 36**. These are Godot 4.7's defaults and meet Google Play's 2026 rule.
  - CPU architectures: **arm64-v8a + armeabi-v7a**. Godot's default is 64-bit only, but many budget phones run 32-bit Android, so the test build includes both.
  - 16 KB memory pages are supported (Godot ≥ 4.5).
  - ETC2/ASTC texture compression is enabled.
  - **Permissions: none.** No internet, so the app can't collect anything.
  - App ids: `com.mrsjoberg.bq` for store builds and `com.mrsjoberg.bq.dev` for test builds, so both can be installed side by side.
  - Names: "BQ" and "BQ Dev".
- **Test APKs** use Godot's **non-Gradle export**. Godot aligns the APK itself and only needs `adb` and `apksigner`, which Ubuntu provides natively for ARM64.
- **Store bundles (AAB)** need Godot's **Gradle build**. Google's build tools for it are x86-64 only, so AABs are built in CI.
- **No physics engine use.** Taps are resolved in screen space against stop markers.

### 8.2 Repository layout

```
BQ/
├── docs/            SPEC.md (this), LEARNING_DESIGN.md, PERF_LOG.md (per-build measurements)
├── content-src/     syllabus.csv (1,046 facts), stops.csv (150 lessons), journey_draft.json, README.md
├── game/            the Godot project (project.godot lives here)
│   ├── data/        journey.json, tuning.json, moods.json
│   ├── content/     lessons and questions (from M3), generated from content-src/
│   ├── scenes/      main, world (terrain, sea, markers, routes, piece, camera), ui
│   ├── scripts/     autoloads + components
│   ├── assets/      fonts, placeholder meshes, terrain/ (generated, not committed)
│   └── tests/       headless test runner + tests
├── tools/
│   ├── setup_wsl.sh     one-time setup in WSL (you)
│   ├── phone.sh         build / install / run / logs / tuning / benchmark (you)
│   ├── test.sh          all automated tests (Claude, optionally you)
│   ├── godot-version    pinned engine version + checksums
│   ├── mapgen/          terrain generator (Python + NumPy) and its small source data
│   └── content/         copyright_guard.py now; content generator and validators from M3
├── .github/workflows/   manual-only workflows (section 11)
├── CREDITS.md           data, font and asset licences
└── README.md
```

### 8.3 Architecture

**Global services (Godot autoloads):**

| Service | Responsibility |
|---|---|
| `Journey` | Loads and validates `journey.json`; answers "which chapter / leg / stop / what's next" |
| `Progress` | The rules (guided order), the game state, signals such as `stop_arrived` and `chapter_changed` |
| `SaveStore` | Versioned JSON save/load with backup on corruption |
| `Tuning` | Defaults plus on-phone overrides; signals live changes so systems update instantly |
| `Geo` | Map projection (lat/lon ↔ map km) and terrain height lookup |
| `Content` | The **learning-content interface**. Returns "nothing yet" in M1 (section 8.6) |
| `Learner`, `Review`, `Quiz` | **Reserved for M3/M4**: lesson and mastery state, the review queue, the question scene. Empty stubs in M1 |
| `DevTools` | Developer menu and overlay. Only exists in test (debug) builds |

**Game states:** `Boot → Title → Map ⇄ Travelling → Arrived → (TimeJump) → … → JourneyComplete → FreeRoam`. M3 and M4 add `Lesson`, `Review` and `Mock`.

**Scenes:**
- `Main`
- `World`: Terrain, Sea, Markers, Routes, Piece, CameraRig, Environment
- `UI`: TopBar, BottomSheet, ArrivalCard, ChapterCard, Settings, About, DevPanel. M3b adds Passport (pages and stamps) and the Citizenship Desk

Systems talk through signals. The UI never reaches into world internals.

### 8.4 Map pipeline

1. **Fetch (one-off; Claude runs it, you never need to):** `tools/mapgen/fetch_dem.py`.
   - Downloads the **GEBCO_2026 grid** (land height + sea depth in one dataset, 15 arc-seconds, roughly 0.3–0.5 km). It's cut to the map box on the server, so the download is ~20–40 MB.
   - Reprojects it to a **1 km grid** in map coordinates.
   - Marks which land is UK, using Natural Earth country boundaries.
   - Writes small compressed arrays (~1–3 MB) into `tools/mapgen/data/`, which are committed.
   - *Why not NOAA ETOPO 2022?* Its UK land layer comes from FABDEM, which is licensed **non-commercial only**. GEBCO explicitly allows commercial use with attribution.
2. **Build (automatic, when inputs change):** `tools/mapgen/build_terrain.py` (Python 3 + NumPy, roughly 10 s).
   - Cuts the map into **128 km chunks**, each with **3 levels of detail** (1, 2 and 4 km grids).
   - Adds skirts at chunk edges so no cracks show between detail levels.
   - Computes smooth normals and drops triangles hidden under the sea.
   - Writes `game/assets/terrain/generated/`: the terrain meshes (`.glb`), a sea-depth texture, and a coarse height grid for placing pins and routes at runtime.
   - Generated files are **not committed**, which keeps the repo small however often we tweak the terrain.
3. **Runtime:** each chunk switches detail level by camera distance, using Godot's *visibility ranges*. This renderer can't cross-fade between levels, so skirts and identical colouring hide the switch.

**Budgets:**
- ≤ 400k triangles at full detail across the whole map.
- ≤ 150k triangles visible at once.
- ≤ 25 MB of mesh memory.
- About 40 terrain draw calls at the whole-UK view.

### 8.5 Rendering for low-end phones

- **Lighting:** one directional light and **no real-time shadows**. In this renderer each shadow split draws every shadow-casting mesh again. The piece gets a cheap blob shadow.
- **Effects:** no post-processing (glow, SSAO, SSR).
- **Distance haze:** the renderer's depth/height fog is supported, but it's 8-bit and can band, so we fall back to haze computed in the terrain shader if it looks poor.
- **Sea:** opaque, so there's no transparency overdraw.
- **Textures:** none on the terrain.
- **Labels and pins:** only the **current leg's** pins (≤ 7) have labels; other stops are small dots.
- **Shader warm-up:** this renderer can't pre-compile shaders, so the first use of a material can stutter. Every material is drawn once, off-screen, during the loading screen.
- **Nothing that's slow on budget PowerVR GPUs:** no skeletal animation and no GPU particles in M1. PowerVR drivers recompile those shaders on every launch.
- **Anti-aliasing:** MSAA stays **off on PowerVR GPUs**, because of a known grey-artifact bug on the GE8320.
- **Frame pacing:** Android's frame-pacing helper only works with Godot's Vulkan renderer, not this one. M1.2 measures how smooth a 30 FPS cap actually is on your phone. If it judders, we switch to an uncapped 60 FPS at a lower render scale.
- **Quality tiers:**

| | Low | Medium | High |
|---|---|---|---|
| Render scale | 0.75 | 1.0 | 1.0 |
| Anti-aliasing | off | off | MSAA 2× (never on PowerVR) |
| FPS cap | 30 | 30 | 60 |
| Terrain detail bias | lower | normal | higher |
| Idle FPS cap | 15 | 15 | 30 |

- **First launch:** **≤ 3 GB RAM → Low**, otherwise Medium. You can change it in Settings.

### 8.6 Learning-content extension points (built in M1, used from M3)

These are cheap and invisible in M1, but they mean M3 can add lessons without breaking saves or reworking the map:
1. **Stable ids.** The 78 stop ids in `journey.json` are final; saves and lessons refer to them.
2. **Journey fields.** `journey.json` carries `legs`, `year_src`, `place_in_handbook`, `start`, and `content` (= the stop id). The map uses `legs` and `start` in M1.
3. **Save.** Per-stop `lesson_done` and `best_quiz_score`, plus an empty `learn` object and a `learn_schema` number (section 3.10).
4. **Content slot.** The arrival card's content slot can host a lesson scene that emits `lesson_finished(stars)` and `lesson_closed`.
5. **Reserved autoloads.** `Learner`, `Review` and `Quiz` exist as empty stubs. `Content.get_for_stop(id)` returns nothing in M1, so the card shows the placeholder.
6. **Content location.** From M3, lessons and questions live in `game/content/`, generated from `content-src/` and kept separate from code. Each file records the handbook **edition and impression** it was checked against (section 12.3).

### 8.7 Automated tests

`./tools/test.sh` runs:
- **Godot headless tests:**
  - journey data validation (section 4)
  - progression rules, including legs and the optional prologue
  - save/load round-trip, plus handling of a corrupt save
  - projection accuracy against known landmarks
  - tuning override merge
- **Python unit tests** for the map generator.
- **Smoke run:** boots the main scene headless for ~300 frames and fails on any script error.
- **From M3:** content checks: every fact belongs to exactly one lesson; at most 9 core and secondary facts per lesson; card and question length and reading level; no approved question uses a pending fact; and the question bank rules (`docs/LEARNING_DESIGN.md`, section 5.8).
- **The copyright guard** runs locally only, because it needs the handbook text, which never enters the repo.

Claude runs these **before every push**, in its own cloud machine. They don't need CI.

## 9. Performance targets

**Baseline device:** budget Android 11+ phone with 2–3 GB RAM and a GPU in the class of PowerVR GE8320, Mali-G52 MC2 or Adreno 610. Your phone is the reference, and its exact model is open question 1.

| Metric | Target (Low tier on baseline) |
|---|---|
| Frame rate | **30 FPS sustained**, 1% low ≥ 25 FPS in the benchmark |
| Smoothness | 95% of frames within 36 ms (no visible judder) |
| Cold start → map | ≤ 10 s (≤ 5 s on mid-range) |
| Memory (PSS) | ≤ 300 MB |
| Draw calls per frame | ≤ 100 |
| Visible triangles | ≤ 150k |
| Test APK (2 architectures) | ≤ 90 MB |
| Store download per device | ≤ 50 MB |
| Heat | 20-minute session without falling below 30 FPS |
| *From M3:* opening a lesson | ≤ 300 ms; card swipes hold 30 FPS |
| *From M3:* lesson art and content | Images ≤ 40 KB each (WebP); whole content pack ≤ 20 MB |

Each build's benchmark result goes into `docs/PERF_LOG.md`, so regressions are caught early.

## 10. Your development workflow (Windows 11 ARM64 + WSL, Ubuntu 26.04)

Everything runs **natively on ARM64 inside WSL**. Test builds never touch GitHub Actions.

### 10.1 One-time setup (~15 minutes, mostly downloads)

1. **Phone:**
   - Settings → About phone → tap *Build number* 7 times, which enables Developer options.
   - Developer options → **Wireless debugging: ON**.
   - The phone and the laptop must be on the same Wi-Fi.
2. **WSL:**
   ```bash
   git clone https://github.com/mrsjoberg/BQ.git && cd BQ
   ./tools/setup_wsl.sh
   ```
   This installs Java 17, `adb`, `apksigner`, Python 3 and NumPy, all from Ubuntu's own ARM64 packages. Google doesn't publish ARM64 Linux versions of its Android tools, so these are the native route. It also:
   - downloads Godot 4.7.2 for Linux ARM64 (~77 MB) and **only the Android parts** of the export templates (~230 MB instead of the full 1.3 GB bundle) into `~/.local/share/bq-tools/`, checking them against Godot's published checksums;
   - builds a tiny "Android SDK" folder that points Godot at Ubuntu's `adb` and `apksigner`, the only two tools it needs;
   - creates a **debug signing key outside the repo**;
   - runs a health check.
3. **Pair the phone once:**
   - Run `./tools/phone.sh pair`.
   - On the phone: Wireless debugging → *Pair device with pairing code*.
   - Type the IP:port and the code it shows.
   - Ubuntu's `adb` can't discover the phone on its own, so after pairing the script switches the phone to a **fixed port** (5555). After that, `phone.sh` reconnects by itself until the phone restarts. The phone still accepts only your paired laptop's key. After a restart, `phone.sh connect` asks once for the IP:port shown under Wireless debugging.

### 10.2 Every day: one command

```bash
git pull
./tools/phone.sh        # build → install → launch → show the game's log
```

Each command below is run as `./tools/phone.sh <command>`:

| Command | Does |
|---|---|
| `./tools/phone.sh` | Build, install, launch and follow the logs (the usual one) |
| `phone.sh build` | Build the test APK only (`build/bq-dev.apk`) |
| `phone.sh install` | Install the last build |
| `phone.sh connect` | Reconnect over Wi-Fi after the phone restarts (asks for the IP:port shown on the phone) |
| `phone.sh logs` | Show the game's log from the phone |
| `phone.sh bench` | Start the benchmark and print the result |
| `phone.sh pull-tuning` | Copy your on-phone tuning into the repo |
| `phone.sh doctor` | Check the toolchain and connection, and explain any problem |

- **Every build is stamped.** The title screen and About show version + commit, e.g. `0.1.0 (a1b2c3d)`, so you always know exactly which build you're testing.
- **Fallbacks** if Wi-Fi debugging misbehaves (for example a VPN, or a router that isolates devices):
  - **(A)** WSL "mirrored" networking (one line in `.wslconfig`).
  - **(B)** the Windows `adb.exe` (USB cable or Wi-Fi), which the script auto-detects through WSL.
  - **(C)** the manual GitHub workflow *Android test APK*: download the APK on the phone from its release page.

### 10.3 Validating a build

Use the 5-minute checklist in **Appendix A**, then send feedback using **Appendix B**.

### 10.4 Claude's side

A session-start script installs Godot in Claude's cloud machine. Before pushing, Claude runs `./tools/test.sh` and a full test export, so broken builds don't reach you and **no CI run is needed** to verify Claude's work.

## 11. CI policy: run only when necessary

- **Nothing runs automatically** on push or pull request.
- **Workflows** (all started by hand, or by a release tag):

| Workflow | Trigger | Purpose | Arrives in |
|---|---|---|---|
| `android-test-apk.yml` | manual | Build a test APK and attach it to a pre-release you can open on the phone | M1 (fallback only) |
| `android-release.yml` | tag `v*` or manual | Signed release bundle (AAB) + APK; later, upload to Google Play testing | M5 |
| `ios.yml` | manual | iOS build on a macOS runner → TestFlight | M6 |

- **Thrift settings:**
  - Godot is cached, and only the needed parts of its export templates are fetched.
  - Duplicate runs cancel each other.
  - Every job has a timeout.
  - No build matrices.
- **Cost:** while the repo is **public**, GitHub's standard runners cost nothing, macOS included. Only "larger" runners are billed, and we never use them. If the repo ever goes private, the Free plan includes 2,000 minutes a month and macOS minutes count 10×, so iOS builds would need to stay rare.
- **Keeping builds:** on public repos, workflow artifacts are deleted after at most 90 days. Builds worth keeping are attached to a **GitHub Release** instead.
- **Secrets** (signing keys, store credentials) live only in GitHub Secrets, never in the repo.
- **Forks** can't trigger any workflow.

## 12. Release plan (later milestones; nothing here is needed for M1)

Facts below were checked in October 2026. Re-check them at the start of M5 and M6, because store rules change.

### 12.1 Android: Google Play (M5)
- **Account:** a Google Play developer account, **US$25 one-off**. You must be 18+ and verify your ID and a device.
- **Closed test first:** personal accounts created after 13 Nov 2023 must run a **closed test with at least 12 testers opted in for at least 14 days in a row**. Only then can you apply for production, and the review takes up to about 7 days. **Start recruiting testers during M4.**
- **Build requirements:**
  - App Bundle (**AAB**), with **Play App Signing**.
  - **Target API 36** (Android 16) for new apps and updates. This has applied since 31 Aug 2026.
  - **64-bit** support.
  - **16 KB memory page** compatibility for native code (the game engine). Treat this as enforced now.
- **Developer verification:**
  - Apps on Play must be registered, which Play does automatically for most apps.
  - **Installs over adb, which is our test workflow, are exempt.**
  - Installs from outside Play in the UK are expected to need verification from 2027 (date not announced).
  - Google's free **limited-distribution** account can share test builds with up to 20 devices outside Play. That's handy for friends and family testing.
- **Store listing:**
  - **Data safety:** "no data collected" (true while the app has no network access).
  - Content rating questionnaire.
  - Privacy policy page.
  - Screenshots.

### 12.2 iOS: App Store (M6)
- **Account:** the **Apple Developer Program, US$99 a year**. It's needed for any iPhone testing, TestFlight or the App Store.
- **Build requirements:** uploads must be built with **Xcode 26 or later and the iOS 26 SDK** (since 28 Apr 2026).
- **No Mac needed for builds:** GitHub's free `macos-26` runners (default Xcode 26.6) build and upload, and they cost nothing while the repo is public.
  - Creating the signing certificate is easiest on a Mac, but it can be done with OpenSSL plus the App Store Connect API, or by borrowing a Mac for half an hour once.
- **Testing:**
  - TestFlight builds expire after 90 days.
  - The first build for external testers goes through Apple review.
  - You need **an iPhone** (yours or borrowed) or TestFlight testers. Without a Mac there's no local simulator, but the CI runner can boot the iOS Simulator for a smoke test, because the Simulator supports Godot's Compatibility renderer.
- **Godot on iOS:**
  - Minimum iOS version **15.0**.
  - The Compatibility renderer runs on Apple's **deprecated OpenGL ES**. It works today. If Apple ever removes it, or it performs poorly, iOS switches to Godot's Metal-based *Mobile* renderer, since iPhones from iOS 15 onward handle it well.
  - Other iOS-specific checks: safe areas, performance on older iPhones.

### 12.3 Content edition (matters from M3)
- **Source:** the test is based only on *Life in the United Kingdom: A Guide for New Residents*, **3rd edition (2013)**. It is reprinted with corrections; the latest amendment list is from January 2026 (King instead of Queen, updated honours titles, Senedd changes, X instead of Twitter, and more).
- **Our copy:** the PDF you supplied mixes 2013 wording with some later edits. That's why 87 facts are flagged (section 7.1). The latest **official reprint** is the authority: before the lessons that teach a flagged core fact ship, a person compares it with the reprint, then marks it verified, rewrites it, or retires it.
- **The test itself:** 24 questions in 45 minutes; you need 75% to pass. These two numbers aren't in the handbook, so they are re-checked on the official test page before launch.
- **A refresh is coming:** the Home Office is **reviewing and refreshing the test**, but no revised handbook had been published by October 2026. A new test-service contract is being procured to start around late 2027, and the current one runs to March 2028.
- **What that means for us:** every fact, lesson and question is **tagged with the handbook edition and impression** it was checked against, and kept as data separate from code. A new edition is swapped in with the diff process in section 7.9.

### 12.4 Compliance basics
- **Credits:** data and font attributions in About and in `CREDITS.md`.
- **Legal notice:** the code is public but **all rights reserved** (see `README.md`).
- **Handbook:** About says the app is based on the official handbook and is **independent, not endorsed by the Home Office**. All text is in our own words (section 7.9).
- **Accessibility:** reading level B1 with a tap glossary from M3, and a basic pass before release (text size, contrast, reduce motion).

---

# Part C: Plan

## 13. Milestones

| | Milestone | Outcome |
|---|---|---|
| **M0** | Spec | This document, reviewed and approved |
| **M1** | **Journey skeleton** | The full 78-stop journey playable on your phone through one command. Developer menu, tuning, benchmark, tests |
| M2 | Feel and look pass | Camera and travel tuned from your testing; final moods; avatar and era vehicles; landmark models; basic audio |
| M3a | Learning content: the journey | Content pipeline (`syllabus.csv` → game files) and validators; a lesson for each of the 78 journey stops; progress saved; the journey's 19 flagged core facts verified or retired |
| M3b | Learning content: the Passport | The 72 Passport lessons on 10 pages, echo unlocks, map-tap drills with the temporary highlight, the Citizenship Desk and the briefcase; the Passport's 25 flagged core facts verified or retired |
| M4 | Practice and test prep | Spaced reviews on the map, quick review, chapter checkpoints, mock tests in the official format, readiness score, fix-it runs, test-date plan, at least 1,400 approved questions |
| M5 | Android release | Store-ready build, closed testing, launch on Google Play |
| M6 | iOS release | Apple account, CI build, TestFlight, App Store |

The acceptance criteria for M3a, M3b and M4 are in `docs/LEARNING_DESIGN.md`, section 7.1.

**M1 is delivered in five steps.** Each one is pushed to the branch so you can install it and react early.

| Step | You can test |
|---|---|
| M1.1 Toolchain + "hello map" | `phone.sh` works end-to-end; app with build stamp and a flat placeholder map |
| M1.2 Terrain + camera | Real UK terrain, sea, pan/zoom/recentre, quality tiers, stats overlay |
| M1.3 Journey | Pins and legs, travel and boats, arrival cards, guided order, save/resume (prologue and chapter I, with Skip to the Romans) |
| M1.4 Chapters | All 78 stops in 8 chapters, time-jumps, moods, shared-place fan-out, end of journey, free roam |
| M1.5 Tuning + performance | Full developer menu, live tuning, benchmark, performance pass on your phone |

### M1 acceptance criteria

1. On WSL (Ubuntu 26.04, ARM64), `./tools/phone.sh` builds the test APK and installs it on your phone over Wi-Fi **without any CI run**.
2. The whole journey plays: the optional prologue (with Skip to the Romans) and 7 chapters, **78 stops** in legs of at most 7, guided order, sea crossings, time-jumps, end screen, free roam.
3. The map shows the UK with smooth stylised terrain from real elevation data. Stops sit within 2 km of their true positions (automated test).
4. Pan, pinch-zoom, double-tap recentre and travel-follow feel responsive, and a pan never registers as a tap, including on stops that share a place.
5. Force-closing at any point and relaunching resumes the journey correctly.
6. The developer menu offers the overlay, jump/unlock/reset, live tuning with save/copy/pull, and the benchmark.
7. On your phone at the auto-selected tier, the benchmark meets section 9, or the gap is written up in `docs/PERF_LOG.md` with a fix plan.
8. `./tools/test.sh` passes, and zero GitHub Actions runs were needed.
9. No learning, quiz or Passport content is shown. The extension points of section 8.6 are in place: stable ids, the journey fields, the empty `learn` save object, the content slot and the stub services.
10. No permissions requested and no data collected. About shows the build id, credits and the handbook disclaimer.

## 14. Risks

| Risk | Mitigation |
|---|---|
| Too slow on budget GPUs | Strict budgets, detail levels, quality tiers, benchmark from M1.2 onward, testing on your actual phone at every step |
| Stutter: no shader pre-compilation and no Android frame-pacing helper in the Compatibility renderer | Warm up shaders while loading; measure frame-time smoothness in the benchmark; choose a 30 or 60 FPS strategy from your phone's data |
| Apple removes OpenGL ES on iOS | Switch iOS to Godot's Metal-based Mobile renderer (a project setting; re-test in M6) |
| Toolchain gaps on ARM64 Linux: Google ships no ARM64 Linux Android tools, and Gradle's `aapt2` doesn't run there | Test APKs use Godot's **non-Gradle export** with Ubuntu's ARM64 `adb` and `apksigner`. Store bundles (AAB, which need Gradle) are built in CI on x86-64. Fallbacks: Windows `adb.exe` from WSL, or the manual CI APK |
| Wi-Fi debugging flakiness (no auto-discovery in Ubuntu's `adb`, port changes, router or VPN isolation) | Fixed-port reconnect, `phone.sh connect` / `doctor`, mirrored networking, Windows `adb.exe` or USB |
| **Outdated or edited facts** in the supplied PDF (87 flagged) | Flagged facts stay pending and are never quizzed until checked against the latest official reprint (section 12.3) |
| A **revised handbook/test** (a refresh is announced but not yet published) | Facts, lessons and questions are data with stable ids and edition tags; the diff-and-migrate process (section 7.9); keep a few weeks free after publication |
| **Copyright:** the handbook is Crown copyright and the repo is public | Our own words only, checked by the copyright guard; the PDF and its text are never committed; About disclaimer |
| **Content volume:** 150 lessons and ~2,300 questions | Journey lessons first (M3a), Passport second (M3b); AI-assisted drafting, but **a person checks every question against the handbook**; ship the 1,400-question minimum first |
| **Learner overload or drop-off** | Five-minute lessons, soft gates, a daily review cap, Express mode, an encouraging tone |
| **Over-confident readiness score** | Never higher than recent mock results; always shown as a number with chapter bars |
| **Map clutter** with 78 pins | Legs of at most 7, labels only on the current leg, fan-out for shared places |
| **Readers with English as a second language** | B1 target, tap glossary, picture cards, testing with real learners |
| **Anchor years and places chosen by BQ** (†, ‡) | Never quizzed; checked once against a trusted source before M3a |
| iOS with no Apple hardware or account | Builds on GitHub macOS runners; account and a test iPhone needed only from M6 |
| Store rules shift (Play testing requirements, developer verification, Apple SDK minimums) | Re-check at the start of M5/M6; release checklist in this doc |
| Public repo | All rights reserved notice; secrets only in GitHub Secrets; only openly licensed data and assets committed |
| Scope creep | M1 is strictly the journey; everything else is listed under later milestones |

## 15. Open questions (none block M1)

1. **Exact test phone model** (Settings → About phone). It lets me set the performance baseline precisely and check that its GPU behaves well.
2. **Final name and app id.** The working title is "BQ" and the app id `com.mrsjoberg.bq`. The id can't change after the first store upload.
3. **Business model:** paid, free with a one-off unlock, or something else. Ads are discouraged on budget phones.
4. **Player piece:** a pawn that changes with the era, era vehicles (marching legion → longship → horse → train → car), or a character. Decide after playing M1.
5. **Should the map itself change with the era** (towns growing, Roman roads, railways, motorways)? It's a big art-scope decision for M2.
6. **Art sourcing for M2:** open-licence (CC0) model packs, a commissioned artist, or hand-made.
7. ~~Stops abroad~~ **Resolved 2026-10-11:** the journey stays in the UK; events abroad are told from UK places with a small inset map.
8. **Languages beyond English:** M3 uses B1 English with a tap glossary. Translated glossaries for the most common first languages of test-takers can come later. Accessibility targets beyond the basics are still to be decided.
9. **Who checks the 87 flagged facts against the latest official reprint, and when?** Recommendation: you, or a reviewer you trust, with a current copy of the official handbook. The journey's 19 flagged core facts are checked before M3a ships, and the Passport's 25 before M3b. I prepare the checklist from `content-src/syllabus.csv`.
10. **The real test's mix:** can the split across chapters and question types be confirmed from an official sample? Until then the mock blueprint (section 7.6) is a labelled assumption.

## 16. Credits and data licences (planned)

| Item | Source | Licence / credit |
|---|---|---|
| Learning content | Facts from *Life in the United Kingdom: A Guide for New Residents*, 3rd edition (Home Office), as supplied in PDF form | Crown copyright. BQ uses the facts in its own words and is independent of, and not endorsed by, the Home Office |
| Elevation + sea depth | **GEBCO_2026 Grid**, GEBCO Compilation Group (2026), doi:10.5285/4f68d5c7-45eb-f999-e063-7086abc036fa | Public domain, commercial use allowed. Credit the source, imply no endorsement, not for navigation |
| UK boundary (for UK vs. context land) | **Natural Earth** 1:10m | Public domain |
| UI font | **Atkinson Hyperlegible Next** (Google Fonts copy) | SIL Open Font License 1.1, with `OFL.txt` shipped in the game |
| Engine | **Godot Engine** | MIT, with licence text shipped in the game |

---

## Appendix A: Build validation checklist (~5 minutes)

Run through this on each new build you install:

1. ☐ The title screen shows the **expected commit** (compare with `git log -1 --oneline`).
2. ☐ **Cold start**: time from tapping the icon to the map (target ≤ 10 s).
3. ☐ **Feel**: pan, flick, pinch, double-tap. Does it feel smooth? Turn on the DEV overlay: is the FPS ≥ 30?
4. ☐ **Travel** to the next stop. Is the duration right? On a sea crossing, does the boat appear?
5. ☐ **Arrival card**: readable? **Continue** works?
6. ☐ **Resume**: swipe the app away mid-travel, reopen. Is the progress kept?
7. ☐ **Time-jump**: DEV → jump to the end of a chapter, then Continue. Does it feel right?
8. ☐ **Legs and shared places**: are only the current leg's pins labelled? Can you tap each Westminster pin?
9. ☐ **Back button** behaves as expected.
10. ☐ **Benchmark**: DEV → Benchmark. Note the numbers.
11. ☐ After 10+ minutes of play: is the phone too warm, or did the frame rate drop?

## Appendix B: Feedback template

```
Build: 0.1.0 (a1b2c3d)        Phone: <model>, Android <ver>, tier <Low/Med/High>
Benchmark: avg __ FPS, 1% low __, worst __ ms, mem __ MB
Felt good:
Felt off (what, where, how often):
Bugs (steps to reproduce):
Tuning JSON (DEV → Copy tuning), if changed:
```

A short screen recording (Android's built-in screen recorder) is the fastest way to show a "feels off" problem.
