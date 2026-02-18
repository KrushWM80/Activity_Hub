```js
import {Switch} from '@walmart/gtp-shared-components';
<>
  <Switch label="Off" />
  <Switch label="On" isOn />
  <Switch label="Off (disabled)" disabled />
  <Switch label="On (dlsabled)" isOn disabled />
</>
```
### Interactive Switch Example

```js
import {StyleSheet} from 'react-native';
import {Checkbox, Switch, TextField} from '@walmart/gtp-shared-components';

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    paddingVertical: 10,
    backgroundColor: 'white',
    borderRadius: 5,
    marginBottom: 10,
  },
  spacing: {
    marginTop: 5
  },
});

const App = () => {
  const [disabled, setDisabled] = React.useState(false);
  const [isOn, setIsOn] = React.useState(false);
  const [label, setLabel] = React.useState('Switch me!');

  return (
    <View>
      <View style={styles.container}>
        <Switch isOn={isOn} disabled={disabled} label={label} onValueChange={() => setIsOn(previousState => !previousState)} />
      </View>
      <Checkbox
        label="Is disabled"
        checked={disabled}
        onPress={() => setDisabled(previousState => !previousState)}
        UNSAFE_style={styles.spacing}
      />
      <Checkbox
        label="Is on"
        checked={isOn}
        onPress={() => setIsOn(previousState => !previousState)}
        UNSAFE_style={styles.spacing}
      />
      <TextField
        label="Enter a label for the switch"
        value={label}
        onChangeText={txt => setLabel(txt)}
        style={styles.spacing}
      />
    </View>
  );
};

<App />
```

### List with Switches

```js
import {List, ListItem, Switch} from '@walmart/gtp-shared-components';

<List>
  <ListItem
    title="Order Updates" trailing={<Switch isOn />}
    UNSAFE_style={{ backgroundColor: 'transparent'}}>
    Get an alert for your pickup and delivery orders
  </ListItem>
  <ListItem
    title="Accounts & Receipts" trailing={<Switch />}
    UNSAFE_style={{ backgroundColor: 'transparent'}}>
    Get updates on your account, view store receipts, track gift cards and more
  </ListItem>
  <ListItem
    title="Events & Specials" trailing={<Switch />}
    UNSAFE_style={{ backgroundColor: 'transparent'}}>
    Mobile promotions and more
  </ListItem>
</List>
```
