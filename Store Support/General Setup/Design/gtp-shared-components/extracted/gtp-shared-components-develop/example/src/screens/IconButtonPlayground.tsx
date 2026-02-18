import * as React from 'react';
import {StyleSheet, Text, TextStyle, View} from 'react-native';

import {
  IconButton,
  Checkbox,
  colors,
  getFont,
  Icons,
} from '@walmart/gtp-shared-components';
import type {IconButtonSize} from '@walmart/gtp-shared-components';

import {Page, RadioGroup} from '../components';
import type {Category} from '../components';

const Spacer = () => <View style={ss.spacer} />;

const IconButtonPlayground: React.FC = () => {
  type Traits = {
    size?: IconButtonSize;
    disabled?: boolean;
    checkIcon?: boolean;
    plusIcon?: boolean;
    homeIcon?: boolean;
  };

  const [traits, setTraits] = React.useState<Traits>({
    size: 'small',
    disabled: false,
    checkIcon: false,
    plusIcon: false,
    homeIcon: false,
  });

  const handleRadioGroupOnChange = (cat: Category, sel: string) => {
    if (cat === 'size') {
      setTraits({
        ...traits,
        size: sel as IconButtonSize,
      });
    }
  };

  React.useEffect(() => {}, []);

  const handleOnPress = (size: IconButtonSize): void => {
    console.log(`IconButton pressed: ${size}`);
  };

  const [Icon, setIcon] = React.useState<React.ReactElement>();

  React.useEffect(() => {
    if (traits.checkIcon) {
      setIcon(<Icons.CheckIcon />);
    } else if (traits.plusIcon) {
      setIcon(<Icons.PlusIcon />);
    } else if (traits.homeIcon) {
      setIcon(<Icons.HomeIcon />);
    } else {
      setIcon(<Icons.EmailIcon />);
    }
  }, [traits]);

  console.log('---- traits:', JSON.stringify(traits, null, '  '));

  return (
    <View style={ss.container}>
      <View style={ss.buttonContainer}>
        <IconButton
          size={traits.size as IconButtonSize}
          disabled={traits.disabled}
          onPress={() => handleOnPress(traits.size as IconButtonSize)}>
          {Icon}
        </IconButton>
      </View>
      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>Button traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Text style={ss.radioHeaderText}>size</Text>
          <RadioGroup
            category="size"
            list={['small', 'medium', 'large']}
            selected="small"
            onChange={(_, sel) => handleRadioGroupOnChange('size', sel)}
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
            label="with CheckIcon"
            disabled={traits.plusIcon || traits.homeIcon}
            checked={!!traits.checkIcon}
            onPress={() =>
              setTraits({
                ...traits,
                checkIcon: !traits.checkIcon,
              })
            }
          />
          <Spacer />
          <Checkbox
            label="with PlusIcon"
            disabled={traits.checkIcon || traits.homeIcon}
            checked={!!traits.plusIcon}
            onPress={() =>
              setTraits({
                ...traits,
                plusIcon: !traits.plusIcon,
              })
            }
          />
          <Spacer />
          <Checkbox
            label="with HomeIcon"
            disabled={traits.checkIcon || traits.plusIcon}
            checked={!!traits.homeIcon}
            onPress={() =>
              setTraits({
                ...traits,
                homeIcon: !traits.homeIcon,
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
    ...getFont('500'),
    lineHeight: 28,
    fontSize: 20,
    color: colors.blue['90'],
  } as TextStyle,
});

export {IconButtonPlayground};
