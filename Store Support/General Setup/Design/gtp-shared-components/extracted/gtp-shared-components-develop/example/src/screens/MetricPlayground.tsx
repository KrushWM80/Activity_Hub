import * as React from 'react';
import {Page} from '../components';
import {StyleSheet, Alert, Text, TextStyle, View} from 'react-native';
import {
  Checkbox,
  Metric,
  MetricVariant,
  TextField,
  colors,
  getFont,
} from '@walmart/gtp-shared-components';

type MetricProps = {
  textLabel?: React.ReactNode;
  timescope?: React.ReactNode;
  title: React.ReactNode;
  unit?: React.ReactNode;
  value: React.ReactNode;
  variant?: MetricVariant;
  withCardLayout?: boolean;
  withOnPress?: boolean;
  showOnPressIndicator?: boolean;
};
const Spacer = () => <View style={ss.spacer} />;

const MetricPlayground: React.FC = () => {
  const variantsArr = [
    'negativeDown',
    'negativeUp',
    'neutral',
    'positiveDown',
    'positiveUp',
  ];
  const [traits, setTraits] = React.useState<MetricProps>({
    title: 'Pre-substitution',
    timescope: 'WTD.3h ago',
    textLabel: '1.2%TW vs LW',
    value: '93.7',
    unit: '%',
    variant: 'positiveUp' as MetricVariant,
    withCardLayout: false,
    withOnPress: false,
    showOnPressIndicator: true,
  });

  const onMetricPress = () => {
    Alert.alert(`${traits?.title}`, `${traits.title} is Pressed`);
  };
  return (
    <View style={ss.container}>
      <View style={ss.MetricParentContainer}>
        <Metric
          title={traits.title}
          textLabel={traits.textLabel}
          timescope={traits.timescope}
          value={traits.value}
          unit={traits.unit}
          variant={traits.variant}
          onPress={traits.withOnPress ? onMetricPress : undefined}
          withCardLayout={traits.withCardLayout}
          showOnPressIndicator={traits.showOnPressIndicator}
        />
      </View>
      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>Metric traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Spacer />
          <Checkbox
            label={'withCardLayout'}
            checked={traits.withCardLayout}
            onPress={() =>
              setTraits({
                ...traits,
                withCardLayout: !traits.withCardLayout,
              })
            }
          />
          <Spacer />
          <Checkbox
            label={'withOnPress'}
            checked={traits.withOnPress}
            onPress={() =>
              setTraits({
                ...traits,
                withOnPress: !traits.withOnPress,
              })
            }
          />
          <Spacer />
          <Checkbox
            label={'showOnPressIndicator'}
            checked={traits.showOnPressIndicator}
            onPress={() =>
              setTraits({
                ...traits,
                showOnPressIndicator: !traits.showOnPressIndicator,
              })
            }
          />
          <Spacer />
          <Text style={ss.radioHeaderText}>variant</Text>
          {variantsArr.map((v, i) => (
            <Checkbox
              key={String(i)}
              label={v}
              checked={traits.variant === v}
              onPress={() =>
                setTraits({
                  ...traits,
                  variant: v as MetricVariant,
                })
              }
            />
          ))}
          <Spacer />
          <TextField
            label="title"
            size="small"
            value={String(traits.title)}
            onChangeText={_text => {
              setTraits({
                ...traits,
                title: _text as React.ReactNode,
              });
            }}
          />

          <Spacer />
          <TextField
            label="timescope"
            size="small"
            value={String(traits.timescope)}
            onChangeText={_text => {
              setTraits({
                ...traits,
                timescope: _text as React.ReactNode,
              });
            }}
          />

          <Spacer />
          <TextField
            label="textLabel"
            size="small"
            value={String(traits.textLabel)}
            onChangeText={_text => {
              setTraits({
                ...traits,
                textLabel: String(_text),
              });
            }}
          />

          <Spacer />
          <TextField
            label="value"
            size="small"
            value={String(traits.value)}
            onChangeText={_text => {
              setTraits({
                ...traits,
                value: String(_text),
              });
            }}
          />

          <Spacer />
          <TextField
            label="unit"
            size="small"
            value={String(traits.unit)}
            onChangeText={_text => {
              setTraits({
                ...traits,
                unit: String(_text),
              });
            }}
          />
        </View>
      </Page>
    </View>
  );
};
const ss = StyleSheet.create({
  container: {
    backgroundColor: colors.white,
    flex: 1,
  },
  MetricParentContainer: {
    backgroundColor: colors.gray['10'],
    minHeight: 150,
    marginTop: 10,
    marginHorizontal: 16,
    borderRadius: 12,
    padding: 10,
    borderColor: colors.blue['90'],
    borderWidth: 0.5,
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
    backgroundColor: colors.white,
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
  rbGroup: {
    marginLeft: 16,
  },
});
export {MetricPlayground};
