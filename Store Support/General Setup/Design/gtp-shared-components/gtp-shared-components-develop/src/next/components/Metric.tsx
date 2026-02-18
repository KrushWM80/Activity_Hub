import * as React from 'react';
import {
  Platform,
  Pressable,
  StyleProp,
  StyleSheet,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Metric';
import {Icons} from '@walmart/gtp-shared-icons';

import {CommonViewProps} from '../types/ComponentTypes';
import {colors} from '../utils';

import {Body, BodySize} from './Body';
import {Card} from './Card';
import {Display, DisplaySize} from './Display';
import {Heading} from './Heading';

// ---------------
// Props
// ---------------
export type MetricVariant =
  | 'negativeDown'
  | 'negativeUp'
  | 'neutral'
  | 'positiveDown'
  | 'positiveUp';

export const MetricTextlabelColors = {
  neutral: {
    iconTintColor: token.componentMetricLabelVariantNeutralTextColor,
    labelColor: token.componentMetricLabelVariantNeutralTextColor,
  },
  negativeDown: {
    iconTintColor:
      token.componentMetricTrendIndicatorVariantNegativeDownIconColor,
    labelColor: token.componentMetricLabelVariantNegativeDownTextColor,
  },
  negativeUp: {
    iconTintColor:
      token.componentMetricTrendIndicatorVariantNegativeUpIconColor,
    labelColor: token.componentMetricLabelVariantNegativeUpTextColor,
  },
  positiveDown: {
    iconTintColor:
      token.componentMetricTrendIndicatorVariantPositiveDownIconColor,
    labelColor: token.componentMetricLabelVariantPositiveDownTextColor,
  },
  positiveUp: {
    iconTintColor:
      token.componentMetricTrendIndicatorVariantPositiveUpIconColor,
    labelColor: token.componentMetricLabelVariantPositiveUpTextColor,
  },
};

export type MetricProps = CommonViewProps & {
  /**
   * The text label providing a description of the metric.
   * Typically a string label.
   */
  textLabel?: React.ReactNode;
  /**
   * The timescope for the metric.
   * Typically a string label.
   */
  timescope?: React.ReactNode;
  /**
   * The title for the metric.
   * Typically a string label.
   */
  title: React.ReactNode;
  /**
   * The unit for the metric.
   * Typically a string label.
   */
  unit?: React.ReactNode;
  /**
   * The value for the metric.
   * Typically a string label.
   */
  value: React.ReactNode;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with `UNSAFE`
   * as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
  /**
   * The variant for the metric.
   * Valid values: 'negativeDown' | 'negativeUp' | 'neutral' | 'positiveDown' | 'positiveUp'
   * @default neutral
   */
  variant?: MetricVariant;
  /**
   * It provides the card layout for the metric component.
   * @default false
   */
  withCardLayout?: boolean;
  /**
   * This Metric press handler
   * if its undefined, the metric will not be clickable
   * if its defined, the metric will show the right chevron icon
   * @default undefined
   */
  onPress?: () => void;
  /**
  /**
   * Whether to show the right chevron indicator on the top right of the card
   * when the onPress prop is present.
   * @default true
   */
  showOnPressIndicator?: boolean;
  /**
   * The pressedColor is a color string
   * when the user taps on the metric the color will be applied
   */
  pressedColor?: string;

  /**
   * @internal
   * To test the pressed colors for the metric
   * @default boolean
   */
  isStatusPressedForTest?: boolean;
};

/**
 * The Metric displays the value of a significant data point.
 *
 * Metric emphasizes a single, specific value that informs users of a critical data point. It allows users to identify meaningful changes and act on them.
 *
 * Leverage Metric to show point-in-time data, trends over time, key performance indicators, or progress against a goal.
 *
 * ## Usage
 * ```js
 * import {Metric} from '@walmart/gtp-shared-components`;
 *
 * <Metric
 *   title="Real-Time WOSH and overtime"
 *   textLabel="3 hours more then last month"
 *   timescope="MTD"
 *   value="24"
 *   unit="hours"
 *   variant="neutral"
 *  />
 *
 * <Metric
 *   title="Real-Time WOSH and overtime"
 *   textLabel="3 hours more then last month"
 *   timescope="MTD"
 *   value="24"
 *   unit="hours"
 *   variant="neutral"
 *   withCardLayout={true}
 *  />
 * ```
 */
const Metric: React.FC<MetricProps> = (props) => {
  const {
    withCardLayout = false,
    textLabel,
    title,
    timescope,
    unit,
    value,
    variant = 'neutral',
    onPress,
    showOnPressIndicator = true,
    pressedColor = colors.gray[20],
    isStatusPressedForTest = false,
    UNSAFE_style = {},
    ...rest
  } = props;

  // ---------------
  // Rendering
  // ---------------

  const metricCoreElements = React.useCallback(() => {
    const _pressedColor = (pressed: boolean) => {
      return pressed && onPress ? {backgroundColor: pressedColor} : {};
    };

    return (
      <Pressable
        onPress={onMetricPress}
        testID={`${Metric.displayName}_Card`}
        testOnly_pressed={isStatusPressedForTest}
        style={({pressed}) => {
          return [ss.pressed, _pressedColor(pressed)];
        }}>
        {renderTitle(title, onPress, showOnPressIndicator)}
        {renderTimeScope(timescope)}
        {renderValueUnit(value, unit)}
        {renderTextLabel(textLabel, variant)}
      </Pressable>
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [title, timescope, value, unit, textLabel, variant, onPress]);

  const onMetricPress = () => {
    onPress?.();
  };

  return (
    <View
      testID={Metric.displayName}
      style={[ss.container, !withCardLayout && UNSAFE_style]}
      {...rest}>
      {withCardLayout ? (
        <Card
          testID={Metric.displayName + '-cardLayout'}
          UNSAFE_style={[ss.cardContainer, UNSAFE_style]}>
          {metricCoreElements()}
        </Card>
      ) : (
        metricCoreElements()
      )}
    </View>
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  container: {
    flex: 1,
  },
  cardContainer: {
    justifyContent: 'center',
    alignItems: 'flex-start',
  },
  timeScope: {
    marginBottom: token.componentMetricTimescopeMarginBottom,
    color: token.componentMetricTimescopeTextColor,
  },
  rowContainer: {
    flexDirection: 'row',
  },
  pressed: {
    width: '100%',
    padding: 16,
    borderRadius: 8,
  },
  nonPressed: {
    padding: 16,
    borderRadius: 8,
    width: '100%',
  },
  value: {
    marginRight: token.componentMetricValueMarginEnd,
    alignSelf: token.componentMetricUnitVerticalAlign as Extract<
      // @cory incorrect TS type here,
      ViewStyle,
      'alignSelf'
    >,
  },
  titleContainer: {flexDirection: 'row'},
  title: {flex: 1},
  unit: {
    alignSelf: token.componentMetricUnitVerticalAlign as Extract<
      // @cory incorrect TS type here
      ViewStyle,
      'alignSelf'
    >,
    paddingBottom: Platform.OS === 'android' ? 4 : 0, //adjusting unit alignment for android
  },
});

Metric.displayName = 'Metric';
export {Metric};

export const renderTitle = (
  title: React.ReactNode,
  onPress?: () => void,
  showOnPressIndicator?: boolean,
) => {
  return (
    <View style={ss.titleContainer}>
      <View style={ss.title}>
        {typeof title === 'string' ? (
          <Body
            testID={Metric.displayName + '-title'}
            size={token.componentMetricTitleAliasOptionsSize as BodySize}
            weight={`${token.componentMetricTitleAliasOptionsWeight}`}>
            {title}
          </Body>
        ) : (
          title
        )}
      </View>
      {onPress && showOnPressIndicator && (
        <Icons.ChevronRightIcon size={'small'} />
      )}
    </View>
  );
};

export const renderTimeScope = (timescope: React.ReactNode) => {
  return (
    timescope && (
      <>
        {typeof timescope === 'string' ? (
          <Body
            testID={Metric.displayName + '-timescope'}
            size={token.componentMetricTimescopeAliasOptionsSize as BodySize}
            UNSAFE_style={ss.timeScope}>
            {timescope}
          </Body>
        ) : (
          timescope
        )}
      </>
    )
  );
};

export const renderValueUnit = (
  value: React.ReactNode,
  unit: React.ReactNode,
) => {
  return (
    <View style={ss.rowContainer}>
      {value && typeof value === 'string' ? (
        <Display
          testID={Metric.displayName + '-value'}
          size={token.componentMetricValueAliasOptionsSize as DisplaySize}
          weight={`${token.componentMetricValueAliasOptionsWeight}`}
          UNSAFE_style={ss.value}>
          {value}
        </Display>
      ) : (
        value
      )}
      {unit && typeof unit === 'string' ? (
        <Heading
          testID={Metric.displayName + '-unit'}
          size={token.componentMetricUnitAliasOptionsSize as BodySize}
          weight={`${token.componentMetricUnitAliasOptionsWeight}`}
          UNSAFE_style={ss.unit}>
          {unit}
        </Heading>
      ) : (
        unit
      )}
    </View>
  );
};

const _renderArrowIcon = (
  textLabel: React.ReactNode,
  variant: MetricVariant,
) => {
  if (textLabel && variant !== 'neutral') {
    const arrowStyle = {
      marginTop: token.componentMetricTrendIndicatorMarginTop,
      marginRight: token.componentMetricTrendIndicatorMarginEnd,
    };
    if (variant === 'negativeDown' || variant === 'positiveDown') {
      return (
        <Icons.ArrowDownIcon
          color={MetricTextlabelColors[variant].iconTintColor}
          UNSAFE_style={arrowStyle}
        />
      );
    } else {
      return (
        <Icons.ArrowUpIcon
          color={MetricTextlabelColors[variant].iconTintColor}
          UNSAFE_style={arrowStyle}
        />
      );
    }
  }
  return null;
};
export const renderTextLabel = (
  textLabel: React.ReactNode,
  variant: MetricVariant,
) => {
  return (
    textLabel && (
      <>
        {typeof textLabel === 'string' ? (
          <View style={ss.rowContainer}>
            {_renderArrowIcon(textLabel, variant)}
            <Body
              testID={Metric.displayName + '-text-label'}
              size={token.componentMetricLabelAliasOptionsSize as BodySize}
              weight={`${token.componentMetricUnitAliasOptionsWeight}`}
              UNSAFE_style={{
                color: MetricTextlabelColors[variant].labelColor,
              }}>
              {textLabel}
            </Body>
          </View>
        ) : (
          textLabel
        )}
      </>
    )
  );
};
