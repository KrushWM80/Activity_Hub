import * as React from 'react';
import {View, StyleSheet, Text, TextStyle} from 'react-native';
import {
  colors,
  Checkbox,
  DateDropdown,
  getFont,
} from '@walmart/gtp-shared-components';
import {Page, RadioGroup, Section, Header} from '../components';
import type {Category} from '../components';

const DateDropdownPlayground: React.FC = () => {
  type Traits = {
    value?: Date;
    label?: string;
    minimumDate?: Date;
    maximumDate?: Date;
    dateFormat?: string;
    helperText?: string;
    error?: string;
    placeholder?: string;
    disabled?: boolean;
  };

  const [traits, setTraits] = React.useState<Traits>({
    label: 'Date',
    dateFormat: 'MM / DD / YYYY',
    disabled: false,
  });
  const Spacer = () => <View style={ss.spacer} />;

  const SpacerHorizontal = () => <View style={ss.horizontalSpacer} />;
  const handleRadioGroupOnChange = (cat: Category, sel: string) => {
    console.log(cat, sel);
    const currentYear = new Date().getFullYear();
    if (cat === 'value') {
      setTraits({
        ...traits,
        value: sel === 'new Date()' ? new Date() : new Date(currentYear, 0, 1),
      });
    } else if (cat === 'minimumDate') {
      setTraits({
        ...traits,
        minimumDate:
          sel === 'new Date()' ? new Date() : new Date(currentYear, 0, 1),
      });
    } else if (cat === 'maximumDate') {
      setTraits({
        ...traits,
        maximumDate:
          sel === 'new Date()' ? new Date() : new Date(currentYear, 11, 31),
      });
    } else if (cat === 'dateFormat') {
      setTraits({
        ...traits,
        dateFormat: sel,
      });
    } else if (cat === 'disabled') {
      setTraits({
        ...traits,
        disabled: sel === 'disabled' ? true : false,
      });
    }
  };
  return (
    <Page>
      <View key={'Template'}>
        <Header>DateDropdown</Header>
        <View style={ss.outerContainer}>
          <View style={ss.innerContainer}>
            <DateDropdown
              disabled={traits.disabled}
              label={traits.label}
              value={traits.value}
              minimumDate={traits.minimumDate}
              maximumDate={traits.maximumDate}
              dateFormat={traits.dateFormat}
              helperText={traits.helperText}
              error={traits.error}
              onSelect={dt => {
                if (dt) {
                  setTraits({
                    ...traits,
                    value: dt,
                  });
                }
              }}
            />
          </View>
        </View>
      </View>

      <View style={ss.header}>
        <Text style={ss.headerText}>DateDropdown traits</Text>
      </View>
      <Section style={ss.sectionsStyle}>
        <View style={ss.innerContainer}>
          <View style={{flexDirection: 'row'}}>
            <Checkbox
              label="label"
              checked={!!traits.label}
              onPress={() =>
                setTraits({
                  ...traits,
                  label: traits.label ? undefined : 'Date',
                })
              }
            />
            <SpacerHorizontal />
            <Checkbox
              label="helperText"
              checked={!!traits.helperText}
              onPress={() =>
                setTraits({
                  ...traits,
                  helperText: traits.helperText
                    ? undefined
                    : 'this is a helperText',
                })
              }
            />
            <SpacerHorizontal />
            <Checkbox
              label="error"
              checked={!!traits.error}
              onPress={() =>
                setTraits({
                  ...traits,
                  error: traits.error ? undefined : 'this field is required',
                })
              }
            />
          </View>
          <Spacer />
          <Text style={ss.radioHeaderText}>value</Text>
          <Spacer />
          <RadioGroup
            category="value"
            orientation="horizontal"
            list={['new Date()', `new Date(${new Date().getFullYear()}, 0, 1)`]}
            selected="undefined (default)"
            onChange={(_: any, sel: any) =>
              handleRadioGroupOnChange('value', sel)
            }
          />
          <Spacer />
          <Text style={ss.radioHeaderText}>minimumDate</Text>
          <Spacer />
          <RadioGroup
            category="minimumDate"
            orientation="horizontal"
            list={['new Date()', `new Date(${new Date().getFullYear()}, 0, 1)`]}
            selected="undefined (default)"
            onChange={(_: any, sel: any) =>
              handleRadioGroupOnChange('minimumDate', sel)
            }
          />
          <Spacer />
          <Text style={ss.radioHeaderText}>maximumDate</Text>
          <Spacer />
          <RadioGroup
            category="maximumDate"
            orientation="horizontal"
            list={[
              'new Date()',
              `new Date(${new Date().getFullYear()}, 11, 31)`,
            ]}
            selected="undefined (default)"
            onChange={(_: any, sel: any) =>
              handleRadioGroupOnChange('maximumDate', sel)
            }
          />
          <Spacer />
          <Text style={ss.radioHeaderText}>dateFormat</Text>
          <Spacer />
          <RadioGroup
            category="dateFormat"
            orientation="horizontal"
            list={['MM / DD / YYYY', 'YYYY / MM / DD', 'MMM Do YY']}
            selected="MM / DD / YYYY"
            onChange={(_: any, sel: any) =>
              handleRadioGroupOnChange('dateFormat', sel)
            }
          />
          <Spacer />
          <Text style={ss.radioHeaderText}>disabled</Text>
          <Spacer />
          <RadioGroup
            category="disabled"
            orientation="horizontal"
            list={['enabled (default)', 'disabled']}
            selected="enabled (default)"
            onChange={(_: any, sel: any) =>
              handleRadioGroupOnChange('disabled', sel)
            }
          />
          <Spacer />
        </View>
      </Section>
    </Page>
  );
};

const ss = StyleSheet.create({
  container: {
    flex: 1,
  },
  dropDownHeight: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    width: '100%',
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
    padding: 10,
    height: 80,
    margin: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  outerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
  innerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
    padding: 10,
  },
  spacer: {
    height: 8,
  },
  horizontalSpacer: {
    width: 8,
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
    marginTop: 10,
    borderTopColor: colors.blue['90'],
    borderLeftColor: colors.blue['90'],
    borderRightColor: colors.blue['90'],
    paddingRight: 16,
  },
  circleContainer: {
    backgroundColor: colors.white,
    flexDirection: 'row',
    padding: 10,
    alignItems: 'center',
    justifyContent: 'space-around',
  },
  circleHeader: {
    backgroundColor: colors.white,
    paddingHorizontal: 10,
    marginTop: -10,
  },
  sectionsStyle: {borderColor: colors.blue['90'], borderWidth: 1},
  headerText: {
    fontSize: 20,
    fontWeight: '500',
    color: colors.blue['90'],
    textAlign: 'left',
    paddingVertical: 10,
    marginLeft: 12,
  },
  imageContainer: {
    backgroundColor: colors.gray['100'],
    borderRadius: 16,
    marginHorizontal: 16,
    paddingVertical: 16,
    marginTop: 8,
  },
  image: {
    width: '100%',
    resizeMode: 'contain',
  },

  radioHeaderText: {
    ...getFont(),
    color: colors.blue['90'],
  } as TextStyle,
  rbGroup: {
    marginLeft: 16,
  },
  marginTop: {
    marginTop: 10,
  },
});

export {DateDropdownPlayground};
