import * as React from 'react';
import {Header, Page, Section, VariantText} from '../components';
import {Alert} from 'react-native';
import {
  MetricGroup,
  MetricVariant,
  colors,
} from '@walmart/gtp-shared-components';

const MetricGroupRecipes: React.FC = () => {
  const twoMetricData = [
    {
      title: 'Actual to demand',
      timescope: 'MTD.5m ago',
      textLabel: 'Hours index to demand',
      value: '95.2',
      unit: '%',
    },
    {
      title: 'Actual to demand',
      timescope: 'MTD.5m ago',
      textLabel: 'Wage index to plan',
      value: '101.2',
      unit: '%',
    },
  ];
  const twoMetricData_1 = [
    {
      value: '20.11',
      unit: 'WOSH',
    },
    {
      title: 'Real-time WOSH and overtime',
      timescope: 'Today.5m ago',
      value: '133.52',
      unit: 'OT hours',
    },
  ];
  const threeMetricData = [
    {
      title: 'Store safety',
      timescope: 'YTD.9h ago',
      textLabel: 'Accident free days',
      value: '21',
    },
    {
      textLabel: 'Customer accidents',
      value: '7',
    },
    {
      textLabel: 'Associate accidents',
      value: '4',
    },
  ];
  const onMetricPress = (title: string) => {
    Alert.alert(title, `${title} is Pressed`);
  };

  const individualMetricData = [
    {
      title: 'First time pick Percentage',
      timescope: 'WTD.3h ago',
      textLabel: '5.5%TY vs LY',
      value: '95.6',
      unit: '%',
      variant: 'positiveUp' as MetricVariant,
      onPress: () => onMetricPress('First time pick Percentage'),
    },
    {
      title: 'Pre-substitution',
      timescope: 'WTD.3h ago',
      textLabel: '1.2%TW vs LW',
      value: '93.7',
      unit: '%',
      variant: 'positiveUp' as MetricVariant,
      onPress: () => onMetricPress('Pre-substitution'),
    },
  ];

  return (
    <Page>
      <Header>
        MetricGroup{'\n  '}
        <VariantText>{'multi data with the single title'}</VariantText>
      </Header>
      <Section>
        <MetricGroup
          data={threeMetricData}
          onPress={() => onMetricPress(threeMetricData[0]?.title!)}
          pressedColor={colors.blue['20']}
        />
        <MetricGroup
          data={twoMetricData}
          onPress={() => onMetricPress(twoMetricData[0]?.title!)}
        />
        <MetricGroup
          data={twoMetricData_1}
          onPress={() => onMetricPress(twoMetricData_1[1]?.title!)}
        />
      </Section>
      <Header>
        MetricGroup{'\n  '}
        <VariantText>{'split Individual Metrics '}</VariantText>
      </Header>
      <Section>
        <MetricGroup data={individualMetricData} allowIndividualTitles={true} />
      </Section>
    </Page>
  );
};

export {MetricGroupRecipes};
