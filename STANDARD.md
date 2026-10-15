# The salah-kit ecosystem standard

Every repo in the salah-kit org follows this standard, so that someone who knows one repo can find their way around all of them. When a repo has a good reason to differ, its README says so.

## The repos

| Repo | What it is | Kind |
|---|---|---|
| SalahTimes | Prayer-time calculation: methods, high-latitude rules, Qibla | Swift package with no dependencies |
| SalahKit | The app layer: schedules, sources, widgets, alerts, UI building blocks | Swift package that depends only on SalahTimes |
| Salah | A macOS menu-bar app for prayer times, built on SalahKit | App |
| SalahStarter | The template a new prayer app starts from | App template |
| `.github` | The org's profile page and shared community files | Meta |

Calculation engines for the web (TypeScript) and Android (Kotlin) come later, each in its own repo, and pass the same JSON vectors as SalahTimes.

## Names

- Repos and Swift modules use UpperCamelCase and start with `Salah`.
- Bundle identifiers start with `io.github.salah-kit.`, the reverse of the org's GitHub Pages domain. App Groups are `group.io.github.salah-kit.<App>`. The template uses `com.example.` placeholders.
- `main` is the only long-lived branch. Work happens on short-lived branches named for their topic.
- Tags are SemVer without a `v`, like `0.1.0`.

## Files in every repo

Start each of these from `templates/`, which `salah-kit/.github` also publishes.

- `README.md`, with these sections in this order:
  1. the name and a one-sentence summary;
  2. badges for CI, the latest release and the license;
  3. what it is, and what it deliberately isn't;
  4. installation;
  5. a quick start;
  6. a link to the documentation;
  7. supported platforms;
  8. status and versioning;
  9. contributing;
  10. the license.
- `LICENSE`: MIT, `Copyright (c) 2026 The Salah Kit Authors`.
- `AUTHORS`: `Omar Khaled (@omar-hanafy)`.
- `NOTICE`, when the repo contains third-party code, data or media: what it is, where it came from, and its license.
- `CHANGELOG.md` in the Keep a Changelog format, with an Unreleased section and one section per tag.
- `CONTRIBUTING.md`: how to build, test and format this repo.
- `.swift-format`, identical in every repo: the formatter's defaults (2-space indentation, 100 columns).
- `.gitignore`, starting from `templates/gitignore`.
- `.github/workflows/ci.yml`, plus `docs.yml` in packages.

The code of conduct, security policy, support page, issue templates and pull-request template live once, in `salah-kit/.github`. Repos don't copy them.

## Swift

- Swift 6 language mode with complete concurrency checking.
- Value types are `Sendable`. `@unchecked Sendable` needs a comment that proves it's safe.
- Keep `swift-tools-version` and the platform minimums as low as the APIs allow:
  - SalahTimes aims lowest;
  - SalahKit uses iOS 16, macOS 13, watchOS 9, tvOS 16 and visionOS 1.
- Every public symbol has a DocC comment.
- Library code doesn't force-unwrap, and doesn't call `fatalError` on a path an adopter can reach.
- Format with `swift format` using the shared configuration. CI runs `swift format lint --strict`.
- Packages build and test on Linux. Code that imports an Apple-only framework sits behind `#if canImport(…)`; pure logic stays outside those guards.
- No dependencies unless they're unavoidable.

## Tests and vectors

- Unit tests use Swift Testing. App journeys use XCUITest.
- Behavior that another language must reproduce is written as JSON in `Vectors/`.
  - `Vectors/README.md` documents the schema.
  - Every file carries a `schemaVersion`.
  - Every vector has an id, its inputs, the expected outputs, and a note on where the expectation comes from.
- A bug fix comes with a regression test that would have caught it.

## CI

GitHub Actions run on pull requests and on pushes to `main`. Official actions are pinned to a major version.
- **Packages:**
  - a macOS job: build and test, plus builds for every supported Apple platform;
  - a Linux job: build and test;
  - a lint job;
  - a docs job on `main`.
- **Apps:** build, unit tests, UI tests on simulators or macOS, and lint.

A job that can't run on hosted runners, for example because a simulator runtime is missing, becomes build-only and says why in the workflow file.

## Documentation

- Every package module has a DocC catalog. The docs job publishes them to `https://salah-kit.github.io/<Repo>/` from `main`.
- Building docs adds no package dependency (no `swift-docc-plugin`):
  1. `xcodebuild docbuild` builds one archive per module;
  2. `xcrun docc merge` combines a multi-module package's archives into one;
  3. `xcrun docc process-archive transform-for-static-hosting --hosting-base-path <Repo>` makes the site.
- The code in getting-started articles comes from tested examples, so it compiles.
- App READMEs show screenshots that the test suite renders, not hand-made ones.

## Releases

- Packages follow SemVer and stay below 1.0 until all of these hold:
  - two shipped apps that differ in platform and in data source have used tagged 0.x releases for a release cycle, and at least one of them is maintained independently of this org;
  - the findings from those integrations are resolved, and the API RFC reflects them and is closed;
  - native speakers have reviewed the localized prayer vocabulary;
  - every example builds in CI, and the device and behavior checks have evidence.
- Apps use a marketing version and a build number.
- Every tag gets a CHANGELOG section and a GitHub release with three headings:
  - **Proven:** the gates and their evidence;
  - **Pending:** what still needs a person or a device;
  - **Known limitations.**
- Commits, tags, releases, issues and pull requests carry no AI attribution and mention no people.

## Apps

- XcodeGen generates the Xcode project from a committed `project.yml`. The generated project is committed too, so building needs nothing extra.
- Signing:
  - Never commit `DEVELOPMENT_TEAM`.
  - A committed `Config/Shared.xcconfig` (from `templates/Config/`) ends with `#include? "Local.xcconfig"`, and each developer puts their team in their own gitignored `Local.xcconfig`.
- Every target that uses a required-reason API has a privacy manifest.
- Strings live in String Catalogs. Every UI supports Arabic and right-to-left layout. Machine-drafted translations are marked as needing review.
- Accessibility:
  - every control has a VoiceOver label;
  - Dynamic Type is supported wherever the platform allows;
  - colors pass SalahUI's `ContrastCheck`.
- Bundled media needs clear redistribution rights, recorded in NOTICE.

## Labels

Every repo uses the same labels: `bug`, `enhancement`, `documentation`, `calculation-method`, `timetable`, `translation`, `rfc`, `good first issue`, `help wanted`.

## Governance

- Public API changes to a package go through an RFC: `docs/rfcs/NNNN-title.md` in that repo, discussed in GitHub Discussions.
- `main` is protected in every repo: no force pushes, no deletion, linear history.
