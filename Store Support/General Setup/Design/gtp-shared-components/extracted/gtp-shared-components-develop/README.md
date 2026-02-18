# LivingDesign React Native Components Library

[![Built with Looper][1]][2]
[![Build Status][3]][4]
[![Quality Gate Status][13]][14]
[![Code Coverage][15]][14]

This repository contains [Living Design][6] themed components for React Native apps at Walmart.

## Installation

```shell static
# First ensure that npm is pointing to Walmart's npm registry for your software
# by running the following command at the top-level directory of the repository.
echo 'registry=https://npme.walmart.com' >> .npmrc

# If you want to install the latest stable version (>= 2.0.0)
yarn add @walmart/gtp-shared-components

# Install peer dependencies
yarn add @react-native-picker/picker @react-native-community/datetimepicker react-native-device-info react-native-drop-shadow
```

See the [README.dependencies.md document][16] for more information on peer dependencies

If you want to install the latest **legacy** version (1.8.\*)

(NOT RECOMMENDED: the legacy version is deprecated and will be removed in the near future)

```shell static
yarn add @walmart/gtp-shared-components@legacy
yarn add @react-native-community/datetimepicker @react-native-picker/picker
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

For the current stable version (releases **2.0.0** and up), docs can be [found here][5]

For the legacy version (releases **1.8.** and below) the docs can be [found here][8]

## Example app

The LivingDesign React Native library comes with an embedded `example` app which is a kitchen-sink
showcase app for demo-ing all components. You can build and run the app locally
in your environment by following the step-by-step instructions [found here][9]

<center><strong>example</strong> app home screen:</center>
<p></p>

<p align="center"><img src="https://gecgithub01.walmart.com/storage/user/67415/files/98bb8e25-ec4a-43d9-9477-898883a38d01" alt="Example home screen"  height="520"></p>

---

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
> ```shell static noeditor
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
>   - ios/<project_name>/Info.plist
>   - ios/link-assets-manifest.json
>   - ios/<project_name>.xcodeproj/project.pbxproj
>   - add group 'Resources' in the Xcode project

## Issues

- Reported on version 1.6.0 onwards
  - [livingdesign tokens are not being transformed by Jest][7]
- there is [a known issue][10] in react-native versions `< 0.66.5` which makes the Android build of a consumer app fail.
  - please make sure you use `react-native@0.66.5 or above` to avoid this issue.

## Contributing

- This project attempts to conform exactly to the `Living Design 3` specs
  from the LD team, and therefore should only include components which are available
  in the LD3 specs.
- Any new component, or new design for an existing component, must go through
  the LD team for review.
- See the [contributing guide][17] to learn how to contribute to the repository and the development workflow.

## For LD React Native developers

### Setup

- For info on how to set up your local development environment
  go to [this page](./README.setup.md)

### Publishing

- For info on how to publish a new version of the library
  go to [this page](./README.publishing.md)

### Migration automation

This project provides automation scripts to assist you with the migration from `legacy` to `next` using `jscodeshift` from Facebook. For more details please see:

- [Description of codemods in the CHANGELOG][11]
- [DX blog on codemods][12]

[1]: https://img.shields.io/badge/Built%20With-Looper-blue.svg
[2]: http://looper.walmart.com/
[3]: https://ci.falcon.walmart.com/buildStatus/icon?job=electrode-mobile-platform/gtp-shared-components/main
[4]: https://ci.falcon.walmart.com/job/electrode-mobile-platform/job/gtp-shared-components/
[5]: https://gecgithub01.walmart.com/pages/electrode-mobile-platform/gtp-shared-components/
[6]: http://livingdesign.walmart.com/
[7]: https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/issues/114
[8]: https://gecgithub01.walmart.com/pages/electrode-mobile-platform/gtp-sc-legacy-docs/
[9]: https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/blob/main/example/README.md
[10]: https://github.com/facebook/react-native/issues/35210
[11]: https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/blob/main/CHANGELOG.md#migration-using-codemods
[12]: https://dx.walmart.com/blogs2/view/#CODEMODS-USING-JSCODESHIFT-4325
[13]: https://sonar.looper.prod.walmartlabs.com/api/project_badges/measure?project=com.walmart.gtp-shared-components&metric=alert_status
[14]: https://sonar.prod.walmart.com/dashboard?id=com.walmart.gtp-shared-components
[15]: https://sonar.looper.prod.walmartlabs.com/api/project_badges/measure?project=com.walmart.gtp-shared-components&metric=coverage
[16]: https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/blob/main/README.dependencies.md
[17]: https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/blob/main/README.contributing.md
