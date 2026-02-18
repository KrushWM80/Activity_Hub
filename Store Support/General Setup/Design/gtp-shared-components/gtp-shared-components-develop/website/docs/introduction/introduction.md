---
slug: /
sidebar_position: 1
---

# Introduction

## LivingDesign React Native Components Library

This repository contains LivingDesign components for React Native apps.

## Installation

```bash
# First ensure that npm is pointing to Walmart's npm registry for your software
# by running the following command at the top-level directory of the repository.
echo 'registry=https://npme.walmart.com' >> .npmrc
```

Install the latest stable version (>= 2.0.0)
```bash npm2yarn
npm install @walmart/gtp-shared-components
```

Install peer dependencies
```bash npm2yarn
npm install @react-native-picker/picker @react-native-community/datetimepicker
npm install react-native-device-info react-native-drop-shadow
```

See the [Dependencies page](./README.dependencies.md) for more information on peer dependencies

If you want to install the latest **legacy** version (< 2.0.0)

(NOT RECOMMENDED: the legacy version is deprecated and will be removed in the near future)

```bash npm2yarn
npm install @walmart/gtp-shared-components@legacy
npm install @react-native-community/datetimepicker @react-native-picker/picker
```

## Usage

```js static noeditor
import * as React from 'react';
import {Button} from '@walmart/gtp-shared-components';

const Example = () => (
  <Button variant="primary" onPress={() => console.log('Submit pressed!')}>
    Submit
  </Button>
);

export {Example};
```

## Documentation

This is the documentaion for the latest version (releases **2.0** and up).

If you want to access the legacy version (releases **1.8.\***) documentation, go to [this link][2]

## Example app

The LivingDesign React Native library comes with an embedded `LDRNExample` app which is a kitchen sink
showcase app for demo-ing all components. You can build and run the app locally
in your environment by following the step-by-step instructions [found here](./Contributors/Example-app.md)

<center><strong>LDRNExample</strong> app home screen:</center>
<p></p>

<p align="center"><img src="https://gecgithub01.walmart.com/storage/user/67415/files/9de976b9-555d-4664-9c1f-8e3a3d8c82b4" alt="Example home screen"  height="520" /></p>

> ### Icons
>
> All icons used in the React Native library are pulled from the [gtp-shared-icons][1] package.
> This is transparent to you though, you import Icons just like any other component:
>
> ```js static noeditor
> import * as React from "react";
> import {Icons} from "@walmart/gtp-shared-components";
>
> <Icons.CloseIcon />
> <Icons.SparkIcon />
> ```
>
> ### Fonts
>
> The React Native library is using the same custom fonts (**Bogle**) used in the other implementations of Living Design.
> In the **next** (releases **2.0** and up) version of the library we provide a script that will install the Bogle fonts in
> the `Android` and `iOS` native scaffolds of your app. To invoke it, run this after installing the gtp-shared-components library:
>
> ```bash
> npx installFonts
> ```
>
> The scripts looks for **./react-native.config.js** file in the root of
> your project. If you don't have one, the script will create one with this
> code:
>
> ```js static noeditor
> module.exports = {
>   project: {
>     ios: {},
>     android: {},
>   },
>   assets: ['.node_modules/@walmart/gtp-shared-components/assets/fonts'],
> };
> ```
>
> The script will install the fonts found under
>
> **node_modules/@walmart/gtp-shared-components/assets/fonts**
>
> to:
>
> - Android
>   - android/app/src/main/assets/fonts
>   - android/link-assets-manifest.json
> - iOS
>   - ios/[project_name]/Info.plist
>   - ios/link-assets-manifest.json
>   - ios/[project_name].xcodeproj/project.pbxproj
>   - add group 'Resources' in the Xcode project

## Philosophy

The Living Design system reinforces Walmart’s principles by providing components
and foundational guidelines that align to the brand with the goal of harmonizing
design across the company’s many digital products. The Living Design team’s
designers, engineers, and partners create components that are accessible,
responsive, performant, and promote good end user experiences. Reducing
customization on these components accelerates product creation by decreasing the
number of decisions feature designers and developers need to make.

The React implementation embodies this philosophy by limiting overrides on
components. Components come with predefined anatomy and features; customizing a
component with one-off colors or different internal spacing is strongly
discouraged.

## CHANGELOG

Please refer to the [CHANGELOG page](./CHANGELOG.md) for details about every release.

## Contributing

- This project attempts to conform exactly to the `Living Design 3` specs
  from the LD team, and therefore should only include components which are available
  in the LD3 specs.
- Any new component, or new design for an existing component, must go through
  the LD team for review.
- See the [contributing guide][11] to learn how to contribute to the repository and the development workflow.

## Repositories

- [Components][6]
- [Icons][7]
- [Design tokens][8]

## Getting support

If you experience any issues while getting started with any of Living Design's tooling, please head over to the [LivingDesign Support page][9] for more guidelines and help.

For React Native onboarding assistance, feature requests, or bug reports, please reach out on the LD React Native support Slack channel: [#ld-support-reactnative][10]

[1]: https://gecgithub01.walmart.com/pages/electrode-mobile-platform/gtp-shared-icons/
[2]: https://gecgithub01.walmart.com/pages/electrode-mobile-platform/gtp-sc-legacy-docs/
[3]: https://gecgithub01.walmart.com/pages/electrode-mobile-platform/gtp-shared-components/
[6]: https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/
[7]: https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-icons/
[8]: https://gecgithub01.walmart.com/LivingDesign/tokens
[9]: https://livingdesign.walmart.com/getting-started/support/
[10]: https://walmart.slack.com/app_redirect?channel=ld-support-reactnative
