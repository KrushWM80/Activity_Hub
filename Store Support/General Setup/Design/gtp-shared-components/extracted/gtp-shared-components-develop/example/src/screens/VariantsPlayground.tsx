import * as React from 'react';
import {Page, VariantText} from '../components';
import {
  Checkbox,
  colors,
  Variants,
  getFont,
} from '@walmart/gtp-shared-components';
import {StyleSheet, Text, TextStyle, View} from 'react-native';

const Spacer = () => <View style={ss.spacer} />;

type VariantExProps = {
  label: string;
  checked: boolean;
  colorVal: string;
};
const VariantsPlayground: React.FC = () => {
  const exampleVariantsData: Array<VariantExProps> = [
    {label: 'blue', colorVal: colors.blue['100'], checked: false},
    {label: 'black', colorVal: colors.black['100'], checked: false},
    {label: 'gray', colorVal: colors.gray['100'], checked: false},
    {label: 'orange', colorVal: colors.orange['100'], checked: false},
    {label: 'pink', colorVal: colors.pink['100'], checked: false},
    {label: 'green', colorVal: colors.green['100'], checked: false},
    {label: 'red', colorVal: colors.red['100'], checked: false},
  ];

  type Traits = {
    variants: Array<string>;
    colors?: boolean;
    variantsVal?: Array<string>;
  };

  const [traits, setTraits] = React.useState<Traits>({
    variants: [],
    colors: true,
    variantsVal: [],
  });

  React.useEffect(() => {
    exampleHandler(0);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const [data, setData] = React.useState(exampleVariantsData);
  const exampleHandler = (index: number) => {
    const newData = [...data];
    setData(newData);
    const text = exampleVariantsData[index].label;
    const id = traits.variants.indexOf(text);
    if (id < 0) {
      traits.variants.push(text);
      newData.splice(index, 1, {
        ...exampleVariantsData[index],
        checked: !data[index].checked,
      });
    } else {
      if (traits.variants.length > 1) {
        traits.variants.splice(id, 1);
        newData.splice(index, 1, {
          ...exampleVariantsData[index],
          checked: !data[index].checked,
        });
      }
    }
  };

  return (
    <View style={ss.container}>
      <View style={ss.buttonContainer}>
        <Variants colors={traits.colors} variants={traits.variants} />
      </View>

      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>Variants traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Spacer />
          <Checkbox
            label="colors"
            checked={!!traits.colors}
            onPress={() =>
              setTraits({
                ...traits,
                colors: !traits.colors,
              })
            }
          />
          <Checkbox disabled label="variants" checked={true} />

          <Spacer />
          <Spacer />

          <Text style={ss.radioHeaderText}>
            Example
            <VariantText>
              {'\n(Add below as Variants.)\n(Variants cannot be empty.)'}
            </VariantText>
          </Text>
          <Spacer />
          {data.map((v: VariantExProps, i) => (
            <Checkbox
              key={v.label}
              label={v.label}
              checked={v.checked}
              onPress={() => {
                exampleHandler(i);
              }}
            />
          ))}
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
  section: {
    paddingVertical: 12,
    paddingHorizontal: 16,
  },
  buttonContainer: {
    backgroundColor: colors.white,
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
    fontSize: 20,
    color: colors.blue['90'],
  } as TextStyle,
});

export {VariantsPlayground};
