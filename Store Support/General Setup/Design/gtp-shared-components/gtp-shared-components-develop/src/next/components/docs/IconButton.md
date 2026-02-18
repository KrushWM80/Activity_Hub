### Icon Button

```js
import {Icons} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 4}} />;

<>
  <IconButton
    size="small"
    children={<Icons.HomeIcon />}
    onPress={console.log}
  />
  <Spacer />
  <IconButton
    size="medium"
    children={<Icons.HomeIcon />}
    onPress={console.log}
  />
  <Spacer />
  <IconButton
    size="large"
    children={<Icons.HomeIcon />}
    onPress={console.log}
  />
  <Spacer />
  <Spacer />
  <IconButton
    size="large"
    children={<Icons.HomeIcon />}
    onPress={console.log}
    UNSAFE_style={{
      backgroundColor: 'yellow',
      height: 42,
      width: 42,
      borderRadius: 21,
    }}
  />
  <Spacer />
</>;
```
