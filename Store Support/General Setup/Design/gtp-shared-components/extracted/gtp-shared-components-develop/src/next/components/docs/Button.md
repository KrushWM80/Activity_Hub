### Button variant="primary"

```js
import {Button} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 4}} />;

<>
  <Button variant="primary" size="small" onPress={console.log}>
    Primary Button Small
  </Button>
  <Spacer />
  <Button variant="primary" size="medium" onPress={console.log}>
    Primary Button Medium
  </Button>
  <Spacer />
  <Button variant="primary" size="large" onPress={console.log}>
    Primary Button Large
  </Button>
</>;
```

### Button variant="secondary"

```js
import {Button} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 4}} />;

<>
  <Button variant="secondary" size="small" onPress={console.log}>
    Secondary Button Small
  </Button>
  <Spacer />
  <Button variant="secondary" size="medium" onPress={console.log}>
    Secondary Button Medium
  </Button>
  <Spacer />
  <Button variant="secondary" size="large" onPress={console.log}>
    Secondary Button Large
  </Button>
</>;
```

### Button variant="tertiary"

```js
import {Button} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 4}} />;

<>
  <Button variant="tertiary" size="small" onPress={console.log}>
    Tertiary Button Small
  </Button>
  <Spacer />
  <Button variant="tertiary" size="medium" onPress={console.log}>
    Tertiary Button Medium
  </Button>
  <Spacer />
  <Button variant="tertiary" size="large" onPress={console.log}>
    Tertiary Button Large
  </Button>
</>;
```

### Button variant="destructive"

```js
import {Button} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 4}} />;

<>
  <Button variant="destructive" size="small" onPress={console.log}>
    Destructive Button Small
  </Button>
  <Spacer />
  <Button variant="destructive" size="medium" onPress={console.log}>
    Destructive Button Medium
  </Button>
  <Spacer />
  <Button variant="destructive" size="large" onPress={console.log}>
    Destructive Button Large
  </Button>
</>;
```

Use the `leading` property to add an element (typically an icon) to the left of the text.
Use the `trailing` property to add an element (typically an icon) to the right of the text.

```js
import {Icons} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 4}} />;

<>
  <Button
    variant="primary"
    leading={<Icons.PlusIcon size={24} />}
    onPress={console.log}>
    Primary Button with left icon
  </Button>
  <Spacer />
  <Button
    variant="primary"
    trailing={<Icons.PlusIcon size={24} />}
    onPress={console.log}>
    Primary Button with right icon
  </Button>
</>;
```
