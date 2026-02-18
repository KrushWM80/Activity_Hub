import * as React from 'react';
import {StyleSheet, View, TextStyle, Text} from 'react-native';
import {
  SpotIcon,
  Icons,
  colors,
  getFont,
  Radio,
  SpotIconColor,
  SpotIconSize,
} from '@walmart/gtp-shared-components';
import {Page} from '../components';

const colorVarient: SpotIconColor[] = ['blue', 'white'];
const sizeVarient: SpotIconSize[] = ['small', 'large'];
const iconVarient = ['homeIcon', 'checkIcon', 'plusIcon', 'truckIcon'];

const Spacer = () => <View style={ss.spacer} />;
const SpotIconPlayground: React.FC = () => {
  type Traits = {
    color: SpotIconColor;
    size: SpotIconSize;
    checkIcon?: boolean;
    plusIcon?: boolean;
    homeIcon?: boolean;
    TruckIcon?: boolean;
    selectedIcon: string;
  };
  const [traits, setTraits] = React.useState<Traits>({
    color: 'blue',
    size: 'small',
    checkIcon: false,
    plusIcon: false,
    homeIcon: false,
    TruckIcon: false,
    selectedIcon: 'homeIcon',
  });

  const colorHandler = (sel: SpotIconColor): void => {
    setTraits({
      ...traits,
      color: sel,
    });
  };

  const variantHandler = (v: SpotIconSize): void => {
    setTraits({
      ...traits,
      size: v,
    });
  };

  const [Icon, setIcon] = React.useState<React.ReactElement>(
    <Icons.HomeIcon />,
  );

  const iconVarientHandler = (val: string): void => {
    setTraits({
      ...traits,
      selectedIcon: val,
    });

    if (val === 'checkIcon') {
      setIcon(<Icons.CheckIcon />);
    } else if (val === 'plusIcon') {
      setIcon(<Icons.PlusIcon />);
    } else if (val === 'homeIcon') {
      setIcon(<Icons.HomeIcon />);
    } else if (val === 'truckIcon') {
      setIcon(<Icons.TruckIcon />);
    } else {
      setIcon(<Icons.EmailIcon />);
    }
  };

  return (
    <View style={ss.container}>
      <View style={ss.buttonContainer}>
        <SpotIcon
          color={traits.color as SpotIconColor}
          size={traits.size as SpotIconSize}>
          {Icon}
        </SpotIcon>
      </View>

      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>SpotIcon traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Spacer />
          <Text style={ss.radioHeaderText}>color</Text>
          {colorVarient.map((v, i) => (
            <Radio
              UNSAFE_style={ss.rbGroup}
              key={i}
              label={v}
              checked={v === traits.color}
              onPress={() => colorHandler(v as SpotIconColor)}
            />
          ))}
          <Spacer />
          <Text style={ss.radioHeaderText}>size</Text>
          {sizeVarient.map((v, i) => (
            <Radio
              UNSAFE_style={ss.rbGroup}
              key={i}
              label={v}
              checked={v === traits.size}
              onPress={() => variantHandler(v as SpotIconSize)}
            />
          ))}

          <Spacer />
          <Spacer />
          <Text style={ss.radioHeaderText}>children(as Icons)</Text>
          {iconVarient.map((v, i) => (
            <Radio
              UNSAFE_style={ss.rbGroup}
              key={i}
              label={v}
              checked={v === traits.selectedIcon}
              onPress={() => iconVarientHandler(v)}
            />
          ))}
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

export {SpotIconPlayground};
