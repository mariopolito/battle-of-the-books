# Battle of the Books Study App

**Double-click `index.html`** to open it, or host it on GitHub Pages. It works offline in any modern browser with no install. Progress is saved in that browser on that device.

## Players
Like the MAL app, **each device belongs to one player**. On the first visit it asks for a name and an avatar (an icon plus a color badge). Click your name in the top bar to change them or to manage **teammates**. Teammates are names and avatars you can pick in Head-to-Head and the Co-op Boss Battle (Guest is always available). Only your own progress is saved, because your teammate's progress lives on their device.

**Teams** have 2 or 3 kids: you plus 1 or 2 teammates. Right after the name screen, players set a **team name** and pick their teammates. The **team badge** defaults to a mix of the members' avatars (their icons on a gradient of their colors), or the team can pick its own icon and colors. The team shows in the top bar (click it to edit), fills the Head-to-Head and Co-op seats, and appears in Co-op and Mock Battle results.

## For the kids
- **Battle tabs** at the top: Battle 1, Battle 2, Battle 3, and District & Regional (all 12 books). Then **pick your books**: tap a book to turn it on or off.
- **🏰 Battle Day**: what to expect at a competition, covering the two phases, the clock, scoring, rules, tips, and key dates (from the school handout).
- **📖 Reference Cards**: characters, settings, key objects, themes, and the plot outline.
- **🃏 Flashcards**: pick one or more decks: a book, the 📋 School study guide, Phase I / Phase II questions, ✍️ Titles & authors, Characters, or Places & objects. Tap **I know this one** to set a card aside as mastered. Missing that question anywhere else puts it back.
- **❓ Quiz**: multiple choice or type-in, from everything, just the School study guide, our question bank, or kid-made questions.
- **⏱️ Mock Battle**: the real format. Phase I is 5 "in which book" rounds (30 s, title 5 pts + author 3). Phase II is 3 short-fact rounds (20 s, 10 pts). Tap answers, or use **Say it out loud**: someone reads the question, the spokesperson answers aloud, and you score yourselves.
- **⚔️ Head-to-Head**: two players, one screen. First correct tap wins (keyboard: A S D F vs J K L ;).
- **🤝 Co-op Boss Battle**: the two players against a boss from one of the books (🧌 the Rogue Troll, 🧛 the Vegetable Vampire…). Each round is a challenge that one player can't beat alone:
  - 🗂️ **Book Sort**: each player guards half the books. Clues (minor characters, places, objects, "in which book" clues) fly in on a timer, and only the right book's guard may grab each one.
  - 🧩 **Match-Up**: one player holds the names, the other holds the descriptions (two books mixed together). Every pair needs both players.
  - 🕰️ **Timeline**: the events are dealt between the players. Whoever holds the next event has to play it.
  - 📡 **Crossed Wires**: each player's question has its answers on the *other* player's side. Read yours aloud and answer your teammate's.
  
  Right moves damage the boss, mistakes cost shared hearts, and a perfect round is a critical hit. Difficulty levels: Warm-up, Challenge, and Legendary.
- **✏️ Write a Question**: add your own questions to the practice pool.
- **🏆 Trophies**: XP, levels, streaks, a badge for each book that grows as you master it, and your teammates.

Questions you miss come back more often (5 "Leitner boxes" per player). Keyboard: 1–4 to answer, Enter to continue. Flashcards: Space flips, ← → move, M marks mastered.

## For parents and coaches (🔒 Parent / Coach area, bottom of the home screen)
- **Review questions**: filter, search, tick **Verified**, or edit any question. Edits are saved on this device.
- **Settings**: Mock Battle timer and scoring, XP, quiz length, and **"Only use questions I've marked verified."**
- **Data**: export/import progress to move it between devices, and export content JSON to keep your edits for good.

## Editing content
The question bank and fact sheets are in `content/battle1-2026.json`. After editing it:

```bash
python tools/build_factcheck.py content/battle1-2026.json
python tools/embed_content.py
```

The first command checks the file and regenerates `content/FACT-CHECK.md`. The second copies the JSON into the block at the top of `index.html`. You can also edit that block in the HTML directly.

To keep edits made in the app's Review screen, use **Export content JSON**, save the file over `content/battle1-2026.json`, and run the two commands above.

Battles 2 and 3 are **skeletons**: their books (title, author, pages, genre, Lexile, AR) are in the JSON with `"status": "skeleton"` and empty fact sheets. Fill in each book's `factSheet` and add `questions` with that book's `id`, and everything (flashcards, quiz, battles, co-op) picks them up. No code changes are needed. The Battle Day page text lives in the JSON's `competition` block.

## Hosting on GitHub Pages
- `index.html` is the whole site. There's nothing to build, and Pages serves it as is.
- `.gitignore` keeps `BoTB.pdf` (the school handout, which includes staff contact details and school forms) and `.claude/` out of the repo. The Battle Day page only paraphrases the rules.
- Progress is saved in each visitor's own browser under the key `bob.v1`, so nothing about the kids is ever uploaded. All your github.io sites share one browser storage area, but this key doesn't collide with the MAL app's.
- Moving from a double-clicked file to the hosted site starts fresh, because a different address means different browser storage. Use Parent area → Data → **Export progress** on the old copy and **Import progress** on the new one.
