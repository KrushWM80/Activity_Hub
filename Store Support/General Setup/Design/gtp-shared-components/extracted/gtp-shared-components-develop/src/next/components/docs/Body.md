### Body

```js
import {Body} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;

const BodyVariant = ({
  weight,
  size,
  isMonospace,
}) => {
  let children = 'Body';
  if (weight) {
    children = `${children} weight="${weight}"`;
  }
  if (size) {
    children = `${children} size="${size}"`;
  }
  if (isMonospace) {
    children = `${children} isMonospace`;
  }
  if (!size && !weight && !isMonospace) {
    children = `${children} (defaults)`;
  }
  return (
  <>
    <Body weight={weight} size={size} isMonospace={isMonospace}>
      {children}
    </Body>
  </>
  );
};

<View style={{width: 800}}>
  <BodyVariant />
  <Spacer />
  <BodyVariant size="small" weight="400" />
  <BodyVariant size="medium" weight="400" />
  <BodyVariant size="large" weight="400" />
  <Spacer />
  <BodyVariant size="small" weight="700" />
  <BodyVariant size="medium" weight="700" />
  <BodyVariant size="large" weight="700" />
  <Spacer />
  <BodyVariant size="small" weight="400" isMonospace />
  <BodyVariant size="medium" weight="400" isMonospace />
  <BodyVariant size="large" weight="400" isMonospace />
  <Spacer />
  <BodyVariant size="small" weight="700" isMonospace />
  <BodyVariant size="medium" weight="700" isMonospace />
  <BodyVariant size="large" weight="700" isMonospace />
</View>;
```
