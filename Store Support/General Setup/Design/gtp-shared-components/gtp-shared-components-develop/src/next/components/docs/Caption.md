### Caption

```js
import {Caption} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;

const CaptionVariant = ({weight}) => {
  let children = 'Caption';
  if (weight) {
    children = `${children} weight="${weight}"`;
  } else {
    children = `${children} (defaults)`;
  }
  return (
    <>
      <Caption weight={weight}>{children}</Caption>
    </>
  );
};

<>
  <CaptionVariant />
  <Spacer />
  <CaptionVariant weight="400" />
  <CaptionVariant weight="700" />
</>;
```
