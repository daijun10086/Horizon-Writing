<!--
Optional always-on rules for clear-writing.
A skill loads only when the agent decides a task needs it, so short pieces of
writing (commit messages, chat answers) can miss it. Paste the block below into
the file your agent reads at the start of every session:
  Claude Code: ~/.claude/CLAUDE.md (all projects) or ./CLAUDE.md (one project)
  Codex:       ~/.codex/AGENTS.md (all projects) or ./AGENTS.md (one project)
  Others:      AGENTS.md, GEMINI.md, .cursor/rules, or the agent's equivalent
-->

## Writing style

When you write prose for people (answers, documentation, commit messages, PR descriptions, review comments, emails, paper text), follow these rules. For longer writing, also use the clear-writing skill and run its checker.

- Write for a capable reader who has not seen this conversation or this codebase. Name things before you refer to them, define abbreviations and internal names on first use, and give every number its setting (what was measured, on what, compared with what).
- Write in full sentences and paragraphs that show the reasoning with words like "because," "so," and "but." Use bullet lists only for parallel items such as steps or options.
- Use short sentences, plain words, active verbs, and the same name for the same thing. Put the main point first.
- Avoid self-vouching words (honest, genuine, legitimate), borrowed rigor (audited, forensic, hypothesis, certify), money and game metaphors (bet, budget, pay, win), engineering metaphors (load-bearing, gate, screen, envelope), and dramatic words (pure, surprise, damage). Use such a word only in its literal technical sense, as in "race condition" or "logic gate." Do not fix one of these by swapping in a synonym; rewrite the sentence to say what you mean.
- Avoid "it's not X, it's Y" framing, groups of three for rhythm, heavy use of em dashes, and opening or closing filler such as praising the question or summarizing what you just said.
