All icons in this repository are pulled from the [Living Design 3 repository](https://gecgithub01.walmart.com/livingdesign/icons), which are then automatically converted from `SVG` to `PNG`s of appropriate size for component ingestion. To request a new icon be added, or to make adjustments to existing icons, please read through their [Contributing](https://gecgithub01.walmart.com/walmart-web/walmart/tree/main/libs/livingdesign/icons#contributing) section.

## Coloring Icons

All icons have a `color` prop, which will change the color of the icon.

```js noeditor
import {colors, Icons} from '@walmart/gtp-shared-icons';

<IconWrapper caption={false}>
  <Icons.SparkIcon size={32} color={colors.spark['100']} />
  <Icons.TwitterIcon size={32} color={colors.blue['100']} />
  <Icons.CheckCircleFillIcon size={32} color={colors.green['100']} />
  <Icons.HeartFillIcon size={32} color={colors.red['100']} />
</IconWrapper>;
```

```js static
import {colors, Icons} from '@walmart/gtp-shared-icons';

<Icons.SparkIcon size={32} color={colors.spark['100']} />;
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
import IconGrid from './icon-grid';

<IconGrid />;
```
