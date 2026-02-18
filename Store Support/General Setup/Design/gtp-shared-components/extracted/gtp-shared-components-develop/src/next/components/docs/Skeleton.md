```js { "props": { "className": "light" } }
import {Skeleton} from '@walmart/gtp-shared-components';

<Skeleton />;
```

Use the `variant` property to show a variant with fully rounded corners.

```js { "props": { "className": "light" } }
<Skeleton variant="rounded" />
```

Use and combine the `height` and `width` and `variant` properties to show desired shapes

```js { "props": { "className": "light" } }
<View style={{ flexDirection: 'row', justifyContent: 'space-around' }}>
  <Skeleton height={50} width={50} />
  <Skeleton height={50} width={50} variant="rounded" />
  <Skeleton height={50} width={100} />
  <Skeleton height={50} width={100} variant="rounded" />
</View>
```
