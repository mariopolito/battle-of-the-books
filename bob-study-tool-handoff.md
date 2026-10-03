# Handoff: Battle of the Books Study Tool (Battle I, 2026–27)

## Goal
Build a single-file, self-contained HTML study app that helps two 6th-grade teammates prepare for Battle I (Sept/Oct) of the 2026–2027 Battle of the Books competition. It should hold reference material for each book and quiz their knowledge in fun, game-like ways.

## Reading list (Battle I)
| Title | Author | Pages | Genre | Lexile |
|---|---|---|---|---|
| Artemis Fowl | Eoin Colfer | 277 | Fantasy | 600L |
| Bunnicula | Deborah and James Howe | 98 | Animal Fantasy / Mystery | 700L |
| Captain Nobody | Dean Pitchford | 195 | Realistic Fiction | 750L |
| Jeremy Thatcher, Dragon Hatcher | Bruce Coville | 151 | Fantasy | 710L |

Design the data model so later Battles (new book lists) can be added without code changes.

## Users and device
- Two students (my son and his teammate), ages ~11–12. Keep the tone friendly and the text readable for that age.
- Primary device: school-issued Lenovo 500w Gen 3 2-in-1 (11.6", 1366x768, touchscreen). Layout must fit that screen without scrolling in quiz modes, with large touch targets. Should also work on a desktop browser and a phone.
- Follow the same pattern as my existing Mesa Academic League study app: one self-contained HTML file, no build step, no server.

## Content rules (important)
- Write all reference material and questions in original wording. Do not reproduce passages or quotes from the books.
- Do not invent plot facts. Every question carries a `verified` flag. Anything not confirmed against a reliable summary stays `verified: false` and is visibly marked in an admin/review view so I can fact-check before the kids see it.
- Keep content in a clearly separated JSON block (or `<script type="application/json">`) at the top of the file so I can edit questions without touching app code.

## Content to create per book
1. **Fact sheet**: main characters (one line each), setting(s), key objects, and a chapter-by-chapter or section-by-section plot outline.
2. **Question bank**: target 40–60 questions per book, mixing:
   - "In which book…" questions (answer = title AND author)
   - Detail recall: who / what / where / which object
   - Sequence: what happened next / put events in order
   - Character ID: "Which character…"
3. **Kid-written questions**: an in-app form where the students can add their own questions (saved locally, exportable as JSON so I can merge them into the main bank).

### Question schema (suggested)
```json
{
  "id": "bun-012",
  "book": "bunnicula",
  "type": "in_which_book | detail | sequence | character",
  "prompt": "string",
  "answer": "string",
  "choices": ["optional", "for", "multiple", "choice"],
  "acceptAlso": ["alternate accepted answers"],
  "difficulty": 1,
  "verified": false,
  "source": "note on where it was checked"
}
```

## Modes
- **Book picker** at the top: select one, some, or all books (mirrors the quarter selector in the MAL app).
- **Reference cards**: browse fact sheets per book.
- **Flashcards**: flip-card review.
- **Quiz**: multiple choice or type-in, with feedback after each answer.
- **Mock Battle**: timed rounds that mirror competition format (per-question timer, score at end).
- **Head-to-head / Co-op**: two players on one device. Head-to-head = split-screen buzz-in race. Co-op = team vs. the clock.
- **Admin/Review view**: list all questions, filter by `verified`, edit or toggle.

**Interaction preference:** explicit click/tap to continue after each answer. No auto-advance.

## Gamification
- Mastery meter per book, filling with correct answers; missed questions come back more often (simple spaced repetition / Leitner boxes).
- Streaks and XP for consecutive correct answers.
- Themed badges per book (e.g., a vampire-bunny badge for Bunnicula, a dragon egg that "hatches" as Jeremy Thatcher mastery grows, something Artemis Fowl–flavored and Captain Nobody–flavored). Use original art (emoji, simple CSS/SVG) — no copyrighted cover art or characters' official likenesses.
- Separate player profiles (at least two) so each kid's progress is tracked.

## Persistence
- Save progress and player profiles in `localStorage`, wrapped in try/catch so the app still works if storage is blocked.
- Export/import progress as a JSON file so it can move between devices.
- Optional later: a shared leaderboard across both kids' devices (would need a hosted backend; out of scope for v1).

## Open questions (make configurable, don't hardcode)
- Competition scoring format is not yet confirmed (e.g., points for title vs. title + author, whether questions are "In which book" or about a named book, time per question). Put scoring rules and the Mock Battle timer in a settings object with sensible defaults: 30 seconds per question, full points for title + author, partial for title only.

## Suggested build order
1. Content JSON: fact sheets + question banks for all four books, all marked `verified: false` until checked.
2. Core app shell: book picker, reference cards, flashcards, quiz.
3. Mock Battle with configurable scoring and timer.
4. Game layer: profiles, mastery meters, streaks, badges, spaced repetition.
5. Head-to-head / co-op two-player mode.
6. Kid question-entry form + admin/review view + JSON export/import.

## Acceptance criteria
- Opens by double-clicking the HTML file, fully offline.
- Fits 1366x768 with no scrolling in quiz/battle modes; touch-friendly.
- No quoted book text; unverified questions clearly flagged in review view.
- Progress survives a page reload on the same device.
- Adding a new book = editing the content JSON only.
