/* eslint-disable react-native/no-inline-styles */
import * as React from 'react';
import {StyleSheet, View} from 'react-native';

import {Checkbox, Switch, TextField} from '@walmart/gtp-shared-components';

const InteractiveSwitches = () => {
  const [disabled, setDisabled] = React.useState(false);
  const [isOn, setIsOn] = React.useState(false);
  const [value, setValue] = React.useState<string>('Switch me!');

  return (
    <View>
      <View style={styles.container}>
        <Switch
          isOn={isOn}
          disabled={disabled}
          label={value}
          onValueChange={() => {
            setIsOn(previousState => !previousState);
          }}
        />
      </View>
      <Checkbox
        label="Is disabled"
        checked={disabled}
        onPress={() => setDisabled(previousState => !previousState)}
        UNSAFE_style={{marginTop: 5}}
      />
      <Checkbox
        label="Is on"
        checked={isOn}
        onPress={() => setIsOn(previousState => !previousState)}
        UNSAFE_style={{marginTop: 5}}
      />
      <TextField
        label="Enter a label for the switch"
        value={value}
        onChangeText={txt => setValue(txt)}
        UNSAFE_style={{marginTop: 5}}
      />
    </View>
  );
};

export {InteractiveSwitches};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    paddingVertical: 10,
    backgroundColor: 'white',
    borderRadius: 5,
    marginBottom: 10,
  },
});
