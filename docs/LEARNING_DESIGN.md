# BQ Learning Design

**Draft 0.2 · 2026-10-11 · companion to SPEC v0.2** · Written for the owner, not for engineers. It covers milestones **M3 (learning content)** and **M4 (practice and test prep)**. This version applies your decisions of 2026-10-11: the map shows only the history journey, and everything else is taught in the Passport (section 8).

> **Effect on M1.** None on features. M1 still builds no lessons, quizzes or tests. The only M1-visible change is the **journey data** (the stop list in `SPEC.md` section 4, now 78 stops) and a few empty **extension points** (section 5.4 and section 7 below). Everything else is for later.

**Files** (paths in the repository)

| File | What it is |
|---|---|
| `content-src/syllabus.csv` | The complete fact inventory: **1,046 facts**, one row per testable fact, all five handbook chapters |
| `content-src/stops.csv` | The lesson list: **150 lessons** (78 map stops and 72 Passport lessons) with chapter or Passport page, topics, fact counts, map targets and whether the handbook names each place |
| `content-src/journey_draft.json` | The 78 map stops in the `journey.json` format of SPEC section 4, ready to review (each stop says whether the handbook names its place) |
| `docs/LEARNING_DESIGN.md` | This document |
| `tools/content/copyright_guard.py` | A small local check that no text shares a long run of words with the handbook (section 5.8). It needs the handbook text, which must never be committed |

**Reading guide.** Section 3 is the heart of it (how the game is built). Section 8 records the decisions made on 2026-10-11 and the questions still open. Sections 5 to 7 are for whoever implements M3 and M4.

---

## The design in one page

1. **The handbook is bigger than its history chapter.** History (chapter 3) is only **44%** of what the test can ask. Society and culture (chapter 4) is **30%**, government, law and your role (chapter 5) is **22%**, and chapters 1 and 2 are **4%** but are explicitly tested. A game that only teaches history would leave more than half the test uncovered.
2. **Two layers.**
   - **Journey**: the guided history trip you decided, Romans to today, one stop at a time in date order. **78 map stops**, including a short optional prologue (3 stops) before the Romans. These are the only pins on the map.
   - **Passport**: everything that is not a history story, *Britain today* included: the test and values, the nations and cities, Parliament and government, law and courts, voting, money, faith and customs, culture and sport. **72 lessons ("stamps") on 10 themed pages.** The way in is the **Citizenship Desk** at the port of entry (Dover) and a briefcase button available anywhere. Stamps unlock in small batches **after each history chapter**, so modern topics are interleaved with the history they grew from. A lesson about a place shows it as a **temporary highlight** and may use map-tap questions, but leaves no pin.
3. **Every lesson is a 5-minute micro-lesson**, 150 in all (78 stops and 72 stamps): 3 story cards, 3 recall questions, a result. No lesson teaches more than **9 A+B facts** (average 6).
4. **Spaced repetition runs on the map.** Facts you are about to forget make their pin glow, and the Citizenship Desk glows with a count when Passport facts are due. A **Review run** is a short trip through up to 5 glowing places. Algorithm: a 6-box **Leitner** schedule (1, 3, 7, 16, 35 days), squeezed automatically when a test date is set.
5. **Mock tests copy the real format**: 24 questions, 45 minutes, 75% to pass (18 of 24). A **readiness score** estimates your chance of passing, and the weakest topics turn into "fix-it" runs.
6. **Time needed**: about **28.5 hours** for everything, about **15 hours** for the core (A) facts only. Plans for 8, 4 and 2 weeks are in section 3.8.
7. **Handle with care**: **87 facts are time-sensitive or conflict** with something else (monarch, Senedd, Brexit, TV licence and more). They stay "pending" until a human compares them with the latest *official* reprint (section 6).
8. **Decided on 2026-10-11:** Journey plus Passport (no separate map layer for modern topics), an optional prologue, all 78 stops in M1, a soft 70% gate, and my recommendations for decisions 5, 7 and 9 to 13. **Still open:** who verifies the 87 flagged facts (section 8).

---

## 1. Handbook at a glance

### 1.1 What the source is

- **Source:** the PDF rendition by "Britizen" of *Life in the United Kingdom: A Guide for New Residents*, 3rd edition (2013), Crown copyright. 98 pages. Some passages were edited after 2013 (the monarch, Brexit, the 2015 to 2024 governments, a 56-country Commonwealth table). Section 6 lists them.
- **What the test can ask:** the handbook says the 24 questions are "based on ALL parts", including chapter 1 and chapter 2. The question set differs for each person.
- **What is not in the PDF:** the **45-minute limit** and the **75% pass mark**. They come from your SPEC (checked October 2026). They are in `syllabus.csv` as `TST-020` and `TST-021`, flagged `needs-check`.
- **Pages 96 to 98** (a "Key Material and Facts" summary) were written by Britizen and contain errors. I used them only to record conflicts.

### 1.2 Chapters

| Chapter | Pages | A | B | C | Total | Share |
|---|---|---:|---:|---:|---:|---:|
| 1 Values and principles | 4-7 | 12 | 12 | 7 | 31 | 3% |
| 2 What is the UK | 8-9 | 9 | 1 | 1 | 11 | 1% |
| 3 A long and illustrious history | 10-42 | 202 | 220 | 37 | 459 | 44% |
| 4 A modern, thriving society | 43-71 | 121 | 116 | 74 | 311 | 30% |
| 5 Government, the law and your role | 72-95 | 130 | 81 | 23 | 234 | 22% |
| **Total** | 4-95 | 474 | 430 | 142 | 1046 | 100% |

### 1.3 Sections, pages and fact counts

The priority letters mean:

| Priority | Meaning | Used for |
|---|---|---|
| **A** | Core and highly testable: dates, firsts, key people, numbers, rules, lists the handbook stresses | Always taught and drilled; the "fast track" |
| **B** | Secondary: named works, people, places, details | Taught in full mode; drilled less often |
| **C** | Context: colour that helps the story | Shown on story cards; never drilled on its own |

| Handbook section | Pages | A | B | C | Total |
|---|---|---:|---:|---:|---:|
| 1.1-1.4 Chapter 1: Values, becoming a resident, the test | 4-7 | 12 | 12 | 7 | 31 |
| 2.1-2.2 Chapter 2: What is the UK? | 8-9 | 9 | 1 | 1 | 11 |
| 3.2 Britain since 1945 | 11-15 | 27 | 38 | 6 | 71 |
| 3.3 A global power (1689 to 1900) | 16-22 | 57 | 50 | 9 | 116 |
| 3.4 The 20th century | 23-26 | 21 | 30 | 3 | 54 |
| 3.5 The Middle Ages | 27-31 | 20 | 26 | 4 | 50 |
| 3.6 The Tudors and Stuarts | 32-38 | 47 | 51 | 4 | 102 |
| 3.7 Early Britain (Stone Age to 1066) | 39-42 | 30 | 25 | 11 | 66 |
| 4.2 Arts and culture | 44-50 | 24 | 38 | 29 | 91 |
| 4.3 Customs and traditions | 51-53 | 18 | 9 | 1 | 28 |
| 4.4 Leisure | 54-58 | 15 | 15 | 24 | 54 |
| 4.5 Places of interest | 59-61 | 10 | 4 | 1 | 15 |
| 4.6 Religion | 62-63 | 16 | 3 | 0 | 19 |
| 4.7 Sport | 64-67 | 17 | 21 | 11 | 49 |
| 4.8 The UK today | 68-71 | 21 | 26 | 8 | 55 |
| 5.1-5.2 Government intro and development of democracy | 72-73 | 9 | 2 | 0 | 11 |
| 5.3 The British constitution | 74-78 | 27 | 15 | 3 | 45 |
| 5.4 Fundamental principles, tax, driving | 79-81 | 22 | 12 | 0 | 34 |
| 5.5 Respecting the law, police, courts | 82-85 | 27 | 17 | 0 | 44 |
| 5.6 The government, devolution, voting | 86-89 | 33 | 23 | 7 | 63 |
| 5.7 The UK and international institutions | 90-92 | 9 | 3 | 2 | 14 |
| 5.8 Your role in the community | 93-95 | 3 | 9 | 11 | 23 |
| **All chapters** | 4-95 | **474** | **430** | **142** | **1046** |

### 1.4 What the inventory looks like

| Measure | Value |
|---|---|
| Facts in total | **1,046** (A 474 · B 430 · C 142) |
| Facts tied to a real place (name plus coordinates) | 176 |
| Facts with a year | 490 |
| Kinds | rule 175 · event 175 · person 170 · date 146 · term 140 · list 98 · number 70 · place 66 · value 6 |
| Facts flagged | 87 (time-sensitive 66 · needs-check 35 · summary-conflict 14 · ambiguous 5; some carry two or three flags). One more fact carries `quote`, an informational flag for a quoted poem title |

**How to read a row.** Every row is one fact in my own words, at most 200 characters, with the handbook section and PDF page, a kind, a year (blank if the handbook gives none), a place with coordinates when the handbook ties the fact to a location, the **lesson** where it is taught (the `stop_id` column), a priority and flags. Ids are stable: `HIS-ROM-003` (history, Roman, 3rd fact), `GOV-PAR-012`, `SOC-SPO-007`, `VAL-001`, `TST-009`, `UKG-004`.

**Years.** The `year` column holds only years the handbook states or clearly implies (for example "about 10,000 years ago" gives -8000). A year that I chose for a stop's pin (for example Hadrian's Wall, AD 122) lives in `stops.csv` and is marked **†** below. Questions must never rely on a † year.

### 1.5 Topics the handbook itself says to expect

