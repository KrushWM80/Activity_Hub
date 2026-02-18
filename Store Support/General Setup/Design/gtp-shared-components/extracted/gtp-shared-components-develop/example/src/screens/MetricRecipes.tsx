import * as React from 'react';
import {View} from 'react-native';

import {Header, Page, Section, VariantText} from '../components';
import {Metric, MetricVariant} from '@walmart/gtp-shared-components';

const MetricRecipes: React.FC = () => {
  const metricData = [
    {
      title: 'Actual to demand',
      timescope: 'MTD.5m ago',
      textLabel: 'Hours index to demand',
      value: '95.2',
      unit: '%',
    },
    {
      value: '20.11',
      unit: 'WOSH',
    },
    {
      title: 'Real-time WOSH and overtime',
      timescope: 'Today.5m ago',
      value: '133.52',
      unit: 'OT hours',
      variant: 'negativeDown' as MetricVariant,
      withCardLayout: true,
    },
    {
      title: 'Store safety',
      timescope: 'YTD.9h ago',
      textLabel: 'Accident free days',
      value: '21',
      withCardLayout: true,
    },
    {
      textLabel: 'Customer accidents',
      value: '7',
      withCardLayout: true,
    },
    {
      textLabel: 'Associate accidents',
      value: '4',
      withCardLayout: true,
    },
    {
      title: 'First time pick Percentage',
      timescope: 'WTD.3h ago',
      textLabel: '5.5%TY vs LY',
      value: '95.6',
      unit: '%',
      variant: 'positiveUp' as MetricVariant,
      withCardLayout: true,
    },
    {
      title: 'Pre-substitution',
      timescope: 'WTD.3h ago',
      textLabel: '1.2%TW vs LW',
      value: '93.7',
      unit: '%',
      variant: 'positiveUp' as MetricVariant,
      withCardLayout: true,
    },

    {
      title: 'Sales',
      timescope: 'MTD',
      textLabel: '3k (3.7%) less than last month',
      value: '$1.23',
      unit: 'M',
      variant: 'negativeDown' as MetricVariant,
      withCardLayout: true,
    },
  ];

  const codeSnippet = (v: any) => {
    let snippet = '<Metric';
    if (v.title) {
      snippet += `\n\t title={${v.title}} `;
    }
    if (v.textLabel) {
      snippet += `\n\t textLabel={${v.textLabel}} `;
    }
    if (v.timescope) {
      snippet += `\n\t timescope={${v.timescope}} `;
    }
    if (v.value) {
      snippet += `\n\t value={${v.value}} `;
    }
    if (v.unit) {
      snippet += `\n\t unit={${v.unit}} `;
    }
    if (v.variant) {
      snippet += `\n\t variant={${v.variant}} `;
    }
    if (v.withCardLayout) {
      snippet += `\n\t withCardLayout={${v.withCardLayout}} `;
    }
    snippet += '/>';

    return snippet;
  };

  return (
    <Page>
      {metricData.map((v, i) => (
        <View key={`container-${i + 1}`}>
          <Header>
            Metric{'\n'}
            <VariantText>{codeSnippet(v)}</VariantText>
          </Header>
          <Section>
            <Metric
              title={v.title}
              textLabel={v.textLabel}
              timescope={v.timescope}
              value={v.value}
              unit={v.unit}
              variant={v.variant}
              withCardLayout={v.withCardLayout}
            />
          </Section>
        </View>
      ))}
    </Page>
  );
};

export {MetricRecipes};
