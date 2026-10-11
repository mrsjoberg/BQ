# Content source data

These files are the source of truth for what BQ teaches. They follow the official handbook *Life in the United Kingdom: A Guide for New Residents* (3rd edition). How they are used is explained in [docs/LEARNING_DESIGN.md](../docs/LEARNING_DESIGN.md).

| File | What it is |
|---|---|
| `syllabus.csv` | **1,046 testable facts**, written in our own words. Each row gives the handbook section and page, a priority (A core, B secondary, C context), any review flags, and the lesson that teaches it |
| `stops.csv` | **150 lessons**: 78 journey stops on the map and 72 Passport lessons on 10 themed pages |
| `journey_draft.json` | The 78 journey stops in the format the game reads (it becomes `game/data/journey.json` in M1) |

## Rules

- **Ids never change** once released, and are never reused. Saves and questions refer to them.
- **Our own words only.** No text may share a run of 8 or more consecutive words with the handbook. Check this locally with `tools/content/copyright_guard.py`, keeping your copy of the handbook text in `content-src/private/`, which git ignores. The only exception is a short quotation of out-of-copyright or statutory text, flagged `quote`.
- **Flagged facts are pending.** A fact flagged `time-sensitive`, `needs-check`, `ambiguous` or `summary-conflict` is never used in a quiz or mock test until a person has checked it against the latest official reprint.
- **Never commit the handbook** PDF or its text. It is Crown copyright, and this repository is public.
