### Checkboxes
```js
import {Checkbox} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 4}} />;

<>
  <Checkbox label="Unchecked" />
  <Checkbox label="Checked" checked />
  <Checkbox label="Indeterminate" indeterminate />
  <Checkbox label="Unchecked (disabled)" disabled />
  <Checkbox label="Checked (disabled)" checked disabled />
  <Checkbox label="Indeterminate (disabled)" indeterminate disabled />
</>;
```

### No Label Checkboxes
```js
import {View} from 'react-native';
import {Checkbox} from '@walmart/gtp-shared-components';

<View style={{flexDirection: 'row'}}>
  <Checkbox />
  <Checkbox checked />
  <Checkbox indeterminate />
  <Checkbox disabled />
  <Checkbox checked disabled />
  <Checkbox indeterminate disabled />
</View>;
```

### Long Label Checkbox
```js
import {Checkbox} from '@walmart/gtp-shared-components';

<>
  <Checkbox label="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua" />
</>;
```

### Interactive (Stateful) Checkboxes
Checkbox, unlike the legacy CheckboxItem, no longer instrinsically provides state.
Instead, it must be handled by the application.
```js
import {Checkbox} from '@walmart/gtp-shared-components';

const App = () => {
  const checkList = ['Lions', 'Tigers', 'And Bears', 'Oh My!'];
  const [checked, setChecked] = React.useState([]);
  const [disabled, setDisabled] = React.useState(false);

  // Add/Remove checked item from list
  const handleCheck = (item) => {
    let updatedList = [...checked];
    if (checked.includes(item)) {
      updatedList = checked.filter(i => i !== item);
    } else {
      updatedList = [...checked, item];
    }
    setChecked(updatedList);
  };

  const renderList = checkList.map((item, index) => (
    <Checkbox
      key={index}
      label={item}
      checked={checked.includes(item)}
      disabled={disabled}
      onPress={() => handleCheck(item)}
    />
  ));

  return (
    <>
      {renderList}
      <Checkbox
        label="Disable All Above"
        checked={disabled}
        onPress={() => setDisabled(!disabled)}
      />
    </>
  );
};

<App />
```
