### Radio buttons w/ labels

```js
import {Radio} from '@walmart/gtp-shared-components';

<>
  <Radio label="Unselected" />
  <Radio label="Selected" checked />
  <Radio label="Unselected (disabled)" disabled />
  <Radio label="Selected (disabled)" checked disabled />
</>
```

### No label Radio buttons
```js
import {View} from 'react-native';
import {Radio} from '@walmart/gtp-shared-components';

<View style={{flexDirection: 'row'}}>
  <Radio />
  <Radio checked />
  <Radio disabled />
  <Radio checked disabled />
</View>;
```

### Long label Radio
```js
import {Radio} from '@walmart/gtp-shared-components';

<>
  <Radio label="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua" />
</>;
```

### Interactive (Stateful) Example
Radio, unlike the legacy RadioItem, no longer instrinsically provides state.
Instead, it must be handled by the application.
```js
import * as React from 'react';
import {Checkbox, Radio} from '@walmart/gtp-shared-components';

const App = () => {
  const list = ['Lions', 'Tigers', 'And Bears', 'Oh My!'];
  const [selected, setSelected] = React.useState('');
  const [disabled, setDisabled] = React.useState(false);

  const renderList = list.map((item, index) => (
    <Radio
      key={index}
      label={item}
      checked={item === selected}
      disabled={disabled}
      onPress={() => setSelected(item)}/>
  ));

  return (
    <>
      {renderList}
      <Checkbox
        label="Disable All Above"
        checked={disabled}
        onPress={() => setDisabled(!disabled)}
        UNSAFE_style={{ paddingTop: 5 }}
      />
    </>
  );
};

<App />
```
