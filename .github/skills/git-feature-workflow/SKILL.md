---
name: git-feature-workflow
description: 'Complete git workflow for feature branches: create branch, commit changes, push to remote, create PR, and review. Use when the user asks to commit and push changes, raise a PR, create a pull request, or review code changes on GitHub.'
argument-hint: 'Optional: branch name or PR title'
---

# Git Feature Workflow

Automates the complete git feature branch workflow from local changes to PR review.

## When To Use

Use this skill when the user asks to:
- Commit and push changes to a feature branch
- Create a pull request or raise a PR
- Push code for review
- Open a PR and review changes
- Complete git workflow for a feature

Do not use for:
- Direct commits to main/master (ask for confirmation)
- Hotfixes requiring immediate merge
- Simple local commits without PR

## Workflow Steps

### 1. Check Current State

First, verify the repository status:
- Check current branch
- List modified/untracked files with `git status --short`
- Confirm no merge conflicts

### 2. Create or Switch to Feature Branch

If not already on a feature branch:

```bash
git checkout -b feature/<descriptive-name>
```

Branch naming conventions:
- `feature/<name>` for new features
- `fix/<name>` for bug fixes
- `docs/<name>` for documentation
- `refactor/<name>` for code improvements

If user provides a branch name, use it. Otherwise, derive from commit message or ask.

### 3. Configure Git Identity (If Needed)

Check if git user is configured:

```bash
git config user.name
git config user.email
```

If empty, ask user for name and email, then set:

```bash
git config user.name "User Name"
git config user.email "user@example.com"
```

Use repository-local config (without `--global`) unless user requests otherwise.

### 4. Stage Changes

Stage intended changes:

```bash
git add <file1> <file2>
```

If the user explicitly requests all current changes, then use:

```bash
git add -A
```

### 5. Commit with Descriptive Message

Create a meaningful commit message following conventions:

Format: `<type>: <short description>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Test changes
- `refactor`: Code restructuring
- `chore`: Maintenance tasks

Example:
```bash
git commit -m "feat: add Flask calendar app with event display"
```

**Strategy**: Auto-generate commit message from changed files when the scope is clear (single feature/fix). If changes span multiple concerns or are complex, ask user for clarification.

### 6. Push to Remote

Push the feature branch to remote:

```bash
git push origin <branch-name>
```

If this is the first push for the branch, set upstream:

```bash
git push -u origin <branch-name>
```

### 7. Create Pull Request

#### Option A: GitHub CLI (Preferred)

Check if GitHub CLI is installed:

```bash
gh --version
```

If available, create PR (using `main` as base branch):

```bash
gh pr create --title "<PR title>" --body "<description>" --base main
```

Use repository defaults for reviewers and labels. Add `--draft` flag only if explicitly requested by user.

#### Option B: Web URL

If GitHub CLI is not available:
1. Get the repository remote URL with `git remote get-url origin`
2. Extract owner/repo from URL
3. Provide user with direct PR creation link:
   ```
   https://github.com/<owner>/<repo>/compare/<branch-name>?expand=1
   ```

### 8. Review Changes

After PR is created, provide review options:

#### Using GitHub CLI:
```bash
gh pr view --web
```

#### Manual review checklist:
- [ ] All tests pass
- [ ] Code follows project conventions
- [ ] No sensitive data committed
- [ ] Commit message is clear
- [ ] Branch is up to date with base

## Decision Points

**Already on a feature branch?**
- Yes -> Skip branch creation, proceed to staging
- No -> Create new feature branch first

**Git identity configured?**
- Yes -> Proceed to commit
- No -> Ask user and configure

**GitHub CLI available?**
- Yes -> Use `gh pr create` for seamless PR creation
- No -> Provide web URL for manual PR creation

**Changes already staged?**
- Yes -> Skip staging, proceed to commit
- No -> Stage with `git add`

## Quality Checks

Before pushing:
1. Verify no `.env` or credential files are staged
2. Check for debug code or console logs (brief scan)
3. Ensure branch name is descriptive

**Note**: Tests are not run automatically before push. CI/CD will handle test validation after push.

After PR creation:
1. Provide PR URL for review
2. Note if CI/CD is running (if visible)
3. Confirm next steps

## Example Interactions

**User:** "commit and push my changes to a feature branch and create a PR"

**Assistant actions:**
1. Run `git status --short` to see changes
2. Create branch `feature/implement-calendar-app`
3. Stage files with `git add .`
4. Commit: `feat: implement Flask calendar app with today's events`
5. Push: `git push -u origin feature/implement-calendar-app`
6. Create PR with `gh pr create` or provide web URL
7. Summarize PR link and review status

## Error Handling

**Merge conflicts:**
- Notify user
- Suggest: `git pull origin main` then resolve conflicts

**Push rejected (remote changes):**
- Run `git pull --rebase origin <branch>`
- If conflicts, guide resolution

**GitHub CLI not authenticated:**
- Run `gh auth status`
- If not logged in: `gh auth login`

**No remote configured:**
- Ask user for remote URL
- Add remote: `git remote add origin <url>`

## Output Contract

After completing the workflow, provide:
1. Branch name used
2. Commit SHA and message
3. Push confirmation
4. PR URL (or creation link)
5. Next steps for review or merging
