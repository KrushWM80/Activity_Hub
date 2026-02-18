import * as React from 'react';
import {StyleProp, StyleSheet, TextStyle, View, ViewStyle} from 'react-native';

import {getFont} from '../../theme/font';
import type {CommonViewProps} from '../types/ComponentTypes';
import {
  a11yRole,
  colors,
  DIAMETER,
  RADIUS,
  RING_WIDTH,
  ROTATE_ANGLES,
} from '../utils';

import {Body} from './Body';
// ---------------
// Props
// ---------------
export type CircularProgressIndicatorOrigin =
  | 'top'
  | 'bottom'
  | 'left'
  | 'right';
export type CircularProgressIndicatorDirection =
  | 'clockwise'
  | 'counterclockwise';
export type CircularProgressIndicatorProps = CommonViewProps & {
  /**
   * The value for the indicator.
   * @default 0
   */
  value: number;
  /**
   * The label for the CircularProgressIndicator.
   */
  label?: string;
  /**
   * Color for the foreground of the CircularProgressIndicator.
   * @default #909196 or gray['80']
   */
  color?: string;
  /**
   * Starting point of the CircularProgressIndicator.
   * Valid values are 'top', 'bottom', 'left', and 'right'.
   * @default 'left'
   */
  origin?: CircularProgressIndicatorOrigin;
  /**
   * Indicator fill direction CircularProgressIndicator.
   * valid values are clockwise and counterclockwise.
   * @default 'counterclockwise'
   */
  fillDirection?: CircularProgressIndicatorDirection;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with
   * `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * CircularProgressIndicator display a visual representation of the completion of a task or process.
 *
 * ## Usage
 * ```js
 * import {CircularProgressIndicator} from '@walmart/gtp-shared-components`;
 *
 * <CircularProgressIndicator value={60} />;
 * ```
 */
const CircularProgressIndicator: React.FC<CircularProgressIndicatorProps> = (
  props,
) => {
  const {
    value,
    label,
    origin = 'left',
    fillDirection = 'counterclockwise',
    color = colors.gray['80'],
    UNSAFE_style,
    ...rest
  } = props;

  //Their is no LD Tokens for the CircularProgressIndicator so we use the default
  const backgroundColor = colors.gray['20'];
  const _ss = ss(origin, fillDirection);

  const renderInternals = () => {
    if (value <= 0) {
      return undefined;
    } else if (value >= 100) {
      return <View style={[_ss.filled, {backgroundColor: color}]} />;
    } else {
      const halfOneStyle = {
        transform: [
          {translateX: RADIUS / 2},
          {rotate: '270deg'},
          {translateX: -RADIUS / 2},
        ],
        backgroundColor: color,
      };
      const rotateDegrees =
        value > 50 ? 270 - 3.6 * (value - 50) : 270 - 3.6 * value;
      const halfTwoStyle = {
        backgroundColor: value > 50 ? color : backgroundColor,
        transform: [
          {translateX: RADIUS / 2},
          {rotate: `${rotateDegrees}deg`},
          {translateX: -RADIUS / 2},
        ],
      };

      return [
        <View key="firstHalf" style={[_ss.ring, halfOneStyle]} />,
        <View key="secondHalf" style={[_ss.ring, halfTwoStyle]} />,
      ];
    }
  };

  // ---------------
  // Rendering
  // ---------------

  return (
    <View
      accessibilityRole={a11yRole('progressbar')}
      testID={CircularProgressIndicator.displayName}
      style={[_ss.container, UNSAFE_style]}
      {...rest}>
      <View style={[{backgroundColor: backgroundColor}, _ss.indicator]}>
        {renderInternals()}
        <View style={_ss.innerCircle} />
      </View>
      <Body
        UNSAFE_style={_ss.text}
        testID={`${CircularProgressIndicator.displayName}-value`}>{`${value}%`}</Body>
      {label ? (
        <Body
          UNSAFE_style={_ss.label}
          testID={`${CircularProgressIndicator.displayName}-label`}>
          {label}
        </Body>
      ) : null}
    </View>
  );
};

// ---------------
// Styles
// ---------------

/**
 * The function `originRotation` returns the rotation angle based on the provided origin value.
 * @param {CircularProgressIndicatorOrigin} [origin=left] - The `origin` parameter is a string
 * @returns the rotation value based on the provided origin. If the origin is 'top'= 90,'right' = 180,'bottom' = 270,'left' = 0.
 */
const originRotation = (origin: CircularProgressIndicatorOrigin = 'left') => {
  switch (origin) {
    case 'right':
      return ROTATE_ANGLES.RIGHT;
    case 'top':
      return ROTATE_ANGLES.TOP;
    case 'bottom':
      return ROTATE_ANGLES.BOTTOM;
    default:
      return ROTATE_ANGLES.LEFT;
  }
};

const ss = (
  origin: CircularProgressIndicatorOrigin = 'left',
  fillDirection: CircularProgressIndicatorDirection = 'counterclockwise',
) =>
  StyleSheet.create({
    container: {
      alignItems: 'center',
      justifyContent: 'center',
      position: 'relative',
      overflow: 'hidden',
      borderRadius: RADIUS,
      height: DIAMETER,
      width: DIAMETER,
    },
    text: {
      ...getFont('bold'),
      fontSize: 18,
      lineHeight: 24,
      position: 'relative',
      textAlign: 'center',
      zIndex: 2,
    } as TextStyle,
    indicator: {
      borderRadius: RADIUS,
      height: DIAMETER,
      width: DIAMETER,
      position: 'absolute',
      top: 0,
      left: 0,
      overflow: 'hidden',
      zIndex: 1,
      transform: [
        {rotate: `${originRotation(origin)}deg`},
        {scaleY: fillDirection === 'clockwise' ? -1 : 1},
      ],
    },
    ring: {
      width: RADIUS,
      height: DIAMETER,
      borderRadius: RADIUS,
      position: 'absolute',
      borderTopRightRadius: 0,
      borderBottomRightRadius: 0,
    },
    filled: {
      width: DIAMETER,
      height: DIAMETER,
      borderRadius: RADIUS,
      position: 'absolute',
    },
    innerCircle: {
      backgroundColor: colors.white,
      borderRadius: RADIUS - RING_WIDTH,
      height: DIAMETER - RING_WIDTH * 2,
      width: DIAMETER - RING_WIDTH * 2,
      margin: RING_WIDTH,
    },
    label: {
      ...getFont(),
      fontSize: 12,
      lineHeight: 16,
      textAlign: 'center',
      zIndex: 2,
    } as TextStyle,
  });

CircularProgressIndicator.displayName = 'CircularProgressIndicator';
export {CircularProgressIndicator};
