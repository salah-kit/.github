# Adopt the packages

SalahTimes and SalahKit are available as tagged, pre-1.0 Swift packages. Start with a released version and keep your app's resolved dependency versions with any feedback. A minor release may change the API before 1.0.

## Choose an entry point

| Your app needs | Start here |
|---|---|
| Prayer-time calculations or Qibla without an app framework | [SalahTimes installation and quick start](https://github.com/salah-kit/SalahTimes#installation) |
| A typed schedule from calculated times | [SalahKit](https://github.com/salah-kit/SalahKit), with `SalahCore` and `SalahCalculation` |
| A mosque's published timetable and iqama | [MosqueBoard](https://github.com/salah-kit/SalahKit/tree/main/Examples/MosqueBoard), with `SalahCore`; a calculation engine is not required |
| Widgets or local prayer alerts | [SalahKit documentation](https://salah-kit.github.io/SalahKit/), with `SalahWidgets` or `SalahAlerts` |
| A new iPhone app with a widget and alerts | [SalahStarter](https://github.com/salah-kit/SalahStarter), using its template setup instructions |

The current package releases are [SalahTimes 0.1.0](https://github.com/salah-kit/SalahTimes/releases/tag/0.1.0) and [SalahKit 0.4.0](https://github.com/salah-kit/SalahKit/releases/tag/0.4.0). SalahKit depends on the released SalahTimes package. Use only the products your app needs.

## Verify your integration

1. Follow the chosen repository's README using your own project. For SalahStarter, use your own bundle identifiers, App Group and signing team.
2. Verify your actual data source, time zone, calculation method or timetable provenance. Check missing prayers, day offsets, high latitudes and timetable expiry where they apply.
3. Exercise the boundaries your app uses: save and relaunch, Arabic and large text, VoiceOver, a real widget update, or an alert while the app is closed. WidgetKit controls reload timing; notification confirmation is not proof that a banner was presented.
4. Read the chosen release's **Pending** and **Known limitations** sections. Simulator and process tests do not establish every physical-device or long-duration behavior.

## Share actionable feedback

Use the affected repository's issue forms for defects and its Discussions for integration questions:

- [SalahTimes issues](https://github.com/salah-kit/SalahTimes/issues/new/choose) and [Discussions](https://github.com/salah-kit/SalahTimes/discussions).
- [SalahKit issues](https://github.com/salah-kit/SalahKit/issues/new/choose) and [Discussions](https://github.com/salah-kit/SalahKit/discussions).
- [SalahStarter issues](https://github.com/salah-kit/SalahStarter/issues/new/choose) for template setup problems.

Include the package tag and resolved versions, platform and OS, the data source, the smallest reproduction, expected and actual behavior, and relevant logs or screenshots. Remove credentials and private location or account details before posting. For a calculation mismatch, include the method, date, time zone and authoritative timetable/source, distinguishing published precautionary minutes from calculation errors.

For API feedback, review the [SalahKit RFCs and their amendments](https://github.com/salah-kit/SalahKit/tree/main/docs/rfcs): schedules and sources, calculation, alerts, and widgets/UI. Describe what your app cannot express, any workaround, and whether another consumer has the same need.

## What independent adoption establishes

An integration by a maintainer outside this organization provides evidence that the examples cannot. Report confusing setup steps as well as defects, and distinguish a successful experiment from a shipped app.

Package 1.0 requires two shipped apps that differ in platform and data source to use tagged releases for a release cycle, with at least one independently maintained. Their findings, native vocabulary review, example builds and required device evidence must be resolved under the [release standard](https://github.com/salah-kit/.github/blob/main/STANDARD.md#releases). The current 0.x releases do not claim that milestone.

Salah's bundled recordings are confined to the separate macOS app. The packages contain no adhan audio. A package integration should choose media with its own documented redistribution terms; Salah's source release is not a notarized app download.
