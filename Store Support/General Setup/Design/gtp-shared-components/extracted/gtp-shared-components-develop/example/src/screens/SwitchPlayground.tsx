import * as React from 'react';
import {StyleSheet, Text, View} from 'react-native';
import {
  Checkbox,
  colors,
  Switch,
  TextField,
  TextFieldRef,
} from '@walmart/gtp-shared-components';

import {Page} from '../components';

const Spacer = () => <View style={ss.spacer} />;

const SwitchPlayground: React.FC = () => {
  const tfRef = React.useRef<TextFieldRef | null>(null);
  type Traits = {
    isOn?: boolean;
    disabled?: boolean;
    value?: boolean;
  };

  const [value, setValue] = React.useState<string>('Switch me!');

  const [traits, setTraits] = React.useState<Traits>({
    isOn: false,
    disabled: false,
    value: false,
  });

  const handleOnPress = (): void => {
    setTraits({
      ...traits,
      isOn: !traits.isOn,
    });
  };

  React.useEffect(() => {
    if (tfRef.current) {
      tfRef.current.blur();
    }
  }, [traits]);

  return (
    <View style={ss.container}>
      <View style={ss.buttonContainer}>
        <Switch
          isOn={traits.isOn}
          disabled={traits.disabled}
          label={value}
          onValueChange={() => handleOnPress()}
        />
      </View>

      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>Switch traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Spacer />
          <Checkbox
            label="Is disabled"
            checked={!!traits.disabled}
            onPress={() =>
              setTraits({
                ...traits,
                disabled: !traits.disabled,
              })
            }
          />
          <Spacer />
          <Checkbox
            label="Is on"
            checked={!!traits.isOn}
            onPress={() =>
              setTraits({
                ...traits,
                isOn: !traits.isOn,
              })
            }
          />
          <Spacer />
          <TextField
            ref={tfRef}
            label="Enter a label for the switch"
            value={value}
            onChangeText={txt => setValue(txt)}
          />
        </View>
      </Page>
    </View>
  );
};

const ss = StyleSheet.create({
  container: {
    flex: 1,
  },
  section: {
    paddingVertical: 12,
    paddingHorizontal: 16,
  },
  buttonContainer: {
    height: 80,
    marginHorizontal: 16,
    borderRadius: 12,
    paddingVertical: 10,
    borderColor: colors.blue['90'],
    paddingHorizontal: 8,
    borderWidth: 0.5,
    alignItems: 'center',
    justifyContent: 'center',
  },
  spacer: {
    height: 8,
  },
  innerContainer: {
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.blue['90'],
    borderTopColor: colors.blue['90'],
    borderBottomColor: colors.blue['90'],
    borderLeftColor: colors.blue['90'],
    borderRightColor: colors.blue['90'],
    paddingHorizontal: 8,
    paddingBottom: 8,
    borderWidth: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderTopWidth: 1,
    borderLeftWidth: 1,
    borderRightWidth: 1,
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
    borderTopColor: colors.blue['90'],
    borderLeftColor: colors.blue['90'],
    borderRightColor: colors.blue['90'],
    paddingRight: 16,
    paddingVertical: 8,
    marginTop: 8,
  },
  headerText: {
    fontSize: 20,
    fontWeight: '500',
    color: colors.blue['90'],
    textAlign: 'left',
    paddingVertical: 4,
    marginLeft: 12,
  },
});

export {SwitchPlayground};
