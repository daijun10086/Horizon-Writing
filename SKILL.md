---
name: clear-writing
description: Write and revise prose that people will read so that it is plain, specific, and understandable without prior context. Use this skill whenever you write or edit text for a human reader, including paper sections, abstracts, reports, emails, README files, documentation, design notes, PR descriptions, commit messages, review comments, and chat answers that explain something. It covers giving the reader enough context, writing in full sentences, avoiding AI-style jargon and a lab-maintained list of discouraged words, and applying Yale Patt's advice on technical writing and Strunk's The Elements of Style. It includes a script that flags discouraged words, undefined abbreviations, and long sentences in a draft.
---

# Clear writing

This skill helps you write text that a reader can understand on the first read, even if they were not part of the conversation or the work behind it. It comes from a research lab's guidance on AI writing.

AI prose tends to have two problems. The first and more serious one is **missing context**. The text assumes the reader already knows the project, the terms, the history, and what was said earlier. As a result, it is full of buzzwords and fragments that only the writer can decode. The second is **inflated vocabulary**: jargon, metaphors, and self-praise that sound impressive but say little. Fix the first problem before the second. Replacing words in a sentence that lacks context does not make it clear.

## Who you are writing for

Before you write, decide who the reader is and what they already know. Unless the user tells you otherwise, picture a capable colleague from a neighboring area: they know the field in general, but they have not seen this conversation, this codebase, or your earlier messages. They do not know your variable names, the internal names of components, or abbreviations you picked up along the way.

If the user names a different reader (a reviewer, an advisor, a new student, a customer), write for that reader instead.

## Rule 1: Give the reader the context

- **Name a thing before you refer to it.** The first time a system, file, experiment, or idea appears, say in plain words what it is. "The cache" is fine only after you have said which cache.
- **Define terms and abbreviations on first use**, unless every reader already knows them (CPU, HTTP, and GPU need no definition for a computing audience). Write "the translation lookaside buffer (TLB)" the first time and "the TLB" afterwards.
- **Say why, not only what.** "We moved the lock" is incomplete. "We moved the lock outside the loop, because taking it on every iteration made the benchmark three times slower" is complete.
- **Give numbers their setting.** A number means little without what was measured, on what, and compared with what. "A 12% speedup" becomes "12% lower median latency than the unmodified server on the YCSB-A workload."
- **Do not point at things the reader never saw.** Avoid "as discussed," "the issue above," "the earlier approach," and "option B" unless the reader can see them. If the reader needs the idea, restate it in a sentence.
- **Let each paragraph stand on its own.** A reader who jumps straight to a paragraph should be able to follow it. Repeating a short definition is better than sending the reader searching.

Context is not the same as length. Cut filler words, but never cut the context. Strunk's rule to omit needless words asks that every word do work; it does not ask that every sentence be short or stripped of detail.

## Rule 2: Write full sentences

- **Use complete sentences with a subject and a verb.** A string of noun phrases such as "Perf regression; root cause lock contention; fix: sharding" makes the reader rebuild the reasoning you left out.
- **Show how ideas connect.** Words such as *because*, *so*, *but*, *although*, and *which means* carry the logic between statements. Without them, the reader has a list of claims and has to guess how they relate.
- **Prefer paragraphs to bullet lists for explanations.** Anything with cause and effect, a comparison, or an argument reads better as a paragraph. Use a list only for items that are truly parallel and independent, such as steps in a procedure, files to change, or options to choose from. Even then, write each item as a full sentence unless it is a plain name or value.
- **Do not use headings in place of transitions.** A short answer needs no headings. In a longer document, the first sentence under each heading should still say what the section is about.

## Rule 3: Use plain words

These rules come from Yale Patt and from Strunk (see `references/`).

- **Short sentences are better than long ones.** When a sentence runs past about 30 words, see whether it is really two sentences.
- **Small words are better than big ones.** Write "use" for "utilize," "show" for "demonstrate," "help" for "facilitate," and "start" for "commence."
- **The verb is the most important word in the sentence.** Put the action in the verb: "we measured latency," not "a measurement of latency was performed." Do not bury verbs in nouns ("perform an analysis of" becomes "analyze"), and do not invent new verbs by adding "-ize" to a noun.
- **Prefer the active voice.** Use the passive only when the actor is unknown or unimportant, or when the thing acted on is the topic of the paragraph.
- **Call the same thing by the same name.** Do not switch among "node," "machine," and "server" for variety; the reader will assume they are three different things. Repeating a word is fine.
- **Put statements in positive form.** "He usually came late" is clearer than "He was not very often on time."
- **Be definite.** State what you found, with the number. If something is uncertain, say once, at the exact point of doubt, what is uncertain and why. Do not hedge every sentence.
- **Put the important words at the end of the sentence**, where the reader's attention lands, and one topic in each paragraph, introduced by its first sentence.
- **Spell every word correctly.** A spell checker does not catch a correctly spelled wrong word.

## Rule 4: Avoid AI-style vocabulary

The lab keeps a list of discouraged words in `references/word-list.txt`. The words are not banned, but you should avoid them unless one is the most precise word in its plain, literal meaning ("race condition," "logic gate," and "pure function" are fine). The list is organized by the habit each word reveals. Learn the habits, because swapping a listed word for its nearest synonym ("honest" to "candid," "load-bearing" to "critical") leaves the same problem in place.

