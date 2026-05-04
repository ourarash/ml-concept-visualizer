---
name: repo-commit-helper
description: Create repo-aware Conventional Commit messages for ml-concept-visualizer from staged diffs, with deep staged-file inspection and optional commit execution. Use when drafting commit messages, preparing commits, or committing staged work in this repo.
---

# Repo Commit Helper

Use this skill when the user wants a commit message or a git commit for this repository.

## Workflow

1. Check whether anything is already staged.

```bash
git diff --cached --name-only
```

2. If nothing is staged:
   - Check whether the working tree has modified or untracked files.

```bash
git status --short
```

   - If the working tree is dirty, ask this exact question before continuing:
     `No files are staged. Should I stage all current changes with git add -A before I prepare the commit?`
   - Only run `git add -A` if the user says yes.
   - If the user says no, stop and let them choose what to stage manually.
   - If the working tree is clean, say there is nothing to commit and stop.

3. Capture and inspect the staged change set:
   - Always read the staged diff non-interactively:

```bash
git --no-pager diff --staged
```

   - Also inspect full staged file contents. Do not rely only on hunks.
   - Prefer staged blob reads so the analysis matches exactly what will commit:

```bash
git diff --cached --name-only
git show :path/to/file
```

4. Interpret changes in repo context:
   - This is an educational ML and performance concept visualizer collection.
   - Most changes are in standalone HTML visualizer pages organized by topic folders.
   - Meaningful impact usually involves interactive behavior, formulas, explanations,
     diagrams, controls, simulation logic, navigation, or learning flow.
   - Some updates may touch project index/navigation or documentation.

5. Filter for meaningful impact:
   - Focus on meaningful behavior, educational content, conceptual correctness, docs,
     or navigation improvements.
   - Ignore pure formatting, whitespace/lint-only edits, import/order-only edits, and
     dependency metadata-only edits unless they unlock a meaningful feature.
   - Ignore generated/build artifacts and lockfiles unless they are central to the
     requested commit.
   - Prefer user-visible learning and interaction outcomes, such as corrected math,
     improved visualizer logic, added controls, clearer explanations, or discoverability.

6. Write a Conventional Commit message following the strict output format below.

7. If the user asked to actually commit:
   - Draft the final commit message first.
   - Show the message to the user for confirmation unless they clearly asked you to
     proceed without review.
   - After confirmation, run a non-interactive `git commit` with the drafted message.

## Strict Commit Message Format

Return only a single plain-text commit message with these sections and no extra commentary.

1. Subject line
   - Format: `<type>: <description>`
   - Allowed types: `feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`
   - Use imperative present tense.
   - Max 250 characters.
   - Reflect highest-level purpose.

2. Body (optional, 1-5 lines)
   - Explain why the change was made: the motivation or problem solved.
   - Wrap at about 80 characters.
   - Leave one blank line after the subject.

3. Changes section (required)
   - Title exactly: `Changes:`
   - Then bullets:
     `- <file_path>: <meaningful functional or structural change>`
   - Include only meaningful changes.
   - Group logically by module or topic when useful.

4. Footer (optional)
   - If needed, include:
     `BREAKING CHANGE: <description>`
   - Wrap at about 80 characters.
   - Separate from the previous section with one blank line.

## Type Selection

- Use `feat` for new visualizers, new interactions, new conceptual sections, or
  substantial navigation/discoverability additions.
- Use `fix` for corrected math, broken UI/runtime behavior, wrong explanations,
  broken links, or inaccurate educational claims.
- Use `docs` when the staged change is primarily README/catalog/documentation.
- Use `refactor` when behavior is preserved but structure changes materially.
- Use `style` only for formatting-only commits.
- Use `chore` for repository maintenance that is not user-facing.
