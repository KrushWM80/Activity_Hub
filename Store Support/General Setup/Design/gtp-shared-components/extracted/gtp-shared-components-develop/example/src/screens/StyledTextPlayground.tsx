import * as React from 'react';
import {StyleSheet, Text, View, TextStyle} from 'react-native';
import {
  Checkbox,
  colors,
  Icons,
  Radio,
  StyledText,
  StyledTextColor,
  getFont,
  StyledTextSize,
} from '@walmart/gtp-shared-components';

import {Page} from '../components';

const Spacer = () => <View style={ss.spacer} />;

const styledTextSize = ['small', 'medium'];
const styledTextColor = ['gray', 'blue', 'green'];

const StyledTextPlayground: React.FC = () => {
  type Traits = {
    color?: StyledTextColor;
    leading?: boolean;
    size?: StyledTextSize;
    isOn?: boolean;
    disabled?: boolean;
    value?: boolean;
  };

  const [traits, setTraits] = React.useState<Traits>({
    color: 'gray',
    leading: true,
    size: 'small',
    isOn: false,
    disabled: false,
    value: false,
  });

  const colorHandler = (sel: StyledTextColor): void => {
    setTraits({
      ...traits,
      color: sel,
    });
  };

  const sizeHandler = (v: StyledTextSize): void => {
    setTraits({
      ...traits,
      size: v,
    });
  };

  return (
    <View style={ss.container}>
      <View style={ss.buttonContainer}>
        <StyledText
          size={traits.size}
          color={traits.color}
          leading={traits.leading ? <Icons.CheckIcon /> : null}>
          Gray large StyledText with Check Icon
        </StyledText>
      </View>

      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>StyleText traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Spacer />
          <Text style={ss.radioHeaderText}>color</Text>
          {styledTextColor.map((v, i) => (
            <Radio
              UNSAFE_style={ss.rbGroup}
              key={i}
              label={v}
              checked={v == traits.color}
              onPress={() => colorHandler(v as StyledTextColor)}
            />
          ))}
          <Spacer />
          <Text style={ss.radioHeaderText}>size</Text>
          {styledTextSize.map((v, i) => (
            <Radio
              UNSAFE_style={ss.rbGroup}
              key={i}
              label={v}
              checked={v == traits.size}
              onPress={() => sizeHandler(v as StyledTextSize)}
            />
          ))}
          <Spacer />
          <Checkbox
            label="leading"
            checked={!!traits.leading}
            onPress={() =>
              setTraits({
                ...traits,
                leading: !traits.leading,
              })
            }
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
  rbGroup: {
    marginLeft: 16,
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

export {StyledTextPlayground};
