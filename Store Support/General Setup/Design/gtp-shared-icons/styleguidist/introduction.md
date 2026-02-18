## LivingDesign React Native Icons Library

This repository contains shared icons that can be used in react-native applications.
These icons are aligned with the [LivingDesign specs](https://gecgithub01.walmart.com/LivingDesign/livingdesign.walmart.com)

### Use

#### Install `gtp-shared-icons` in your project:

```shell static
# yarn
yarn add @walmart/gtp-shared-icons
```

#### Import and use the components:

```js static noeditor
import * as React from 'react';
import {Icons} from '@walmart/gtp-shared-icons';

const Example = () => (
  <View>
    <Icons.CloseIcon color="white" size={24} />
  </View>
);

export {Example};
```

> **NOTE**: if you use the `LivingDesign React Native Library` in your project, Icons come embedded, so you don't have to import them directly.

> ```js static noeditor
> import * as React from "react";
> import {Icons} from "@walmart/gtp-shared-components";
>
> <Icons.CloseIcon />
> <Icons.SparkIcon />
> ```

### Sizing

You can specify the size of the icon using the `size` prop. Any of the following constructs will work:

```js static noeditor
  <Icons.ArrowDownIcon size={16} />
  <Icons.CameraIcon size={24} />
  <Icons.CartFill size={32} />

  <Icons.ArrowDownIcon size="small" />
  <Icons.CameraIcon size="medium" />
  <Icons.CartFill size="large" />
```

### Single source of truth

All icons in this repository are pulled from the [LivingDesign 3 repository](https://gecgithub01.walmart.com/walmart-web/walmart/tree/main/libs/livingdesign/icons).
(SVG format). The `SVG` files are converted to `PNG`s of appropriate size for component ingestion, and React Native components are generated using the `PNG`'s as image source.
