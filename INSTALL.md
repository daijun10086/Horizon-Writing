# Installing Horizon Writing (instructions for AI agents)

This file is written for an AI coding agent (Claude Code, Codex, or similar) that a user has asked to install this skill. If you are a person, the README has the same steps in shorter form.

The repository is https://github.com/daijun10086/Horizon-Writing. The skill is the repository itself: `SKILL.md` sits at the top level, next to `references/`, `scripts/`, and `snippets/`.

## Step 1: Ask the user before changing anything

Installing a skill writes files into the user's configuration, so ask first. Tell the user what the skill does in one or two sentences (it helps agents write clear prose with full context, and it includes a word list and a checker script). Then ask two questions and wait for the answers:

1. Should the skill be available in **all projects** (a personal install) or **only the current project**?
2. Should you also add the short **always-on writing rules** from `snippets/always-on.md` to their agent instructions file? Explain that a skill loads only when the agent decides a task needs it, while the always-on rules apply to every reply, including short ones such as commit messages.

## Step 2: Pick the install folder

The folder must be named `horizon-writing`, matching the `name` field in `SKILL.md`.

| Agent | All projects | Current project only |
|---|---|---|
| Claude Code | `~/.claude/skills/horizon-writing` | `.claude/skills/horizon-writing` |
| Codex | `~/.agents/skills/horizon-writing` | `.agents/skills/horizon-writing` |
| Other agents that support `SKILL.md` skills | the agent's documented personal skills folder | the agent's documented project skills folder |

On Windows, `~` means `%USERPROFILE%`. Some older versions of Codex read personal skills from `~/.codex/skills` instead; if the skill does not appear after a restart, tell the user and offer to move it there.

If your agent has no skill support at all, clone the repository to any stable place, such as `~/.local/share/horizon-writing`. Then, in Step 5, add the always-on rules together with one more line: tell the agent to read `<that path>/SKILL.md` before longer writing tasks.

## Step 3: Download the skill

If the target folder already exists, do not overwrite it. Ask the user whether to update it (`git -C <folder> pull` if it is a git clone) or leave it alone.

Otherwise, clone the repository into the target folder:

```bash
git clone --depth 1 https://github.com/daijun10086/Horizon-Writing.git <target-folder>
```

If `git` is not available, download https://github.com/daijun10086/Horizon-Writing/archive/refs/heads/main.zip, unzip it, and rename the extracted folder (`Horizon-Writing-main`) to `horizon-writing` at the target location.

## Step 4: Check the install

1. Confirm that `<target-folder>/SKILL.md` exists and starts with a front matter block containing `name: horizon-writing`.
2. Run the checker on the examples file, which contains deliberately bad "before" text:

   ```bash
   python3 <target-folder>/scripts/check_writing.py <target-folder>/references/examples.md
   ```

   It should print a list of findings and exit with status 1. That is the expected result, and it shows the script and its word list work. The script needs only Python 3. If Python 3 is missing, tell the user that the skill still works without the checker.

## Step 5: Add the always-on rules (only if the user agreed)

Copy the part of `snippets/always-on.md` that starts at `## Writing style` (skip the HTML comment above it) and append it to the right file:

| Agent | All projects | Current project only |
|---|---|---|
| Claude Code | `~/.claude/CLAUDE.md` | `./CLAUDE.md` |
| Codex | `~/.codex/AGENTS.md` | `./AGENTS.md` |
| Other agents | the agent's global rules file | `AGENTS.md` or the agent's project rules file |

Before appending, check whether the file already has a `## Writing style` section from this skill. If it does, do not add a second copy. Create the file if it does not exist. Show the user the text you added.

## Step 6: Tell the user how to use it

Tell the user where you installed the skill and what you changed. Then explain:

- The agent may need a new session, or a restart, to see a newly installed skill.
- The skill loads on its own for writing tasks. The user can also ask for it by name: in Claude Code, type `/horizon-writing` or say "use the horizon-writing skill"; in Codex, mention `$horizon-writing`.
- To get updates later, run `git -C <target-folder> pull`.
- The lab adds words to `references/word-list.txt` over time; updates bring those in.
