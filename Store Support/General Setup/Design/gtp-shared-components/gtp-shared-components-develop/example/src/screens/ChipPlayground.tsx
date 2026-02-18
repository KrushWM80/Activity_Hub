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
  Chip,
  ChipId,
  ChipSize,
  TextField,
  TextFieldRef,
} from '@walmart/gtp-shared-components';

import {Page} from '../components';

const Spacer = () => <View style={ss.spacer} />;

const ChipPlayground: React.FC = () => {
  const tfRef = React.useRef<TextFieldRef | null>(null);

  type Traits = {
    color: TagColor;
    leading: boolean;
    variant: TagVariant;
    disabled: boolean;
    trailing: boolean;
    size: ChipSize;
    children: React.ReactNode;
    disableOnPress: boolean;
    styles: object;
  };

  const sizeVariant = ['small', 'large'];
  const stylesObj = [
    {backgroundColor: colors.spark['60']},
    {paddingHorizontal: 14, paddingVertical: 0},
  ];

  const [selectedStyle, setSelectedStyle] = React.useState<null | number>(null);
  const [resetStyle, setResetStyle] = React.useState<boolean>(false);

  const [inputFieldValue, setInputFieldValue] =
    React.useState<string>('Chip label');
  const [isSingleChipSmallSelected, setIsSingleChipSmallSelected] =
    React.useState<boolean>(false);
  const [traits, setTraits] = React.useState<Traits>({
    color: 'gray',
    leading: true,
    variant: 'primary',
    disabled: false,
    trailing: true,
    size: 'small',
    children: inputFieldValue,
    disableOnPress: false,
    styles: {},
  });

  const onChipPressSmall = (chipId: ChipId, selected: boolean) => {
    setIsSingleChipSmallSelected(!isSingleChipSmallSelected);
    console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
  };

  React.useEffect(() => {
    if (tfRef.current) {
      tfRef.current.blur();
    }
  }, [traits]);

  const stylesHandler = (sel: object, index: number): void => {
    setTraits({
      ...traits,
      styles: sel,
    });
    setSelectedStyle(index);
  };

  const sizeVariantHandler = (v: ChipSize): void => {
    setTraits({
      ...traits,
      size: v,
    });
  };

  return (
    <View style={ss.container}>
      <View style={ss.buttonContainer}>
        <Chip
          id={0}
          selected={isSingleChipSmallSelected}
          size={traits.size}
          children={inputFieldValue}
          onPress={onChipPressSmall}
          disabled={traits.disabled}
          disableOnPress={traits.disableOnPress}
          leading={traits.leading ? <Icons.StarIcon /> : <></>}
          trailing={traits.trailing ? <Icons.CheckIcon /> : <></>}
          UNSAFE_style={traits.styles}
        />
      </View>

      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>Chip traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Spacer />

          <Text style={ss.radioHeaderText}>size</Text>
          {sizeVariant.map((v, i) => (
            <Radio
              UNSAFE_style={ss.rbGroup}
              key={i}
              label={v}
              checked={v === traits.size}
              onPress={() => sizeVariantHandler(v as ChipSize)}
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

          <Spacer />
          <Checkbox
            label="trailing"
            checked={!!traits.trailing}
            onPress={() =>
              setTraits({
                ...traits,
                trailing: !traits.trailing,
              })
            }
          />

          <Spacer />
          <Checkbox
            label="selected"
            checked={isSingleChipSmallSelected}
            disabled={traits.disableOnPress}
            onPress={() =>
              setIsSingleChipSmallSelected(!isSingleChipSmallSelected)
            }
          />

          <Spacer />
          <Checkbox
            label="disableOnPress"
            checked={!!traits.disableOnPress}
            onPress={() => {
              setIsSingleChipSmallSelected(false);
              setTraits({
                ...traits,
                disableOnPress: !traits.disableOnPress,
              });
            }}
          />

          <Spacer />
          <Text style={ss.radioHeaderText}>children</Text>
          <TextField
            ref={tfRef}
            label="(as text)"
            value={inputFieldValue}
            onChangeText={txt => setInputFieldValue(txt)}
          />

          <Spacer />
          <Text style={ss.radioHeaderText}>UNSAFE_style</Text>
          {stylesObj.map((v, i) => (
            <Radio
              disabled={resetStyle}
              UNSAFE_style={[ss.rbGroup, {marginBottom: 10}]}
              key={i}
              label={JSON.stringify(v)}
              checked={i == selectedStyle}
              onPress={() => stylesHandler(v as object, i)}
            />
          ))}

          <Spacer />
          <Checkbox
            label="Reset style"
            UNSAFE_style={ss.rbGroup}
            checked={resetStyle}
            onPress={() => {
              setTraits({
                ...traits,
                styles: {},
              });
              setSelectedStyle(null);
              setResetStyle(!resetStyle);
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

export {ChipPlayground};
