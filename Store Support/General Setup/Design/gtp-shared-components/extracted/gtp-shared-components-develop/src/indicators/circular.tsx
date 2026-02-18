import * as React from 'react';
import {StyleSheet, View, ViewProps} from 'react-native';

import {Body} from '../next/components/Body';
import {getThemeFrom, ThemeContext} from '../theme/theme-provider';

import {composed as defaultTheme} from './theme';

export type CircularProgressIndicatorProps = ViewProps & {
  /** Current value, 0-100 */
  value: number;
  /** Additional label to be displayed under the percentage */
  label?: string;
  /** Color for the foreground of the indicator */
  color?: string;
  /** Starting point of the indicator (default `left`) */
  origin?: 'top' | 'right' | 'bottom' | 'left';
  /** Indicator fill direction (default `counterclockwise`) */
  fillDirection?: 'clockwise' | 'counterclockwise';
};

/**
 * @deprecated: CircularProgressIndicator is refactored to current coding standards and moved to the next folder
 */

export default class CircularProgressIndicator extends React.Component<CircularProgressIndicatorProps> {
  static contextTypes = ThemeContext;
  static defaultProps: Partial<CircularProgressIndicatorProps> = {
    origin: 'left',
    fillDirection: 'counterclockwise',
  };

  renderInternals(
    color: any,
    backgroundColor: any,
    styles: any,
    RADIUS: number,
  ): any {
    const {value} = this.props;

    if (value <= 0) {
      return undefined;
    } else if (value >= 100) {
      return <View style={[styles.filled, {backgroundColor: color}]} />;
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
        <View key="firstHalf" style={[styles.ring, halfOneStyle]} />,
        <View key="secondHalf" style={[styles.ring, halfTwoStyle]} />,
      ];
    }
  }

  originRotation = () => {
    const {origin} = this.props;
    if (!origin || origin === 'left') {
      return 0;
    }
    if (origin === 'top') {
      return 90;
    }
    if (origin === 'right') {
      return 180;
    }
    if (origin === 'bottom') {
      return 270;
    }
  };

  render() {
    const {value, label, color, origin, fillDirection, ...rootProps} =
      this.props;

    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'indicator',
      'circular.default',
    );
    const themeStatic = getThemeFrom(
      this.context,
      defaultTheme,
      'indicator',
      'circular.static',
    );
    const baseColor = theme.part('indicator').color;
    const backgroundColor = theme.part('indicator').backgroundColor;

    const RADIUS = themeStatic.part('radius');
    const DIAMETER = RADIUS * 2;
    const RING_WIDTH = themeStatic.part('ringWidth');

    const styles = StyleSheet.create({
      container: {
        borderRadius: RADIUS,
        height: DIAMETER,
        width: DIAMETER,
      },
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
          {rotate: `${this.originRotation()}deg`},
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
        borderRadius: RADIUS - RING_WIDTH,
        height: DIAMETER - RING_WIDTH * 2,
        width: DIAMETER - RING_WIDTH * 2,
        margin: RING_WIDTH,
      },
    });

    return (
      <View {...rootProps} style={[theme.part('container'), styles.container]}>
        <View style={[{backgroundColor: backgroundColor}, styles.indicator]}>
          {this.renderInternals(
            color ?? baseColor,
            backgroundColor,
            styles,
            RADIUS,
          )}
          <View style={[theme.part('innerCircle'), styles.innerCircle]} />
        </View>
        <Body UNSAFE_style={theme.part('text')}>{`${value}%`}</Body>
        {label ? <Body UNSAFE_style={theme.part('label')}>{label}</Body> : null}
      </View>
    );
  }
}
