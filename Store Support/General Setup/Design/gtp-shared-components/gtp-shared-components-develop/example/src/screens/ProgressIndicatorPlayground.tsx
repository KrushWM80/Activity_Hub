import * as React from 'react';
import {StyleSheet, Text, View, TextStyle} from 'react-native';

import {
  Checkbox,
  colors,
  ProgressIndicator,
  ProgressIndicatorVariant,
  TextField,
  TextFieldRef,
  getFont,
} from '@walmart/gtp-shared-components';

import {Page} from '../components';

const Spacer = () => <View style={ss.spacer} />;

const ProgressIndicatorPlayground: React.FC = () => {
  const variantsArr = ['error', 'info', 'success', 'warning'];
  const tfRef = React.useRef<TextFieldRef | null>(null);
  type Traits = {
    value: number;
    max: number;
    min: number;
    valueLabel: string;
    variant: ProgressIndicatorVariant;
    label?: string;
  };

  const [traits, setTraits] = React.useState<Traits>({
    value: 0,
    max: 100,
    min: 0,
    valueLabel: '0',
    variant: 'info',
    label: 'Account setup is in progress',
  });

  React.useEffect(() => {
    if (tfRef.current) {
      tfRef.current.blur();
    }
  }, [traits]);

  return (
    <View style={ss.container}>
      <View style={ss.buttonContainer}>
        <ProgressIndicator
          label={traits.label}
          value={traits.value}
          valueLabel={traits.valueLabel}
          variant={traits.variant}
          max={traits.max}
          min={traits.min}
        />
      </View>
      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>ProgressIndicator traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Spacer />
          <Text style={ss.radioHeaderText}>variant</Text>
          {variantsArr.map((v, i) => (
            <Checkbox
              key={String(i)}
              label={v}
              checked={traits.variant === v}
              onPress={() =>
                setTraits({
                  ...traits,
                  variant: v as ProgressIndicatorVariant,
                })
              }
            />
          ))}
          <Spacer />
          <TextField
            label="label"
            size="small"
            value={traits.label}
            onChangeText={_text => {
              setTraits({
                ...traits,
                label: _text as string,
              });
            }}
          />

          <Spacer />
          <TextField
            label="valueLabel"
            size="small"
            value={traits.valueLabel}
            onChangeText={_text => {
              setTraits({
                ...traits,
                valueLabel: _text as string,
              });
            }}
          />

          <Spacer />
          <TextField
            label="value"
            keyboardType="numeric"
            helperText="Please enter numbers only"
            size="small"
            value={String(traits.value)}
            onChangeText={_text => {
              setTraits({
                ...traits,
                value: Number(_text),
                valueLabel: _text as string,
              });
            }}
          />

          <Spacer />
          <TextField
            label="max"
            size="small"
            keyboardType="numeric"
            helperText="Please enter numbers only"
            value={String(traits.max)}
            onChangeText={_text => {
              setTraits({
                ...traits,
                max: Number(_text),
              });
            }}
          />

          <Spacer />
          <TextField
            label="min"
            size="small"
            helperText="Please enter numbers only"
            keyboardType="numeric"
            value={String(traits.min)}
            onChangeText={_text => {
              setTraits({
                ...traits,
                min: Number(_text),
              });
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
    minHeight: 80,
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
  radioHeaderText: {
    ...getFont('500'),
    lineHeight: 28,
    fontSize: 20,
    color: colors.blue['90'],
  } as TextStyle,
});

export {ProgressIndicatorPlayground};
