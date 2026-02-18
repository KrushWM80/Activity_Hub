import * as React from 'react';
import {
  FlexStyle,
  StyleProp,
  StyleSheet,
  Text,
  TextStyle,
  View,
  ViewProps,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/ProgressIndicator';

import {getFont} from '../../theme/font';
import {a11yRole} from '../utils';

// ---------------
// Props
// ---------------
export type ProgressIndicatorVariant = 'error' | 'info' | 'success' | 'warning';
export type ProgressIndicatorProps = ViewProps & {
  /**
   * The label for the progress indicator.
   * It is marked as optional to support a plain Progress indicator
   */
  label?: React.ReactNode;
  /**
   * The min number for the indicator.
   * @default 0
   */
  min?: number;
  /**
   * The max number for the indicator.
   * @default 100
   */
  max?: number;
  /**
   * The value for the indicator.
   * The value should not exceed max (default 100).
   * (value <= max),
   * @default 0
   */
  value?: number;
  /**
   * The value label for the indicator.
   * It is marked as optional to support a plain Progress indicator
   */
  valueLabel?: React.ReactNode;
  /**
   * The variant for the indicator.
   * Valid values: "error" | "info" | "success" | "warning"
   * @default info
   */
  variant?: ProgressIndicatorVariant;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Progress Indicators display a visual representation of the completion of a task or process.
 *
 * ## Usage
 * ```js
 * import {ProgressIndicator} from '@walmart/gtp-shared-components`;
 *
 * <ProgressIndicator
 *   label={'Account setup is complete'}
 *   value={50}
 *   valueLabel="5 0f 10"
 * />
 * ```
 */
const ProgressIndicator: React.FC<ProgressIndicatorProps> = (props) => {
  const {
    label,
    min = 0,
    max = 100,
    value = 0,
    valueLabel,
    variant = 'info',
    UNSAFE_style,
    ...rest
  } = props;

  const resolveBackgroundColor = (v: ProgressIndicatorVariant) => {
    switch (v) {
      case 'error':
        return token.componentProgressIndicatorIndicatorVariantErrorBackgroundColor;
      case 'info':
        return token.componentProgressIndicatorIndicatorVariantInfoBackgroundColor;
      case 'success':
        return token.componentProgressIndicatorIndicatorVariantSuccessBackgroundColor;
      case 'warning':
        return token.componentProgressIndicatorIndicatorVariantWarningBackgroundColor;
      default:
        return token.componentProgressIndicatorIndicatorVariantErrorBackgroundColor;
    }
  };

  const getProgressIndicatorWidth = React.useMemo(() => {
    return value > max
      ? ((max - min) / Number(max - min)) * 100
      : ((value - min) / Number(max - min)) * 100;
  }, [value, min, max]);

  const hasLabel = React.useMemo(() => {
    return label || valueLabel;
  }, [label, valueLabel]);

  // ---------------
  // Rendering
  // ---------------
  return (
    <View
      accessibilityRole={a11yRole('progressbar')}
      testID={ProgressIndicator.displayName}
      style={[ss.container, UNSAFE_style]}
      {...rest}>
      <View
        testID={`${ProgressIndicator.displayName}-trackContainer`}
        style={ss.trackContainer}>
        <View
          testID={`${ProgressIndicator.displayName}-track`}
          style={[
            ss.track,
            {width: `${getProgressIndicatorWidth}%`},
            {backgroundColor: resolveBackgroundColor(variant)},
          ]}
        />
      </View>
      {hasLabel && (
        <View
          testID={`${ProgressIndicator.displayName}-labelContainer`}
          style={ss.labelContainer}>
          {label && (
            <Text
              accessibilityRole={a11yRole('text')}
              style={ss.label}
              testID={`${ProgressIndicator.displayName}_label`}>
              {label}
            </Text>
          )}
          {valueLabel && (
            <Text
              accessibilityRole={a11yRole('text')}
              style={ss.valueLabel}
              testID={`${ProgressIndicator.displayName}_valueLabel`}>
              {valueLabel}
            </Text>
          )}
        </View>
      )}
    </View>
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  container: {
    width: '100%',
    justifyContent: 'flex-start',
    alignItems: 'center',
    borderRadius: token.componentProgressIndicatorIndicatorBorderRadius,
  },
  trackContainer: {
    width: '100%',
    backgroundColor: token.componentProgressIndicatorTrackBackgroundColor,
    borderRadius: token.componentProgressIndicatorTrackBorderRadius,
  },
  track: {
    borderRadius: token.componentProgressIndicatorTrackBorderRadius,
    height: token.componentProgressIndicatorTrackHeight,
    alignSelf: 'flex-start',
  },
  labelContainer: {
    width: '100%',
    flexDirection: 'row',
    marginTop: token.componentProgressIndicatorLabelContainerMarginTop,
    justifyContent:
      token.componentProgressIndicatorLabelContainerAlignHorizontal as Extract<
        FlexStyle,
        'justifyContent'
      >,
    alignItems: 'center',
  },
  label: {
    ...getFont(),
    fontSize: token.componentProgressIndicatorTextLabelFontSize,
    color: token.componentProgressIndicatorTextLabelTextColor,
    maxWidth: '90%',
    flex: 1,
    flexWrap: 'wrap',
    alignSelf: 'flex-start',
  } as TextStyle,
  valueLabel: {
    ...getFont(),
    fontSize: token.componentProgressIndicatorHelperTextFontSize,
    marginLeft: token.componentProgressIndicatorHelperTextMarginStart,
    marginTop: token.componentProgressIndicatorHelperTextMarginTop,
    color: token.componentProgressIndicatorHelperTextTextColor,
    maxWidth: '90%',
    alignSelf: 'flex-start',
    flexWrap: 'wrap',
  } as TextStyle,
});

ProgressIndicator.displayName = 'ProgressIndicator';
export {ProgressIndicator};
