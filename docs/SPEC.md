# BQ: Game Specification

**Working title:** BQ · **Version:** draft 0.1 · **Date:** 2026-10-10 · **Status:** awaiting your review

> **What this is.** The plan for a mobile game that takes the player on a journey across a 3D map of the UK, from the Romans to today, to prepare for the *Life in the UK* test.
> **What gets built first.** Only **Milestone 1 (M1)**, the *journey skeleton*: the 3D map, travelling between stops, and chapters, as a test build for your Android phone.
> **Not built in M1.** No lessons, quizzes or tests. M1 only leaves room for them.

**How to review:** Part A is about the game, so read it first. Part B covers how it's built and tested. Part C is the plan. Section 14 lists the questions that are still open. None of them block M1.

---

## Decisions from the interview (2026-10-10)

| Topic | Decision |
|---|---|
| Engine | **Godot 4.7** (GDScript, *Compatibility* renderer for low-end phones) |
| Core journey | **Tap-to-travel diorama**: the whole UK as a tilted 3D tabletop map. Tap the next stop and your piece travels there |
| Orientation | **Portrait** only |
| Test device | **Budget Android phone, Android 11+** (exact model to confirm, see section 14) |
| Chapters | **7**, following the history chapter of the official handbook, Romans → today |
| Progression | **Guided**: one stop at a time, in date order |
| Stops in M1 | Real places, **name + year only**, no learning text |
| Art direction | **Smooth stylised** terrain built from real elevation data |
| Test builds | **One command in WSL** builds and installs on the phone over Wi-Fi. No CI needed |
| Repo / CI | Repo **stays public**. CI only runs **manually or for releases** |
| iOS | Planned but not built in M1. No Apple hardware or account yet |
| Process | Spec → your review → M1 skeleton, on branch `claude/upbeat-cray-2adgy3` |

---

# Part A: The game

## 1. Vision

The player travels across a 3D diorama of the United Kingdom **and through time**, from the Roman invasion to the present day. Every stop is a real place at a real moment. In later milestones each stop teaches part of the official *Life in the United Kingdom* handbook: history, government and law, geography, famous people and major events. The game then drills the player until they're ready to pass the Life in the UK test.

**Pillars**
1. **The journey is the menu.** Progress is a route you can see across the map, not a list of lessons.
2. **Place + time = memory.** Every fact is pinned to where and when it happened.
3. **Runs on cheap phones.** It's designed for a budget Android phone first.
4. **Short sessions.** A stop takes minutes and the game always resumes where you left off.
5. **Accurate.** Later content follows the *current* official handbook.

**Audience:** adults preparing for the test, many with English as a second language. That means plain wording, large touch targets and high-legibility text.

## 2. Milestone 1 scope: the journey skeleton

