# Security policy

This policy covers every repository in the [salah-kit](https://github.com/salah-kit) organization: SalahTimes, SalahKit, Salah, SalahStarter and `.github`.

## Reporting a vulnerability

Report a vulnerability privately. Don't open a public issue, discussion or pull request for it.

1. Open the affected repository's **Security** tab and choose **Report a vulnerability**. The form is at `https://github.com/salah-kit/<Repo>/security/advisories/new`, for example [SalahKit's](https://github.com/salah-kit/SalahKit/security/advisories/new).
2. If that button isn't there, email omar_hanafy@icloud.com instead, with "salah-kit security" in the subject.

Include what you can:

- the repository, and the release or commit you tested;
- what an attacker can do, and what they need first;
- steps or a small input that reproduces it;
- whether you plan to publish your findings, and when.

You can expect an acknowledgment within about a week. Anything after that, including a fix and an advisory, is worked out with you in the private report.

## Supported versions

| Repository | Supported |
|---|---|
| SalahTimes | The latest release |
| SalahKit | The latest release |
| Salah | The latest release; the `main` branch until its first release |
| SalahStarter | The `main` branch, the template new projects start from |

The packages are pre-1.0. A fix ships in a new release; older releases don't get backports.

## What counts as a vulnerability

In scope:

- a crash, hang or unbounded memory use caused by untrusted input, for example timetable JSON that an app downloads and decodes with SalahKit;
- data exposed through the App Group that an app shares with its widget extension, beyond what the documentation says is stored there;
- anything that lets one app, extension or process read or change another app's data;
- a workflow or release process in these repositories that would let someone change what adopters download.

Out of scope. These are bugs: report them in public, with the affected repository's issue forms.

- a wrong prayer time, a wrong calculation-method parameter or a timetable that SalahKit reads differently from its publisher;
- a crash from input that only the app's own code creates, such as an out-of-range setting;
- a missing or wrong translation.
