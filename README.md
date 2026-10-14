# salah-kit/.github

The salah-kit organization's profile page, the community files every repository shares, and the ecosystem standard.

[![CI](https://github.com/salah-kit/.github/actions/workflows/ci.yml/badge.svg)](https://github.com/salah-kit/.github/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## What it is

GitHub gives this repository a special role. Its `profile/README.md` is the [organization's page](https://github.com/salah-kit), and its community files apply to every repository in the organization that doesn't have its own.

| Path | What it is | How GitHub uses it |
|---|---|---|
| [`profile/README.md`](profile/README.md) | The organization's profile | Shown on the organization's page |
| [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) | The Contributor Covenant 2.1 | Linked in every repository's sidebar |
| [`SECURITY.md`](SECURITY.md) | How to report a vulnerability privately | Shown in every repository's Security tab |
| [`SUPPORT.md`](SUPPORT.md) | Where to get help | Linked when someone opens an issue |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to change this repository | Linked when someone opens an issue or pull request in a repository without its own |
| [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE) | Issue forms: bug, calculation method, timetable, translation, RFC | Offered by every repository without its own forms |
| [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md) | The pull-request checklist | Prefills every new pull request |
| [`STANDARD.md`](STANDARD.md) | The ecosystem standard every repository follows | Not used by GitHub |
| [`templates/`](templates) | The files a new repository starts from | Not used by GitHub |
| [`labels.json`](labels.json), [`scripts/sync-labels.sh`](scripts/sync-labels.sh) | The standard's labels, and a script that applies them | Not used by GitHub |

What it deliberately isn't: this repository has no Swift code, no package and no app, so it has no releases, no DocC site and no supported platforms. Where the standard asks for those, this README says so.

## Installation

Nothing to install. GitHub reads these files from `main`.

## Quick start

To start a new repository, copy the files in [`templates/`](templates) and follow [STANDARD.md](STANDARD.md). To apply the standard's labels to a repository:

```sh
scripts/sync-labels.sh --dry-run --prune salah-kit/SalahKit   # see what would change
scripts/sync-labels.sh --prune salah-kit/SalahKit             # apply it
```

`--prune` deletes labels that aren't in `labels.json`, but only those no issue or pull request uses.

## Documentation

[STANDARD.md](STANDARD.md) is this repository's documentation. The packages' documentation is at <https://salah-kit.github.io/SalahTimes/> and <https://salah-kit.github.io/SalahKit/>.

## Supported platforms

Not applicable. The checks need Python 3 and PyYAML, and `sync-labels.sh` needs Bash, Python 3 and the GitHub CLI.

## Status and versioning

This repository has no versions and no tags. Changes land on `main` and take effect right away; [CHANGELOG.md](CHANGELOG.md) lists them.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). A change to [STANDARD.md](STANDARD.md) or [`templates/`](templates) affects every repository, so explain why in the pull request.

## License

MIT. See [LICENSE](LICENSE). The code of conduct is adapted from the Contributor Covenant, under CC BY 4.0: see [NOTICE](NOTICE).
