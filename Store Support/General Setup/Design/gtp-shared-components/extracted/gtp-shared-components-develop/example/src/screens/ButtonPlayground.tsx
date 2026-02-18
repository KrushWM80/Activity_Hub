import * as React from 'react';
import {StyleSheet, Text, TextStyle, View} from 'react-native';

import {
  Button,
  Checkbox,
  colors,
  getFont,
  Icons,
  TextField,
} from '@walmart/gtp-shared-components';
import type {
  ButtonSize,
  ButtonVariant,
  TextFieldRef,
} from '@walmart/gtp-shared-components';

import {Page, RadioGroup} from '../components';
import type {Category} from '../components';

const Spacer = () => <View style={ss.spacer} />;

const ButtonPlayground: React.FC = () => {
  type Traits = {
    variant?: ButtonVariant;
    size?: ButtonSize;
    disabled?: boolean;
    title?: string;
    leading?: React.ReactNode;
    trailing?: React.ReactNode;
    isLoading?: boolean;
    isFullWidth?: boolean;
    withHorizontalMargin?: boolean;
  };

  const tfRef = React.useRef<TextFieldRef | null>(null);

  const [tfText, setTfText] = React.useState('Submit');
  const [traits, setTraits] = React.useState<Traits>({
    variant: 'primary',
    size: 'small',
    disabled: false,
    title: tfText,
    leading: undefined,
    trailing: undefined,
    isLoading: false,
    isFullWidth: false,
    withHorizontalMargin: false,
  });

  const handleRadioGroupOnChange = (cat: Category, sel: string) => {
    if (cat === 'size') {
      setTraits({
        ...traits,
        size: sel as ButtonSize,
      });
    }
    if (cat === 'variant') {
      setTraits({
        ...traits,
        variant: sel as ButtonVariant,
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

  const handleOnPress = (variant: ButtonVariant, size: ButtonSize): void => {
    console.log(`Button pressed: ${size}, ${variant}`);
  };

  return (
    <View style={ss.container}>
      <View style={ss.buttonContainer}>
        <Button
          variant={traits.variant as ButtonVariant}
          size={traits.size as ButtonSize}
          disabled={traits.disabled}
          leading={traits.leading as React.ReactElement}
          trailing={traits.trailing as React.ReactElement}
          isLoading={traits.isLoading}
          isFullWidth={traits.isFullWidth}
          onPress={() =>
            handleOnPress(
              traits.variant as ButtonVariant,
              traits.size as ButtonSize,
            )
          }>
          {traits.title}
        </Button>
      </View>
      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>Button traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Spacer />
          <TextField
            ref={tfRef}
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

          <Text style={ss.radioHeaderText}>variant</Text>
          <RadioGroup
            category="variant"
            list={['primary', 'secondary', 'tertiary', 'destructive']}
            selected="primary"
            onChange={(_, sel) => handleRadioGroupOnChange('variant', sel)}
          />
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
            label="with leading icon"
            disabled={!!traits.trailing}
            checked={!!traits.leading}
            onPress={() =>
              setTraits({
                ...traits,
                leading: traits.leading ? undefined : <Icons.PlusIcon />,
              })
            }
          />
          <Spacer />
          <Checkbox
            label="with trailing icon"
            disabled={!!traits.leading}
            checked={!!traits.trailing}
            onPress={() =>
              setTraits({
                ...traits,
                trailing: traits.trailing ? undefined : <Icons.PlusIcon />,
              })
            }
          />
          <Spacer />
          <Checkbox
            label="isLoading"
            checked={!!traits.isLoading}
            disabled={false}
            onPress={() =>
              setTraits({
                ...traits,
                isLoading: !traits.isLoading,
              })
            }
          />
          <Spacer />
          <Checkbox
            label="isFullWidth"
            checked={!!traits.isFullWidth}
            disabled={false}
            onPress={() =>
              setTraits({
                ...traits,
                isFullWidth: !traits.isFullWidth,
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

export {ButtonPlayground};
