import * as React from 'react';
import {StyleSheet, Text, View, TextStyle} from 'react-native';
import {
  colors,
  getFont,
  BadgeColor,
  Badge,
  Radio,
  TextField,
  TextFieldRef,
} from '@walmart/gtp-shared-components';

import {Page} from '../components';

const Spacer = () => <View style={ss.spacer} />;

const radioColor = ['gray', 'blue', 'green', 'purple', 'red', 'spark', 'white'];

const BadgePlayground: React.FC = () => {
  const tfRef = React.useRef<TextFieldRef | null>(null);
  type Traits = {
    badgeColor?: BadgeColor;
    label: string;
  };

  const [tfText, setTfText] = React.useState('1');
  const [traits, setTraits] = React.useState<Traits>({
    badgeColor: 'white',
    label: tfText,
  });

  const colorHandler = (sel: BadgeColor): void => {
    setTraits({
      ...traits,
      badgeColor: sel,
    });
  };

  return (
    <View style={ss.container}>
      <View style={ss.buttonContainer}>
        <Badge color={traits.badgeColor}>{traits.label}</Badge>
      </View>

      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>Switch traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Spacer />
          <Text style={ss.radioHeaderText}>color</Text>
          {radioColor.map((v, i) => (
            <Radio
              key={i}
              label={v}
              checked={v === traits.badgeColor}
              onPress={() => colorHandler(v as BadgeColor)}
            />
          ))}

          <Spacer />
          <Text style={ss.radioHeaderText}>children</Text>

          <TextField
            ref={tfRef}
            label="label text"
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

          <Spacer />
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
  radioHeaderText: {
    ...getFont('500'),
    lineHeight: 28,
    fontSize: 20,
    color: colors.blue['90'],
  } as TextStyle,
});

export {BadgePlayground};
