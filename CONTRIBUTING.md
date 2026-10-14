# Contributing

This file has two jobs.

- **For this repository** (`salah-kit/.github`), it explains how to change the profile page,
  the community files, the standard and the labels.
- **For any salah-kit repository without its own CONTRIBUTING.md**, GitHub shows it as the
  fallback. SalahTimes, SalahKit, Salah and SalahStarter each have their own, which explains
  how to build, test and format that repository. To contribute code, read that one.

Everyone follows the [code of conduct](CODE_OF_CONDUCT.md). Report vulnerabilities privately,
as the [security policy](SECURITY.md) describes.

## Changing this repository

- Keep each pull request to one topic, on a branch named for it.
- Add a line to the Unreleased section of [CHANGELOG.md](CHANGELOG.md).
- Write like the rest of the ecosystem: plain, short sentences, and no claim that isn't true
  today. The profile page states only evidence that has been collected.
- In `profile/README.md`, use absolute `https://` links. GitHub shows the profile on the
  organization's page, where relative links don't resolve.

### The standard and the templates

[STANDARD.md](STANDARD.md) and [`templates/`](templates) apply to every repository. Explain the
reason for a change in the pull request, and list the repositories that need a follow-up
change. `.swift-format` at the root must stay byte-identical to `templates/.swift-format`; CI
checks it.

### Issue forms and labels

The issue forms in [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE) use GitHub's issue
form syntax. A form may use only labels from [labels.json](labels.json), and `labels.json`
holds exactly the labels STANDARD.md lists. To add a label, change STANDARD.md and
`labels.json` together, then apply it:

```sh
scripts/sync-labels.sh --dry-run --prune salah-kit/SalahTimes salah-kit/SalahKit \
  salah-kit/Salah salah-kit/SalahStarter salah-kit/.github
```

Check the output, then run the same command without `--dry-run`. The script creates missing
labels and updates colors and descriptions. With `--prune` it also deletes labels that aren't
in `labels.json`, but keeps any that an issue or pull request uses, and says so. Running it
twice changes nothing the second time. It needs the GitHub CLI, signed in with permission to
manage labels.

## Checks

CI runs these on every pull request. Run them before you push:

```sh
python3 -m pip install pyyaml==6.0.3
python3 scripts/check.py
shellcheck scripts/sync-labels.sh
```

`check.py` checks that every issue form parses and has the fields GitHub requires, that the
forms' labels and `labels.json` match STANDARD.md, that `.swift-format` matches the template,
and that every relative link in the Markdown files resolves. Markdown in `templates/` is
skipped, because its links resolve only in the repository that copies it.

The absolute links are checked separately, weekly and on demand, so that a slow external site
never blocks a pull request:

```sh
python3 scripts/check-links.py
```
