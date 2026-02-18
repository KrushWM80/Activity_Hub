### Display

```js
import {Display} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;

const DisplayVariant = ({
  weight,
  size,
}) => {
  let children = 'Display';
  if (weight) {
    children = `${children} weight="${weight}"`;
  }
  if (size) {
    children = `${children} size="${size}"`;
  }
  if (!size && !weight) {
    children = `${children} (defaults)`;
  }
  return (
    <>
      <Display weight={weight} size={size}>
        {children}
      </Display>
    </>
  );
};

<View style={{width: 800}}>
  <DisplayVariant />
  <Spacer />
  <DisplayVariant size="small" weight="400" />
  <DisplayVariant size="large" weight="400" />
  <Spacer />
  <DisplayVariant size="small" weight="700" />
  <DisplayVariant size="large" weight="700" />
</View>;
```
