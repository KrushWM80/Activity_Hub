import * as React from 'react';
import {StyleSheet, Text, View} from 'react-native';

import {
  Checkbox,
  colors,
  TextField,
  TextFieldRef,
} from '@walmart/gtp-shared-components';

import {Page} from '../components';

const Spacer = () => <View style={ss.spacer} />;

const CheckboxPlayground: React.FC = () => {
  type Traits = {
    checked?: boolean;
    disabled?: boolean;
    indeterminate?: boolean;
    label?: string;
  };

  const tfRef = React.useRef<TextFieldRef | null>(null);

  const [tfText, setTfText] = React.useState('label text');
  const [traits, setTraits] = React.useState<Traits>({
    checked: true,
    disabled: false,
    indeterminate: false,
    label: tfText,
  });

  const handleOnPress = (): void => {
    /**
     * On click of handleOnPress, it will update 'indeterminate' to false
     * but for 'checked' it will update it's value to true/false based on the current value,
     * as the user will check and uncheck the checkbox.
     */
    setTraits({
      ...traits,
      checked: !traits.checked,
      indeterminate: false,
    });
  };

  return (
    <View style={ss.container}>
      <View style={ss.buttonContainer}>
        <Checkbox
          checked={traits.checked}
          disabled={traits.disabled}
          label={traits.label}
          indeterminate={traits.indeterminate}
          onPress={() => handleOnPress()}
        />
      </View>
      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>Checkbox traits</Text>
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
            label="indeterminate"
            checked={!!traits.indeterminate}
            onPress={() =>
              setTraits({
                ...traits,
                indeterminate: !traits.indeterminate,
              })
            }
          />
          <Spacer />
          <Checkbox
            label="label"
            checked={!!traits.label}
            disabled={false}
            onPress={() =>
              setTraits({
                ...traits,
                label: traits.label ? '' : 'label text',
              })
            }
          />
          <Spacer />
          <TextField
            ref={tfRef}
            label="Custom label"
            size="small"
            value={traits.label}
            onChangeText={_text => {
              setTraits({
                ...traits,
                label: _text as string,
              });
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
  headerVariantText: {
    color: colors.blue['90'],
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
  radioHeaderText: {
    lineHeight: 28,
    fontSize: 20,
    color: colors.blue['90'],
  },
});

export {CheckboxPlayground};
