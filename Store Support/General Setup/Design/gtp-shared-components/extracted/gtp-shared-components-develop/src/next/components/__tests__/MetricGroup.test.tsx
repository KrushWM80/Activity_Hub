import * as React from 'react';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Metric';
import * as texttoken from '@livingdesign/tokens/dist/react-native/light/regular/components/Text';
import {fireEvent, render, screen} from '@testing-library/react-native';

import {colors} from '../../utils';
import {
  MetricTextlabelColors,
  MetricVariant,
  renderTextLabel,
  renderTimeScope,
  renderTitle,
  renderValueUnit,
} from '../Metric';
import {MetricGroup} from '../MetricGroup';

const _metricTimescope = 'Metric-timescope';
const _metricTitle = 'Metric-title';
const _metricValue = 'Metric-value';
const _metricTextLabel = 'Metric-text-label';
const metricPress = jest.fn();
describe.each<MetricVariant>([
  'neutral',
  'positiveUp',
  'positiveDown',
  'negativeUp',
  'negativeDown',
])('Should render MetricGroup correctly for Variants', (variant) => {
  test(`Test MetricGroup with single title for variant="${variant} `, async () => {
    const threeMetricData = [
      {
        title: 'Store safety',
        timescope: 'YTD.9h ago',
        textLabel: 'Accident free days',
        value: '21',
        variant: variant,
      },
      {
        textLabel: 'Customer accidents',
        value: '7',
        variant: variant,
      },
      {
        textLabel: 'Associate accidents',
        value: '4',
        variant: variant,
      },
    ];
    const wrapper = render(<MetricGroup data={threeMetricData} />);

    const metricGroupTitle = await wrapper.findByTestId(_metricTitle);
    expect(metricGroupTitle).toHaveStyle([
      {
        fontSize:
          token.componentMetricTitleAliasOptionsSize.toString() === 'small'
            ? texttoken.componentTextBodySizeSmallFontSize
            : token.componentMetricTitleAliasOptionsSize.toString() === 'medium'
            ? texttoken.componentTextBodySizeMediumFontSize
            : texttoken.componentTextBodySizeLargeFontSize,
        fontWeight: `${token.componentMetricTitleAliasOptionsWeight}`,
      },
    ]);

    const metricGroupTimeScope = await wrapper.findByTestId(_metricTimescope);
    expect(metricGroupTimeScope).toHaveStyle([
      {
        fontSize:
          token.componentMetricTimescopeAliasOptionsSize === 'small'
            ? texttoken.componentTextBodySizeSmallFontSize
            : token.componentMetricTimescopeAliasOptionsSize === 'medium'
            ? texttoken.componentTextBodySizeMediumFontSize
            : texttoken.componentTextBodySizeLargeFontSize,
        marginBottom: token.componentMetricTimescopeMarginBottom,
        color: token.componentMetricTimescopeTextColor,
      },
    ]);

    const metricValue = wrapper.queryAllByTestId(_metricValue);
    expect(metricValue.length).toEqual(3);
    expect(metricValue[0]).toHaveStyle([
      {
        fontSize:
          token.componentMetricValueAliasOptionsSize === 'small'
            ? texttoken.componentTextDisplaySizeSmallFontSizeBS
            : texttoken.componentTextDisplaySizeLargeFontSizeBS,
        fontWeight: `${token.componentMetricValueAliasOptionsWeight}`,
        marginRight: token.componentMetricValueMarginEnd,
        alignSelf: token.componentMetricUnitVerticalAlign,
      },
    ]);

    const metricTextLabel = wrapper.queryAllByTestId(_metricTextLabel);
    expect(metricTextLabel.length).toEqual(3);
    expect(metricTextLabel[0]).toHaveStyle([
      {
        fontSize:
          token.componentMetricLabelAliasOptionsSize === 'small'
            ? texttoken.componentTextBodySizeSmallFontSize
            : token.componentMetricLabelAliasOptionsSize === 'medium'
            ? texttoken.componentTextBodySizeMediumFontSize
            : texttoken.componentTextBodySizeLargeFontSize,
        fontWeight: `${token.componentMetricUnitAliasOptionsWeight}`,
        color: MetricTextlabelColors[variant].labelColor,
      },
    ]);
    if (variant === 'negativeDown' || variant === 'positiveDown') {
      const arrowDownIcon = wrapper.queryAllByTestId('ArrowDownIcon');
      expect(arrowDownIcon[0]).toHaveStyle([
        {
          tintColor: MetricTextlabelColors[variant].iconTintColor,
          marginTop: token.componentMetricTrendIndicatorMarginTop,
          marginRight: token.componentMetricTrendIndicatorMarginEnd,
        },
      ]);
    } else if (variant !== 'neutral') {
      const arrowUpIcon = wrapper.queryAllByTestId('ArrowUpIcon');
      expect(arrowUpIcon[0]).toHaveStyle([
        {
          tintColor: MetricTextlabelColors[variant].iconTintColor,
          marginTop: token.componentMetricTrendIndicatorMarginTop,
          marginRight: token.componentMetricTrendIndicatorMarginEnd,
        },
      ]);
    }
  });
  test(`Test MetricGroup allowIndividualTitles=true variant="${variant}`, async () => {
    const individualMetricData = [
      {
        title: 'First time pick Percentage',
        timescope: 'WTD.3h ago',
        textLabel: '5.5%TY vs LY',
        value: '95.6',
        unit: '%',
        variant: variant,
      },
      {
        title: 'Pre-substitution',
        timescope: 'WTD.3h ago',
        textLabel: '1.2%TW vs LW',
        value: '93.7',
        unit: '%',
        variant: variant,
      },
    ];
    const wrapper = render(
      <MetricGroup data={individualMetricData} allowIndividualTitles={true} />,
    );
    const metricGroupContainer = wrapper.queryAllByTestId('MetricGroup');
    expect(metricGroupContainer.length).toEqual(1);

    const metricTitle = wrapper.queryAllByTestId(_metricTitle);
    expect(metricTitle.length).toEqual(2);

    const metricTimescope = wrapper.queryAllByTestId(_metricTimescope);
    expect(metricTimescope.length).toEqual(2);

    const metricValue = wrapper.queryAllByTestId(_metricValue);
    expect(metricValue.length).toEqual(2);

    const metricUnit = wrapper.queryAllByTestId('Metric-unit');
    expect(metricUnit.length).toEqual(2);

    const metricTextLabel = wrapper.queryAllByTestId(_metricTextLabel);
    expect(metricTextLabel.length).toEqual(2);

    if (variant === 'negativeDown' || variant === 'positiveDown') {
      const arrowDownIcon = wrapper.queryAllByTestId('ArrowDownIcon');
      expect(arrowDownIcon.length).toEqual(2);
    } else if (variant !== 'neutral') {
      const arrowUpIcon = wrapper.queryAllByTestId('ArrowUpIcon');
      expect(arrowUpIcon.length).toEqual(2);
    }
  });
});

