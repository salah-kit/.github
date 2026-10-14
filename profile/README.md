# salah-kit

Open-source Swift packages that any prayer app can build on.

salah-kit gives a prayer-time app its foundations: a calculation engine, a typed prayer schedule from calculated times or a mosque's published timetable, widget timelines that don't need the app to run, prayer alerts within the system's notification limit, and SwiftUI building blocks you restyle. Public adopters come first: the API is shaped by what many apps need. Salah, the ecosystem's own macOS app, uses the packages as one consumer and a working sample; it doesn't set the shape of the API. To make a prayer app, build your own on the packages instead of forking an existing one. The code is MIT-licensed; each repository's NOTICE lists the third-party data and media it includes, under their own terms.

## Repositories

| Repository | What it's for | Latest release |
|---|---|---|
| [SalahTimes](https://github.com/salah-kit/SalahTimes) | The calculation engine: published methods, high-latitude rules and Qibla, in a Swift package with no dependencies. Its JSON vectors are the contract that engines in other languages must pass. | [![SalahTimes release](https://img.shields.io/github/v/release/salah-kit/SalahTimes?include_prereleases&sort=semver&label=)](https://github.com/salah-kit/SalahTimes/releases) |
| [SalahKit](https://github.com/salah-kit/SalahKit) | The app layer, in six products: SalahCore (the schedule, published timetables, iqama, prayer names), SalahCalculation (SalahTimes as a schedule source), SalahWidgets, SalahUI, SalahAlerts and SalahFixtures. | [![SalahKit release](https://img.shields.io/github/v/release/salah-kit/SalahKit?include_prereleases&sort=semver&label=)](https://github.com/salah-kit/SalahKit/releases) |
| [SalahStarter](https://github.com/salah-kit/SalahStarter) | The template a new app starts from: an iPhone app and a widget extension wired to a shared App Group, with prayer alerts, on SalahKit. | Template |
| [Salah](https://github.com/salah-kit/Salah) | A macOS menu-bar app for prayer times, open source and built on SalahKit. Its source releases are a working sample of the packages in use. | [![Salah release](https://img.shields.io/github/v/release/salah-kit/Salah?include_prereleases&sort=semver&label=)](https://github.com/salah-kit/Salah/releases) |
| [.github](https://github.com/salah-kit/.github) | This page, the community files every repository shares, and the [ecosystem standard](https://github.com/salah-kit/.github/blob/main/STANDARD.md) all of them follow. | |

## Start here

1. **Create your app from [SalahStarter](https://github.com/salah-kit/SalahStarter).** Choose "Use this template", then follow its README: set your signing team, your bundle identifiers and your App Group, and you have a working prayer widget.
2. **Read the documentation.** [SalahKit's](https://salah-kit.github.io/SalahKit/) getting-started articles cover a calculated prayer app, a mosque timetable with iqama, widgets and alerts. [SalahTimes'](https://salah-kit.github.io/SalahTimes/) cover choosing a method and high latitudes.
3. **Or add the packages to an app you have.** Both install with Swift Package Manager; their READMEs show how.

The [adoption guide](https://github.com/salah-kit/.github/blob/main/docs/adopting.md) helps you choose products, test an integration and report feedback. Both packages are listed on Swift Package Index: [SalahTimes](https://swiftpackageindex.com/salah-kit/SalahTimes) and [SalahKit](https://swiftpackageindex.com/salah-kit/SalahKit). Their [submission was accepted](https://github.com/SwiftPackageIndex/PackageList/pull/15688); the index's compatibility results are pending.

## Status

The packages are pre-1.0. They follow Semantic Versioning, so until 1.0 a minor release may change the API. Each release's notes list what is proven and what is pending.

SalahTimes' [validation report](https://github.com/salah-kit/SalahTimes/blob/main/docs/validation.md) records independent ephemeris comparisons, official timetable coverage and remaining method-specific differences. Choose and check the method or published timetable appropriate to your location; a named preset is not a guarantee of agreement with every local authority.

Simulators, cross-process harnesses and fixed-clock tests cover the packages' behavior today. The evidence that still needs a person, hardware or elapsed time includes:

- a native-language check of the calculation methods' sources, several of which are secondary;
- a seven-day iPhone widget soak, with the app never opened, and the timeline's cost on the oldest supported iPhone;
- the examples on real devices: a mosque board on an iPad, a phone app on an iPhone, a watch complication on an Apple Watch;
- notification delivery on a real iPhone while the app is closed, and in-process alerts across real Mac sleep and wake;
- a tap on a widget on a Mac desktop;
- native-speaker review of the translations;
- outside review of the API RFCs;
- an app maintained independently of this organization.

Each release's notes list what that release leaves pending: [SalahTimes](https://github.com/salah-kit/SalahTimes/releases), [SalahKit](https://github.com/salah-kit/SalahKit/releases), [Salah](https://github.com/salah-kit/Salah/releases).

The [1.0 conditions](https://github.com/salah-kit/.github/blob/main/STANDARD.md#releases) are in the standard.

## Roadmap

- Calculation engines for the web (TypeScript) and Android (Kotlin), each in its own repository. Each must pass the same [JSON vectors](https://github.com/salah-kit/SalahTimes/blob/main/Vectors/README.md) as SalahTimes before its first release.
- 1.0 of the packages, once the conditions above hold.

## Contributing

- **Report a problem** with the issue forms in the repository it concerns: bugs, calculation-method corrections, timetables that disagree with the computed times, and translations.
- **Propose an API change** with an RFC. Each package keeps its RFCs in `docs/rfcs/` and discusses them in GitHub Discussions.
- **Send code** after reading the repository's own `CONTRIBUTING.md`. Every repository follows the [ecosystem standard](https://github.com/salah-kit/.github/blob/main/STANDARD.md).

Questions go to [SalahTimes](https://github.com/salah-kit/SalahTimes/discussions) or [SalahKit](https://github.com/salah-kit/SalahKit/discussions) Discussions. Everyone here follows the [code of conduct](https://github.com/salah-kit/.github/blob/main/CODE_OF_CONDUCT.md). Report vulnerabilities privately, as the [security policy](https://github.com/salah-kit/.github/blob/main/SECURITY.md) describes.
