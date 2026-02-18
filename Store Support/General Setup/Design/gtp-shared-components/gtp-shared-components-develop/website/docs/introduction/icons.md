---
sidebar_position: 4
---

import IconsList from '@site/src/components/IconsList.tsx';


# Icons

All icons in this repository are pulled from [gtp-shared-icons](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-icons). [docs](https://gecgithub01.walmart.com/pages/electrode-mobile-platform/gtp-shared-icons/)

## Icons List

<details>
<summary>See the list of available icons</summary>
 <IconsList />
</details>


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

```js static noeditor
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

```js static noeditor
import {Icons} from '@walmart/gtp-shared-icons';

<IconWrapper caption>
  <Icons.SparkIcon size={16} />
  <Icons.SparkIcon size={24} />
  <Icons.SparkIcon size={32} />
</IconWrapper>;
```