describe.each<MetricVariant>([
  'neutral',
  'positiveUp',
  'positiveDown',
  'negativeUp',
  'negativeDown',
])('Test render Functions', (variant) => {
  test(`renderTitle ${variant}`, () => {
    render(<>{renderTitle('title')}</>);
    const title = screen.getByTestId(_metricTitle);
    expect(title).toHaveStyle([
      {
        fontSize:
          token.componentMetricTitleAliasOptionsSize.toString() === 'small'
            ? texttoken.componentTextBodySizeSmallFontSize
            : token.componentMetricTitleAliasOptionsSize.toString() === 'medium'
            ? texttoken.componentTextBodySizeMediumFontSize
            : texttoken.componentTextBodySizeLargeFontSize,
        fontWeight: `${token.componentMetricTitleAliasOptionsWeight}`,
      },
    ]);
  });
  test(`renderTimeScope ${variant}`, () => {
    render(<>{renderTimeScope('YTD.9h ago')}</>);
    const timeScope = screen.getByTestId(_metricTimescope);
    expect(timeScope).toHaveStyle([
      {
        fontSize:
          token.componentMetricTimescopeAliasOptionsSize === 'small'
            ? texttoken.componentTextBodySizeSmallFontSize
            : token.componentMetricTimescopeAliasOptionsSize === 'medium'
            ? texttoken.componentTextBodySizeMediumFontSize
            : texttoken.componentTextBodySizeLargeFontSize,
        marginBottom: token.componentMetricTimescopeMarginBottom,
        color: token.componentMetricTimescopeTextColor,
      },
    ]);
  });
  test(`renderValueUnit ${variant}`, () => {
    render(renderValueUnit('21', '%'));
    const valueUnit = screen.getByTestId(_metricValue);
    expect(valueUnit).toHaveStyle([
      {
        fontSize:
          token.componentMetricValueAliasOptionsSize === 'small'
            ? texttoken.componentTextDisplaySizeSmallFontSizeBS
            : texttoken.componentTextDisplaySizeLargeFontSizeBS,
        fontWeight: `${token.componentMetricValueAliasOptionsWeight}`,
        marginRight: token.componentMetricValueMarginEnd,
        alignSelf: token.componentMetricUnitVerticalAlign,
      },
    ]);
  });
  test(`renderTextLabel for ${variant}`, () => {
    render(<>{renderTextLabel('TextLabel', variant)}</>);
    const textLabel = screen.getByTestId(_metricTextLabel);
    expect(textLabel).toHaveStyle([
      {
        fontSize:
          token.componentMetricLabelAliasOptionsSize === 'small'
            ? texttoken.componentTextBodySizeSmallFontSize
            : token.componentMetricLabelAliasOptionsSize === 'medium'
            ? texttoken.componentTextBodySizeMediumFontSize
            : texttoken.componentTextBodySizeLargeFontSize,
        fontWeight: `${token.componentMetricUnitAliasOptionsWeight}`,
        color: MetricTextlabelColors[variant].labelColor,
      },
    ]);
    if (variant === 'negativeDown' || variant === 'positiveDown') {
      const arrowDownIcon = screen.getByTestId('ArrowDownIcon');
      expect(arrowDownIcon).toHaveStyle([
        {
          tintColor: MetricTextlabelColors[variant].iconTintColor,
          marginTop: token.componentMetricTrendIndicatorMarginTop,
          marginRight: token.componentMetricTrendIndicatorMarginEnd,
        },
      ]);
    } else if (variant !== 'neutral') {
      const arrowUpIcon = screen.getByTestId('ArrowUpIcon');
      expect(arrowUpIcon).toHaveStyle([
        {
          tintColor: MetricTextlabelColors[variant].iconTintColor,
          marginTop: token.componentMetricTrendIndicatorMarginTop,
          marginRight: token.componentMetricTrendIndicatorMarginEnd,
        },
      ]);
    }
  });
});
describe('Test MetricGroup with OnPress', () => {
  test(`Test MetricGroup with rightChervon OnPress `, async () => {
    const threeMetricData = [
      {
        title: 'Store safety',
        timescope: 'YTD.9h ago',
        textLabel: 'Accident free days',
        value: '21',
        variant: 'neutral' as MetricVariant,
      },
      {
        textLabel: 'Customer accidents',
        value: '7',
        variant: 'neutral' as MetricVariant,
      },
      {
        textLabel: 'Associate accidents',
        value: '4',
        variant: 'neutral' as MetricVariant,
      },
    ];
    const wrapper = render(
      <MetricGroup data={threeMetricData} onPress={metricPress} />,
    );
    const metricGroupContainer = wrapper.queryAllByTestId('MetricGroup_Card');
    const chevronRightIcon = await wrapper.findByTestId('ChevronRightIcon');
    expect(chevronRightIcon).toBeDefined();
    fireEvent.press(metricGroupContainer[0]);
    expect(metricPress).toHaveBeenCalled();
  });
  test(`Test MetricGroup allowIndividualTitles=true  onPress`, async () => {
    const individualMetricData = [
      {
        title: 'First time pick Percentage',
        timescope: 'WTD.3h ago',
        textLabel: '5.5%TY vs LY',
        value: '95.6',
        unit: '%',
        onPress: metricPress,
        variant: 'neutral' as MetricVariant,
      },
      {
        title: 'Pre-substitution',
        timescope: 'WTD.3h ago',
        textLabel: '1.2%TW vs LW',
        value: '93.7',
        unit: '%',
        onPress: metricPress,
        variant: 'neutral' as MetricVariant,
      },
    ];
    const wrapper = render(
      <MetricGroup data={individualMetricData} allowIndividualTitles={true} />,
    );
    const metric1 = wrapper.queryAllByTestId('MetricGroup_Card-0');
    expect(metric1.length).toEqual(1);
    const metric2 = wrapper.queryAllByTestId('MetricGroup_Card-1');
    expect(metric2.length).toEqual(1);
    const chevronRightIcon = await wrapper.queryAllByTestId('ChevronRightIcon');
    expect(chevronRightIcon.length).toEqual(2);
    fireEvent.press(metric1[0]);
    expect(metricPress).toHaveBeenCalled();
    fireEvent.press(metric2[0]);
    expect(metricPress).toHaveBeenCalled();
  });
  test(`Test MetricGroup allowIndividualTitles=true  onPress without chevron`, async () => {
    const individualMetricData = [
      {
        title: 'First time pick Percentage',
        timescope: 'WTD.3h ago',
        textLabel: '5.5%TY vs LY',
        value: '95.6',
        unit: '%',
        onPress: metricPress,
        variant: 'neutral' as MetricVariant,
      },
      {
        title: 'Pre-substitution',
        timescope: 'WTD.3h ago',
        textLabel: '1.2%TW vs LW',
        value: '93.7',
        unit: '%',
        onPress: metricPress,
        variant: 'neutral' as MetricVariant,
      },
    ];
    const wrapper = render(
      <MetricGroup
        data={individualMetricData}
        showOnPressIndicator={false}
        allowIndividualTitles={true}
      />,
    );
    const metric1 = wrapper.queryAllByTestId('MetricGroup_Card-0');
    expect(metric1.length).toEqual(1);
    const metric2 = wrapper.queryAllByTestId('MetricGroup_Card-1');
    expect(metric2.length).toEqual(1);
    const chevronRightIcon = await wrapper.queryAllByTestId('ChevronRightIcon');
    expect(chevronRightIcon.length).toEqual(0);
    fireEvent.press(metric1[0]);
    expect(metricPress).toHaveBeenCalled();
    fireEvent.press(metric2[0]);
    expect(metricPress).toHaveBeenCalled();
  });
  test(`Test MetricGroup allowIndividualTitles=true  onPress with Custom pressed colors`, async () => {
    const individualMetricData = [
      {
        title: 'First time pick Percentage',
        timescope: 'WTD.3h ago',
        textLabel: '5.5%TY vs LY',
        value: '95.6',
        unit: '%',
        onPress: metricPress,
        isStatusPressedForTest: true,
        variant: 'neutral' as MetricVariant,
      },
      {
        title: 'Pre-substitution',
        timescope: 'WTD.3h ago',
        textLabel: '1.2%TW vs LW',
        value: '93.7',
        unit: '%',
        isStatusPressedForTest: true,
        onPress: metricPress,
        variant: 'neutral' as MetricVariant,
      },
    ];
    const wrapper = render(
      <MetricGroup
        data={individualMetricData}
        allowIndividualTitles={true}
        pressedColor="#ffcc00"
      />,
    );
    const metric1 = wrapper.queryAllByTestId('MetricGroup_Card-0');
    expect(metric1.length).toEqual(1);
    const metric2 = wrapper.queryAllByTestId('MetricGroup_Card-1');
    expect(metric2.length).toEqual(1);
    const chevronRightIcon = await wrapper.queryAllByTestId('ChevronRightIcon');
    expect(chevronRightIcon.length).toEqual(2);
    expect(metric1[0]).toHaveStyle([
      {width: '100%', padding: 16, borderRadius: 8},
      {backgroundColor: '#ffcc00'},
    ]);
    expect(metric2[0]).toHaveStyle([
      {width: '100%', padding: 16, borderRadius: 8},
      {backgroundColor: '#ffcc00'},
    ]);
    fireEvent.press(metric1[0]);
    expect(metricPress).toHaveBeenCalled();
    fireEvent.press(metric2[0]);
    expect(metricPress).toHaveBeenCalled();
  });
  test(`Test MetricGroup with OnPress with default pressed colors `, async () => {
    const threeMetricData = [
      {
        title: 'Store safety',
        timescope: 'YTD.9h ago',
        textLabel: 'Accident free days',
        value: '21',
        variant: 'neutral' as MetricVariant,
      },
      {
        textLabel: 'Customer accidents',
        value: '7',
        variant: 'neutral' as MetricVariant,
      },
      {
        textLabel: 'Associate accidents',
        value: '4',
        variant: 'neutral' as MetricVariant,
      },
    ];
    const wrapper = render(
      <MetricGroup
        data={threeMetricData}
        onPress={metricPress}
        isStatusPressedForTest={true}
      />,
    );
    const metricGroupContainer = wrapper.queryAllByTestId('MetricGroup_Card');
    const chevronRightIcon = await wrapper.findByTestId('ChevronRightIcon');
    expect(chevronRightIcon).toBeDefined();
    expect(metricGroupContainer[0]).toHaveStyle([
      {width: '100%', padding: 16, borderRadius: 8},
      {backgroundColor: colors.gray[20]},
    ]);
    fireEvent.press(metricGroupContainer[0]);
    expect(metricPress).toHaveBeenCalled();
  });
});
