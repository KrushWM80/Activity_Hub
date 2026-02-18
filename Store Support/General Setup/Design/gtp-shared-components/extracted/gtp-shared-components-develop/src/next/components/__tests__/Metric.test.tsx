import * as React from 'react';
import {View} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Metric';
import * as texttoken from '@livingdesign/tokens/dist/react-native/light/regular/components/Text';
import {fireEvent, render, screen} from '@testing-library/react-native';

import {colors} from '../../utils';
import {Caption} from '../Caption';
import {Heading} from '../Heading';
import {Metric, MetricTextlabelColors, MetricVariant} from '../Metric';

const metricPress = jest.fn();

describe.each<MetricVariant>([
  'neutral',
  'positiveUp',
  'positiveDown',
  'negativeUp',
  'negativeDown',
])('Should render Metric correctly for Variants', (variant) => {
  test(`Test Metric variant="${variant} `, async () => {
    const wrapper = render(
      <Metric
        title={'Title'}
        value={'$43'}
        unit={'M'}
        timescope={'Today'}
        textLabel={'3 hours more then last month'}
        variant={variant}
      />,
    );
    const metricContainer = await wrapper.findByTestId('Metric');
    expect(metricContainer).toHaveStyle([
      {
        flex: 1,
      },
    ]);

    const metricTitle = await wrapper.findByTestId('Metric-title');
    expect(metricTitle).toHaveStyle([
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

    const metricTimescope = await wrapper.findByTestId('Metric-timescope');
    expect(metricTimescope).toHaveStyle([
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

    const metricValue = await wrapper.findByTestId('Metric-value');
    expect(metricValue).toHaveStyle([
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

    const metricUnit = await wrapper.findByTestId('Metric-unit');
    expect(metricUnit).toHaveStyle([
      {
        fontSize:
          token.componentMetricUnitAliasOptionsSize === 'small'
            ? texttoken.componentTextHeadingSizeSmallFontSizeBS
            : token.componentMetricUnitAliasOptionsSize === 'medium'
            ? texttoken.componentTextHeadingSizeMediumFontSizeBS
            : texttoken.componentTextHeadingSizeLargeFontSizeBS,
        fontWeight: `${token.componentMetricUnitAliasOptionsWeight}`,
        alignSelf: token.componentMetricUnitVerticalAlign,
      },
    ]);

    const metricTextLabel = await wrapper.findByTestId('Metric-text-label');
    expect(metricTextLabel).toHaveStyle([
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
      const arrowDownIcon = await wrapper.findByTestId('ArrowDownIcon');
      expect(arrowDownIcon).toHaveStyle([
        {
          tintColor: MetricTextlabelColors[variant].iconTintColor,
          marginTop: token.componentMetricTrendIndicatorMarginTop,
          marginRight: token.componentMetricTrendIndicatorMarginEnd,
        },
      ]);
    } else if (variant !== 'neutral') {
      const arrowUpIcon = await wrapper.findByTestId('ArrowUpIcon');
      expect(arrowUpIcon).toHaveStyle([
        {
          tintColor: MetricTextlabelColors[variant].iconTintColor,
          marginTop: token.componentMetricTrendIndicatorMarginTop,
          marginRight: token.componentMetricTrendIndicatorMarginEnd,
        },
      ]);
    }
  });
  test(`Test Metric variant="${variant} without optional props`, async () => {
    const wrapper = render(
      <Metric title={'Title'} value={'$43'} variant={variant} />,
    );
    const metricContainer = wrapper.queryAllByTestId('Metric');
    expect(metricContainer.length).toEqual(1);

    const metricTitle = wrapper.queryAllByTestId('Metric-title');
    expect(metricTitle.length).toEqual(1);

    const metricTimescope = wrapper.queryAllByTestId('Metric-timescope');
    expect(metricTimescope.length).toEqual(0);

    const metricValue = wrapper.queryAllByTestId('Metric-value');
    expect(metricValue.length).toEqual(1);

    const metricUnit = wrapper.queryAllByTestId('Metric-unit');
    expect(metricUnit.length).toEqual(0);

    const metricTextLabel = wrapper.queryAllByTestId('Metric-text-label');
    expect(metricTextLabel.length).toEqual(0);

    if (variant === 'negativeDown' || variant === 'positiveDown') {
      const arrowDownIcon = wrapper.queryAllByTestId('ArrowDownIcon');
      expect(arrowDownIcon.length).toEqual(0);
    } else if (variant !== 'neutral') {
      const arrowUpIcon = wrapper.queryAllByTestId('ArrowUpIcon');
      expect(arrowUpIcon.length).toEqual(0);
    }
  });

  test(`Test Metric variant="${variant} with withCardLayout and UNSAFE_style={{}}`, async () => {
    render(
      <Metric
        title={'Title'}
        value={'$43'}
        variant={variant}
        withCardLayout={true}
      />,
    );
    const metricCardContainer = screen.getByTestId('Card');
    expect(metricCardContainer).toBeDefined();
    expect(metricCardContainer).toHaveStyle({
      flex: 1,
      justifyContent: 'center',
      alignItems: 'flex-start',
      backgroundColor: '#fff',
      borderRadius: 8,
      shadowColor: '#000',
      shadowOpacity: 0.15,
      shadowRadius: 2,
      shadowOffset: {height: 1, width: 0},
    });
  });
});

describe('Test Metric with OnPress', () => {
  test(`render rightChervon  `, async () => {
    const wrapper = render(
      <Metric
        title={'Title'}
        value={'$43'}
        unit={'M'}
        timescope={'Today'}
        textLabel={'3 hours more then last month'}
        variant={'neutral'}
        onPress={metricPress}
      />,
    );
    const metricContainer = await wrapper.findByTestId('Metric_Card');
    const chevronRightIcon = await wrapper.findByTestId('ChevronRightIcon');
    expect(chevronRightIcon).toBeDefined();
    fireEvent.press(metricContainer);
    expect(metricPress).toHaveBeenCalled();
  });
  test(`should not render rightChervon with OnPress`, async () => {
    const wrapper = render(
      <Metric
        title={'Title'}
        value={'$43'}
        unit={'M'}
        timescope={'Today'}
        textLabel={'3 hours more then last month'}
        variant={'neutral'}
        onPress={metricPress}
        showOnPressIndicator={false}
      />,
    );
    const metricContainer = await wrapper.findByTestId('Metric_Card');
    const chevronRightIcon = await wrapper.queryAllByTestId('ChevronRightIcon');
    expect(chevronRightIcon.length).toEqual(0);
    fireEvent.press(metricContainer);
    expect(metricPress).toHaveBeenCalled();
  });
  test(`should not render rightChervon  `, async () => {
    const wrapper = render(
      <Metric
        title={'Title'}
        value={'$43'}
        unit={'M'}
        timescope={'Today'}
        textLabel={'3 hours more then last month'}
        variant={'neutral'}
      />,
    );
    const metricContainer = await wrapper.findByTestId('Metric_Card');
    const chevronRightIcon = await wrapper.queryAllByTestId('ChevronRightIcon');
    expect(chevronRightIcon.length).toEqual(0);
    fireEvent.press(metricContainer);
    expect(metricPress).toHaveBeenCalled();
  });
  test(`test the default pressed color  `, async () => {
    const wrapper = render(
      <Metric
        title={'Title'}
        value={'$43'}
        unit={'M'}
        timescope={'Today'}
        isStatusPressedForTest={true}
        textLabel={'3 hours more then last month'}
        variant={'neutral'}
        onPress={metricPress}
      />,
    );
    const metricContainer = await wrapper.findByTestId('Metric_Card');
    const chevronRightIcon = await wrapper.findByTestId('ChevronRightIcon');
    expect(metricContainer).toHaveStyle([
      {width: '100%', padding: 16, borderRadius: 8},
      {backgroundColor: colors.gray[20]},
    ]);
    expect(chevronRightIcon).toBeDefined();
  });
  test(`test the custom pressed color`, async () => {
    const wrapper = render(
      <Metric
        title={'Title'}
        value={'$43'}
        unit={'M'}
        onPress={metricPress}
        isStatusPressedForTest={true}
        pressedColor="#ff00cc"
        timescope={'Today'}
        textLabel={'3 hours more then last month'}
        variant={'neutral'}
      />,
    );
    const metricContainer = await wrapper.findByTestId('Metric_Card');
    expect(metricContainer).toHaveStyle([
      {width: '100%', padding: 16, borderRadius: 8},
      {backgroundColor: '#ff00cc'},
    ]);
  });
});

describe.each<MetricVariant>([
  'neutral',
  'positiveUp',
  'positiveDown',
  'negativeUp',
  'negativeDown',
])('Should render Metric correctly for Variants', (variant) => {
  test(`Test Metric variant="${variant} CustomNode `, async () => {
    const wrapper = render(
      <Metric
        title={'Title'}
        value={
          <View accessible>
            <Heading size={'large'} weight={'Bold'}>
              {'$43'}
            </Heading>
          </View>
        }
        unit={
          <View accessibilityLabel={'M'} accessible>
            <Caption>{'M'}</Caption>
          </View>
        }
        timescope={
          <View accessibilityLabel={'Today'} accessible>
            <Caption>{'Today'}</Caption>
          </View>
        }
        textLabel={
          <View accessible>
            <Heading size={'large'} weight={'Bold'}>
              {'3 hours more then last month'}
            </Heading>
          </View>
        }
        variant={variant}
      />,
    );
    const metricContainer = await wrapper.findByTestId('Metric');
    expect(metricContainer).toHaveStyle([
      {
        flex: 1,
      },
    ]);

    const metricTitle = await wrapper.findByTestId('Metric-title');
    expect(metricTitle).toHaveStyle([
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
});
