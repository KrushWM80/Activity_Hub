import * as React from 'react';
import {StyleSheet, Text, TextStyle, View} from 'react-native';
import {
  Checkbox,
  colors,
  CircularProgressIndicator,
  getFont,
  CircularProgressIndicatorOrigin,
  CircularProgressIndicatorDirection,
} from '@walmart/gtp-shared-components';

import {Page, RadioGroup, Section, Header, VariantText} from '../components';
import type {Category} from '../components';

const Spacer = () => <View style={ss.spacer} />;

const CircularProgressIndicatorPlayground: React.FC = () => {
  type Traits = {
    color?: string;
    value: number;
    label?: string;
    origin?: CircularProgressIndicatorOrigin;
    fillDirection?: CircularProgressIndicatorDirection;
  };

  const [traits, setTraits] = React.useState<Traits>({
    color: undefined,
    value: 20,
    label: 'Test',
    origin: 'left',
    fillDirection: 'counterclockwise',
  });
  const min = 0;
  const max = 100;
  const [count, setCount] = React.useState(min);

  React.useEffect(() => {
    if (count !== max) {
      const timeout = setTimeout(() => {
        setCount(count + 1);
      }, 100);

      return () => {
        clearTimeout(timeout);
      };
    }
  }, [count, traits]);
  const handleRadioGroupOnChange = (cat: Category, sel: string) => {
    if (cat === 'value') {
      setTraits({
        ...traits,
        value: parseInt(sel, 10),
      });
    } else if (cat === 'color') {
      setTraits({
        ...traits,
        color: sel.replace(' (default)', ''),
      });
    } else if (cat === 'origin') {
      setCount(0);
      setTraits({
        ...traits,
        origin: sel.replace(
          ' (default)',
          '',
        ) as CircularProgressIndicatorOrigin,
      });
    } else {
      setCount(0);
      setTraits({
        ...traits,
        fillDirection: sel.replace(
          ' (default)',
          '',
        ) as CircularProgressIndicatorDirection,
      });
    }
  };
  const renderCircularProgressIndicator = () => {
    return (
      <View>
        <VariantText>{'Fixed Value'}</VariantText>
        <CircularProgressIndicator
          value={traits.value}
          label={traits.label}
          origin={traits.origin}
          fillDirection={traits.fillDirection}
          color={traits.color}
          UNSAFE_style={ss.marginTop}
        />
      </View>
    );
  };

  const renderLoadingCircularProgressIndicator = () => {
    return (
      <View>
        <VariantText>{'With Loading'}</VariantText>
        <CircularProgressIndicator
          value={count}
          label={traits.label}
          origin={traits.origin}
          fillDirection={traits.fillDirection}
          color={traits.color}
          UNSAFE_style={ss.marginTop}
        />
      </View>
    );
  };

  return (
    <View style={ss.container}>
      <View style={ss.circleHeader}>
        <Header>
          CircularProgressIndicator{'\n'}
          <VariantText>
            {`origin= ${traits.origin} ${'\n'} fillDirection=${
              traits.fillDirection
            }`}
          </VariantText>
        </Header>
      </View>
      <View style={ss.circleContainer}>
        {renderCircularProgressIndicator()}
        {renderLoadingCircularProgressIndicator()}
      </View>
      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>CircularProgressIndicator traits</Text>
        </View>
        <Section style={ss.sectionsStyle}>
          <View style={ss.innerContainer}>
            <Checkbox
              label="With Label"
              checked={!!traits.label}
              onPress={() =>
                setTraits({
                  ...traits,
                  label: traits.label ? undefined : 'Test',
                })
              }
            />

            <Spacer />
            <Text style={ss.radioHeaderText}>value</Text>
            <Spacer />
            <RadioGroup
              category="value"
              orientation="horizontal"
              list={['0 (default)', '20', '40', '50', '80', '100']}
              selected="20"
              onChange={(_: any, sel: any) =>
                handleRadioGroupOnChange('value', sel)
              }
            />
            <Spacer />
            <Text style={ss.radioHeaderText}>
              color (you can pass any valid color)
            </Text>
            <Spacer />
            <RadioGroup
              category="color"
              orientation="horizontal"
              list={[
                'red',
                'green',
                'orange',
                'blue',
                '#cb2c90',
                '#909196 (default)',
                '#b36a16',
              ]}
              selected="#909196 (default)"
              onChange={(_: any, sel: any) =>
                handleRadioGroupOnChange('color', sel)
              }
            />
            <Spacer />
            <Text style={ss.radioHeaderText}>origin</Text>
            <Spacer />
            <RadioGroup
              category="origin"
              list={['left (default)', 'right', 'top', 'bottom']}
              selected="left"
              onChange={(_: any, sel: any) =>
                handleRadioGroupOnChange('origin', sel)
              }
            />
            <Spacer />
            <Text style={ss.radioHeaderText}>fillDirection</Text>
            <Spacer />
            <RadioGroup
              category="fillDirection"
              list={['counterclockwise (default)', 'clockwise']}
              selected="counterclockwise"
              onChange={(_: any, sel: any) =>
                handleRadioGroupOnChange('fillDirection', sel)
              }
            />
            <Spacer />
          </View>
        </Section>
      </Page>
    </View>
  );
};

const ss = StyleSheet.create({
  container: {
    flex: 1,
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
  innerContainer: {
    marginLeft: 16,
    width: '100%',
    justifyContent: 'flex-start',
  },
  spacer: {
    height: 8,
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

CircularProgressIndicatorPlayground.displayName =
  'CircularProgressIndicatorPlayground';
export {CircularProgressIndicatorPlayground};
