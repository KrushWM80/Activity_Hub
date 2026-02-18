import * as React from 'react';
import {StyleSheet, Text, View} from 'react-native';

import {
  Checkbox,
  colors,
  Radio,
  TextField,
  TextFieldRef,
} from '@walmart/gtp-shared-components';

import {Page} from '../components';

const Spacer = () => <View style={ss.spacer} />;

const RadioPlayground: React.FC = () => {
  const tfRef = React.useRef<TextFieldRef | null>(null);
  type Traits = {
    checked: boolean;
    disabled?: boolean;
    label?: boolean;
  };

  const [tfText, setTfText] = React.useState('Radio button');
  const [traits, setTraits] = React.useState<Traits>({
    checked: true,
    disabled: false,
    label: true,
  });

  React.useEffect(() => {
    if (tfRef.current) {
      tfRef.current.blur();
    }
  }, [traits]);

  return (
    <View style={ss.container}>
      <View style={ss.buttonContainer}>
        <Radio
          checked={!!traits.checked}
          disabled={!!traits.disabled}
          label={traits.label && tfText}
          onPress={() => {}}
        />
      </View>
      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>Radio traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Spacer />
          <Checkbox
            label="disabled"
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
            label="checked"
            checked={!!traits.checked}
            onPress={() =>
              setTraits({
                ...traits,
                checked: !traits.checked,
              })
            }
          />
          <Spacer />
          <Checkbox
            label="with label"
            checked={!!traits.label}
            onPress={() =>
              setTraits({
                ...traits,
                label: !traits.label,
              })
            }
          />
          <Spacer />
          <TextField
            disabled={!traits.label}
            ref={tfRef}
            label="Label text"
            size="small"
            value={tfText}
            onChangeText={_text => {
              setTfText(_text);
            }}
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
  spacer: {
    height: 8,
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

export {RadioPlayground};