1. **Self-vouching** (honest, genuine, legitimate). These ask the reader for trust instead of giving a reason. Delete the word or show the evidence.
2. **Borrowed rigor** (audited, certify, forensic, provenance, hypothesis, refute, foundational, guarantee). These dress ordinary work up as an audit, a trial, or a formal experiment. Say what you actually did: "I read the three callers of `parse()`," not "I audited `parse()`."
3. **Money and games** (bet, budget, pay, trade, win, race, economics). These hide the literal cost or benefit behind a metaphor. Give the cost or benefit in numbers: "this uses 2 GB more memory and halves the run time."
4. **Physical and engineering metaphors** (load-bearing, gate, screen, envelope, sharpen, onion-peeling, line in the sand, signal). These make the reader decode an image. Name the relationship: "the rest of the proof depends on this lemma."
5. **Moral and dramatic words** (pure, punish, discipline, damage, hazard, surprise, lost). These add judgment or drama to neutral content. Describe what happened and what it caused.
6. **Product talk** (ship). Say what exists and where: "the fix is merged," "the code is on GitHub."
7. **Common AI filler** (delve, leverage, seamless, crucial, notably, showcase) and **needless phrases** from Strunk ("the fact that," "as to whether," "one of the most").

## Rule 5: Avoid AI-style sentence patterns

- **"It's not X, it's Y" and "not just X, but Y."** Say what the thing is. The contrast with a claim nobody made adds nothing.
- **Groups of three** ("fast, robust, and scalable") used for rhythm. Keep only the items you can support, even if that leaves one.
- **Heavy use of em dashes.** Most can be a period, a comma, a colon, or parentheses.
- **Bold labels on every bullet**, **colon-style headings** ("Performance: A Deep Dive"), and **rhetorical questions** answered in the next sentence ("The result? A 2x speedup.").
- **Framing at the start and end.** Do not open by praising the question or restating the task, and do not close with a summary of what you just said or a list of offers. Start with the answer.
- **Stacked hedges** such as "may potentially help to some extent." One qualifier, placed where the doubt is, is enough.

## How to use this skill

1. **Plan.** Before drafting anything longer than a few sentences, write down for yourself who the reader is, what they already know, and the one thing they should take away. Put that thing first.
2. **Draft** following Rules 1 and 2. Worry about context first and word choice second.
3. **Check.** For anything longer than a short chat reply, save the draft to a file and run the checker:

   ```bash
   python3 <this-skill-dir>/scripts/check_writing.py draft.md
   ```

   It also reads standard input (`-`) and handles Markdown, plain text, and LaTeX. It flags listed words, abbreviations used before they are defined, sentences over 35 words, em dashes, and "not X, but Y" framing, and it skips code blocks, inline code, URLs, and citations. Use `--allow ISA,ROB` for abbreviations your readers already know. For a short reply, apply the checklist below from memory instead.
4. **Revise.** For each finding, reread the whole sentence. If the flagged word is the precise literal term, keep it. Otherwise rewrite the sentence around what you mean, instead of swapping in a synonym.
5. **Reread as the reader.** Read the draft as the person from the "Who you are writing for" section would. Wherever they would ask "which one?", "what does that mean?", or "why?", add the answer.

## Checklist

- Would a capable reader who never saw this conversation understand every paragraph?
- Is every term, abbreviation, and internal name defined or explained at first use?
- Does every number come with what was measured and what it was compared with?
- Are the explanations written as full sentences and paragraphs, with the connecting words that show the reasoning?
- Does the main point come first?
- Did the checker's findings get rewritten rather than replaced with synonyms?
- Are the sentences short, the words plain, and the verbs active?

## When the rules give way

- If the user or a venue asks for a specific style, format, or length, follow that and apply these rules inside it.
- When editing someone else's text, keep their voice and structure. Fix clarity and missing context, and leave style choices alone unless asked.
- Quotations, code, identifiers, commands, error messages, and established technical terms stay exactly as they are.
- Strunk wrote in 1918. Follow his rules on composition (Chapter III) and his word advice (Chapter V), but skip the parts that are out of date. These include dividing words at line ends (Rule 8), handwritten-manuscript form (Chapter IV), "he" as the default pronoun (use singular "they"), "should" in place of "would," and spellings such as "to-day." `references/strunk-for-technical-writing.md` lists what applies.

## Reference files

- `references/word-list.txt`: the discouraged words, grouped, with the reason for each group and the literal technical uses that are exempt. The lab adds to it over time.
- `references/examples.md`: before-and-after rewrites of typical AI prose (status updates, commit messages, paper paragraphs, review comments, emails). Read it when you are unsure what a rule looks like in practice.
- `references/patt-on-writing.md`: a summary of Yale Patt's advice on technical writing, with a link to the original.
- `references/strunk-for-technical-writing.md`: which of Strunk's rules apply to technical writing, with examples, and which to skip.
- `references/elements-of-style-1918.md`: the full public-domain text of Strunk's *The Elements of Style* (1918). Read a specific rule when you need its full explanation; do not load the whole book for ordinary tasks.
- `scripts/check_writing.py`: the checker described above. It needs only Python 3.
