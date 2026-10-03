"""Validate content JSON and write a printable fact-check checklist.

Usage: python tools/build_factcheck.py content/battle1-2026.json
Writes FACT-CHECK.md next to the JSON file.
"""
import json, sys, collections, pathlib

path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "content/battle1-2026.json")
data = json.loads(path.read_text(encoding="utf-8"))
books = {b["id"]: b for b in data["books"]}
TYPES = {"in_which_book", "detail", "sequence", "character"}
errors, ids = [], set()

for q in data["questions"]:
    qid = q.get("id", "?")
    if qid in ids: errors.append(f"{qid}: duplicate id")
    ids.add(qid)
    if q.get("book") not in books: errors.append(f"{qid}: unknown book {q.get('book')}")
    if q.get("type") not in TYPES: errors.append(f"{qid}: bad type {q.get('type')}")
    for k in ("prompt", "answer"):
        if not q.get(k): errors.append(f"{qid}: missing {k}")
    d = q.get("distractors", [])
    norm = lambda x: x.strip().lower()
    right = {norm(q.get("answer", ""))} | {norm(a) for a in q.get("acceptAlso", [])}
    if len(d) != 3: errors.append(f"{qid}: needs exactly 3 distractors (has {len(d)})")
    if len({norm(x) for x in d}) != len(d): errors.append(f"{qid}: duplicate distractors")
    if any(norm(x) in right for x in d): errors.append(f"{qid}: a distractor matches a correct answer")
    for k in ("hint", "explanation"):
        if not q.get(k): errors.append(f"{qid}: missing {k}")
    if q.get("hint") and q["type"] != "in_which_book" and len(q["answer"]) > 3 and norm(q["answer"]) in norm(q["hint"]):
        errors.append(f"{qid}: hint gives away the answer")

counts = collections.Counter((q["book"], q["type"]) for q in data["questions"])
conf = collections.Counter((q["book"], q.get("confidence", "?")) for q in data["questions"])

out = ["# Fact-Check Checklist — " + ", ".join(b["name"] + " " + b["season"] for b in data["battles"]), "",
       "Tick each box once you've confirmed it against the book. Then set `\"verified\": true` in the JSON",
       "(or use the app's Review view later). Check **memory** and **weak** items first.", "",
       "Source key: " + "; ".join(f"**{k}** = {v}" for k, v in data["sources"].items()), ""]
for bid, b in books.items():
    qs = [q for q in data["questions"] if q["book"] == bid]
    out += [f"## {b['title']} — {b['author']}", "",
            f"{len(qs)} questions · " + ", ".join(f"{t}: {counts[(bid, t)]}" for t in sorted(TYPES)) +
            " · confidence: " + ", ".join(f"{c}: {conf[(bid, c)]}" for c in ("school", "sourced", "weak", "memory") if conf[(bid, c)]), ""]
    if b.get("status") == "skeleton" and not qs:
        out += ["_Skeleton only: fact sheet and questions not written yet._", ""]
        continue
    fs = b["factSheet"]
    out += ["### Fact sheet", "", f"> {fs['summary']}", "", "**Characters**", ""]
    out += [f"- [ ] **{c['name']}** ({c['role']}): {c['desc']} _[{c.get('source','')}]_" for c in fs["characters"]]
    out += ["", "**Settings**", ""] + [f"- [ ] **{s['name']}**: {s['desc']} _[{s.get('source','')}]_" for s in fs["settings"]]
    out += ["", "**Key objects**", ""] + [f"- [ ] **{o['name']}**: {o['desc']} _[{o.get('source','')}]_" for o in fs["keyObjects"]]
    out += ["", "**Themes**", ""] + [f"- **{t['name']}**: {t['desc']}" for t in fs["themes"]]
    out += ["", "**Plot outline**", ""] + [f"- [ ] **{o['section']} — {o['title']}**: {o['summary']} _[{o.get('source','')}]_" for o in fs["outline"]]
    out += ["", "### Questions", ""]
    for q in sorted(qs, key=lambda q: ({"memory": 0, "weak": 1}.get(q.get("confidence"), 2), q["id"])):
        flag = {"memory": " ⚠️ MEMORY", "weak": " ⚠️ WEAK"}.get(q.get("confidence"), "")
        ans = " → ".join(q["order"]) if "order" in q else q["answer"]
        out.append(f"- [ ] `{q['id']}` ({q['type']}, diff {q.get('difficulty')}){flag} — {q['prompt']}  ")
        out.append(f"      **A:** {ans} _[{q.get('source','')}]_  ")
        if q["type"] != "in_which_book":
            out.append(f"      Wrong choices: {' · '.join(q['distractors'])}  ")
        out.append(f"      Hint: {q['hint']}  ")
        out.append(f"      Why: {q['explanation']}")
    out.append("")

(path.parent / "FACT-CHECK.md").write_text("\n".join(out), encoding="utf-8")
print(f"{len(data['questions'])} questions, {len(books)} books")
for bid in books:
    print(f"  {bid}: " + ", ".join(f"{t}={counts[(bid, t)]}" for t in sorted(TYPES)) +
          " | " + ", ".join(f"{c}={conf[(bid, c)]}" for c in ("school", "sourced", "weak", "memory")))
print("ERRORS:" if errors else "No errors.", *errors, sep="\n  ")
sys.exit(1 if errors else 0)
