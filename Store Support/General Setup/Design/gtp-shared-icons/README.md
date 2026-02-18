# gtp-shared-icons

[![Built with Looper][1]][2]
[![Build Status][3]][4]

Shared icons for [Living Design][6] themed
React Native apps at Walmart.

Conforms to `LivingDesign Icons` version: 1.4.3

## Getting Started

```sh
yarn add @walmart/gtp-shared-icons
```

## Usage

```js
import * as React from 'react';
import {Icons} from '@walmart/gtp-shared-Icons';

const Example = () => (
  <>
    <Icons.ArrowDownIcon size={16} />
    <Icons.CameraIcon size={24} />
    <Icons.CartFill size={32} />

    <Icons.ArrowDownIcon size="small" />
    <Icons.CameraIcon size="medium" />
    <Icons.CartFill size="large" />
  </>
);

export {Example};
```

## [Browse available icons][5]

![Screen Shot 2022-06-29 at 2 24 00 PM](https://gecgithub01.walmart.com/storage/user/67415/files/8a17e789-6d6d-4e38-9e47-feb7c77056c1)

## Example app

- You can find and example app in the `example/` folder which is a showcase
  of all icons exposed by the library.
  Please refer to [example/README.md](./example/README.md) for instructions
  on how to run the `example` app

## Contributing

- This project attempts to conform exactly to the Living Design 3 stickersheet
  from UX, and therefore should only include icons which are available
  in said stickersheet.
- Any new icons, or new design for an existing icon, must go through
  the vetting process by the global UX council.
- Start by filing an LD issue [here](https://jira.walmart.com/servicedesk/customer/portal/7425)

## For LD React Native developers

### Setup

- For info on how to set up your local development environment
  go to [this page](./README.setup.md)

### Publishing

- For info on how to publish a new version of the library
  go to [this page](./README.publishing.md)

[1]: https://img.shields.io/badge/Built%20With-Looper-blue.svg
[2]: http://looper.walmart.com/
[3]: https://ci.mobile.walmart.com/buildStatus/icon?job=electrode-mobile-platform/gtp-shared-icons/main
[4]: https://ci.mobile.walmart.com/job/electrode-mobile-platform/job/gtp-shared-icons/
[5]: https://gecgithub01.walmart.com/pages/electrode-mobile-platform/gtp-shared-icons/
[6]: http://livingdesign.walmart.com/
