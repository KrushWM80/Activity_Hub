Links can be inserted within a line of text, used on their own, or at the end of content.

```js
import {Link} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 4}} />;

<>
  <Link onPress={console.log}>This is a Link</Link>
  <Spacer />
  <Link disabled onPress={console.log}>
    This is a disabled Link
  </Link>
</>;
```

### Link white variant

```js {"props": { "className": "dark" } }
import {Link} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 4}} />;

<>
  <Link color="white" onPress={console.log}>
    This is a white Link
  </Link>
  <Spacer />
  <Link color="white" disabled onPress={console.log}>
    This is a disabled white Link
  </Link>
</>;
```

### Embedded Link

```js
import {Text} from 'react-native';
import {Link} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 4}} />;

<>
  <Text>
    {'This '}
    <Link children="link" onPress={console.log} />
    {' is embedded'}
  </Text>
  <Spacer />
</>;
```