The chapter openers (they appear to be commentary added by the PDF's publisher, so treat them as hints, not as official policy) stress these. The design gives each one extra drilling:

- Chapter 2: how **Great Britain, the British Isles and Britain** differ, and what the **Crown dependencies** are.
- Chapter 3: the relationship of monarch and Parliament, Protestants and Catholics, Britain and its colonies; the growth of the vote; and the handbook says the dates it gives all matter.
- Chapter 4: identifying **cities** such as Leeds and Bradford; the sizes of ethnic and religious groups and their festivals; who each named person is; **Olympic medals** (who won what); poems, films and books; landmarks.
- Chapter 5: the monarch's role and powers; how the two Houses are appointed; the Speaker and the cabinet; voting and standing for election; the devolved administrations; the differences between the **Commonwealth, EU, UN and NATO**; the differences between **courts** in each nation.

---

## 2. Learning principles and how BQ applies each one

| Principle | What the research says, in one line | What BQ does (short version) |
|---|---|---|
| Retrieval practice and instant feedback | Recalling beats re-reading | Every lesson ends with 3 questions; each wrong answer shows the right one at once with a 1-line reason |
| Spaced repetition | Reviews just before forgetting stick best | 6-box Leitner schedule per fact; due facts glow on their pin, or on the Citizenship Desk for Passport stamps |
| Map as memory palace, time anchoring | Place and sequence are strong memory hooks | Journey pins are the "rooms", the guided route is the fixed walk, the year counter is the time spine; Passport pages and pictures are a second, book-shaped palace |
| Chunking | Working memory holds only a few items | At most 9 A+B facts per lesson, 3 cards, 3 linked facts per card |
| Interleaving | Mixing topics improves long-term recall | Review runs, "echo" lessons and checkpoints mix chapters on purpose |
| Elaboration and storytelling | "Why" and "so what" create links | Cause-and-effect cards, recurring story threads, a "because" question in each lesson |
| Dual coding | Words plus pictures beat words alone | Every card has a visual key; the map, flags and timeline carry meaning |
| Mastery thresholds | Move on when it is solid, not just seen | Four mastery levels per lesson; a soft checkpoint per chapter |
| Exam simulation | Practising the real format reduces test anxiety | Official-format mocks, readiness score, targeted fix-it runs |

### 2.1 Retrieval practice and immediate feedback

- **Test before you feel ready.** The 3 questions come straight after the story cards, while the facts are fresh. Getting one wrong is the point: it is the moment learning happens.
- **Feedback rule:** after each answer, show (1) right or wrong, (2) the correct answer in plain words, (3) one sentence of why, (4) a button to re-read the matching card. Never just "Incorrect".
- **Second chance.** A missed question comes back at the end of the same lesson (a "retry"). It is not scored; if the retry is right, the fact moves to box 2 and is due again tomorrow.
- **No timers in lessons.** Timers belong to mocks only. Many players read English as a second language.
- **Question variants.** Each fact has several questions (section 4). The scheduler never repeats the same wording twice in a row, so the player learns the fact, not the answer position.

### 2.2 Spaced repetition: the algorithm

**Choice: a 6-box Leitner schedule, per fact** (not per question). I recommend it over FSRS for version 1 because it is easy to explain, easy to test headlessly, needs no tuning data, and gives a predictable daily load when a test date is fixed. FSRS stays a possible upgrade once there is real usage data (section 8, decision 9).

| Box | Meaning | Next review after entering the box |
|---|---|---|
| 0 | Not yet learned | When its lesson is played |
| 1 | Missed just now | Same session (re-asked after 5 to 8 other questions, or at the end of the lesson) |
| 2 | Fragile | **1 day** |
| 3 | Getting there | **3 days** |
| 4 | Solid | **7 days** |
| 5 | Strong | **16 days** |
| 6 | Long-term | **35 days**; after one more correct answer the fact rests for 60 days |

**Moving between boxes**

- Correct and quick (under 8 seconds, no hint): **up one box**.
- Correct but slow, or a hint was used: **stay** in the box; reschedule after the same interval.
- Wrong: **back to box 1** (re-asked in the session; then box 2 tomorrow).
- First exposure in a lesson: right first time goes to box 2; wrong goes to box 1.

**The review queue**

1. A fact is *due* when its due day is today or earlier.
2. Sort by "how overdue relative to its interval" (most overdue first); A facts before B facts when tied. C facts are never queued.
3. **Daily cap: 30 questions** (about 4 minutes; a "light day" option halves it). The rest slides to the next day.
4. **Debt guard:** if more than 80 facts are overdue, new lessons pause with a friendly "Review first" banner that the player can override.
5. **Test-date compression.** If a test date is set, with D days left, all intervals are multiplied by `clamp((D - 3) / 45, 0.25, 1)` (never below 1 day). In the last 3 days the queue becomes a "test-eve sweep" of the 40 weakest facts.
6. Limits are tunable data (like `tuning.json`), not code.

### 2.3 The map as a memory palace, and time anchoring

- **Pins are loci.** A history fact is remembered "at" a place. The guided order means the learner always walks the same route, which is the method-of-loci rule that makes a palace work.
- **One strong image per lesson.** M2 art gives each pin a distinctive landmark (a legion fort, a longship, a castle). Each Passport stamp has its own picture (a flag, a coin, a building). The card's first line says what to picture.
- **Time is the second anchor.** The year counter already rolls during travel. In lessons every date question also shows a mini timeline strip with the event's year marked.
- **Walk the palace.** A "Palace walk" mode lets the player tap the visited pins of a chapter in order, with the prompt "What happened here?" and a reveal. It is free recall along the route. A Passport page offers the same walk through its stamps ("What is on this stamp?").
- **Places in the Passport.** A Passport lesson about a place borrows the map without keeping a pin: it opens with a ring on the place (Land's End, Westminster, Lord's), and map-tap questions ask the player to tap it. When the lesson closes the ring goes. The memory hook is the stamp's page and picture, plus a place the player has just seen on the map.
- **Threads.** Five story threads connect pins across chapters, drawn as faint lines after a chapter ends: *Crown and Parliament*, *Who can vote*, *Church and faith*, *The Union (England, Wales, Scotland, Ireland)*, *Invention and industry*. The Westminster stops in chapters III, IV (twice), VI and VII, together with Downing Street in chapter V, form one visible "Parliament thread" (from the first Parliaments to today).
- **Revisit = rehearsal.** Tapping a visited stop re-opens its card (already in SPEC 3.3). Tapping a finished stamp re-opens its lesson. In M4 that re-opening offers 2 quick questions.

### 2.4 Chunking

- **Hard rule:** a lesson teaches at most **9** A+B facts. Target 5 to 8. The final list has an average of 6.0.
- **Cards:** 3 per lesson (4 for the heaviest lessons). Each card has 25 to 40 words, one picture slot and 1 to 3 linked facts.
- **C facts** appear as colour inside cards but are never asked on their own.
- **Big topics are split, not squeezed.** Parliament has 5 Passport lessons (Commons, Elections, Lords, Speaker, Ceremony), each with the same temporary highlight on Westminster.
- **Lists are chunked by meaning**, never by length (for example the 6 wives: three per card).

### 2.5 Interleaving

1. **Review runs** pull due facts from different chapters into one trip.
2. **Echo lessons.** After each history chapter, the Passport stamps linked to that era unlock (table in section 3.4). Learn about Magna Carta, and the *Criminal courts* stamp appears; learn about the Civil War, and *The monarch* appears.
3. **Callback question.** One in four lesson questions asks about an earlier lesson in the same thread.
4. **Checkpoints and mocks** always mix chapters.

### 2.6 Elaboration and storytelling

- Every lesson has a **hook** (one sentence: why this place and why now; for a stamp, why it matters), a **because-so chain** (cause, event, result) and a **remember card** (year, person, rule).
- One of the 3 lesson questions is a **"why or what next"** question (for example "Why did Parliament invite William to England?"), because explaining forces links.
- Optional **prediction pause**: before a reveal, "What do you think happened next?" with two choices. No score; it simply primes attention.
- **Plain English.** Target level B1 (the handbook's own target is ESOL Entry Level 3). Short sentences, no idioms, a tap-for-meaning glossary of about 150 words.

### 2.7 Dual coding

- Every A fact has a **visual key**: an icon, a flag, a coin, a timeline marker or a mini-map. Cards show the picture first, then the words.
- Geography facts use the **map itself**: cities and landmarks are learned by tapping the right place, with a temporary highlight in Passport lessons. The map's muted non-UK land (Isle of Man, Channel Islands, Ireland) teaches "not part of the UK" by sight.
- Audio is a later option (SPEC: not in M1 or M2). Cards must work silent.

### 2.8 Mastery thresholds

| Level | Condition (per lesson) | Shown as |
|---|---|---|
| Visited | Arrived at the stop, or opened the stamp | Tick on the pin; a faint outline on the stamp |
| Learned | Lesson finished (3 questions answered, retries done) | 1 to 3 stars from the lesson score |
| Solid | Every A fact is in **box 3 or higher** (answered right in two separate sessions) | Silver ring on the pin; silver edge on the stamp |
| Mastered | Every A and B fact is in **box 4 or higher** | Gold ring on the pin; gold edge on the stamp |

- **Chapter checkpoint:** after a chapter's last stop, 10 mixed questions. **70% or more** unlocks the time-jump with a flourish. Below 70% the game suggests the weak stops but **lets the player continue anyway** ("soft gate"). Adults with a test date resent hard gates; the readiness score, not a lock, is the honest signal.
- Journey progress is the share of stops at Solid or better, per chapter. Passport progress is the share of stamps at Solid or better, per page; a page whose stamps are all Solid shows a silver border.

### 2.9 Exam simulation

- A "Test Centre" (a building at the Citizenship Desk) offers: **Full mock** (24 questions, 45 minutes, no feedback until the end, pass at 18), **Mini mock** (12 questions, 20 minutes), **Fix-it mock** (weak topics) and **Chapter checkpoint**.
- Exam conditions: countdown, flag-for-review, a review screen, and the real pass mark. The handbook's own test-day rules (take identification and proof of address) appear as a pre-test checklist.
- Details of sampling and scoring are in section 3.7.

---

## 3. Game structure

### 3.1 Two layers: the journey on the map, the Passport beside it

| Layer | What it teaches | Order | Lessons | A / B / C facts | Where it lives |
|---|---|---|---:|---|---|
| **Journey** | History (chapter 3) plus the modern facts that history created (for example the first Parliaments, the Church of England, Remembrance Day, the devolved parliaments) | Guided, date order, one at a time | **78** | 229 / 230 / 35 | The tilted UK map: 78 pins in a prologue and chapters I to VII. **The only pins on the map** |
| **Passport** | Everything else: the test and values, the nations and cities, Parliament and government, law and courts, voting and the world, money and everyday life, faith and customs, culture, sport | Free order inside each unlocked batch; ten themed pages | **72** | 245 / 200 / 107 | The Citizenship Desk at Dover and a briefcase button. **No pins** |
| **Total** | | | **150** | **474 / 430 / 142** | |

A **lesson** is the unit of learning: one micro-lesson of at most 9 A+B facts. A journey lesson is a **stop** on the map; a Passport lesson is a **stamp** on a page. Every lesson has a stable **stop id**. Several journey stops share one place (Westminster has five; Belfast and Liverpool three each); the map shows them as a small fan-out (a proposed change, section 7).

**Why not just the history journey?** It leaves 56% of the test without a home. **Why not a plain quiz mode for the rest?** Because it throws away much of the game's memory support: the Passport keeps the same lesson format and review loop, and it borrows the map whenever a lesson is about a place. **Why no second set of pins?** The map stays a single guided route of 78 pins, which keeps it readable on cheap phones.

### 3.2 The journey

**Seven history chapters, as you decided, plus an optional prologue.** The prologue (decision 2, decided 2026-10-11) is optional: the handbook teaches the Stone, Bronze and Iron Ages and tests them. Its pins show the era (*Stone Age*, *Iron Age*) instead of a year, because the handbook dates the periods (first farmers about 6,000 years ago, bronze about 4,000 years ago) but not the sites; the sort years behind them are BQ's (†) and only order the stops.

| Chapter | Years | Stops | Legs (stops per leg) | A / B / C | Suggested mood |
|---|---|---:|---|---|---|
| 0 Prologue: Before the Romans *(optional)* | Stone Age to 55 BC | 3 | 3 | 7 / 7 / 6 | Pale dawn, chalk grey, heather |
| I Roman Britain | 55 BC to AD 410 | 3 | 3 | 7 / 5 / 1 | Warm golden afternoon (as SPEC) |
| II Anglo-Saxons and Vikings | AD 410 to 1066 | 5 | 5 | 12 / 9 / 3 | Cool misty morning (as SPEC) |
| III The Middle Ages | 1066 to 1485 | 10 | 5 + 5 | 25 / 31 / 6 | Earthy parchment (as SPEC) |
| IV Tudors and Stuarts | 1485 to 1714 | 18 | 6 + 6 + 6 | 62 / 56 / 3 | Rich red and gold (as SPEC) |
| V A Global Power | 1714 to 1900 | 17 | 6 + 5 + 6 | 46 / 45 / 8 | Smoky amber (as SPEC) |
| VI The 20th Century | 1900 to 1945 | 11 | 6 + 5 | 34 / 35 / 3 | Desaturated grey-blue (as SPEC) |
| VII Britain since 1945 | 1945 to today | 11 | 6 + 5 | 36 / 42 / 5 | Bright, clean daylight (as SPEC) |
| **Total** | | **78** | | **229 / 230 / 35** | |

**Legs.** SPEC 8.5 limits labelled pins to about 7 per chapter on cheap phones. Chapters IV and V have 17 or 18 stops, so every chapter is cut into **legs of at most 7 stops**. Only the current leg's pins are labelled; earlier legs shrink to dots. The chapter count stays at seven.

**Chapter boundaries follow the handbook.** The handbook ends the Tudor-and-Stuart section at the Glorious Revolution and starts "A global power" with the Bill of Rights (1689). To keep your 1714 boundary, I teach the Bill of Rights at the *end* of chapter IV (it is a result of 1688) and start chapter V with George I and the first Prime Minister.

**Geography.** England 59 stops, Scotland 10, Northern Ireland 5, Wales 4. Wales is thin because the handbook has little Welsh history; the Passport adds Cardiff and Swansea as lessons with a map highlight. Events abroad (Agincourt, Dunkirk, the Somme, the Boyne, Waterloo, D-Day) are told from UK places and a small inset map, so the journey never leaves the UK (this settles SPEC open question 7 unless you decide otherwise, decision 5).

**What happened to your 35 draft stops.** **31 are kept** (some re-dated or re-purposed). **4 are dropped** because the handbook says nothing that would be taught there:

| Draft stop | Outcome |
|---|---|
| Colchester, AD 60 | Dropped. Boudicca is taught at Roman London (the handbook gives her statue at Westminster Bridge) |
| Bath, c. AD 70 | Dropped. The handbook mentions Bath only for the 18th-century Royal Crescent (taught in the Passport lesson *Architecture*) |
| Lindisfarne, AD 793 | Dropped. The handbook dates the first Viking visit to **AD 789** and never names Lindisfarne; a second date would invite confusion |
| Bletchley Park, 1939 | Dropped. Turing is taught at the Cambridge stop (the handbook names Cambridge for Rutherford's team, not for Turing) |
| Edinburgh, 1603 | Re-purposed: Act of Union 1707 (Edinburgh); James VI becoming James I moves to Greenwich |
| Belfast, 1861 | Re-dated to 1801 (Act of Union and the Union Flag); the famine moves to Liverpool |
| Caernarfon, 1283 | Re-dated to **1284** (the handbook's Statute of Rhuddlan year) |
| Manchester, 1830 | Re-dated to 1832 (Reform Act) |
| Hampton Court, 1529 | Shown as "1530s" (the handbook's date for the break with Rome) |
| Dover, 1940 | Now 1939 to 1940 (war declared, fall of France, Dunkirk) |

**Reading the tables below.** **†** = the year shown at the pin was chosen by BQ and is not in the handbook (verify, never quiz). **‡** = the place is BQ's choice, because the handbook does not name it for what the lesson teaches (journey stops), or does not name the venue at all (Passport lessons about a place). A place does not count as named when the handbook mentions it only somewhere else, for example in the list of cities (Southampton, Plymouth, Newcastle, Newport), as a venue for something unrelated (Greenwich) or inside a book title (*Brighton Rock*). Two links the handbook does make count as named: Parliament sits at Westminster, and the Prime Minister's official home is 10 Downing Street. Never quiz a ‡ location; check it once against a trusted source. The coordinates are good to roughly 1 km and should be checked by the M1 test of "within 2 km of the true position".

#### Prologue: Before the Romans (Stone Age to 55 BC): 3 stops, 7 A / 7 B / 6 C

| # | stop_id | Place | Year | Lat | Lon | Topics taught | A/B/C |
|---:|---|---|---|---:|---:|---|---|
| 1 | `pro-skara-brae` | Skara Brae, Orkney | Stone Age † | 59.049 | -3.343 | Stone Age: hunter-gatherers, land bridge, Channel forms about 10,000 years ago, first farmers, Skara Brae | 2/3/3 |
| 2 | `pro-stonehenge` | Stonehenge, Wiltshire | Stone Age † | 51.179 | -1.826 | Stonehenge and its ceremonies; Bronze Age: roundhouses, round barrows, metalwork | 2/1/2 |
| 3 | `pro-maiden-castle` | Maiden Castle, Dorset | Iron Age † | 50.695 | -2.471 | Iron Age: iron tools, hill forts, Celtic languages, first coins | 3/3/1 |

#### Chapter I: Roman Britain (55 BC to AD 410): 3 stops, 7 A / 5 B / 1 C

| # | stop_id | Place | Year | Lat | Lon | Topics taught | A/B/C |
|---:|---|---|---|---:|---:|---|---|
| 1 | `rom-richborough` | Richborough, Kent ‡ | 55 BC / AD 43 | 51.293 | 1.332 | Caesar fails in 55 BC; Claudius succeeds in AD 43; Romans stay 400 years | 4/1/0 |
| 2 | `rom-london` | London (Westminster Bridge) | AD 60 † | 51.501 | -0.122 | Boudicca and her statue; Roman roads, buildings, law, plants and animals | 2/1/0 |
| 3 | `rom-housesteads` | Housesteads, Northumberland | AD 122 † | 55.013 | -2.327 | Hadrian's Wall, Picts, Housesteads and Vindolanda, UNESCO; Scotland never conquered | 1/3/1 |

#### Chapter II: Anglo-Saxons and Vikings (AD 410 to 1066): 5 stops, 12 A / 9 B / 3 C

| # | stop_id | Place | Year | Lat | Lon | Topics taught | A/B/C |
|---:|---|---|---|---:|---:|---|---|
| 1 | `ang-sutton-hoo` | Sutton Hoo, Suffolk | AD 410-600 | 52.089 | 1.338 | Romans leave 410; Jutes, Angles, Saxons; kingdoms by 600; ship burial | 4/1/1 |
| 2 | `ang-iona` | Iona, Scotland | c. AD 563 † | 56.335 | -6.393 | Irish missionaries: St Patrick and St Columba | 2/1/1 |
| 3 | `ang-canterbury` | Canterbury, Kent | c. AD 597 † | 51.280 | 1.083 | First Christians in Roman times; St Augustine; first Archbishop of Canterbury | 3/0/0 |
| 4 | `vik-york` | York, North Yorkshire ‡ | from AD 789 | 53.960 | -1.081 | Vikings from 789; Danelaw; Grimsby and Scunthorpe; Kenneth MacAlpin and 'Scotland' | 2/5/1 |
| 5 | `ang-winchester` | Winchester, Hampshire ‡ | c. AD 880 † | 51.063 | -1.308 | Alfred the Great defeats the Vikings; Danish kings; Cnut | 1/2/0 |

#### Chapter III: The Middle Ages (1066 to 1485): 10 stops, 25 A / 31 B / 6 C

| # | stop_id | Place | Year | Lat | Lon | Topics taught | A/B/C |
|---:|---|---|---|---:|---:|---|---|
| 1 | `med-hastings` | Hastings (Battle), East Sussex | 1066 | 50.914 | 0.487 | William beats Harold; William the Conqueror; Bayeux Tapestry; last invasion | 3/3/1 |
| 2 | `med-tower` | Tower of London | c. 1080 † | 51.508 | -0.076 | Domesday Book; feudalism, serfs and clans; the White Tower | 3/2/0 |
| 3 | `med-runnymede` | Runnymede, Surrey ‡ | 1215 | 51.444 | -0.565 | King John and Magna Carta: even the king is under the law | 2/2/0 |
| 4 | `med-caernarfon` | Caernarfon, Gwynedd | 1284 | 53.139 | -4.277 | Statute of Rhuddlan; Welsh castles; end of Welsh rebellions; the Pale in Ireland | 1/5/2 |
| 5 | `med-westminster` | Palace of Westminster | c. 1295 † | 51.500 | -0.125 | Parliament begins; Lords and Commons; Scottish Estates; common law and codified law | 5/3/0 |
| 6 | `med-bannockburn` | Bannockburn, Stirling | 1314 | 56.094 | -3.923 | Robert the Bruce wins; Scotland stays unconquered; The Bruce | 1/3/0 |
| 7 | `med-weymouth` | Weymouth (Melcombe Regis), Dorset ‡ | 1348 | 50.607 | -2.457 | The Black Death: one third die; labour shortages, wages, the gentry | 2/2/0 |
| 8 | `med-lincoln` | Lincoln | c. 1400 | 53.234 | -0.538 | English becomes the official language; Chaucer; Caxton; castles and cathedrals | 2/4/2 |
| 9 | `med-southampton` | Southampton, Hampshire ‡ | 1415 | 50.900 | -1.404 | Crusades; Hundred Years War; Agincourt; wool trade; foreign craftsmen | 2/4/0 |
| 10 | `med-bosworth` | Bosworth Field, Leicestershire | 1485 | 52.580 | -1.430 | Wars of the Roses; Richard III dies; Henry VII; the Tudor rose | 4/3/1 |

#### Chapter IV: Tudors and Stuarts (1485 to 1714): 18 stops, 62 A / 56 B / 3 C

| # | stop_id | Place | Year | Lat | Lon | Topics taught | A/B/C |
|---:|---|---|---|---:|---:|---|---|
| 1 | `tud-hampton-court` | Hampton Court Palace ‡ | 1530s | 51.404 | -0.338 | Henry VIII, his six wives, Wales united with England | 8/0/0 |
| 2 | `tud-canterbury` | Canterbury, Kent | 1530s | 51.285 | 1.087 | Break with Rome; Church of England; Reformation; head of the Church; Archbishop | 6/3/0 |
| 3 | `tud-greenwich` | Greenwich, London ‡ | 1547-1603 † | 51.482 | -0.008 | Edward VI, 'Bloody Mary', Elizabeth I; James VI becomes James I in 1603 | 5/4/0 |
| 4 | `tud-stirling` | Stirling Castle ‡ | 1560 | 56.123 | -3.948 | Scottish Reformation 1560; Mary, Queen of Scots; Church of Scotland | 3/5/0 |
| 5 | `tud-stratford` | Stratford-upon-Avon | 1564 | 52.192 | -1.707 | Shakespeare: plays, quotations, the Globe | 2/5/0 |
| 6 | `tud-plymouth` | Plymouth, Devon ‡ | 1588 | 50.365 | -4.142 | Spanish Armada 1588; Drake and the Golden Hind; first American colonies | 3/3/0 |
| 7 | `stu-westminster` | Palace of Westminster | 1605-1642 | 51.501 | -0.126 | Divine Right; King James Bible; Gunpowder Plot; Charles I and Parliament; five MPs | 6/2/0 |
| 8 | `stu-derry` | Derry/Londonderry ‡ | c. 1609 † | 54.996 | -7.309 | Ireland under Tudors and Stuarts; Ulster plantations | 0/6/1 |
| 9 | `stu-newcastle` | Newcastle upon Tyne ‡ | 1640 | 54.978 | -1.617 | Charles I, the Prayer Book, the Scottish army, Puritans | 1/3/1 |
| 10 | `stu-naseby` | Naseby, Northamptonshire | 1642-1649 | 52.395 | -0.990 | Civil war: Cavaliers, Roundheads, Naseby; execution 1649; the Commonwealth | 5/0/0 |
| 11 | `stu-worcester` | Worcester | 1651 † | 52.192 | -2.220 | Cromwell: Ireland, Dunbar, Worcester; Lord Protector; only republic; oak tree | 2/6/0 |
| 12 | `stu-dover` | Dover, Kent ‡ | 1660 | 51.129 | 1.321 | Restoration: Charles II returns | 1/2/0 |
| 13 | `stu-london-1666` | St Paul's Cathedral, London | 1665-1666 | 51.514 | -0.098 | Plague, Great Fire, Wren, Pepys; Habeas Corpus 1679; Jews and Huguenots | 5/3/0 |
| 14 | `stu-cambridge` | Cambridge | 1660s † | 52.205 | 0.119 | Royal Society, Halley, Isaac Newton | 2/2/0 |
| 15 | `stu-torbay` | Torbay (Brixham), Devon ‡ | 1688 | 50.395 | -3.514 | James II; William of Orange; the Glorious Revolution | 3/4/0 |
| 16 | `stu-westminster-1689` | Palace of Westminster | 1689 | 51.499 | -0.124 | Bill of Rights; Protestant monarch; ministers; Whigs and Tories; free press 1695 | 5/3/0 |
| 17 | `stu-glencoe` | Glencoe, Highland | 1690-1692 † | 56.682 | -5.100 | Battle of the Boyne; Killiecrankie; Glencoe massacre; Jacobites | 3/4/1 |
| 18 | `stu-edinburgh` | Edinburgh (Parliament House) ‡ | 1707 | 55.950 | -3.190 | Act of Union 1707 creates Great Britain; Scotland keeps its law, schools, Church | 2/1/0 |

#### Chapter V: A Global Power (1714 to 1900): 17 stops, 46 A / 45 B / 8 C

| # | stop_id | Place | Year | Lat | Lon | Topics taught | A/B/C |
|---:|---|---|---|---:|---:|---|---|
| 1 | `glo-downing` | 10 Downing Street, London | 1714-1742 | 51.503 | -0.128 | George I; first Prime Minister Walpole; ministers; 1715 Jacobite attempt | 4/4/1 |
| 2 | `glo-culloden` | Culloden, Highland | 1746 | 57.478 | -4.096 | Bonnie Prince Charlie; Culloden; clans lose power; Highland Clearances | 3/2/0 |
| 3 | `glo-glasgow` | Glasgow ‡ | 18th century | 55.861 | -4.251 | Enlightenment: Adam Smith, David Hume, James Watt | 4/1/0 |
| 4 | `glo-whitby` | Whitby, North Yorkshire ‡ | 1770 † | 54.486 | -0.614 | Captain Cook; Australia, Canada, India, southern Africa; imports | 1/3/1 |
| 5 | `glo-cromford` | Cromford Mill, Derbyshire ‡ | 1771 † | 53.113 | -1.556 | Arkwright and factories; cottage industries | 0/4/0 |
| 6 | `glo-portsmouth` | Portsmouth, Hampshire | 1776-1815 | 50.800 | -1.107 | American independence; French wars; Trafalgar; Nelson; Waterloo | 3/3/1 |
| 7 | `glo-ironbridge` | Ironbridge Gorge, Shropshire ‡ | 1779 † | 52.627 | -2.485 | Industrial Revolution: steam, coal, canals, Bessemer steel; harsh conditions | 3/5/0 |
| 8 | `glo-belfast` | Belfast ‡ | 1801 | 54.599 | -5.926 | Act of Union 1800/1801; the Union Flag and its three crosses | 5/1/0 |
| 9 | `glo-liverpool` | Liverpool ‡ | 1807 | 53.408 | -2.992 | Slave trade; Quakers; Wilberforce; 1807 ban; 1833 Emancipation Act | 4/3/1 |
| 10 | `glo-manchester` | Manchester ‡ | 1832 | 53.478 | -2.243 | Reform Acts 1832 and 1867; who could vote; wives and property | 2/6/0 |
| 11 | `glo-bristol` | Bristol ‡ | c. 1835 † | 51.449 | -2.581 | Railways: the Stephensons, Brunel, Great Western Railway | 1/2/0 |
| 12 | `glo-windsor` | Windsor Castle ‡ | 1837 | 51.484 | -0.604 | Queen Victoria; the Empire; emigration and migrants; Mahomet | 3/3/1 |
| 13 | `glo-newport` | Newport, Wales ‡ | c. 1839 † | 51.588 | -2.998 | The Chartists and their six demands | 4/0/0 |
| 14 | `glo-liverpool-irish` | Liverpool | c. 1850 | 53.411 | -2.985 | Irish famine; Irish in British cities; Fenians; Parnell and Home Rule | 1/3/0 |
| 15 | `glo-hyde-park` | Hyde Park, London | 1851 | 51.503 | -0.170 | Great Exhibition 1851; free trade; factory hours; British industry leads | 2/2/1 |
| 16 | `glo-st-thomas` | St Thomas' Hospital, London | 1854-1860 | 51.499 | -0.119 | Crimean War; Victoria Cross; Florence Nightingale | 4/0/1 |
| 17 | `glo-burwash` | Bateman's, Burwash, East Sussex ‡ | 1899-1902 | 51.007 | 0.387 | Boer War; the Empire's future; Kipling | 2/3/1 |

#### Chapter VI: The 20th Century (1900 to 1945): 11 stops, 34 A / 35 B / 3 C

| # | stop_id | Place | Year | Lat | Lon | Topics taught | A/B/C |
|---:|---|---|---|---:|---:|---|---|
| 1 | `mod-manchester` | Pankhurst Centre, Manchester | 1903 | 53.466 | -2.232 | Emmeline Pankhurst and the suffragettes | 4/2/0 |
| 2 | `mod-belfast` | Belfast ‡ | 1913-1922 | 54.595 | -5.931 | Home Rule; Easter Rising 1916; partition 1921-22; the Troubles begin | 4/4/0 |
| 3 | `mod-brighton` | Brighton, East Sussex ‡ | 1914 | 50.823 | -0.137 | First World War begins; causes; the Empire fights | 2/3/0 |
| 4 | `mod-cenotaph` | Cenotaph, Whitehall, London | 1916-1918 | 51.503 | -0.126 | Somme 1916; armistice 1918; Remembrance Day; Lutyens | 5/2/0 |
| 5 | `mod-westminster` | Palace of Westminster | 1918 | 51.500 | -0.126 | Early 1900s reforms; votes for women 1918 and 1928; Chartist aims achieved | 4/3/0 |
| 6 | `mod-glasgow` | Glasgow | 1929 | 55.859 | -4.254 | Great Depression; BBC; Baird; Keynes; cars | 2/5/1 |
| 7 | `mod-cambridge` | Cambridge | 1930s | 52.209 | 0.114 | Turing, radar, jet engine, insulin, Rutherford, penicillin | 3/4/0 |
| 8 | `mod-dover` | Dover, Kent ‡ | 1939-1940 | 51.126 | 1.318 | Hitler; war declared 1939; fall of France; Dunkirk | 4/4/0 |
| 9 | `mod-blenheim` | Blenheim Palace, Oxfordshire ‡ | 1940 † | 51.841 | -1.361 | Churchill: career, speeches, honours | 1/3/0 |
| 10 | `mod-coventry` | Coventry | 1940 | 52.408 | -1.507 | Battle of Britain; Spitfire and Hurricane; the Blitz | 2/3/0 |
| 11 | `mod-portsmouth` | Portsmouth, Hampshire ‡ | 1944-1945 | 50.797 | -1.103 | Pearl Harbour; D-Day; victory 1945; atom bombs | 3/2/2 |

#### Chapter VII: Britain since 1945 (1945 to today): 11 stops, 36 A / 42 B / 5 C

| # | stop_id | Place | Year | Lat | Lon | Topics taught | A/B/C |
|---:|---|---|---|---:|---:|---|---|
| 1 | `pos-tredegar` | Tredegar, Wales ‡ | 1945-1948 | 51.775 | -3.246 | Attlee 1945; Beveridge; NHS 1948; welfare state; Education Act 1944 | 5/4/2 |
| 2 | `pos-tilbury` | Tilbury Docks, Essex ‡ | 1948 | 51.454 | 0.357 | Post-war migration from Ireland, Europe, the West Indies and South Asia | 0/4/0 |
| 3 | `pos-jodrell-bank` | Jodrell Bank, Cheshire | 1950s | 53.236 | -2.307 | 1947 independence; NATO; Macmillan; DNA 1953; Jodrell Bank; hovercraft | 2/5/0 |
| 4 | `pos-liverpool` | Liverpool ‡ | 1960s | 53.405 | -2.989 | Swinging Sixties; Beatles; liberal laws; equal pay; voting age 18 | 3/4/1 |
| 5 | `pos-enfield` | Enfield, north London | 1967-1996 | 51.652 | -0.081 | Concorde, cash machine 1967, IVF 1978, MRI, World Wide Web 1990, Dolly 1996 | 5/2/0 |
| 6 | `pos-belfast` | Belfast ‡ | 1969-1973 | 54.601 | -5.924 | 1970s economy; direct rule 1972; Troubles deaths; Mary Peters; EEC 1973 | 3/4/0 |
| 7 | `pos-grantham` | Grantham, Lincolnshire | 1979-1990 | 52.911 | -0.642 | Thatcher; reforms; Falklands 1982; John Major | 3/4/0 |
| 8 | `pos-stormont` | Stormont, Belfast | 1998 | 54.605 | -5.832 | Good Friday Agreement 1998; NI Assembly: 90 MLAs, powers | 4/4/1 |
| 9 | `pos-holyrood` | Holyrood, Edinburgh | 1997-1999 | 55.952 | -3.175 | Devolution 1997; Scottish Parliament: 129 MSPs, powers | 6/2/0 |
| 10 | `pos-senedd` | Senedd, Cardiff Bay | 1999 | 51.464 | -3.162 | Welsh Assembly: 60 AMs, powers, 2011 law-making | 3/3/0 |
| 11 | `pos-westminster` | Palace of Westminster | Today | 51.500 | -0.124 | Reserved powers; Brown; conflicts abroad; 2010 coalition; Brexit-era governments | 2/6/1 |

**Moods and map.** The mood names above reuse SPEC 5.3. The prologue needs one new mood and one new chapter colour. Nothing else about M1's look changes.

### 3.3 Where the non-chronological content lives

The rule: **history, and the institutions that history created, are taught on the journey where they happened; everything else goes to the Passport. A Passport lesson that is about a place shows that place with a temporary highlight.**

| Handbook block | Where it lives | How |
|---|---|---|
| 1.2 Becoming a permanent resident, 1.4 The test | **Passport**, page *Welcome & the test* (*Becoming a resident*, *Taking the test*); the test lesson is available on day 1 | A short "welcome desk" story; sets expectations and the optional test date |
| 1.3 Values and principles, pledge | **Passport**, same page (*Principles and pledge*, *Responsibilities and freedoms*) with callbacks at Runnymede (rule of law), Westminster (democracy) | Echo question links the value to the history that created it |
| Chapter 2: what the UK is, Crown dependencies | **Passport**, page *The UK & its nations* (*Land's End*, *Isle of Man*) | Uses the map's own styling: the lesson opens with the muted Isle of Man, Channel Islands and Ireland; tap them to learn "not part of the UK" |
| 4.8 Cities, capitals, population, languages | **Passport**, page *The UK & its nations* (London, northern cities, Edinburgh, Belfast, Cardiff, Swansea, *John o' Groats*) | **City tap drills**: "Where is Bradford?" is answered by tapping the map |
| 4.8 Currency, equality, diversity | **Passport**, pages *Money & everyday life* (*Money*) and *The UK & its nations* (*The UK today*) | Picture cards (coins and notes) |
| 4.2 Arts and culture | **Passport**, pages *Music, theatre & the arts* and *Books, film & media*; each lesson highlights its venue while it runs (Royal Albert Hall, West End, Tate, Ealing, Edinburgh, Poets' Corner, Greenwich); the BBC lessons highlight Broadcasting House, which the handbook does not name (‡) | One venue, one story |
| 4.3 Customs and traditions | **Passport**, page *Faith & customs* ("year wheel", 4 lessons), plus place callbacks on the journey: Bonfire Night at Westminster 1605, Remembrance at the Cenotaph, Hogmanay in the *Edinburgh festivals* lesson | A calendar picture instead of a map |
| 4.4 Leisure | **Passport**: *Gardens*, *Cinema*, *Comedy and TV*, *BBC and the licence* (arts pages) and *Everyday life* (page *Money & everyday life*) | The rules (ages, pets, licence) sit in *Everyday life* |
| 4.5 Places of interest | **Passport**, page *The UK & its nations* (*London landmarks*, *National parks and landmarks*) | A map-matching drill |
| 4.6 Religion | Journey: Church of England at Canterbury (1530s), Church of Scotland at Stirling. **Passport**: *Religion in the UK* (page *Faith & customs*), patron saints inside the nation lessons | Percentages as a simple bar picture |
| 4.7 Sport | **Passport**, page *Sport* (8 lessons: Olympic Park twice, Wembley, Wimbledon, St Andrews, Aintree, Cowes, Lord's) | One event, one place, one set of heroes |
| 5.2 to 5.3 Democracy, constitution, Parliament, monarch | **Passport**, page *Government* (*How Britain is governed*, *The monarch*, five lessons on Parliament); history stops at Westminster on the journey | The Parliament thread |
| 5.4 Rights, tax, driving | **Passport**, pages *Law & courts* (rights) and *Money & everyday life* (income tax, National Insurance, driving) | Short, rule-based lessons |
| 5.5 Law, police, courts | **Passport**, page *Law & courts* (criminal and civil law, everyday offences, the police, complaints and extremism, three court lessons) | Courts are learned with a highlight on the right nation |
| 5.6 Government, devolution, voting | **Passport**: page *Government* (Prime Minister and cabinet, Opposition and parties, Civil service, Local government) and page *Voting, community & the world* (who can vote, how to vote and stand). The devolved parliaments are **journey** stops (Stormont, Holyrood, Senedd) because they are 1997 to 1999 history | Parliaments are visited where they sit |
| 5.7 International institutions | **Passport**, page *Voting, community & the world* (*The Commonwealth*; *EU, Council of Europe, UN, NATO*) | A world-map card |
| 5.8 Your role in the community | **Passport**, page *Voting, community & the world* (*Your role in the community*) | Checklist-style |

**The Passport is the mechanism for everything that is not a history story.** It is not a menu of lessons; it is a place: the *Citizenship Desk*, a small building at the port where your piece arrives (Dover; a landmark, not a stop), plus a briefcase button reachable from anywhere. Each stamp is a normal lesson (same 5-minute flow, same review glow) and earns an ink stamp on its page. This keeps "the journey is the menu" true on the map while giving the other topics an address.

### 3.4 The Passport

**What it is.** The Passport is the second layer of the game: **72 lessons, called stamps, on 10 themed pages.** It teaches everything the journey does not tell as a story: the test and values, the nations and cities, Parliament and government, law and courts, voting, money, faith and customs, culture and sport. The way in is the **Citizenship Desk**, a small building at Dover (a landmark, not a stop), and a **briefcase button** available from anywhere. **The map shows only the 78 journey pins**; a Passport lesson never leaves a pin behind.

**Pages and stamps.** A page is a spread with 4 to 12 stamps. A stamp is a normal lesson: the same 5-minute flow as a journey stop (section 3.5), the same stars and the same review badge. A finished stamp is inked; when every stamp on a page is Solid, the page gets a silver border (section 2.8).

**Lessons about a place.** 45 of the 72 stamps are about a place (a capital, Parliament, a court, a venue, a stadium, a national park). While such a lesson runs, the map behind the cards shows a **temporary highlight** (a ring) on the place, and the lesson can use **map-tap questions**: "Where is Bradford?" is answered by tapping the map. When the lesson closes, the ring disappears. The target is stored as `lat` and `lon` in `stops.csv` (for Passport lessons they mean nothing else). Seven targets are marked ‡ because the handbook never names them: Buckingham Palace, the Old Bailey (two lessons), London City Hall, Broadcasting House (two lessons) and Lord's. They are highlighted but never asked in a map-tap question. The other 27 stamps have no place and no highlight.

**How stamps unlock.** Finish a history chapter's checkpoint (or skip it) and a batch of **echo stamps** unlocks on its pages. The batch is linked to the era just finished, so modern facts meet the history that explains them. Inside a batch the order is free; the game suggests a sequence. A "welcome" batch of four stamps is available before the journey starts (the test format, the principles, and the map's own geography). **For a learner with a test date**, every stamp is unlocked from the start (section 3.8), because the order then matters less than coverage.

| Unlocks after | New Passport stamps | Stamps | A+B facts |
|---|---|---:|---:|
| Welcome (before the journey) | Taking the test; Principles and pledge; Land's End; Isle of Man | 4 | 24 |
| Chapter I | Becoming a resident; Responsibilities and freedoms; John o' Groats | 3 | 24 |
| Chapter II | England: London; England: northern cities; Scotland: Edinburgh; Northern Ireland: Belfast; Religion in the UK | 5 | 36 |
| Chapter III | Wales: Cardiff; Wales: Swansea; London landmarks; How Britain is governed; The Commons; Elections; The Lords; The Speaker and the Lords' role; Criminal and civil law; Criminal courts (England, Wales, NI) | 10 | 60 |
| Chapter IV | The monarch; Ceremony and visits; Human rights and equality; Christmas and Easter; Lent and pancakes; Festivals of other faiths; Dates and holidays; The West End; Architecture; Authors; Poets and prizes | 11 | 71 |
| Chapter V | Prime Minister and cabinet; Opposition and parties; Civil service and lobbying; Local government and media; Civil and youth courts; Scottish courts; Who can vote; How to vote and stand; The Commonwealth; Income tax; National Insurance; Money; Edinburgh festivals and Hogmanay; Galleries and prizes; British artists; Gardens | 16 | 90 |
| Chapter VI | Everyday offences; The police; Complaints and extremism; Protection from harm; Cinema; Comedy and TV; The BBC and the TV licence; Wimbledon; St Andrews; Horse racing; Sailing and rowing; Cricket and more | 12 | 62 |
| Chapter VII | National parks and landmarks; The UK today; Your role in the community; EU, Council of Europe, UN, NATO; Driving; Everyday life; Royal Albert Hall; Festivals and pop; Football and rugby; The Olympics and Paralympics; Heroes of 2012 | 11 | 78 |

**The ten pages** (the page id is used in `passport.json`):

| # | Page | Page id | Stamps | With a place | A / B / C | A+B facts |
|---:|---|---|---:|---:|---|---:|
| 1 | Welcome & the test | `welcome-test` | 4 | 0 | 14 / 15 / 7 | 29 |
| 2 | The UK & its nations | `uk-nations` | 12 | 11 | 45 / 33 / 10 | 78 |
| 3 | Government | `government` | 11 | 10 | 44 / 23 / 9 | 67 |
| 4 | Law & courts | `law-courts` | 9 | 3 | 37 / 22 / 0 | 59 |
| 5 | Voting, community & the world | `voting-world` | 5 | 0 | 18 / 15 / 15 | 33 |
| 6 | Money & everyday life | `money-life` | 5 | 0 | 22 / 7 / 5 | 29 |
| 7 | Faith & customs | `faith-customs` | 5 | 0 | 19 / 11 / 1 | 30 |
| 8 | Music, theatre & the arts | `music-theatre-arts` | 8 | 8 | 17 / 34 / 18 | 51 |
| 9 | Books, film & media | `books-film-media` | 5 | 5 | 12 / 20 / 31 | 32 |
| 10 | Sport | `sport` | 8 | 8 | 17 / 20 / 11 | 37 |
| | **Passport** | | **72** | **45** | **245 / 200 / 107** | **445** |

**Drill lessons.** Where the facts are *places* (cities, landmarks), the lesson uses a **map-tap drill** instead of story cards: the player taps the right city or landmark on the map (for example the 6 northern cities in *England: northern cities*). A drill may carry up to 9 A+B items because each item takes seconds.

**The stamps, page by page.** "Map target" is the place that is highlighted and used by map-tap questions; "none" means the lesson has no place. The unlock column uses the same batches as the table above ("Day 1" is the welcome batch).

#### Page 1: Welcome & the test (4 stamps, 14 A / 15 B / 7 C)

| # | stop_id | Lesson | Map target (place) | Lat | Lon | Topics taught | A/B/C | Unlocks after |
|---:|---|---|---|---:|---:|---|---|---|
| 1 | `pp-resident-test` | Taking the test | none | - | - | 24 questions; centres; booking; ID; language; 45 minutes and 75% | 2/6/3 | Day 1 |
| 2 | `pp-resident-route` | Becoming a resident | none | - | - | Residence requirements; ESOL route; English level; applying | 4/4/2 | I |
| 3 | `pp-values-principles` | Principles and pledge | none | - | - | Five principles; pledge; oath and affirmation; extremism | 4/2/2 | Day 1 |
| 4 | `pp-values-duties` | Responsibilities and freedoms | none | - | - | What residents should do; what the UK offers; shared values | 4/3/0 | I |

#### Page 2: The UK & its nations (12 stamps, 45 A / 33 B / 10 C)

| # | stop_id | Lesson | Map target (place) | Lat | Lon | Topics taught | A/B/C | Unlocks after |
|---:|---|---|---|---:|---:|---|---|---|
| 1 | `uk-lands-end` | Land's End | Land's End, Cornwall | 50.066 | -5.716 | The UK vs Great Britain; four nations; Ireland; Westminster and devolution | 6/1/1 | Day 1 |
| 2 | `uk-isle-of-man` | Isle of Man | Isle of Man | 54.230 | -4.550 | Crown dependencies; overseas territories; not part of the UK | 3/0/0 | Day 1 |
| 3 | `uk-jog` | John o' Groats | John o' Groats, Highland | 58.644 | -3.069 | Size of the UK; population growth; shares of each nation | 3/6/6 | I |
| 4 | `nat-london` | England: London | London | 51.507 | -0.128 | Capital; southern cities; St George; roast beef | 4/5/1 | II |
| 5 | `nat-leeds` | England: northern cities | Leeds | 53.800 | -1.549 | Leeds, Bradford, Sheffield, Manchester, Liverpool, Newcastle | 0/6/0 | II |
| 6 | `nat-edinburgh` | Scotland: Edinburgh | Edinburgh | 55.953 | -3.189 | Capital; Scottish cities; Gaelic; St Andrew; haggis | 5/3/0 | II |
| 7 | `nat-belfast` | Northern Ireland: Belfast | Belfast | 54.597 | -5.930 | Capital; Irish Gaelic; St Patrick; Ulster fry | 5/0/0 | II |
| 8 | `nat-cardiff` | Wales: Cardiff | Cardiff | 51.481 | -3.179 | Capital; Swansea and Newport; Welsh language; St David; Welsh cakes | 5/2/0 | III |
| 9 | `nat-swansea` | Wales: Swansea | Swansea | 51.621 | -3.944 | Dylan Thomas; Roald Dahl; the Eisteddfod | 1/3/0 | III |
| 10 | `plc-london` | London landmarks | London Eye, London | 51.503 | -0.119 | Big Ben and Elizabeth Tower, London Eye, Tower of London | 4/0/0 | III |
| 11 | `plc-lake-district` | National parks and landmarks | Lake District, Cumbria | 54.460 | -3.090 | 15 national parks, National Trust, Lake District, Snowdonia, Loch Lomond, Giant's Causeway, Eden | 6/3/1 | VII |
| 12 | `pp-today` | The UK today | none | - | - | Diversity; ageing; equality of men and women | 3/4/1 | VII |

#### Page 3: Government (11 stamps, 44 A / 23 B / 9 C)

| # | stop_id | Lesson | Map target (place) | Lat | Lon | Topics taught | A/B/C | Unlocks after |
|---:|---|---|---|---:|---:|---|---|---|
| 1 | `pp-constitution` | How Britain is governed | none | - | - | Democracy; unwritten constitution; main institutions | 6/1/1 | III |
| 2 | `gov-buckingham` | The monarch | Buckingham Palace, London ‡ | 51.501 | -0.142 | Role of the monarch; Prime Minister appointed; Commonwealth head; stability | 5/4/1 | IV |
| 3 | `gov-westminster-commons` | The Commons | Palace of Westminster | 51.500 | -0.125 | Constituencies, MPs, majority, coalition, what MPs do | 3/2/1 | III |
| 4 | `gov-westminster-elections` | Elections | Palace of Westminster | 51.500 | -0.125 | General Election every 5 years, by-elections, first past the post, proportional representation | 4/3/0 | III |
| 5 | `gov-westminster-lords` | The Lords | Palace of Westminster | 51.500 | -0.125 | Peers, hereditary and life peers, 1958 and 1999 changes | 3/2/0 | III |
| 6 | `gov-westminster-speaker` | The Speaker and the Lords' role | Palace of Westminster | 51.500 | -0.125 | Speaker's neutrality; Lords scrutiny; Commons can overrule; bishops | 6/2/0 | III |
| 7 | `gov-westminster-ceremony` | Ceremony and visits | Palace of Westminster | 51.500 | -0.125 | State Opening, Acts in the monarch's name, Hansard, visiting Parliament | 3/1/1 | IV |
| 8 | `gov-downing-pm` | Prime Minister and cabinet | 10 Downing Street, London | 51.503 | -0.128 | PM, Chequers, cabinet posts: Chancellor, Home, Foreign Secretaries | 6/2/1 | V |
| 9 | `gov-downing-opposition` | Opposition and parties | 10 Downing Street, London | 51.503 | -0.128 | Opposition, shadow cabinet, PMQs, main parties, independents, pressure groups | 4/2/2 | V |
| 10 | `gov-downing-civil-service` | Civil service and lobbying | 10 Downing Street, London | 51.503 | -0.128 | Civil service neutrality and values; pressure groups: CBI, Greenpeace, Liberty | 1/2/0 | V |
| 11 | `gov-city-hall` | Local government and media | London City Hall ‡ | 51.505 | -0.079 | Councils, mayors, funding, London's 33 authorities; free press; balanced broadcasting | 3/2/2 | V |

#### Page 4: Law & courts (9 stamps, 37 A / 22 B / 0 C)

| # | stop_id | Lesson | Map target (place) | Lat | Lon | Topics taught | A/B/C | Unlocks after |
|---:|---|---|---|---:|---:|---|---|---|
| 1 | `pp-law-basics` | Criminal and civil law | none | - | - | Equal treatment; criminal vs civil law; examples | 4/1/0 | III |
| 2 | `pp-law-offences` | Everyday offences | none | - | - | Weapons, drugs, racial crime, tobacco and alcohol rules | 6/1/0 | VI |
| 3 | `gov-old-bailey-criminal` | Criminal courts (England, Wales, NI) | Old Bailey, London ‡ | 51.516 | -0.102 | Judges, magistrates, Crown Court, juries of 12 | 5/3/0 | III |
| 4 | `gov-old-bailey-civil-youth` | Civil and youth courts | Old Bailey, London ‡ | 51.516 | -0.102 | County Court, High Court, small claims, Youth Court, solicitors | 2/6/0 | V |
| 5 | `gov-edinburgh-courts` | Scottish courts | Court of Session, Edinburgh | 55.950 | -3.191 | JP courts, Sheriff Court, High Court, jury of 15, Not proven, Court of Session | 2/2/0 | V |
| 6 | `pp-police-duties` | The police | none | - | - | Police duties; Chief Constables; PCCs; arrest rights | 5/2/0 | VI |
| 7 | `pp-police-complaints` | Complaints and extremism | none | - | - | Complaints bodies; terrorism and extremism; reporting | 3/2/0 | VI |
| 8 | `pp-rights-human` | Human rights and equality | none | - | - | Roots of rights; ECHR 1950; Human Rights Act 1998; equal opportunities | 5/2/0 | IV |
| 9 | `pp-rights-protection` | Protection from harm | none | - | - | Domestic violence; FGM; forced and arranged marriage | 5/3/0 | VI |

#### Page 5: Voting, community & the world (5 stamps, 18 A / 15 B / 15 C)

| # | stop_id | Lesson | Map target (place) | Lat | Lon | Topics taught | A/B/C | Unlocks after |
|---:|---|---|---|---:|---:|---|---|---|
| 1 | `pp-voting-register` | Who can vote | none | - | - | Voting age; who may vote; electoral register | 3/3/1 | V |
| 2 | `pp-voting-ballot` | How to vote and stand | none | - | - | Polling hours, ID, postal vote, standing for office | 3/3/0 | V |
| 3 | `pp-community` | Your role in the community | none | - | - | Neighbours, jury service, governors, volunteering, donating, recycling | 3/6/11 | VII |
| 4 | `pp-world-commonwealth` | The Commonwealth | none | - | - | Aims, head, size, values, members by region | 3/2/1 | V |
| 5 | `pp-world-others` | EU, Council of Europe, UN, NATO | none | - | - | EU origins and Brexit; Council of Europe; UN Security Council; NATO | 6/1/2 | VII |

#### Page 6: Money & everyday life (5 stamps, 22 A / 7 B / 5 C)

| # | stop_id | Lesson | Map target (place) | Lat | Lon | Topics taught | A/B/C | Unlocks after |
|---:|---|---|---|---:|---:|---|---|---|
| 1 | `pp-money-tax` | Income tax | none | - | - | Income tax, HMRC, PAYE, self-assessment | 4/1/0 | V |
| 2 | `pp-money-ni` | National Insurance | none | - | - | National Insurance contributions; NI number at 16; right to work | 3/3/0 | V |
| 3 | `pp-money-currency` | Money | none | - | - | Pound and pence; coins; notes; Scottish and NI banknotes | 4/0/0 | V |
| 4 | `pp-driving` | Driving | none | - | - | Ages, licence, tests, foreign licences, insurance, MOT | 5/3/0 | VII |
| 5 | `pp-leisure` | Everyday life | none | - | - | Shopping, drinking and gambling ages, pets, social media | 6/0/5 | VII |

#### Page 7: Faith & customs (5 stamps, 19 A / 11 B / 1 C)

| # | stop_id | Lesson | Map target (place) | Lat | Lon | Topics taught | A/B/C | Unlocks after |
|---:|---|---|---|---:|---:|---|---|---|
| 1 | `pp-religion` | Religion in the UK | none | - | - | Percentages; other Christian groups; no established Church in Wales/NI; saints' day holidays | 6/2/0 | II |
| 2 | `pp-calendar-christmas-easter` | Christmas and Easter | none | - | - | Christmas, Boxing Day, Easter, public holidays | 4/1/1 | IV |
| 3 | `pp-calendar-lent` | Lent and pancakes | none | - | - | Lent, Shrove Tuesday, Ash Wednesday, Easter eggs | 2/2/0 | IV |
| 4 | `pp-calendar-faiths` | Festivals of other faiths | none | - | - | Diwali, Hannukah, Eid al-Fitr, Eid ul-Adha, Vaisakhi | 5/1/0 | IV |
| 5 | `pp-calendar-dates` | Dates and holidays | none | - | - | New Year, Valentine, April Fool, Mother's and Father's Day, Halloween, bank holidays | 2/5/0 | IV |

#### Page 8: Music, theatre & the arts (8 stamps, 17 A / 34 B / 18 C)

| # | stop_id | Lesson | Map target (place) | Lat | Lon | Topics taught | A/B/C | Unlocks after |
|---:|---|---|---|---:|---:|---|---|---|
| 1 | `cul-albert-hall` | Royal Albert Hall | Royal Albert Hall, London | 51.501 | -0.177 | The Proms, Last Night, Purcell, Handel, Holst, Elgar | 3/5/1 | VII |
| 2 | `cul-glastonbury` | Festivals and pop | Glastonbury, Somerset | 51.155 | -2.586 | Britten and Aldeburgh; pop since the 1960s; Glastonbury; Mercury Prize | 4/1/7 | VII |
| 3 | `cul-west-end` | The West End | West End, London | 51.511 | -0.128 | Mousetrap, Gilbert and Sullivan, Lloyd Webber, pantomime, Olivier Awards | 3/3/1 | IV |
| 4 | `cul-edinburgh` | Edinburgh festivals and Hogmanay | Edinburgh Castle | 55.949 | -3.200 | Festival and Fringe; Hogmanay; Burns and Auld Lang Syne; the Castle; skiing | 5/2/1 | V |
| 5 | `cul-tate-galleries` | Galleries and prizes | Tate Britain, London | 51.491 | -0.127 | Galleries, Holbein and Van Dyck, Turner Prize, Pre-Raphaelites | 1/4/2 | V |
| 6 | `cul-tate-artists` | British artists | Tate Britain, London | 51.491 | -0.127 | Gainsborough, Allan, Turner, Constable, Moore, Hockney | 0/6/3 | V |
| 7 | `cul-greenwich-arch` | Architecture | Queen's House, Greenwich | 51.481 | -0.009 | Cathedrals, Inigo Jones, Wren, Adam, Gothic revival, modern architects | 1/7/3 | IV |
| 8 | `lei-kew` | Gardens | Kew Gardens, London | 51.478 | -0.295 | Allotments, famous gardens, national flowers, Capability Brown, Chelsea Flower Show | 0/6/0 | V |

#### Page 9: Books, film & media (5 stamps, 12 A / 20 B / 31 C)

| # | stop_id | Lesson | Map target (place) | Lat | Lon | Topics taught | A/B/C | Unlocks after |
|---:|---|---|---|---:|---:|---|---|---|
| 1 | `cul-poets-corner-authors` | Authors | Westminster Abbey, London | 51.499 | -0.127 | Austen, Dickens, Stevenson, Hardy, Conan Doyle, Rowling, Tolkien | 5/2/3 | IV |
| 2 | `cul-poets-corner-poets` | Poets and prizes | Westminster Abbey, London | 51.499 | -0.127 | Beowulf, sonnets, Milton, war poets, Poets' Corner, Nobel and Booker prizes | 2/6/9 | IV |
| 3 | `cul-ealing` | Cinema | Ealing Studios, London | 51.508 | -0.305 | Early cinema, Chaplin, Hitchcock, Nick Park, BAFTA, famous films | 1/6/17 | VI |
| 4 | `cul-bbc-comedy` | Comedy and TV | Broadcasting House, London ‡ | 51.519 | -0.144 | Punch, music hall, Monty Python, soaps, regional-language TV | 0/6/1 | VI |
| 5 | `cul-bbc-licence` | The BBC and the TV licence | Broadcasting House, London ‡ | 51.519 | -0.144 | Licence rules and fines; BBC funding and independence; radio | 4/0/1 | VI |

#### Page 10: Sport (8 stamps, 17 A / 20 B / 11 C)

| # | stop_id | Lesson | Map target (place) | Lat | Lon | Topics taught | A/B/C | Unlocks after |
|---:|---|---|---|---:|---:|---|---|---|
| 1 | `spo-wembley` | Football and rugby | Wembley Stadium, London | 51.556 | -0.280 | Sports born in Britain; football 1966; Premier League; rugby and Six Nations | 5/3/3 | VII |
| 2 | `spo-stratford-games` | The Olympics and Paralympics | Olympic Park, Stratford, London | 51.543 | -0.016 | 1908, 1948, 2012; Paralympic origins; Torvill and Dean; Holmes | 3/3/0 | VII |
| 3 | `spo-stratford-heroes` | Heroes of 2012 | Olympic Park, Stratford, London | 51.543 | -0.016 | Wiggins, Farah, Ennis, Hoy, Grey-Thompson, Weir, Simmonds | 3/2/2 | VII |
| 4 | `spo-wimbledon` | Wimbledon | Wimbledon, London | 51.434 | -0.214 | Origins of tennis; Wimbledon; Andy Murray | 2/1/0 | VI |
| 5 | `spo-st-andrews` | St Andrews | St Andrews, Fife | 56.343 | -2.803 | Golf: Scottish origin, home of golf, The Open | 2/1/0 | VI |
| 6 | `spo-aintree` | Horse racing | Aintree, Liverpool | 53.477 | -2.944 | Royal Ascot, Grand National, Scottish Grand National, Newmarket | 0/3/1 | VI |
| 7 | `spo-cowes` | Sailing and rowing | Cowes, Isle of Wight | 50.763 | -1.298 | Chichester, Knox-Johnston, MacArthur, Redgrave, Boat Race | 0/5/1 | VI |
| 8 | `spo-lords` | Cricket and more | Lord's Cricket Ground, London ‡ | 51.529 | -0.173 | Cricket and the Ashes; Bannister; Formula 1 | 2/2/4 | VI |

### 3.5 What happens at a lesson

**Target: about 5 minutes (4 to 6).** Everything autosaves after each card and each answer, so a lesson can be paused mid-way (SPEC 3.10).

| Step | What the player sees | Time |
|---|---|---|
| 0. Arrive | Journey: the existing arrival card (place, year, chapter), with the lesson in the content slot and a **Start** button. Passport: tap a stamp on its page; a lesson about a place shows a temporary highlight on the map behind the cards | 5 s |
| 1. Story cards | **3 cards** (4 for the heaviest lessons), swipe to advance. Card 1 is the hook and the picture. Card 2 is the because-so chain with the key facts highlighted. Card 3 is the "remember" card: year, person, rule. 25 to 40 words per card; tap a word for its meaning | 2 to 2.5 min |
| 2. Recall | **3 questions** (a 4th for lessons with 8 or 9 facts). One is a "why or what next" question; one in four is a callback to an earlier lesson in the same thread. Instant feedback after each (section 2.1) | 1.5 min |
| 3. Retry | Any missed question is asked once more | 0.5 min |
| 4. Result | 1 to 3 stars; a list of "facts learned" with their icons; the next place or stamp glows. **Missed facts go to box 1, others to box 2** | 15 s |

**Scoring.** 3 of 3 right first time is 3 stars; 2 of 3 is 2 stars; 0 or 1 is 1 star plus a friendly "ask me again later?" button. A lesson is **complete after any attempt**. Stars measure the first try; mastery (section 2.8) measures the long term.

**Chapter checkpoint.** After the last stop of a chapter: 10 questions mixing the chapter's stops (60% from facts that were missed or are in low boxes). Pass mark 70%. Pass: time-jump plays with a "chapter mastered" flourish. Fail: the game lists the weak stops and offers a **fix-it run**, but the player can continue anyway. Either way the echo stamps unlock.

**Session shape.** A typical session is 2 to 3 new lessons (10 to 15 minutes) plus one review run (3 to 5 minutes). The game ends a session gracefully: "Good place to stop; next time: Stonehenge."

**Fast track.** An "Express" setting shows only A facts and skips the travel animation: about 2 to 3 minutes per lesson. Nine lessons have no A facts (they are skipped): the journey stops `stu-derry`, `glo-cromford` and `pos-tilbury`, and the Passport stamps `nat-leeds`, `cul-tate-artists`, `cul-bbc-comedy`, `lei-kew`, `spo-aintree` and `spo-cowes`.

### 3.6 The review loop: reviews as revisits

- **Glow badges.** A journey stop with facts due shows a small amber badge with the number due (1 to 9). The **Citizenship Desk** shows the same badge with the number of Passport facts due, and inside the Passport a stamp with facts due has its own small badge. Nothing due looks normal. The home screen shows one line: "6 places to revisit (2 at the Desk), about 3 minutes".
- **Review run (the default).** Tap **Review**: the game picks up to **5 due places**: glowing journey stops and, when at least 4 Passport facts are due, the Citizenship Desk as one place. It orders them by distance, draws a short route and flies the piece through it (each leg about 1 second, skippable). At each journey stop it asks **2 to 4 questions**, mixing due facts from that stop with due facts of the **same thread** from other chapters (this is the interleaving). At the Desk it asks **3 to 6 questions** from the due Passport facts, mixed across pages. Finishing the run "refreshes" the pins and badges.
- **Quick review (no travel).** A 2-minute question set from the due queue, for low battery or a train ride. It uses the same scheduler and covers journey and Passport facts together.
- **Palace walk.** Optional free recall along a chapter's pins or through a Passport page's stamps (section 2.3). It does not change the schedule unless the player taps "I knew it" or "I missed it".
- **Overdue pins and stamps fade** gently (a grey ring) rather than turning red; the tone is encouraging.
- **Priority:** A facts are queued before B facts, and facts missed in a mock test are queued first.
- **Cost on a cheap phone:** badges are small sprites on pins that already exist, plus one on the Desk; Passport badges are ordinary page elements. No new draw-heavy effects.

### 3.7 Mock tests in the official format

**Format.** 24 questions, 45 minutes, pass at 75% (18 of 24). Nothing in the handbook PDF states the time or the pass mark; they come from SPEC 12.3 and must be re-checked on the official test page before launch (`TST-020`, `TST-021`).

**Which mocks exist**

| Mock | Questions | Time | Feedback | Purpose |
|---|---:|---|---|---|
| Full mock | 24 | 45 min | Only at the end | The real thing |
| Mini mock | 12 | 20 min | At the end | A quick temperature check |
| Fix-it mock | 24 | 45 min | At the end | Half of the questions from the learner's weakest topics |
| Chapter checkpoint | 10 | none | After each answer | Gate to the next chapter (soft) |

**How the 24 questions are sampled (blueprint v1)**

| Chapter | Questions | Why |
|---|---:|---|
| 1 Values, resident, the test | 2 | Small but explicitly tested |
| 2 What is the UK | 1 | Small; the handbook says Great Britain vs UK vs British Isles is "very likely" |
| 3 History | 8 | Largest block (44% of facts), capped so the test is not a history exam |
| 4 Society and culture | 6 | 30% of facts |
| 5 Government, law, role | 7 | 22% of facts, but rule-based and heavily emphasised |
| **Total** | **24** | |

*This blueprint is my assumption.* The Home Office does not publish a chapter-by-chapter split. If you can obtain a few real sample tests or tester reports, tune the table (it is data). A second table with the exact proportions (1 / 1 / 10 / 7 / 5 for chapters 1 to 5) can be offered as a "proportional" option.

Sampling rules:

1. Within a chapter, pick sections in proportion to their A+B size, **at most 2 questions per section** per mock.
2. Draw facts **70% A, 30% B**. C facts are never sampled.
3. **No fact twice in a mock; at most one question per lesson; no fact repeated from the last two mocks** unless the pool is exhausted.
4. Question types follow the shape of the real test (single answer about 50%, true/false pair about 20%, "which statement is correct" about 15%, "choose two" about 15%). The exact current mix is not in the handbook; verify against an official sample.
5. **Never use** facts flagged `time-sensitive`, `needs-check`, `ambiguous` or `summary-conflict` until a human marks them verified (section 6).
6. A fix-it mock takes 12 questions from the 3 weakest topics and 12 as above.

**After a mock**

- Score, pass or not, time used, and a **bar per chapter**.
- The questions missed, each with the lesson it belongs to. Tapping "Revisit these" **glows those pins** (and the Citizenship Desk for missed Passport facts) and queues the missed facts at box 1.
- The 3 weakest topics, with a one-tap **fix-it run** (10 questions: 7 from those topics, 3 random).

**Readiness score (the "will I pass?" number)**

1. For every A or B fact, estimate the chance the player recalls it from its box (assumption, recalibrate with real data): box 0 = 0.30, 1 = 0.45, 2 = 0.60, 3 = 0.72, 4 = 0.82, 5 = 0.90, 6 = 0.95. Multiply by 0.98 for each day overdue.
2. Turn recall into the chance of a *correct answer* by adding guessing: `p = r + (1 - r) x g`, with g = 0.25 for four-option questions and 0.5 for true/false pairs.
3. Combine by the blueprint: expected score per question = the blueprint-weighted average of `p` across chapters (A weighted 70%, B 30%).
4. **Pass chance** = the probability of 18 or more right out of 24, using a normal approximation: `1 - Phi((17.5 - 24p) / sqrt(24p(1-p)))`.
5. After two or more mocks, show the **lower** of the model and the recent mock results, so the number is never over-confident.
6. Labels: **90% or more** "Ready: book your test"; **75 to 89%** "Nearly ready"; **50 to 74%** "Getting there"; **below 50%** "Keep going". The player always sees the number and the chapter bars, never a bare label.

### 3.8 Total study time and a plan for a learner with a test date

**Time model** (my estimates; the real values will come from M3 and M4 telemetry-free testing with you and friends).

| Part | Full (everything) | Core only (A facts, "Express") |
|---|---|---|
| New lessons | 150 lessons x 5 min = **12.5 h** | 141 lessons x 2.5 min = **5.9 h** |
| Chapter checkpoints | 8 x 4 min = **0.5 h** | skipped |
| Spaced reviews | 904 A+B facts x about 5 reviews x 8 s = **10 h** | 474 A facts x 5 x 8 s = **5.3 h** |
| Mock tests | 6 x (45 min + 10 min of review) = **5.5 h** | 4 x 55 min = **3.7 h** |
| **Total** | **about 28.5 hours** | **about 15 hours** |

**Plans** (all steps are suggestions the game computes for you from the test date):

| Test in | Mode | Per day | New lessons per day | Reviews | Mocks |
|---|---|---|---|---|---|
| 8 weeks | Full, relaxed | about 30 min | 3 | about 10 min | 1 per week from week 5 (4 in all) |
| 4 weeks | Full, standard | about 1 hour | 6 | about 20 min | 1 mini mock at the end of week 1, full mocks in weeks 3 and 4 (6 in all) |
| 2 weeks | **Express** (A only) | about 1 hour | 10 | about 20 min | Days 6, 9, 12 and 14 |
| Under 1 week | Express plus mocks | as much as you can | A facts of the Passport first (Government, Law & courts, Voting) | the "test-eve sweep" | One a day; the readiness score is shown honestly |

**A typical 4-week plan (lesson counts are cumulative)**

| Week | Lessons finished by the end of the week | What is covered |
|---:|---:|---|
| 1 | 43 | Welcome, Prologue, chapters I, II, III and their echo stamps; a mini mock |
| 2 | 86 | Chapter IV and its echo stamps, and the first part of chapter V; checkpoints |
| 3 | 128 | Rest of V, chapter VI and their echo stamps; **first full mock** |
| 4 | 150 | Chapter VII; days 25 to 28: full mocks, fix-it runs, the test-eve sweep |

**Test-date mode** (set once on the *Welcome & the test* page): unlocks all lessons, orders the work by A-first then B, shows "on track" or "behind by N lessons", scales the spaced-repetition intervals (section 2.2) and offers Express if the learner falls more than 20% behind. It never nags with phone notifications (the app asks for no permissions; SPEC 8.1), only on opening.

---

## 4. Question design

### 4.1 Question types

Four types copy the shapes of the real test (I recommend checking the current mix against an official sample, since the PDF does not describe it). Five learning-only formats help teaching but never appear in mocks.

| Type | What the player does | Typical fact kinds | In mocks? |
|---|---|---|---|
| **1 Single answer** | Pick the one right answer from 4 | dates, people, numbers, terms | Yes |
| **2 True/false pair** | Two statements; pick the true one | rules, definitions, common mix-ups | Yes |
| **3 Choose two** | Pick the two right answers from 4 (both needed) | lists (wives, parties, Commonwealth aims) | Yes |
| **4 Which statement is correct** | Four full statements; pick the one correct | rules and processes (Speaker, courts, voting) | Yes |
| Map tap | Tap the right place on the map | cities, landmarks, nations | Lessons and reviews only |
| Timeline order | Put 3 or 4 events in order | dates and sequences | Lessons and reviews only |
| Match | Pair people with achievements, saints with days | persons, lists | Lessons and reviews only |
| Number entry | Choose a number from a small dial | numbers (24, 45, 75, 129) | Lessons and reviews only |
| "What happens next?" | Pick the next event in a story | events | Lessons only |

### 4.2 Rules for writing questions

1. **One fact per question** (two for callbacks). Stem 20 words or fewer; options 10 words or fewer. Plain B1 English, no idioms.
2. **Positive stems only.** No "NOT" or "EXCEPT". They defeat second-language readers.
3. **Four parallel options**: same grammar, similar length (within about 30%), no overlap, no "all of the above" or "none of the above", no jokes.
4. **Distractors come from the handbook** whenever possible, in this order of preference: (a) a real fact from the same section that answers a *different* question (the other Houses' member numbers for a "129 MSPs" question); (b) neighbouring items in the same list or timeline (other handbook dates, never invented ones); (c) a well-known mix-up (Great Britain vs the UK). Never absurd.
5. **A distractor must be false in that question.** A script flags a distractor that equals the correct answer of another fact with a similar stem.
6. **Answer positions are balanced** (A to D within 22% to 28% across the bank).
7. **No ambiguity.** If the handbook is vague, garbled or inconsistent (flags `ambiguous`, `summary-conflict`) or may have changed (`time-sensitive`, `needs-check`), no question is approved until a human has settled the fact (section 6).
8. **Dates:** ask only years the handbook gives. Never ask about a † year or a year not in `syllabus.csv`.
9. **Names and spelling** follow the handbook (Caernarfon is "Caernarvon" there; show both once).
10. **Explanation** of 25 words or fewer for every question, linking back to the card.
11. **Sensitive topics** (domestic violence, FGM, forced marriage, terrorism, slavery, famine) use respectful, factual wording and no graphic images.
12. **Two-person check**: an author and a checker, with the handbook open, sign each question off.
13. **Map-tap targets** come only from places the handbook names. A ‡ target (section 3.4) is highlighted in its lesson but never asked.

### 4.3 Every question is linked to facts

- Each question stores **1 to 3 fact ids** (`fact_ids`), the **edition** it was checked against and a **review status** (draft, reviewed, approved).
- Automatic checks (headless, in `tools/test.sh`): every A fact has at least **3 approved questions in at least 2 different types**; every B fact has at least 2; no approved question points to a flagged unresolved fact; no question has zero facts; stems are unique; options are within the length rules; answer positions are balanced; reading level is B1 or lower.
- When a fact changes (a new edition), every question that links to it is automatically set back to *draft* (section 5.6).

### 4.4 Target size of the question bank

| Fact priority | Facts | Questions per fact | Questions |
|---|---:|---:|---:|
| A | 474 | 3 (at least 2 types) | 1,422 |
| B | 430 | 2 | 860 |
| C | 142 | 0 (colour only) | 0 |
| **Full target** | | | **about 2,300** |
| **Minimum for a first release (M4)** | | 2 per A, 1 per B | **about 1,400** |

The M3 lessons need only **3 questions per lesson** (about 450 questions). With 2,300 questions a learner can take well over 90 different mocks before facts repeat.

Mix by type: about 50% single answer, 20% true/false pairs, 15% which-statement, 15% choose-two.

### 4.5 Worked examples (my own wording)

**Type 1: single answer**

> **Which Roman emperor led the successful invasion of Britain in AD 43?**
> A Julius Caesar · B **Claudius** · C Hadrian · D William the Conqueror
>
> *Feedback:* "Claudius led the invasion in AD 43. Julius Caesar tried in 55 BC and did not succeed."
> *Facts:* `HIS-ROM-001`, `HIS-ROM-003`. *Why these distractors:* Caesar is the earlier attempt, Hadrian is the wall-builder, William is another invader.

**Type 2: true/false pair**

> **Which statement is true?**
> A Great Britain includes Northern Ireland. · B **Great Britain means England, Scotland and Wales.**
>
> *Feedback:* "Great Britain does not include Northern Ireland. The UK is Great Britain plus Northern Ireland."
> *Facts:* `UKG-003`, `UKG-004`.

**Type 3: choose two**

> **Which TWO of these were wives of King Henry VIII?**
> A **Anne Boleyn** · B Elizabeth of York · C **Catherine Parr** · D Mary Tudor
>
> *Feedback:* "Anne Boleyn and Catherine Parr were Henry VIII's wives. Elizabeth of York was Henry VII's queen. Mary was his daughter."
> *Facts:* `HIS-TUD-005`, `HIS-TUD-009`, `HIS-MED-049`.

**Type 4: which statement is correct**

> **Which statement about the Speaker of the House of Commons is correct?**
> A The Prime Minister chooses the Speaker.
> B **The Speaker is neutral and is chosen by MPs in a secret ballot.**
> C The Speaker always belongs to the largest party.
> D The House of Lords chooses the Speaker.
>
> *Feedback:* "MPs choose the Speaker by secret ballot, and the Speaker stays neutral, representing no party."
> *Facts:* `GOV-PAR-015`, `GOV-PAR-016`.

---

## 5. Data model for M3 and M4

Content is **data, not code**, as SPEC 8.6 already says. This section is for whoever builds M3 and M4.

### 5.1 Where things live

```
content-src/syllabus.csv       source of truth for facts (this deliverable, kept in the repo)
game/content/
  edition.json                 which handbook edition and impression this content was checked against
  facts.json                   generated from syllabus.csv (never edited by hand)
  stops/<stop_id>.json         one lesson per stop id (journey stops and Passport stamps): cards and the recall question ids
  passport.json                the 10 Passport pages: ordered stamp ids, unlock batch and map target of each stamp (M3b)
  questions/<chapter>.json     the question bank, one file per chapter (not 2,300 tiny files)
  glossary.json                tap-for-meaning words (about 150)
tools/content/                 generator and validators (run by tools/test.sh)
```

The handbook PDF is **never** committed (section 6.6).

### 5.2 Fact (generated from `syllabus.csv`)

```json
{ "id": "HIS-ROM-003", "section": "3.7", "page": 39, "topic": "Claudius",
  "text": "In AD 43 the emperor Claudius himself took an army to Britain in a fresh attempt at conquest.",
  "kind": "date", "year": 43, "place": null, "lat": null, "lon": null,
  "stop": "rom-richborough", "priority": "A", "flags": [],
  "edition": { "id": "LITUK-3E", "status": "verified",
               "verified_by": "initials", "verified_on": "2026-11-02", "source_ref": "3.7 p39" } }
```

`status` is `pending` (default for facts with a review flag), `verified` or `retired`. Ids are **never reused or renumbered**.

### 5.3 Lesson (one file per stop id)

```json
{ "id": "rom-richborough", "part": "journey", "chapter": "roman", "edition": "LITUK-3E",
  "hook": "One sentence: why this place, why now.",
  "cards": [ { "id": "c1", "text": "25 to 40 words.", "image": "img/roman/richborough.webp",
               "facts": ["HIS-ROM-001", "HIS-ROM-002"], "flags": [] } ],
  "recall": ["Q-HIS-ROM-003-a", "Q-HIS-ROM-005-b", "Q-HIS-ROM-001-c"],
  "colour_only": ["HIS-ROM-002"] }
```

A Passport lesson has `"part": "passport"`, a `page` instead of a `chapter`, the echo batch it unlocks with, and, when it is about a place, a `target`:

```json
{ "id": "gov-westminster-lords", "part": "passport", "page": "government", "unlock": "III", "edition": "LITUK-3E",
  "target": { "name": "Palace of Westminster", "lat": 51.500, "lon": -0.125, "named_in_handbook": true },
  "hook": "...", "cards": [ ], "recall": [ ], "colour_only": [] }
```

`target` is absent for the 27 place-less stamps. When `named_in_handbook` is `false` (7 lessons, marked ‡) the place is highlighted in the lesson but never asked in a map-tap question. The page ids are listed in section 3.4.

The `Content.get_for_stop(id)` interface from SPEC 8.6 returns this object (or nothing in M1).

### 5.4 Extension points to add in M1 (cheap, invisible)

1. **Stable stop ids** from the new `journey_draft.json`. Saves refer to stop ids, so they must not change later.
2. `journey.json` fields: `chapter.legs`, `stop.year_src`, `stop.place_in_handbook`, `stop.content = stop id`. The map reads `legs`; nothing else uses them yet. `journey.json` holds only the 78 map stops; the Passport has no pins, so M1 needs nothing else for it.
3. Save format: per-stop `lesson_done` and `best_quiz_score` (already in SPEC 8.6) plus an empty top-level `learn: {}` object and a `learn_schema` number.
4. The **arrival card content slot** accepts a scene with these signals: `lesson_finished(stars)` and `lesson_closed`.
5. Reserve three autoload names: `Learner` (boxes and mastery), `Review` (queue) and `Quiz` (question scene). In M1 they are empty stubs.

### 5.5 Question

```json
{ "id": "Q-HIS-ROM-003-a", "type": "single",
  "stem": "Which Roman emperor led the successful invasion of Britain in AD 43?",
  "options": [ {"id":"a","text":"Julius Caesar"}, {"id":"b","text":"Claudius"},
               {"id":"c","text":"Hadrian"}, {"id":"d","text":"William the Conqueror"} ],
  "answer": ["b"], "explain": "Claudius led the invasion in AD 43. Julius Caesar tried in 55 BC.",
  "facts": ["HIS-ROM-001", "HIS-ROM-003"], "difficulty": 1,
  "status": "approved", "edition": "LITUK-3E", "tags": ["roman"], "flags": [] }
```

`type` is one of `single`, `pair`, `two`, `statement`, `map`, `order`, `match`, `number`, `next`. Map questions carry the target place's coordinates (from the lesson's `target`) and a tolerance in km; a target with `named_in_handbook: false` is never used.

### 5.6 Learner state (spaced repetition) inside the save

```json
"learn": {
  "plan":  { "test_date": "2026-12-14", "mode": "full", "daily_cap": 30 },
  "facts": { "HIS-ROM-003": { "box": 3, "due": 20548, "seen": 4, "ok": 3, "lapses": 0, "last": 20541, "ms": 5200 } },
  "stops": { "rom-richborough": { "done": true, "stars": 3, "day": 20535 },
             "pp-money-tax": { "done": true, "stars": 2, "day": 20536 } },
  "checkpoints": { "roman": { "best": 9, "of": 10 } },
  "mocks": [ { "day": 20560, "score": 19, "secs": 2210, "by_chapter": [2,1,6,4,6], "missed": ["GOV-PAR-016"] } ]
}
```

Journey stops and Passport stamps share one record format, keyed by stop id. Days are whole day numbers (so no time-zone trouble). The state is small: about 100 bytes per fact, about 90 KB for the whole syllabus. Mastery and readiness are **computed**, never stored.

### 5.7 Edition tagging and swapping in a revised handbook

Every fact, stop file and question carries the **edition id** it was checked against. The app ships **one active edition**. A future revision is a **data swap**:

1. Add `edition.json` for the new edition (id, impression, date, source link).
2. Read the new official text (never committed) and produce a new `syllabus.csv`. A script `edition_diff` compares old and new ids and lists each fact as **same**, **changed**, **removed** or **new**. New facts get new ids.
3. A human checks the report; 10% of "same" facts are spot-checked.
4. **Changed** facts: text updated, status back to `pending`, linked questions back to `draft`. Learner state: the fact **drops to box 1** and the player sees a one-time "what's new" card.
5. **Removed** facts: kept with `retired: true`, never asked; their learner state is archived.
6. **New** facts are attached to stops; a stop that would exceed 9 A+B facts is split (stop ids are added, never renamed).
7. Validators run; About shows "Content: edition X".

A **save migration** function takes the old edition id and the diff report, applies rules 4 and 5 to the learner's boxes and keeps everything else.

### 5.8 Automatic checks (extend `tools/test.sh`)

- Journey: unique ids; `sort` never decreases; every leg has at most 7 stops; every stop is on land inside the map (SPEC 4).
- Passport: every Passport lesson is on exactly one page; every page has 4 to 12 stamps; a lesson has `lat` and `lon` only if it has a place; a map-tap question uses only a target with `named_in_handbook: true`.
- Facts: every fact has exactly one stop id (a map stop or a stamp); every lesson has 3 to 9 A+B facts; ids unique; coordinates sensible.
- Lessons: at most 4 cards; at most 45 words per card; every A fact appears on a card; reading level B1 or lower.
- Questions: the rules of section 4.3.
- Currency: **no approved question and no mock-eligible fact is `pending`.**
- **Copyright guard** (run locally by the owner, because it needs the PDF text, which is not in the repo). **One rule for everything that ships:** the facts in `syllabus.csv`, the cards, the questions and the feedback. No run of **8 or more consecutive words** may be shared with the handbook text. Words are compared in lower case, ignoring punctuation (letters, digits and apostrophes only), so a quotation that is merely re-punctuated still counts. The only exception is a short quotation of out-of-copyright or statutory text (a poem title or opening, the oath of allegiance), flagged `quote`: in the `flags` column of `syllabus.csv`, and in a `flags` list on cards and questions. A quotation must stay as short as possible; the guard fails a `quote` item that shares more than 12 words. `tools/content/copyright_guard.py` (standard library only) implements exactly this rule and reads the `quote` flag. **`syllabus.csv` passes this check today:** no fact shares 8 or more words with the handbook, except one row flagged `quote` (`HIS-POS-027`, whose 8-word poem title is the whole overlap).

---

## 6. Accuracy and currency

### 6.1 The policy

1. **Teach what the official handbook says**, not what is true in the world today. The test is written from the handbook. (Example: the handbook's 2009 survey says 70% Christian; do not replace it with a newer census figure.)
2. **The authority for every flagged fact is the latest official reprint** (SPEC 12.3 records an amendment list from January 2026), not this PDF. A human compares each flagged fact with that reprint:
   - if the reprint agrees, mark the fact `verified`;
   - if it differs, the reprint wins and the fact and its questions are rewritten;
   - if the reprint does not contain the statement (for example paragraphs the PDF's publisher added), the fact becomes colour only and is never tested.
3. **Flagged facts stay `pending`.** Pending facts may be taught as story colour but are **never** used in approved questions or mock tests. Of the 1,046 facts, **828 A and B facts are unflagged** and ready for questions today; **87 are flagged** (44 A, 32 B, 11 C).
4. **M3 gate:** all 44 flagged A facts must be verified or retired before the lessons that use them ship: 19 are taught in journey lessons (they gate M3a) and 25 in Passport lessons (they gate M3b). The 32 flagged B facts split 10 and 22 in the same way, and the 11 flagged C facts (1 and 10) are colour only.

### 6.2 Text that looks edited after 2013

The PDF's publisher appears to have updated some passages and left others in the 2013 wording. These are the places I noticed (page numbers are PDF pages); I cannot tell from the PDF alone which match the official reprint.

| Page | What the PDF says | Observation |
|---|---|---|
| 15 | "Conservative Government from 2015 to 2024" and "Labour Government from 2024" paragraphs; the first still says the Prime Minister "has called" the election of 4 July 2024 | Not in the 2013 text; stale tense; likely not in the official reprint |
| 58 | A lottery age rise from 16 to 18 dated April 2021, with a verb error in the sentence | Garbled edit |
| 69 | Population table ends "2022: estimated 67.6 million" | Edited; the table's other rows are 2013 data |
| 75 | Charles III is the monarch; William, Prince of Wales; Prince Edward made Duke of Edinburgh in 2023 | Edited; the Duke of Edinburgh sentence is garbled |
| 75 to 76 | Anthem verse printed "God save our gracious King" but with "Send her victorious" | Half-edited |
| 76 | Oath and affirmation name "King Charles the Third" | Edited |
| 87 to 88 | "Welsh Assembly", 60 members, elections every four years, "20 areas", "since 2011" | 2013 wording; SPEC records "Senedd changes" in the January 2026 amendments |
| 90 | Prose says the Commonwealth has **54** members; the table below it lists **56** | Prose is 2013, table is newer |
| 91 to 92 | Brexit date, 27 EU members, and a statement that from 2024 the general principles of EU law no longer form part of UK law | Added text; other EU wording elsewhere is 2013 (pages 13, 78, 88, 94) |
| 96 to 98 | "Sources" and a "Key Material and Facts" summary | Written by the PDF's publisher; contains errors (6.4) |

### 6.3 Time-sensitive facts (all are flagged `time-sensitive` or `needs-check` in `syllabus.csv`)

"My understanding" is a prompt for the human checker, **not** a statement to copy into the game.

| Theme | Fact ids (PDF page) | What the PDF says | What to check, and my understanding |
|---|---|---|---|
| Monarch and titles | `GOV-CON-011` (75), `GOV-CON-012` (75), `GOV-CON-013` (75), `GOV-CON-018` (75), `GOV-CON-019` and `GOV-CON-020` (76), `GOV-INT-002` (90), `HIS-GLO-074` (19) | Elizabeth II died 2022; Charles III; heir William; oath to King Charles III; Victoria's reign was "the longest" in 2013 | Names, titles and the anthem wording in the reprint. Victoria's "longest reign" sentence dates from 2013 and no longer holds; use the reprint's wording or drop it |
| Devolved bodies | `HIS-POS-056` (14), `HIS-POS-058` (14), `GOV-DEV-002`, `-005`, `-006`, `-008`, `-009`, `-017` (87 to 88), `GOV-VOT-017` (89) | "Welsh Assembly"; 60 members; four-year term; 20 areas; law-making since 2011; NI Assembly "running successfully since 2007" | The Welsh body is now called the Senedd (Welsh Parliament); legislation in 2024 provides for more members; the Welsh law-making model changed after 2017; the NI Assembly was suspended again after 2007. Use the reprint |
| EU and Brexit | `HIS-POS-046` (13), `GOV-PAR-022` (78), `GOV-VOT-003` (88), `GOV-INT-008`, `-009`, `-010` (91 to 92), `GOV-COM-009` (94), `GOV-DRV-005` (80) | UK "is a full member" of the EU; MEP elections; EU citizens can vote; EU licences | The UK left the EU in 2020; these rules no longer apply. If the reprint keeps them, teach the reprint |
| Recent politics and wars | `HIS-POS-062`, `-063` (15), `HIS-POS-065`, `-066` (15) | Iraq and Afghanistan operations; ISAF; 2015 to 2024 governments; Labour in 2024 | Likely not in the official reprint. Do not test names or dates of recent governments unless the reprint has them |
| Settlement route and test | `TST-003`, `-004`, `-005`, `-008`, `-009`, `-010` (5), `TST-020`, `-021` (7) | "As of January 2013"; UK Border Agency; B1 English from October 2013; 45 minutes and 75% are not in the PDF | The agency no longer exists; check the current English requirement, the test page, the time and the pass mark |
| Law, police, welfare, voting | `GOV-POL-003`, `-004`, `-008`, `-009`, `-012` (83), `GOV-TAX-008` (80), `GOV-DRV-006` (81), `GOV-COM-003` (93), `GOV-VOT-001`, `-009` (88 to 89), `GOV-PAR-024` (78), `GOV-RTS-010` (79) | Police and Crime Commissioners; the Independent Police Complaints Commission; Jobseeker's Allowance; the windscreen tax disc; jury age 18 to 70; photo ID only in Northern Ireland; voting age 18; phone book and a helpline number | Bodies renamed or replaced (the complaints commission became a different body in 2018, the tax disc was abolished in 2014, Jobseeker's Allowance is being replaced); jury age limit and voter ID rules changed; voting age differs in Scottish and Welsh devolved elections. Use the reprint |
| Society and culture | `SOC-LIT-004` (48), `SOC-MED-009`, `-010` (57 to 58), `SOC-MED-013` (58), `SOC-LEI-014` (58), `SOC-PLC-004`, `-008` (59), `SOC-REL-001`, `-002`, `-003` (62), `SOC-TOD-001`, `-045` (68 to 69), `SOC-SPO-017`, `-018` (65), `SOC-SPO-029` (66) | Man Booker rules; free licence at 75 and discounts; Facebook and Twitter; lottery age; 61,000 volunteers; Historic Scotland; 2009 religion figures; 67.6 million; athletes' medal tallies ("has won"); England's "only" tournament win | Prize rules and name, licence concessions, the platform name (now X), the volunteer count and population are likely to differ; Historic Scotland has since been merged into a wider heritage body, and tallies such as Wiggins's seven Olympic medals have grown. For religion keep the handbook's figures. England's men's team still has only the 1966 win, but the women's team won a major title in 2022, so the sentence needs the reprint's wording |
| House of Lords | `GOV-PAR-010` (77) | Hereditary peers elect a few of their number | Legislation to end the remaining hereditary seats has been under way; check the reprint |
| International counts | `GOV-INT-003`, `-006` (90), `GOV-INT-011` (92), `GOV-INT-009` (91) | Commonwealth 54 (prose) vs 56 (table); Council of Europe 47; 27 EU members | The Commonwealth has had 56 members since 2022; Russia left the Council of Europe in 2022; EU 27 is correct. Teach the reprint's numbers |
| Length of Parliament | `HIS-GLO-004` (16) | "three years (later seven, now five)" | Consistent with page 78; only check that the reprint still says five |

### 6.4 Conflicts between the main chapters and the summary pages (96 to 98)

The main text is the source of truth. The summary is wrong or imprecise at these points (flagged `summary-conflict`; the fact in `syllabus.csv` follows the main text):

| Fact id | Main text (page) | Summary (page 97 to 98) |
|---|---|---|
| `HIS-TUD-010` | Wales united with England under **Henry VIII** (33) | "under King Henry VII, 1500s" |
| `HIS-STU-014` | English civil war began in **1642** (37; the king recalled Parliament in 1640) | "1640: Beginning of English Civil War" |
| `HIS-GLO-105` | Boer War **1899 to 1902** (22) | "1889-1902" |
| `HIS-ANG-010`, `HIS-ANG-011` | St Columba came from **Ireland** and founded Iona; only St Augustine led missionaries from **Rome** (40) | Says both saints led missionaries sent from Rome |
| `HIS-STU-024` | Cromwell became Lord Protector after the victory at Worcester and ruled until 1658 (37) | "circa 1640s-1650s" |
| `HIS-TUD-025` | Golden Hind was one of the first ships to sail round the world (35) | Says Drake "later" sailed round the world, after the Armada |
| `HIS-MED-018` | A third of the people of **England** died (28) | "over 1/3 of Britain" |
| `HIS-POS-058` | NI Assembly elected 1999, suspended 2002, restored 2007 (14) | "led to establishment of Northern Irish parliament" |
| `HIS-GLO-082`, `HIS-POS-031`, `HIS-MOD-039` | Stephenson (21), Cockerell (13), Fleming (25) | Misspelled "Stevenson", "Cockrell", "Flemming" |
| `HIS-GLO-014` | Huguenots came **1680 to 1720** (16) | "pre-1720", spelled "Hugunots" |
| `GOV-INT-003` | 54 members in the prose; 56 in the table (90) | Not in the summary; the conflict is inside the main text |

Other small errors in the summary: "1945-1950: NHS and social security" (the NHS began in 1948), "Lord Wellington" (Duke of Wellington) and "causalities".

### 6.5 Garbled text, omissions and oddities in the main chapters

| Where | Issue | What I did |
|---|---|---|
| p9 | The sentence on 'Britain' and 'British' mentions "Isles" with missing words | Taught that 'Britain' and 'British' mean everyone in the UK; flagged `ambiguous`; **the British Isles is never defined in the PDF**, so do not write a question on it until the reprint is checked |
| p34 | The sentence on the Protestant Church of Scotland has a word missing from its description of the leadership | Taught only that it was established and was not a state Church; flagged |
| p75 | Duke of Edinburgh sentence is garbled | Flagged; colour only |
| p54 | **The table of national flowers is missing** from the PDF | One row (`SOC-LEI-003`) from the official text (rose, thistle, daffodil and leek, shamrock), flagged `needs-check` |
| p21 | "middle of the century" for the famine; "see Chapter 4" for boroughs (they are in chapter 3) | Year given as about 1850; flagged `ambiguous` |
| p39 to 41 | No dates for the Iron Age, Alfred, Cnut or Kenneth MacAlpin | `year` left blank |
| p21 and p73 | The Chartists are described twice, with different detail | Combined in one lesson |
| p11 | "Clement Atlee" in the main text, "Attlee" in the box | Used "Attlee" |
| p13 | "Sir Ian Wilmot" (usually spelled Wilmut) | Kept the handbook spelling and noted the usual one in the fact |
| p27 | "Caernarvon" (now spelled Caernarfon) | Both shown in the fact |
| 3.2 | The inventions list mixes 1930s and 1990s items | Split by date between chapters VI and VII |
| 5.5 | "PSCOs" is a typo for PCSOs | Used PCSOs |
| p38 | "quickly defeated at Killiecrankie": the 1689 rising is usually described differently (the Jacobite army won that battle, and the rising ended weeks later) | `HIS-STU-050` states the handbook's version and is flagged `needs-check`; do not write a question on it |
| p67 | "Jensen Button" (the driver's name is spelled Jenson) | `SOC-SPO-048` uses Jenson |

### 6.6 Other currency and copyright notes

- **Years chosen by BQ (†).** The sort years of the three prologue stops (shown as *Stone Age* or *Iron Age*), `rom-london` (AD 60), `rom-housesteads` (AD 122), `ang-iona` (AD 563), `ang-canterbury` (AD 597), `ang-winchester` (AD 880), `med-tower` (c. 1080), `med-westminster` (c. 1295), `tud-greenwich`, `stu-derry`, `stu-worcester`, `stu-cambridge`, `stu-glencoe`, `glo-whitby`, `glo-cromford`, `glo-ironbridge`, `glo-bristol`, `glo-newport`, `mod-blenheim`. They are standard historical dates used only as map anchors.
- **Places the handbook does not name (‡):** **35 of the 78 journey stops** and 7 of the 45 Passport lessons that have a place (marked in the tables; `place_in_handbook` is N in `stops.csv` and false in `journey_draft.json`). I checked every journey stop against the handbook text. Many of these places appear in the handbook only for something else: in the list of cities (Southampton, Plymouth, Newcastle, Newport, Bristol), for another event (Greenwich, Windsor, Portsmouth, Glasgow, Liverpool, Manchester, Belfast, Edinburgh) or not at all (Richborough, Runnymede, Dover, Tredegar). Places named for what the stop teaches are not marked, for example Enfield (the first cash machine), Lincoln (its cathedral), Canterbury, Cambridge (Newton and Rutherford), Westminster (Parliament) and 10 Downing Street (the Prime Minister). No fact at a ‡ journey stop is tied to the pin's place in `syllabus.csv`. The same is true of the ‡ Passport lessons with one exception: `SOC-MED-010` and `SOC-MED-011` (lesson `cul-bbc-licence`) name the BBC and carry the coordinates of Broadcasting House, which I chose because the handbook gives the BBC no address. Treat those two coordinates like any ‡ target and never use them in a map-tap question. The 27 place-less Passport lessons have no place, so their flag is blank.
- **Copyright.** The handbook is Crown copyright and this repository is public. Everything here is my own wording of facts (names, dates, numbers and short terms are not protected). Rules for M3 and M4: never commit the PDF or its text; never paste its sentences into cards, questions or code comments; follow the one rule of section 5.8 (no run of 8 or more consecutive words shared with the handbook, with short out-of-copyright or statutory quotations flagged `quote` as the only exception); run `copyright_guard.py` locally before every commit of content. About 710 of the 1,046 facts were reworded after a first draft that was too close to the source, and `syllabus.csv` now passes the check (one row, `HIS-POS-027`, carries the `quote` flag). This document names the handbook and its section headings and quotes a few short passages from the summary pages only to describe their errors; it is not game content. Add to About: "Based on the official *Life in the United Kingdom* handbook. BQ is an independent app, not published or endorsed by the Home Office."
- **No images from the handbook** may be used. Illustrations come from M2's art plan.

---

## 7. Proposed changes to `SPEC.md`

**Applied in SPEC v0.2 (2026-10-11).** This table is kept as a record. Its section numbers refer to SPEC v0.1: in v0.2 a new section 7 (*Learning design*) was inserted, so v0.1 sections 7 to 15 are now 8 to 16.

| SPEC section | Proposed change |
|---|---|
| Title block | Version 0.2. Add one line: "Learning design: `docs/LEARNING_DESIGN.md`; fact inventory: `content-src/syllabus.csv`." |
| **Decisions from the interview** | Keep every existing row unchanged. Add rows (decided 2026-10-11): *Learning layers* (the journey on the map, the Passport off the map; decision 1); *Prologue* (decision 2); *Stops in M1* now 78 (decision 3); *Gating* (soft, 70%; decision 6); *Content source* (official handbook, latest reprint, own wording); *Spaced repetition* (6-box Leitner, shown as map revisits; decision 9); *Mock tests* (official format 24 / 45 min / 75%) |
| **1 Vision** | Replace "In later milestones each stop teaches part of the official handbook: history, government and law, geography, famous people and major events" with a sentence naming the two layers (the journey and the Passport). Add pillar **6. Remembered: every lesson ends with recall and old places come back as revisits.** Add to Audience: "plain English at reading level B1 with a tap-for-meaning glossary" |
| **2 M1 scope** | In the table: "7 chapters, 35 stops, guided progression" becomes "**7 chapters plus an optional prologue, 78 stops in legs of at most 7, guided progression**". Under "Not in M1" add "the Passport (pages, lessons, the Citizenship Desk and the briefcase), lessons, spaced repetition". The map shows only the 78 journey pins |
| **3.1 Core loop** | If the prologue is accepted, the first glowing stop is the prologue's first stop (Skara Brae), not Richborough. Otherwise unchanged |
| **3.2 Screen layout** | The chapter name can show the numeral **0** for the prologue. No other layout change |
| **3.4 Chapters and stops** | Add: *a chapter has legs of at most 7 stops; only the current leg's pins are labelled* (replaces the "≤ 7 per chapter" wording in 7.5); *several stops may share one place and fan out* |
| **3.6 Arrival card** | M1 unchanged. Note for M3: the slot hosts the lesson (a **Start** button, then cards and questions); for M4 it also shows the review badge |
| **3.7 Time-jump** | M3: the title card may show the chapter-mastery flourish after a checkpoint (no change in M1) |
| **3.8 End of journey** | "35/35" becomes "**78/78**" |
| **3.10 Save** | Add `learn_schema` and an empty `learn: {}` object to the save contents; keep `lesson_done` and `best_quiz_score` per stop |
| **4 Journey data** | **Replace the table** with section 3.2 of the learning design (`journey_draft.json`). Extend the JSON format with `chapter.legs`, `stop.year_src`, `stop.place`, `stop.place_in_handbook`, and set `content` to the stop id. Extend the automated checks: ids are unique **and frozen once released**; every leg has at most 7 stops; `sort` never decreases (the prologue uses negative years). Change the draft banner to say which years are † (chosen by BQ) |
| **5.3 Chapter moods** | Add *Prologue*: pale dawn, chalk grey and heather |
| **7.3 Architecture** | Add autoloads `Learner` (boxes, mastery, readiness), `Review` (queue) and `Quiz` (question scene); `Content` grows (below). In M3b add a `Passport` scene (pages and stamps) and the Citizenship Desk. Add game states `Lesson`, `Review`, `Mock` after M3 and M4 |
| **7.5 Rendering** | Replace "only the current chapter's (≤ 7) are shown with labels" with "only the current leg's (≤ 7)" |
| **7.6 Learning-content extension points** | Replace with section 5.4 of the learning design: stable stop ids, the new `journey.json` fields, `learn: {}` in the save, the lesson signals, and the three reserved autoloads |
| **7.7 Automated tests** | In M3 add the content validators of section 5.8 and the local-only copyright guard |
| **8 Performance targets** | Add: lesson art at most 40 KB per image (WebP), the whole content pack at most 20 MB, lesson opens in under 300 ms on the baseline phone, card swipes hold 30 FPS |
| **11.3 Content edition** | Add: the authority for flagged facts is the **latest official reprint**; flagged facts are `pending` and are never used in approved questions or mocks; the verification workflow; edition swap rules (learning design 5.7); the list of time-sensitive facts (learning design 6.3) |
| **11.4 Compliance basics** | Add: copyright policy (own words, PDF never committed, copyright guard) and the About disclaimer "independent app, not endorsed by the Home Office"; reading level B1 |
| **12 Milestones** | Replace the M3 and M4 rows with the definitions below. Add a note that **M3 is split**: M3a = content pipeline and the 78 journey lessons; M3b = the 72 Passport lessons |
| **12 M1 acceptance criteria** | Criterion 2: "7 chapters, 35 stops" becomes "**prologue plus 7 chapters, 78 stops**". Criterion 9 (no learning content) is unchanged |
| **13 Risks** | Add the rows below |
| **14 Open questions** | Mark question 7 (stops abroad) **resolved: stay in the UK** (decision 5). Add the open questions below |
| **15 Credits** | Add: "*Life in the United Kingdom: A Guide for New Residents*, Home Office, Crown copyright. BQ is independent and not endorsed by the Home Office." |

### 7.1 Proposed M3 and M4 definitions

| | Milestone | Outcome |
|---|---|---|
| **M3a** | Learning content: pipeline and the journey | `syllabus.csv` becomes `facts.json`; validators; a lesson for each of the 78 journey stops (3 to 4 cards, 3 questions, result, stars); progress saved; the 19 flagged A facts taught in the journey verified or retired against the latest reprint |
| **M3b** | Learning content: the Passport | The 72 Passport lessons on 10 pages, the echo unlocks, map-tap drills with the temporary highlight, the Citizenship Desk and the briefcase; the 25 flagged A facts taught there verified or retired against the latest reprint |
| **M4** | Practice and test prep | Leitner schedule and review runs on the map, quick review, chapter checkpoints, mocks in the official format, readiness score, fix-it runs, test-date plan, a question bank of at least 1,400 approved questions |

**M3a acceptance criteria**

1. `tools/content` turns `syllabus.csv` into `facts.json`, and every automatic check in 5.8 passes.
2. Each of the 78 journey stops has a lesson; every A fact appears on a card; at most 4 cards, at most 45 words per card.
3. An average lesson takes 6 minutes or less on the baseline phone; card swipes stay at 30 FPS.
4. Stars and `lesson_done` survive a force-close.
5. All 19 flagged A facts taught in the journey lessons are verified or retired by the owner (a signed list), and no `pending` fact is in an approved question.
6. The copyright guard finds no run of 8 or more words shared with the handbook (items flagged `quote` excepted).
7. Reading level is B1 or lower on every card and question.

**M3b acceptance criteria**

1. Each of the 72 Passport lessons sits on exactly one of the 10 pages and meets the lesson rules of M3a criterion 2.
2. The Welcome batch is open from the start, every other batch unlocks after its chapter's checkpoint (passed or skipped), and test-date mode opens all stamps. The Citizenship Desk and the briefcase button open the Passport from anywhere.
3. A lesson about a place shows its temporary highlight and leaves no pin behind. Map-tap questions use only the 38 targets the handbook names, never the 7 marked ‡.
4. All 25 flagged A facts taught in Passport lessons are verified or retired by the owner (a signed list), and the copyright guard still finds nothing.

**M4 acceptance criteria**

1. The schedule (boxes, intervals, queue, daily cap, debt guard, test-date compression) has unit tests that pass headless.
2. A review run visits up to 5 glowing places (journey pins, plus the Citizenship Desk when Passport facts are due) and the badges clear afterwards; quick review works without travel.
3. Chapter checkpoints apply the 70% soft gate; mocks run in the exact official format (24 questions, 45 minutes, pass at 18), with a timer, a flag-for-review, and a results screen with chapter bars.
4. The readiness score and the weak-topic fix-it run work, and the score is never higher than the lower of the model and the last mock results.
5. At least 1,400 approved questions with at least 2 per A fact in at least 2 types, and 1 per B fact; the bank checks pass.
6. The edition-swap script and the save migration are tested with a fake "edition 2".
7. No new permissions; a 20-minute session with reviews still holds 30 FPS on the baseline phone.

### 7.2 Risks to add to SPEC section 14

| Risk | Mitigation |
|---|---|
| **Content volume**: 150 lessons and about 2,300 questions is large | Build the 78 journey lessons first (M3a) and the 72 Passport lessons second (M3b); draft with AI help but **a human checks every question against the handbook**; ship the 1,400-question minimum first |
| **Copyright**: the handbook is Crown copyright and the repo is public | Own wording only; PDF never committed; local copyright guard; About disclaimer |
| **Outdated or edited facts** in the PDF | 87 flagged facts stay `pending`; the latest official reprint is the authority (learning design 6) |
| **A revised handbook** is published (a refresh is announced) | Stable ids, edition tags, the diff-and-migrate process (5.7); keep a few weeks free after publication |
| **Learner drop-off or overload** | Five-minute lessons, soft gates, a daily cap with a debt guard, Express mode, encouraging tone |
| **Over-confident readiness score** | The score is the lower of model and mocks; labels always show the number |
| **Map clutter** with up to 78 journey pins | Legs, fan-out for shared places, labels only for the current leg |
| **English-as-a-second-language readers** | B1 target, tap-for-meaning glossary, picture cards, test with real learners |
| **Anchor years and places chosen by BQ (†, ‡)** | Never quizzed; checked once against a trusted source before M3a |

### 7.3 Open questions to add to SPEC section 15

9. Who will verify the flagged facts against the latest official reprint, and by when? (decision 8, section 8)
10. Can the real test's chapter mix and question types be confirmed from an official sample? (section 8.1)

---

## 8. Decisions made on 2026-10-11, and what is still open

The numbers are the ones used elsewhere in this document. Decision 1 is your choice and differs from my three-layer proposal; decisions 2 to 7 and 9 to 13 adopt my recommendations. Decision 8 is still open (section 8.1).

| # | Decision | Outcome | What it means in this document |
|---|---|---|---|
| **1** | **Learning layers** | **Journey and Passport only.** The map has one layer. The 45 lessons I had planned as place-anchored pins are now Passport stamps | 78 map stops, 72 Passport lessons on 10 pages, **150 lessons in all**. My earlier alternative "Journey plus Passport only: 105 stops" undercounted: with the 45 place-based lessons moved in, the Passport holds 72 lessons, not 27. Stop ids are unchanged; place-based stamps keep their coordinates as highlight and map-tap targets, with no pin (sections 3.1 and 3.4) |
| **2** | **Prologue "Before the Romans"** (3 stops, 14 A+B facts) | **Yes**, as an optional chapter 0 | Your seven chapters stay seven. The first hop is long (Kent to Orkney, 6 seconds); swap the first two stops if it feels odd (section 3.2) |
| **3** | **Journey stops in M1** | **All 78** | Only data changes, saves keep stable ids, and the pacing is tested early. M1 acceptance criterion 2 changes (section 7) |
| **4** | **Home for the Passport** | **The Citizenship Desk at Dover plus a briefcase button** | It is the single entry point for all 72 lessons; the map shows no Passport pins (section 3.4) |
| **5** | **Should the journey leave the UK?** | **No.** Agincourt, Dunkirk, the Somme, the Boyne, Waterloo and D-Day are told from UK places with a small inset map | SPEC question 7 is resolved |
| **6** | **Gating** | **Soft gate at 70%**: it unlocks a flourish and the echo stamps; below it the game advises but never blocks | Sections 2.8 and 3.5 |
| **7** | **Default study depth** | **Full** by default, with a one-tap **Express** (A facts only, about 15 hours instead of 28.5) and an automatic suggestion when a test date is close | Section 3.8 |
| **9** | **Spaced-repetition algorithm** | **6-box Leitner now**; revisit FSRS after real usage | Section 2.2 |
| **10** | **Language level and other languages** | **English at level B1 with a 150-word tap glossary** in M3; translated glossaries (for example the five most common first languages of test-takers) for a later milestone | Section 2.6 |
| **11** | **Mock-test chapter blueprint** (2 / 1 / 8 / 6 / 7) | **Use it as a labelled assumption** and tune it if real sample tests or tester reports turn up | Section 3.7 |
| **12** | **Chapter boundaries** | **Keep your years.** Chapter IV ends 1714 and holds the Bill of Rights (1689) and the Union (1707); chapter V starts with George I | Section 3.2 |
| **13** | **Reminders** | **No phone notifications** (the app asks for no permissions); show a "plan" line when the app opens | Section 3.8 |

### 8.1 Still open

| # | Question | My recommendation | Alternative |
|---|---|---|---|
| **8** | **Who verifies the 87 flagged facts, and how?** The PDF mixes 2013 text with later edits | **You (or a trusted reviewer) compare each flagged A fact with the latest official reprint before the lessons that teach it ship: the 19 in the journey before M3a, the 25 in the Passport before M3b**; I prepare the checklist from `syllabus.csv` (filter `flags`). The 32 flagged B facts are checked before M3b ships; the 11 flagged C facts stay colour only until someone checks them | Drop all flagged facts from tests for ever: safest, but loses 44 A facts (monarch, devolution, Brexit, the test itself) that the real test may ask |

**What I could not settle**

1. **The current official reprint was not available to me**, so none of the 87 flagged facts is verified, and I cannot say which paragraphs of the PDF the official text shares.
2. **The real test's mix of question types and chapters** is not in the handbook. The blueprint and the type mix are assumptions. The 45 minutes and the 75% pass mark come from your SPEC.
3. **The national-flowers table** is missing from the PDF; `SOC-LEI-003` uses the official wording from memory and is flagged `needs-check`.
4. **Pin and target coordinates** are good to about 1 km from my own knowledge; they need the M1 "within 2 km" check against a trusted gazetteer.
5. **Years chosen by BQ (†)** and **places the handbook does not name (‡)** need a one-time check against a trusted source.

---

## Appendix A: ids, kinds and how to regenerate

| Id prefix | Handbook part |
|---|---|
| `TST-` | Becoming a resident and the test (1.2, 1.4) |
| `VAL-` | Values and principles (1.3, 5.8 values) |
| `UKG-` | What is the UK (chapter 2) |
| `HIS-PRE/ROM/ANG/VIK/NOR/MED/TUD/STU/GLO/MOD/POS-` | History by era: prehistory, Romans, Anglo-Saxons, Vikings, Normans, Middle Ages, Tudors, Stuarts, Global Power, 20th century, since 1945 |
| `SOC-MUS/THE/ART/ARC/DES/LIT/POE/CUS/LEI/FIL/MED/PLC/REL/SPO/TOD-` | Chapter 4: music, theatre, art, architecture, design, literature, poetry, customs, leisure, film, media, places, religion, sport, UK today |
| `GOV-DEM/CON/PAR/RTS/TAX/DRV/LAW/POL/CRT/EXE/DEV/MED/VOT/INT/COM-` | Chapter 5: democracy, constitution and monarch, Parliament, rights, tax, driving, law, police, courts, government, devolution, media, voting, international bodies, community |

**Kinds:** `date`, `person`, `place`, `event`, `number`, `term`, `rule`, `list`, `value`. **Flags:** `time-sensitive`, `summary-conflict`, `ambiguous`, `needs-check` (review flags: the fact stays pending until a person checks it) and `quote` (informational: the fact quotes a short out-of-copyright or statutory text, so it is exempt from the copyright guard; it does not make the fact pending).

`syllabus.csv` is UTF-8, comma-separated, RFC 4180 quoting and CRLF line ends, one header row. The `stop_id` column uses the lesson ids in `stops.csv`; the 78 journey ids are also in `journey_draft.json`.

`stops.csv` has the same file format and one row for each of the 150 lessons. Columns: `part` (`journey` or `passport`); `chapter` (journey only: `P` for the prologue, then `I` to `VII`); `page` (Passport only: the page title of section 3.4); `order` (position inside the chapter or the page); `stop_id`; `name`; `place` (the pin of a journey stop, or the map-tap target of a Passport lesson; blank when a Passport lesson has no place); `display_year`, `sort_year` and `year_source` (journey only; `HB` = the year is in the handbook, `EXT` = chosen by BQ and marked †); `place_in_handbook` (`Y` or `N`; `N` is the ‡ mark; blank when there is no place); `lat` and `lon` (the pin, or the map-tap target and temporary highlight of a Passport lesson); `topics`; `facts_A`, `facts_B`, `facts_C` and `facts_AB` (counts); `echo_after` (Passport only: the batch that unlocks the stamp, `Day 1` or the chapter after which it appears).

**Changing a fact later.** Edit its row in `syllabus.csv` (never its id), rerun the M3 generator that writes `facts.json`, and re-check every question that lists the fact. To drop a fact, set its status to `retired` in `facts.json` instead of deleting the row, so old saves still make sense (section 5.7). Keep the wording your own: run `copyright_guard.py` (section 5.8) on the changed rows before committing.
