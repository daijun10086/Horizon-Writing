# clear-writing

A writing skill for AI agents such as Claude Code and Codex. It teaches an agent to write prose that a reader can understand without having seen the conversation behind it: full sentences, defined terms, numbers with their setting, and plain words instead of AI jargon.

The skill grew out of a complaint that is common in research groups. AI-written text often assumes the reader already has all the knowledge and context, so it arrives as a string of fragments and buzzwords ("root-caused it; the gate was load-bearing; shipped"). This skill puts context first, adds a lab-maintained list of discouraged words with the reason each is discouraged, and draws on two classic sources: Yale Patt's advice on technical writing and William Strunk Jr.'s *The Elements of Style* (1918).

## Install

### The easy way: ask your agent

Paste this into Claude Code, Codex, or another coding agent:

```text
Install the clear-writing skill from https://github.com/daijun10086/clear-writing.
Read INSTALL.md in that repository and follow it, and ask me before you change any files.
```

The agent will ask whether you want the skill in all projects or one project, and whether to add a short set of always-on writing rules to your `CLAUDE.md` or `AGENTS.md`.

### By hand

Clone the repository into your agent's skills folder. The folder must be named `clear-writing`.

For Claude Code, available in all projects:

```bash
git clone --depth 1 https://github.com/daijun10086/clear-writing.git ~/.claude/skills/clear-writing
```

For Codex, available in all projects:

```bash
git clone --depth 1 https://github.com/daijun10086/clear-writing.git ~/.agents/skills/clear-writing
```

For a single project, clone into `.claude/skills/clear-writing` (Claude Code) or `.agents/skills/clear-writing` (Codex) inside that project instead. Other agents that support `SKILL.md` skills work the same way with their own skills folder. Start a new agent session afterwards.

To update, run `git -C ~/.claude/skills/clear-writing pull` (or the Codex path).

### Optional: always-on rules

An agent loads a skill only when it decides the task needs one, so it may skip the skill for a quick commit message or chat reply. The file [`snippets/always-on.md`](snippets/always-on.md) holds a five-point version of the rules. Paste it into `~/.claude/CLAUDE.md` (Claude Code) or `~/.codex/AGENTS.md` (Codex), and the rules will apply to every reply.

## Use

Once installed, the agent uses the skill on its own when it writes documents, emails, paper sections, READMEs, commit messages, and similar text. You can also ask for it directly: type `/clear-writing` in Claude Code, mention `$clear-writing` in Codex, or say "use the clear-writing skill to revise this."

The checker script also works on its own, without an agent. It needs only Python 3:

```bash
python3 ~/.claude/skills/clear-writing/scripts/check_writing.py draft.md
```

It reads Markdown, plain text, and LaTeX, and flags discouraged words, abbreviations used before they are defined, sentences longer than 35 words, em dashes, and "it's not X, it's Y" framing. It skips code, URLs, and citations. Run it with `--help` for options, such as `--allow ISA,ROB` for abbreviations your readers already know.

## What is in the skill

| File | Contents |
|---|---|
| `SKILL.md` | The rules and the workflow the agent follows. |
| `references/word-list.txt` | Discouraged words, grouped by the habit they reveal, with exemptions for literal technical terms such as "race condition." |
| `references/examples.md` | Before-and-after rewrites of typical AI prose. |
| `references/patt-on-writing.md` | A summary of Yale Patt's advice, with a link to the original page. |
| `references/strunk-for-technical-writing.md` | Which of Strunk's rules apply to technical writing today and which to skip. |
| `references/elements-of-style-1918.md` | The full public-domain text of *The Elements of Style* (1918). |
| `scripts/check_writing.py` | The checker. |
| `snippets/always-on.md` | The short always-on rules. |
| `INSTALL.md` | Step-by-step install instructions written for agents. |

## Adding words to the list

The list is meant to grow. To add a word, edit [`references/word-list.txt`](references/word-list.txt) and put the word under the group that fits, or start a new group with its own `# why:` and `# instead:` lines. The comments at the top of the file explain the format. If the word has a normal technical meaning, add an `except:` list so the checker leaves that use alone. Then open a pull request, or push directly if you have access.

The words are discouraged rather than banned. An agent may still use one when it is the most precise word in its literal meaning.

## Sources

- The context rules and the original word list come from guidance our advisor gave the lab about AI writing.
- Yale Patt, "On writing": https://users.ece.utexas.edu/~patt/writing/ (summarized here, not copied).
- William Strunk Jr., *The Elements of Style* (1918), converted from https://daoyuan14.github.io/elos.pdf. The 1918 text is in the public domain in the United States.

## License

The skill's own text and code are under the MIT License (see `LICENSE`). The text of *The Elements of Style* (1918) is in the public domain.
