import * as React from 'react';
import {StyleSheet, Text, TextStyle, View} from 'react-native';

import {
  Checkbox,
  colors,
  getFont,
  Link,
  TextField,
  LinkColorType,
} from '@walmart/gtp-shared-components';

import {Page, RadioGroup} from '../components';
import type {Category} from '../components';

const Spacer = () => <View style={ss.spacer} />;

const LinkPlayground: React.FC = () => {
  type Traits = {
    color?: LinkColorType;
    disabled?: boolean;
    title?: string;
    embedded?: boolean;
  };

  const [tfText, setTfText] = React.useState('Submit');
  const [traits, setTraits] = React.useState<Traits>({
    color: 'default',
    disabled: false,
    title: tfText,
    embedded: false,
  });

  const handleRadioGroupOnChange = (cat: Category, sel: string) => {
    if (cat === 'color') {
      setTraits({
        ...traits,
        color: sel as LinkColorType,
      });
    }
  };

  React.useEffect(() => {
    setTraits({
      ...traits,
      title: tfText,
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleOnPress = (color: LinkColorType): void => {
    console.log(`Link pressed: ${color}`);
  };

  return (
    <View style={ss.container}>
      <View
        style={[
          ss.linkContainer,
          {
            backgroundColor:
              traits.color === 'default' ? colors.white : colors.blue['90'],
          },
        ]}>
        {!traits.embedded ? (
          <Link
            color={traits.color}
            disabled={traits.disabled}
            onPress={() => handleOnPress(traits.color as LinkColorType)}>
            {traits.title}
          </Link>
        ) : (
          // eslint-disable-next-line react-native/no-inline-styles
          <Text style={{color: traits.color === 'default' ? 'black' : 'white'}}>
            {'This '}
            <Link
              color={traits.color}
              disabled={traits.disabled}
              onPress={() => handleOnPress(traits.color as LinkColorType)}>
              {traits.title}
            </Link>
            {' is embedded'}
          </Text>
        )}
      </View>
      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>Link traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Spacer />
          <TextField
            label="title"
            size="small"
            value={traits.title}
            onChangeText={_text => {
              setTraits({
                ...traits,
                title: _text as string,
              });
              setTfText(_text);
            }}
          />

          <Text style={ss.radioHeaderText}>color</Text>
          <RadioGroup
            category="color"
            list={['default', 'white']}
            selected="default"
            onChange={(_, sel) => handleRadioGroupOnChange('color', sel)}
          />
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
            label="embedded"
            checked={!!traits.embedded}
            onPress={() =>
              setTraits({
                ...traits,
                embedded: !traits.embedded,
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
  linkContainer: {
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
    ...getFont('500'),
    lineHeight: 28,
    fontSize: 20,
    color: colors.blue['90'],
  } as TextStyle,
});

export {LinkPlayground};
