# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). This repository has no versions, so
every change is listed under Unreleased.

## [Unreleased]

### Changed

- Give the organization profile a Contribute section, which links the open `help wanted`
  issues, each repository's CONTRIBUTING and the RFC process.
- Link the adoption guide's API feedback to the SalahKit RFCs, and state the standard's
  branch protection plainly.
- Describe Salah's released use of SalahKit on the organization profile, link its pending
  evidence, and apply the security policy to its latest release.

### Added

- The organization's profile page, `profile/README.md`: the ecosystem and its public-first goal,
  the repositories, where to start, the status and pending evidence, the roadmap and how to
  contribute.
- Community files for every repository without its own: the Contributor Covenant 2.1 code of
  conduct, a security policy with private vulnerability reporting, a support page, a
  pull-request template, and issue forms for bugs, calculation methods, timetables,
  translations and RFCs.
- The ecosystem standard, `STANDARD.md`, and the `templates/` a new repository starts from.
- `labels.json`, the standard's nine labels, and `scripts/sync-labels.sh`, which applies them to
  repositories.
- CI: `scripts/check.py` checks the issue forms, the labels, `.swift-format` and relative links
  on every pull request; `scripts/check-links.py` checks absolute links weekly.
- This repository's README, LICENSE, AUTHORS, NOTICE, CONTRIBUTING and `.swift-format`.
