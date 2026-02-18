All icons in this repository are pulled from [gtp-shared-icons](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-icons).

## [Browse available icons](https://gecgithub01.walmart.com/pages/electrode-mobile-platform/gtp-shared-icons/)

![Screen Shot 2022-06-29 at 2 24 00 PM](https://gecgithub01.walmart.com/storage/user/67415/files/8a17e789-6d6d-4e38-9e47-feb7c77056c1)

## Usage

```js static noeditor
import * as React from 'react';
import {Icons} from '@walmart/gtp-shared-components';

const Example = () => (
  <>
    <Icons.ArrowDownIcon color="black" size="16" />
    <Icons.CameraIcon color="white" size="24" />
    <Icons.CartFill color="blue" size="32" />
  </>
);

export {Example};
```

## Coloring Icons

All icons have a `color` prop, which will change the color of the icon.

```js
import {colors, Icons} from '@walmart/gtp-shared-components';

<IconWrapper caption={false}>
  <Icons.SparkIcon size={32} color={colors.spark['100']} />
  <Icons.TwitterIcon size={32} color={colors.blue['100']} />
  <Icons.CheckCircleFillIcon size={32} color={colors.green['100']} />
  <Icons.HeartFillIcon size={32} color={colors.red['100']} />
</IconWrapper>;
```

## Sizing Icons

All icons have a `size` prop, which will change the size of the icon.

```js
import {Icons} from '@walmart/gtp-shared-icons';

<IconWrapper caption>
  <Icons.SparkIcon size={16} />
  <Icons.SparkIcon size={24} />
  <Icons.SparkIcon size={32} />
</IconWrapper>;
```

## All Icons

Deprecated icons are marked with

```js noeditor
import {DeprecatedBadge} from '../example/src/components/DeprecatedBadge.tsx';
<View style={{width: 200, height: 40, marginTop: -44, marginLeft: 100}}>
  <DeprecatedBadge />
</View>;
```

```js noeditor
import {IconGrid} from './IconGrid';

<IconGrid />;
```
