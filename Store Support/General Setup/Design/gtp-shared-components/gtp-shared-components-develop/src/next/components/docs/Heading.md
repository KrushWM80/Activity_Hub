### Heading

```js
import {Heading} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;

const HeadingVariant = ({
  weight,
  size,
}) => {
  let children = 'Heading';
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
      <Heading weight={weight} size={size}>
        {children}
      </Heading>
    </>
  );
};

<View style={{width: 800}}>
  <HeadingVariant />
  <Spacer />
  <HeadingVariant size="small" weight="400" />
  <HeadingVariant size="medium" weight="400" />
  <HeadingVariant size="large" weight="400" />
  <Spacer />
  <HeadingVariant size="small" weight="700" />
  <HeadingVariant size="medium" weight="700" />
  <HeadingVariant size="large" weight="700" />
</View>;
```