| In M1 | Not in M1 (later milestones) |
|---|---|
| Whole-UK 3D map with smooth stylised terrain from real elevation data | Lessons, facts, quizzes, practice tests, scoring |
| 7 chapters, 35 stops, guided progression | Audio and music |
| Travel animation along routes, including sea crossings | Final art (avatar, era vehicles, landmark models, era-specific towns and roads) |
| Arrival card with an **empty content slot** | Accounts, cloud save, analytics, ads, purchases |
| Time-jump transitions between chapters, then end of journey and free roam | iOS build; store release |
| Camera: pan, pinch-zoom, double-tap recentre, follow during travel | Languages other than English |
| Save/resume; Settings; About (build info, credits) | Tablet-specific layouts (they will work, but won't be tuned) |
| **Developer menu** (test builds only): stats, jump to any stop, live tuning, benchmark | |
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

- **First launch:** title screen (placeholder) → **Start journey** → the camera sweeps from the whole-UK view to the English Channel. Your piece starts **at sea off the Kent coast**, "arriving from Gaul", and the first stop (Richborough, AD 43) glows.
- **Later launches:** the game resumes exactly where you left off.

### 3.2 Screen layout (portrait)

```
┌──────────────────────────────────┐
│ I · ROMAN BRITAIN        AD 60   │ ← chapter + current year (rolls during travel)
│ ● ● ● ◉ ○                    ⚙  │ ← stop progress · settings   [DEV in test builds]
│                                  │
│              (3D map)            │
│          ▲ Hadrian's Wall        │ ← locked stop: dim pin
│                                  │
│                    @ Colchester  │ ← your piece (on the last stop visited)
│   ✦ Bath        ✓ London         │ ← next stop glows · ✓ = visited
│                      ✓ Richboro' │
│                             [◎]  │ ← recentre
├──────────────────────────────────┤
│ NEXT STOP                        │ ← bottom sheet
│ Bath · c. AD 70                  │
│ [          Travel  ▶          ]  │
└──────────────────────────────────┘
```

### 3.3 Controls

| Gesture | Result |
|---|---|
| Drag (one finger) | Pan the map, with inertia, kept inside the map edges |
| Pinch | Zoom between the whole-UK view and a ~60 km close view |
| Tap the next stop, or **Travel** | Travel there |
| Tap a visited stop | Camera flies there and re-opens its card (your piece doesn't move) |
| Tap a locked stop | Hint: "Visit *London* first" |
| Double-tap the map | Recentre on your piece |
| Tap during travel / time-jump | Skip to the end of it |
| Android **Back** | Close the card or menu that's open. On the map, it asks whether to leave |

The map is always **north-up with no rotation**, which keeps the geography consistent for learning. Camera tilt is fixed but tunable in the developer menu.

### 3.4 Chapters and stops

- A **chapter** is an era. It has a title, a year range, a mood (lighting and colour) and an ordered list of stops.
- Stops unlock **strictly in list order** (date order), and exactly one stop is "next" at any time.
- **Stop states:**
  - *Locked:* dim pin, label only when zoomed in.
  - *Next:* glowing, pulsing pin with label.
  - *Visited:* tick pin with label.
  - *Here:* your piece is standing on it.
- Only the current chapter's pins are shown in full. Earlier chapters' stops shrink to small faded dots, so the map stays uncluttered. States differ by **shape as well as colour** (colour-blind safe).

### 3.5 Travel

- **Route:** a path from your current position to the next stop, draped over the terrain and drawn as a dashed line that reveals itself just ahead of the piece. A route can bend through optional waypoints set in the data.
- **Sea crossings:** where a route crosses at least ~6 km of sea, the piece turns into a **boat** for that stretch, for example to Iona, Belfast or Stormont. Shorter water gaps such as estuaries are simply crossed, with no boat.
- **Timing:** duration = distance ÷ speed, clamped between about 1.5 s and 6 s, with ease-in/ease-out. Every number is tunable (section 6).
- **Camera:** frames the start and end, then follows the piece.
- **Year counter:** the year in the top bar **rolls forward** during travel (e.g. AD 60 → AD 70), so the piece moves through time as well as space.

### 3.6 Arrival card

On arrival the camera eases into a close regional view and the pin pops. A card slides up showing:

```
  CHAPTER I · ROMAN BRITAIN
  Bath
  c. AD 70
  ┌──────────────────────────────────────┐
  │  Lessons for this stop will appear   │ ← content slot (M3 fills this)
  │  here in a later version.            │
  └──────────────────────────────────────┘
  [            Continue            ]
```

**Continue** closes the card and the next stop starts glowing. After a chapter's last stop, **Continue** starts the time-jump.

### 3.7 Time-jump between chapters (~3 s, skippable)

1. The camera pulls back to the whole-UK view.
2. The year counter rolls quickly from the last stop's year to the next chapter's start year (e.g. AD 122 → 410). It keeps rolling during the next leg (410 → 563, Iona).
3. The lighting and colour **mood crossfades** to the new era.
4. A title card fades in and out: *"Chapter II · Anglo-Saxons & Vikings · 410–1066"*.
5. Your piece changes to the new chapter's colour, and the new chapter's first stop glows.

The journey stays **continuous**: chapter II's first leg runs from wherever chapter I ended.

### 3.8 End of journey

After the final stop (Westminster, *Today*), a **Journey complete** card shows the stops visited (35/35), the distance travelled and the time played. It has two buttons:
- **Free roam:** every stop is unlocked. Tap any stop to fly there, and the mood follows that stop's chapter.
- **Start again:** asks for confirmation, then resets progress.

### 3.9 Settings and About

- **Graphics:** Low / Medium / High. The game picks one automatically on first launch, based on the phone's memory.
- **Reduce motion:** shorter, gentler camera moves and no pulsing.
- **Reset journey** (with confirmation).
- **About:** version and **build id** (git commit), plus credits and data licences.

### 3.10 Save and resume

- The game **autosaves** after each arrival, chapter change and settings change, and whenever it goes into the background.
- The save holds: current chapter and next stop, visited stops, piece and camera position, settings, distance, play time and the save format version.
- An unreadable or unknown save is backed up and the game starts fresh. It must never crash because of a bad save.

## 4. Journey data (draft)

> **Draft for M1.** These names, years and positions exist to test the map and the journey. They will be checked against the **current edition** of the official handbook when lesson content is written (M3). Editing a stop is a one-line change in `game/data/journey.json`.

| Ch | # | Stop | Year | Lat | Lon |
|---|---|---|---|---|---|
| **I · Roman Britain** (AD 43 – 410) | 1 | Richborough | AD 43 | 51.293 | 1.332 |
| | 2 | London (Londinium) | c. AD 47 | 51.513 | -0.089 |
| | 3 | Colchester | AD 60 | 51.890 | 0.902 |
| | 4 | Bath | c. AD 70 | 51.381 | -2.360 |
| | 5 | Hadrian's Wall (Housesteads) | AD 122 | 55.013 | -2.331 |
| **II · Anglo-Saxons & Vikings** (410 – 1066) | 1 | Iona | AD 563 | 56.335 | -6.393 |
| | 2 | Canterbury | AD 597 | 51.280 | 1.083 |
| | 3 | Sutton Hoo | c. AD 625 | 52.089 | 1.338 |
| | 4 | Lindisfarne | AD 793 | 55.669 | -1.801 |
| | 5 | York (Jórvík) | AD 866 | 53.960 | -1.081 |
| **III · The Middle Ages** (1066 – 1485) | 1 | Hastings (Battle) | 1066 | 50.914 | 0.487 |
| | 2 | Runnymede | 1215 | 51.444 | -0.565 |
| | 3 | Caernarfon | 1283 | 53.139 | -4.277 |
| | 4 | Bannockburn | 1314 | 56.094 | -3.923 |
| | 5 | Bosworth | 1485 | 52.580 | -1.430 |
| **IV · Tudors & Stuarts** (1485 – 1714) | 1 | Hampton Court | 1529 | 51.404 | -0.338 |
| | 2 | Stratford-upon-Avon | 1564 | 52.192 | -1.707 |
| | 3 | Plymouth | 1588 | 50.365 | -4.142 |
| | 4 | Edinburgh | 1603 | 55.949 | -3.200 |
| | 5 | Naseby | 1645 | 52.395 | -0.990 |
| **V · A Global Power** (1714 – 1900) | 1 | Culloden | 1746 | 57.478 | -4.096 |
| | 2 | Ironbridge | 1779 | 52.627 | -2.485 |
| | 3 | Manchester | 1830 | 53.477 | -2.255 |
| | 4 | London (Hyde Park) | 1851 | 51.503 | -0.170 |
| | 5 | Belfast | 1861 | 54.608 | -5.909 |
| **VI · The 20th Century** (1900 – 1945) | 1 | Westminster | 1918 | 51.500 | -0.125 |
| | 2 | Belfast | 1921 | 54.597 | -5.930 |
| | 3 | Bletchley Park | 1939 | 51.998 | -0.741 |
| | 4 | Dover | 1940 | 51.129 | 1.321 |
| | 5 | Coventry | 1940 | 52.408 | -1.507 |
| **VII · Britain since 1945** (1945 – today) | 1 | Tilbury | 1948 | 51.454 | 0.357 |
| | 2 | Stormont, Belfast | 1998 | 54.605 | -5.832 |
| | 3 | Holyrood, Edinburgh | 1999 | 55.952 | -3.175 |
| | 4 | Senedd, Cardiff Bay | 1999 | 51.464 | -3.162 |
| | 5 | Westminster | Today | 51.500 | -0.125 |

**File format** (`game/data/journey.json`, human-editable):

```json
{
  "version": 1,
  "start": { "lat": 51.10, "lon": 1.60, "name": "The Channel" },
  "chapters": [
    { "id": "roman", "numeral": "I", "title": "Roman Britain", "years": "AD 43 – 410",
      "mood": "roman", "end_year": 410,
      "stops": [
        { "id": "richborough", "name": "Richborough", "year": "AD 43", "sort": 43,
          "lat": 51.293, "lon": 1.332, "content": "roman.richborough" }
      ] }
  ]
}
```

- `year` is the text that's displayed. `sort` is the numeric year used for ordering and the rolling counter (BC years are negative).
- `via` is an optional list of waypoints that bend a route.
- `content` reserves an id for the future lesson. It's unused in M1.
- **Automated checks:** ids are unique; `sort` never decreases across the whole journey; every stop is inside the map and within 3 km of land (this catches typos in coordinates).

## 5. The map and the look

### 5.1 Extent and projection

- **Area:** 49.0–61.0°N, 11.0°W–2.5°E. That covers Great Britain, Northern Ireland, Orkney, Shetland and the Isles of Scilly, plus the island of Ireland, the Isle of Man, the Channel Islands and the nearest strip of continental coast.
- **What's highlighted:** only **UK land** is in full colour. Everything else, including the Isle of Man and the Channel Islands (Crown Dependencies, not part of the UK), is shown **muted** and unlabelled.
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
- **Final look:** the avatar, vehicles and landmark models are open questions for M2 (section 14).

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
| Journey | Jump to any chapter or stop, unlock all, reset progress, replay a time-jump |
| Tuning | The sliders above, plus save, reset and copy |
| Performance | Quality tier, render scale, FPS cap, a **simulate low-end** preset |
| Benchmark | 60-second automatic run (pans, zooms, 3 journeys, 1 time-jump). Reports average FPS, 1% low, worst frame, peak draw calls, triangles and memory, and also writes a `BQ_BENCH {...}` line to the phone log |
| Build | Version, commit, build time |

---

# Part B: How it's built and tested

## 7. Technical design

### 7.1 Engine and project settings

- **Godot 4.7.x.** The exact patch version is pinned in `tools/godot-version`, with download checksums. Upgrades are deliberate, never automatic.
- **GDScript** with static typing everywhere. No C#: it adds a runtime, APK size and toolchain weight for no M1 benefit.
- **Compatibility renderer** (OpenGL ES 3.0), the Godot renderer intended for low-end mobile.
- **Display:** portrait locked; stretch mode `canvas_items` with `expand` aspect; UI respects the safe area (notches, rounded corners).
- **Android:**
  - CPU architectures: **arm64-v8a + armeabi-v7a**. Many budget phones run 32-bit "Android Go", so the test build includes both.
  - **Permissions: none.** No internet, so the app can't collect anything.
  - App ids: `com.mrsjoberg.bq` for store builds and `com.mrsjoberg.bq.dev` for test builds, so both can be installed side by side.
  - Names: "BQ" and "BQ Dev".
- **No physics engine use.** Taps are resolved in screen space against stop markers.

### 7.2 Repository layout

```
BQ/
├── docs/            SPEC.md (this), PERF_LOG.md (per-build measurements)
├── game/            the Godot project (project.godot lives here)
│   ├── data/        journey.json, tuning.json, moods.json
│   ├── scenes/      main, world (terrain, sea, markers, routes, piece, camera), ui
│   ├── scripts/     autoloads + components
│   ├── assets/      fonts, placeholder meshes, terrain/ (generated, not committed)
│   └── tests/       headless test runner + tests
├── tools/
│   ├── setup_wsl.sh     one-time setup in WSL (you)
│   ├── phone.sh         build / install / run / logs / tuning / benchmark (you)
│   ├── test.sh          all automated tests (Claude, optionally you)
│   ├── godot-version    pinned engine version + checksums
│   └── mapgen/          terrain generator (Python + NumPy) and its small source data
├── .github/workflows/   manual-only workflows (section 10)
├── CREDITS.md           data, font and asset licences
└── README.md
```

### 7.3 Architecture

**Global services (Godot autoloads):**

| Service | Responsibility |
|---|---|
| `Journey` | Loads and validates `journey.json`; answers "which chapter / stop / what's next" |
| `Progress` | The rules (guided order), the game state, signals such as `stop_arrived` and `chapter_changed` |
| `SaveStore` | Versioned JSON save/load with backup on corruption |
| `Tuning` | Defaults plus on-phone overrides; signals live changes so systems update instantly |
| `Geo` | Map projection (lat/lon ↔ map km) and terrain height lookup |
| `Content` | The **learning-content interface**. Returns "nothing yet" in M1 (section 7.6) |
| `DevTools` | Developer menu and overlay. Only exists in test (debug) builds |

**Game states:** `Boot → Title → Map ⇄ Travelling → Arrived → (TimeJump) → … → JourneyComplete → FreeRoam`

**Scenes:**
- `Main`
- `World`: Terrain, Sea, Markers, Routes, Piece, CameraRig, Environment
- `UI`: TopBar, BottomSheet, ArrivalCard, ChapterCard, Settings, About, DevPanel

Systems talk through signals. The UI never reaches into world internals.

### 7.4 Map pipeline

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
3. **Runtime:** each chunk switches detail level by camera distance.

**Budgets:**
- ≤ 400k triangles at full detail across the whole map.
- ≤ 150k triangles visible at once.
- ≤ 25 MB of mesh memory.
- About 40 terrain draw calls at the whole-UK view.

### 7.5 Rendering for low-end phones

- **Lighting:** one directional light and **no real-time shadows**. The piece gets a cheap blob shadow.
- **Effects:** no post-processing (glow, SSAO, SSR). Distance haze only if it's cheap in the Compatibility renderer, otherwise it's faked in the terrain shader.
- **Sea:** opaque, so there's no transparency overdraw.
- **Textures:** none on the terrain.
- **Labels and pins:** only the current chapter's (≤ 7) are shown with labels.
- **Quality tiers:**

| | Low | Medium | High |
|---|---|---|---|
| Render scale | 0.75 | 1.0 | 1.0 |
| Anti-aliasing | off | off | MSAA 2× |
| FPS cap | 30 | 30 | 60 |
| Terrain detail bias | lower | normal | higher |
| Idle FPS cap | 15 | 15 | 30 |

- **First launch:** **≤ 3 GB RAM → Low**, otherwise Medium. You can change it in Settings.

### 7.6 Learning-content extension points (designed now, built from M3)

- Every stop has a `content` id. In M1, `Content.get_for_stop(id)` returns nothing and the card shows the placeholder.
- The arrival card has a **content slot** (a container) where future lesson and quiz scenes will be mounted.
- Per-stop progress already has room for `lesson_done` and `best_quiz_score` (unused in M1).
- Content will live in `game/content/`, one file per stop, kept separate from code. Each file records the handbook **edition and impression** it was checked against (section 11.3).

### 7.7 Automated tests

`./tools/test.sh` runs:
- **Godot headless tests:**
  - journey data validation (section 4)
  - progression rules
  - save/load round-trip, plus handling of a corrupt save
  - projection accuracy against known landmarks
  - tuning override merge
- **Python unit tests** for the map generator.
- **Smoke run:** boots the main scene headless for ~300 frames and fails on any script error.

Claude runs these **before every push**, in its own cloud machine. They don't need CI.

## 8. Performance targets

**Baseline device:** budget Android 11+ phone with 2–3 GB RAM and a GPU in the class of PowerVR GE8320, Mali-G52 MC2 or Adreno 610. Your phone is the reference, and its exact model is open question 1.

| Metric | Target (Low tier on baseline) |
|---|---|
| Frame rate | **30 FPS sustained**, 1% low ≥ 25 FPS in the benchmark |
| Cold start → map | ≤ 10 s (≤ 5 s on mid-range) |
| Memory (PSS) | ≤ 300 MB |
| Draw calls per frame | ≤ 100 |
| Visible triangles | ≤ 150k |
| Test APK (2 architectures) | ≤ 90 MB |
| Store download per device | ≤ 50 MB |
| Heat | 20-minute session without falling below 30 FPS |

Each build's benchmark result goes into `docs/PERF_LOG.md`, so regressions are caught early.

## 9. Your development workflow (Windows 11 ARM64 + WSL, Ubuntu 26.04)

Everything runs **natively on ARM64 inside WSL**. Test builds never touch GitHub Actions.

### 9.1 One-time setup (~15 minutes, mostly downloads)

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
   - downloads Godot 4.7 (Linux ARM64) and its Android export templates (once) into `~/.local/share/bq-tools/`;
   - creates a **debug signing key outside the repo**;
   - runs a health check.
3. **Pair the phone once:**
   - Run `./tools/phone.sh pair`.
   - On the phone: Wireless debugging → *Pair device with pairing code*.
   - Type the IP:port and the code it shows.
   - Ubuntu's `adb` can't discover the phone on its own, so after pairing the script switches the phone to a **fixed port** (5555). After that, `phone.sh` reconnects by itself until the phone restarts. After a restart, `phone.sh connect` asks once for the IP:port shown under Wireless debugging.

### 9.2 Every day: one command

```bash
git pull
./tools/phone.sh        # build → install → launch → show the game's log
```

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

### 9.3 Validating a build

Use the 5-minute checklist in **Appendix A**, then send feedback using **Appendix B**.

### 9.4 Claude's side

A session-start script installs Godot in Claude's cloud machine. Before pushing, Claude runs `./tools/test.sh` and a full test export, so broken builds don't reach you and **no CI run is needed** to verify Claude's work.

## 10. CI policy: run only when necessary

- **Nothing runs automatically** on push or pull request.
- **Workflows** (all started by hand, or by a release tag):

| Workflow | Trigger | Purpose | Arrives in |
|---|---|---|---|
| `android-test-apk.yml` | manual | Build a test APK and attach it to a pre-release you can open on the phone | M1 (fallback only) |
| `android-release.yml` | tag `v*` or manual | Signed release bundle (AAB) + APK; later, upload to Google Play testing | M5 |
| `ios.yml` | manual | iOS build on a macOS runner → TestFlight | M6 |

- **Thrift settings:**
  - Godot and its templates are cached.
  - Duplicate runs cancel each other.
  - Every job has a timeout.
  - No build matrices.
- **Cost:** while the repo is **public**, GitHub's standard runners cost nothing, macOS included. Only "larger" runners are billed, and we never use them. If the repo ever goes private, the Free plan includes 2,000 minutes a month and macOS minutes count 10×, so iOS builds would need to stay rare.
- **Keeping builds:** on public repos, workflow artifacts are deleted after at most 90 days. Builds worth keeping are attached to a **GitHub Release** instead.
- **Secrets** (signing keys, store credentials) live only in GitHub Secrets, never in the repo.
- **Forks** can't trigger any workflow.

## 11. Release plan (later milestones; nothing here is needed for M1)

Facts below were checked in October 2026. Re-check them at the start of M5 and M6, because store rules change.

### 11.1 Android: Google Play (M5)
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

### 11.2 iOS: App Store (M6)
- **Account:** the **Apple Developer Program, US$99 a year**. It's needed for any iPhone testing, TestFlight or the App Store.
- **Build requirements:** uploads must be built with **Xcode 26 or later and the iOS 26 SDK** (since 28 Apr 2026).
- **No Mac needed for builds:** GitHub's free `macos-26` runners (default Xcode 26.6) build and upload, and they cost nothing while the repo is public.
  - Creating the signing certificate is easiest on a Mac, but it can be done with OpenSSL plus the App Store Connect API, or by borrowing a Mac for half an hour once.
- **Testing:**
  - TestFlight builds expire after 90 days.
  - The first build for external testers goes through Apple review.
  - You need **an iPhone** (yours or borrowed) or TestFlight testers, because without a Mac there is no local simulator.
  - iOS-specific checks: rendering backend, safe areas, performance on older iPhones.

### 11.3 Content edition (matters from M3)
- **Source today:** the test is based only on *Life in the United Kingdom: A Guide for New Residents*, **3rd edition (2013)**. It is reprinted with corrections (the latest amendment list is from January 2026: King instead of Queen, updated honours titles, Senedd changes, X instead of Twitter, and more).
- **The test itself:** 24 questions in 45 minutes; you need 75% to pass.
- **A refresh is coming:** the Home Office is **reviewing and refreshing the test**, but no revised handbook had been published by October 2026. A new test-service contract is being procured to start around late 2027, and the current one runs to March 2028.
- **What that means for us:** all learning content will be **tagged with the handbook edition and impression** it was checked against, and kept as data separate from code so a new edition can be swapped in.

### 11.4 Compliance basics
- **Credits:** data and font attributions in About and in `CREDITS.md`.
- **Legal notice:** the code is public but **all rights reserved** (see `README.md`).
- **Accessibility:** a basic pass before release (text size, contrast, reduce motion).

---

# Part C: Plan

## 12. Milestones

| | Milestone | Outcome |
|---|---|---|
| **M0** | Spec | This document, reviewed and approved |
| **M1** | **Journey skeleton** | The full journey playable on your phone through one command. Developer menu, tuning, benchmark, tests |
| M2 | Feel and look pass | Camera and travel tuned from your testing; final moods; avatar and era vehicles; landmark models; basic audio |
| M3 | Learning content | Lessons at stops; content pipeline checked against the current handbook |
| M4 | Practice and test prep | Quizzes, spaced repetition, mock tests in the official test format |
| M5 | Android release | Store-ready build, closed testing, launch on Google Play |
| M6 | iOS release | Apple account, CI build, TestFlight, App Store |

**M1 is delivered in five steps.** Each one is pushed to the branch so you can install it and react early.

| Step | You can test |
|---|---|
| M1.1 Toolchain + "hello map" | `phone.sh` works end-to-end; app with build stamp and a flat placeholder map |
| M1.2 Terrain + camera | Real UK terrain, sea, pan/zoom/recentre, quality tiers, stats overlay |
| M1.3 Journey | Pins, travel and boats, arrival cards, guided order, save/resume (chapter I) |
| M1.4 Chapters | All 7 chapters, time-jumps, moods, end of journey, free roam |
| M1.5 Tuning + performance | Full developer menu, live tuning, benchmark, performance pass on your phone |

### M1 acceptance criteria

1. On WSL (Ubuntu 26.04, ARM64), `./tools/phone.sh` builds the test APK and installs it on your phone over Wi-Fi **without any CI run**.
2. The whole journey plays: 7 chapters, 35 stops, guided order, sea crossings, time-jumps, end screen, free roam.
3. The map shows the UK with smooth stylised terrain from real elevation data. Stops sit within 2 km of their true positions (automated test).
4. Pan, pinch-zoom, double-tap recentre and travel-follow feel responsive, and a pan never registers as a tap.
5. Force-closing at any point and relaunching resumes the journey correctly.
6. The developer menu offers the overlay, jump/unlock/reset, live tuning with save/copy/pull, and the benchmark.
7. On your phone at the auto-selected tier, the benchmark meets section 8, or the gap is written up in `docs/PERF_LOG.md` with a fix plan.
8. `./tools/test.sh` passes, and zero GitHub Actions runs were needed.
9. No learning or quiz content. The content slot and the `Content` interface are in place.
10. No permissions requested and no data collected. About shows the build id and credits.

## 13. Risks

| Risk | Mitigation |
|---|---|
| Too slow on budget GPUs | Strict budgets, detail levels, quality tiers, benchmark from M1.2 onward, testing on your actual phone at every step |
| Toolchain gaps on ARM64 Linux: Google ships no ARM64 Linux Android tools, and Gradle's `aapt2` doesn't run there | Test APKs use Godot's **non-Gradle export** with Ubuntu's ARM64 `adb` and `apksigner`. Store bundles (AAB, which need Gradle) are built in CI on x86-64. Fallbacks: Windows `adb.exe` from WSL, or the manual CI APK |
| Wi-Fi debugging flakiness (no auto-discovery in Ubuntu's `adb`, port changes, router or VPN isolation) | Fixed-port reconnect, `phone.sh connect` / `doctor`, mirrored networking, Windows `adb.exe` or USB |
| Historical accuracy, or a **revised handbook/test** (a refresh is announced but not yet published, section 11.3) | Stops and content are data, not code; checked against the current edition at M3; every item tagged with its edition so a new edition can be swapped in |
| iOS with no Apple hardware or account | Builds on GitHub macOS runners; account and a test iPhone needed only from M6 |
| Store rules shift (Play testing requirements, developer verification, Apple SDK minimums) | Re-check at the start of M5/M6; release checklist in this doc |
| Public repo | All rights reserved notice; secrets only in GitHub Secrets; only openly licensed data and assets committed |
| Scope creep | M1 is strictly the journey; everything else is listed under later milestones |

## 14. Open questions (none block M1)

1. **Exact test phone model** (Settings → About phone). It lets me set the performance baseline precisely and check that its GPU behaves well.
2. **Final name and app id.** The working title is "BQ" and the app id `com.mrsjoberg.bq`. The id can't change after the first store upload.
3. **Business model:** paid, free with a one-off unlock, or something else. Ads are discouraged on budget phones.
4. **Player piece:** a pawn that changes with the era, era vehicles (marching legion → longship → horse → train → car), or a character. Decide after playing M1.
5. **Should the map itself change with the era** (towns growing, Roman roads, railways, motorways)? It's a big art-scope decision for M2.
6. **Art sourcing for M2:** open-licence (CC0) model packs, a commissioned artist, or hand-made.
7. **Stops abroad:** events such as Agincourt, Dunkirk and D-Day are currently told from UK places (e.g. Dover in 1940). Should the journey ever leave the UK?
8. **Languages** beyond English, and accessibility targets.

## 15. Credits and data licences (planned)

| Item | Source | Licence / credit |
|---|---|---|
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
8. ☐ **Back button** behaves as expected.
9. ☐ **Benchmark**: DEV → Benchmark. Note the numbers.
10. ☐ After 10+ minutes of play: is the phone too warm, or did the frame rate drop?

## Appendix B: Feedback template

```
Build: 0.1.0 (a1b2c3d)        Phone: <model>, Android <ver>, tier <Low/Med/High>
Benchmark: avg __ FPS, 1% low __, worst __ ms, mem __ MB
Felt good:
Felt off (what, where, how often):
Bugs (steps to reproduce):
Tuning JSON (DEV → Copy tuning), if changed:
```
