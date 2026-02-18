import * as React from 'react';
import {StyleSheet, Text, View, TextStyle} from 'react-native';
import {
  Checkbox,
  colors,
  Icons,
  Radio,
  getFont,
  TagColor,
  TagVariant,
  Tag,
} from '@walmart/gtp-shared-components';

import {Page} from '../components';

const Spacer = () => <View style={ss.spacer} />;

const TagPlayground: React.FC = () => {
  type Traits = {
    color: TagColor;
    leading: boolean;
    variant: TagVariant;
  };

  const tagVariant = ['primary', 'secondary', 'tertiary'];
  const tagColor = ['red', 'spark', 'green', 'blue', 'purple', 'gray'];

  const [traits, setTraits] = React.useState<Traits>({
    color: 'gray',
    leading: true,
    variant: 'primary',
  });

  const colorHandler = (sel: TagColor): void => {
    setTraits({
      ...traits,
      color: sel,
    });
  };

  const variantHandler = (v: TagVariant): void => {
    setTraits({
      ...traits,
      variant: v,
    });
  };

  return (
    <View style={ss.container}>
      <View style={ss.buttonContainer}>
        <Tag
          UNSAFE_style={ss.tag}
          color={traits.color}
          variant={traits.variant}
          leading={traits.leading ? <Icons.TruckIcon /> : null}>
          {traits.color}
        </Tag>
      </View>

      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>Tag traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Spacer />
          <Text style={ss.radioHeaderText}>color</Text>
          {tagColor.map((v, i) => (
            <Radio
              UNSAFE_style={ss.rbGroup}
              key={i}
              label={v}
              checked={v == traits.color}
              onPress={() => colorHandler(v as TagColor)}
            />
          ))}
          <Spacer />
          <Text style={ss.radioHeaderText}>variant</Text>
          {tagVariant.map((v, i) => (
            <Radio
              UNSAFE_style={ss.rbGroup}
              key={i}
              label={v}
              checked={v === traits.variant}
              onPress={() => variantHandler(v as TagVariant)}
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
  tag: {
    alignSelf: 'center',
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

export {TagPlayground};
