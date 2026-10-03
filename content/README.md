# Content

- `battle1-2026.json` holds all study content for Battle I: settings, battles, books (fact sheets), and questions. `tools/embed_content.py` embeds it in `index.html`. To add a Battle later, add a `battles` entry, its `books`, and its `questions`. No code changes are needed.
- `FACT-CHECK.md` is **generated**, so don't edit it. It's a printable checklist of every fact and question, with the weakest items listed first. Regenerate it after editing the JSON (this also validates the file):

  ```bash
  python tools/build_factcheck.py content/battle1-2026.json
  ```

## Battles, sets and the Battle Day page

- `battles[]`: one tab each on the home page. A book can be in several battles (District & Regional lists all 12).
- `books[].status`: `ready` or `skeleton` (metadata only, with study material still to be written). `arLevel` / `arPoints` / `lexile` come from the school reading list.
- `questions[].set`: `bank` (ours) or `study-guide` (the school's 50 questions from BoTB.pdf, marked verified from the school's answer key, with `confidence: "school"`).
- `competition`: the text of the 🏰 Battle Day page (sections, tips, dates).
- `settings.mockBattle`: the real format, `phase1Rounds` / `phase1Seconds` / `pointsTitle` / `pointsAuthor` / `phase2Rounds` / `phase2Seconds` / `pointsPhase2`.

## Book extras

- `factSheet.characters / settings / keyObjects[].emoji`: the icon shown on the Reference Cards. If it's missing, the app uses 👤, 📍 or 🔑.
- `badge.tiers`: the mastery badge ladder (`at` = mastery fraction, 0–1).
- `coopBoss`: `{ "name", "icon" }`, the boss a Co-op Boss Battle can summon for this book.
- `settings.coop`: `hearts` and `bossHp` for the "Challenge" difficulty. Warm-up and Legendary scale these up or down.
- The Co-op rounds are built from the fact sheets. Book Sort and Match-Up use each book's characters, settings and key objects. Timeline uses each book's `outline` plus any put-in-order questions. Richer fact sheets make for more varied rounds.

## Question fields

| Field | Notes |
|---|---|
| `id` | Unique. Prefix by book (`af-`, `bun-`, `cn-`, `jt-`). |
| `book` | A book `id`. |
| `type` | `in_which_book` · `detail` · `character` · `sequence` |
| `prompt`, `answer` | Required. For `in_which_book`, the answer is "Title — Author", and the app scores title vs. title+author using each book's `titleAccept` / `authorAccept`. |
| `distractors` | Exactly 3 wrong answers. The app builds multiple-choice options from `answer` + `distractors`, shuffled. For `in_which_book`, these are the other books in the same Battle. Put-in-order questions use wrong orderings in the same arrow format as `answer`. |
| `order` | Only for put-in-order `sequence` questions: events listed in the correct order (the app shuffles them for drag-to-order mode). |
| `hint` | A one-line nudge that doesn't give away the answer. |
| `explanation` | Why the answer is right. Shown after the player answers. |
| `acceptAlso` | Other type-in answers that count as correct. |
| `difficulty` | 1 (easy) – 3 (hard). |
| `verified` | `false` until checked against the book. |
| `confidence` | `sourced` / `weak` / `memory`: how well the fact was backed up when it was written. |
| `source` | Codes from the top-level `sources` map. |
