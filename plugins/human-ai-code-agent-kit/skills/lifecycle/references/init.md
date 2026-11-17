# lifecycle init — prepare a project for a long run

Goal: a contract-conforming `LIFECYCLE.md` at the repository root
(`contract.md`; skeleton `../assets/LIFECYCLE.template.md`), the development
rules adopted into the rules doc, the rule check vendored, the state
directory created, the commit authorization recorded, and the host contract
located. Every write below needs the human's approval of the drafted
content.

## Procedure

1. **Guard.** `LIFECYCLE.md` exists → show its first lines; change it only
   with explicit confirmation. It is human-owned.
2. **Explore before asking.** From the repository: the requirements and spec
   documents, milestone or roadmap lists with acceptance items, check commands
   (CI configuration, task runners, the rules doc), branch and merge habits
   (`git log --oneline -30`, `git branch -a`), version source and changelog,
   packaging and install path, existing benchmarks, `.gitignore`.
3. **Interview only for policy the repository cannot show:** protected
   standards, spec sections the agent may edit, system scope (users, trust
   boundaries, threat model) when the spec does not state it, hotfix classes
   beyond the defaults, project gates, what publishing means.
4. **Draft `LIFECYCLE.md`** from the template: marker on line 1, every
   required section filled or marked as an open question. Before showing it,
   scan the draft for personal and machine facts (home-directory paths, user
   and host names, addresses, model tier names, agent command lines, private
   repository names); they belong in the host contract. The draft is tracked
   and may be published.
5. **Rules.** If `<rules doc>` is missing, offer `impl init` first. Propose the
   block from `development-rules.md` as a new section of the rules doc, the
   listed human-owned files as protected zones, and the linter configuration
   changes. Vendor `../scripts/check_diff_rules.py` to the path `<rule check>`
   names. Each is a Rules gate item; apply only what the human approves.
6. **State directory.** Create `<state dir>` with the agent-workspace files,
   an empty `INBOX.md` with a one-line note on its use, `human-inputs.md`
   holding the human's initiating instruction verbatim as H1, `backlog.md`,
   `decided.md`, and the state line
   `lifecycle: state=running cycle=1 stage=cycle-planning step=- last=init`.
   If the project doc says the directory is untracked and git does not ignore
   it, report that; do not edit `.gitignore` without approval.
7. **Commit authorization.** Ask the human to approve local commits,
   merges, and tags on the run's branches as `<branch policy>` names them;
   pushing and publishing stay behind the Authorization boundary gate.
   Record the approval verbatim as H<n> in `human-inputs.md`, or the human
   adds it as a standing-authorization row in the host contract. Without
   it the run asks at its first commit, merge, or tag.
8. **Host contract.** Look for `LIFECYCLE-HOST.md` in the user-level contract
   directory. Missing → offer `../assets/LIFECYCLE-HOST.template.md` to the
   human; filling it is the human's work, drafted together on request. Never
   copy it into the project.
9. **Smoke.** Run `status`; it must print the state line, no missing P key,
   and the host keys that fall back to defaults.
