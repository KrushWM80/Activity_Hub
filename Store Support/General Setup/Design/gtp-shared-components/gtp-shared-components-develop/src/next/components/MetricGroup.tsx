import * as React from 'react';
import {
  Pressable,
  StyleProp,
  StyleSheet,
  View,
  ViewProps,
  ViewStyle,
} from 'react-native';

import {colors} from '../utils';

import {Card} from './Card';
import {
  MetricVariant,
  renderTextLabel,
  renderTimeScope,
  renderTitle,
  renderValueUnit,
} from './Metric';

// ---------------
// Props
// ---------------
export type MetricsData = {
  title?: React.ReactNode;
  timescope?: React.ReactNode;
  textLabel?: React.ReactNode;
  value?: React.ReactNode;
  unit?: React.ReactNode;
  variant?: MetricVariant;
  onPress?: () => void;
  isStatusPressedForTest?: boolean;
};

export type MetricGroupProps = ViewProps & {
  /**
   * The array of MetricsData.
   * Sample data : [
   * {
   *   title: 'Title';
   *   timescope?: '5';
   *   textLabel?: 'TextLabel';
   *   value?:'21';
   *   unit?: '%';
   *   variant?: negativeDown;
   * },
   *  ];
   */
  data: Array<MetricsData>;
  /**
   * Allow title/timeScope for the each metric if it's true else single title and timeScope for all the
   * metrics
   * @default false
   */
  allowIndividualTitles?: boolean;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with
   * `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
  /**
   * This MetricGroup press handler
   * if its undefined, the metricGroup will not be clickable
   * if its defined, the metricGroup will show the right chevron icon
   * @default undefined
   */
  onPress?: () => void;
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
   * To test the pressed colors for the metricGroup
   * @default boolean
   */
  isStatusPressedForTest?: boolean;
};

/**
 * MetricGroup is a group of metrics displayed together.
 *
 * ## Usage
 * ```js
 * import {MetricGroup} from '@walmart/gtp-shared-components`;
 *
 * const threeMetricData = [
 *   {
 *     title: 'Store safety',
 *     timescope: 'YTD.9h ago',
 *     textLabel: 'Accident free days',
 *     value: '21',
 *   },
 *   {
 *     textLabel: 'Customer accidents',
 *     value: '7',
 *   },
 *   {
 *     textLabel: 'Associate accidents',
 *     value: '4',
 *   },
 * ];
 * <MetricGroup data={threeMetricData} />
 * ```
 */
const MetricGroup: React.FC<MetricGroupProps> = (props) => {
  const {
    data,
    allowIndividualTitles = false,
    UNSAFE_style = {},
    onPress,
    showOnPressIndicator = true,
    pressedColor = colors.gray['20'],
    isStatusPressedForTest = false,
  } = props;

  // ---------------
  // Rendering
  // ---------------
  const filterTitleTimeScope = () => {
    return data.filter((metric: MetricsData) => {
      const {title, timescope} = metric;
      return title && timescope;
    });
  };

  const _pressedColor = (pressed: boolean) => {
    return pressed && onPress ? {backgroundColor: pressedColor} : {};
  };

  const _renderSingleTitleMetricGroup = () => {
    const titleData = filterTitleTimeScope();
    return (
      <Card UNSAFE_style={[ss.singleCard, UNSAFE_style]}>
        <Pressable
          style={({pressed}) => {
            return [ss.pressed, _pressedColor(pressed)];
          }}
          onPress={() => onPress?.()}
          testOnly_pressed={isStatusPressedForTest}
          testID={`${MetricGroup.displayName}_Card`}>
          {renderTitle(titleData[0]?.title, onPress, showOnPressIndicator)}
          {renderTimeScope(titleData[0]?.timescope)}
          <View style={ss.rowContainer}>
            {data.map((metric: MetricsData, index) => {
              const {textLabel, unit, value, variant = 'neutral'} = metric;
              return (
                <View
                  key={index}
                  accessible
                  style={ss.valueUnit}
                  testID={`${MetricGroup.displayName}_Values`}>
                  {renderValueUnit(value, unit)}
                  {renderTextLabel(textLabel, variant)}
                </View>
              );
            })}
          </View>
        </Pressable>
      </Card>
    );
  };

  const _renderIndividualMetrics = () => {
    return (
      <View style={ss.rowContainer}>
        {data.map((metric: MetricsData, index) => {
          const {
            textLabel,
            title,
            timescope,
            unit,
            value,
            variant = 'neutral',
            onPress: _onPress,
            isStatusPressedForTest: _isStatusPressedForTest = false,
          } = metric;
          const _individualPressedColor = (pressed: boolean) => {
            return pressed && _onPress ? {backgroundColor: pressedColor} : {};
          };
          return (
            <Card UNSAFE_style={[ss.metricCard, UNSAFE_style]} key={index}>
              <Pressable
                style={({pressed}) => {
                  return [ss.pressed, _individualPressedColor(pressed)];
                }}
                testOnly_pressed={_isStatusPressedForTest}
                onPress={() => _onPress?.()}
                testID={`${MetricGroup.displayName}_Card-${index}`}>
                {renderTitle(title, _onPress, showOnPressIndicator)}
                {renderTimeScope(timescope)}
                {renderValueUnit(value, unit)}
                {renderTextLabel(textLabel, variant)}
              </Pressable>
            </Card>
          );
        })}
      </View>
    );
  };
  return (
    <View testID={MetricGroup.displayName}>
      {allowIndividualTitles
        ? _renderIndividualMetrics()
        : _renderSingleTitleMetricGroup()}
    </View>
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  singleCard: {
    justifyContent: 'flex-start',
    alignItems: 'flex-start',
    margin: 5,
    flex: 0,
  },
  metricCard: {
    justifyContent: 'flex-start',
    alignItems: 'flex-start',
    margin: 5,
  },
  pressed: {
    width: '100%',
    padding: 16,
    borderRadius: 8,
  },
  valueUnit: {
    flex: 1,
    paddingRight: 16,
    marginTop: 8,
  },
  rowContainer: {
    flexDirection: 'row',
  },
});

MetricGroup.displayName = 'MetricGroup';
export {MetricGroup};
