import * as React from 'react';
import {StyleProp, StyleSheet, View, ViewStyle} from 'react-native';

export type TriangleDirection =
  | 'up'
  | 'right'
  | 'down'
  | 'left'
  | 'up-right'
  | 'up-left'
  | 'down-right'
  | 'down-left';

export type TriangleProps = {
  direction?: TriangleDirection;
  width: number;
  height: number;
  color?: string;
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Inspired by https://github.com/Jpoliachik/react-native-triangle
 * @internal
 */
const _Triangle: React.FC<TriangleProps> = (props) => {
  const {
    direction = 'up',
    width,
    height,
    color = 'white',
    UNSAFE_style,
  } = props;

  const _borderStyles = () => {
    if (direction === 'up') {
      return {
        borderTopWidth: 0,
        borderRightWidth: width / 2.0,
        borderBottomWidth: height,
        borderLeftWidth: width / 2.0,
        borderTopColor: 'transparent',
        borderRightColor: 'transparent',
        borderBottomColor: color,
        borderLeftColor: 'transparent',
      };
    } else if (direction === 'right') {
      return {
        borderTopWidth: height / 2.0,
        borderRightWidth: 0,
        borderBottomWidth: height / 2.0,
        borderLeftWidth: width,
        borderTopColor: 'transparent',
        borderRightColor: 'transparent',
        borderBottomColor: 'transparent',
        borderLeftColor: color,
      };
    } else if (direction === 'down') {
      return {
        borderTopWidth: height,
        borderRightWidth: width / 2.0,
        borderBottomWidth: 0,
        borderLeftWidth: width / 2.0,
        borderTopColor: color,
        borderRightColor: 'transparent',
        borderBottomColor: 'transparent',
        borderLeftColor: 'transparent',
      };
    } else if (direction === 'left') {
      return {
        borderTopWidth: height / 2.0,
        borderRightWidth: width,
        borderBottomWidth: height / 2.0,
        borderLeftWidth: 0,
        borderTopColor: 'transparent',
        borderRightColor: color,
        borderBottomColor: 'transparent',
        borderLeftColor: 'transparent',
      };
    } else if (direction === 'up-left') {
      return {
        borderTopWidth: height,
        borderRightWidth: width,
        borderBottomWidth: 0,
        borderLeftWidth: 0,
        borderTopColor: color,
        borderRightColor: 'transparent',
        borderBottomColor: 'transparent',
        borderLeftColor: 'transparent',
      };
    } else if (direction === 'up-right') {
      return {
        borderTopWidth: 0,
        borderRightWidth: width,
        borderBottomWidth: height,
        borderLeftWidth: 0,
        borderTopColor: 'transparent',
        borderRightColor: color,
        borderBottomColor: 'transparent',
        borderLeftColor: 'transparent',
      };
    } else if (direction === 'down-left') {
      return {
        borderTopWidth: height,
        borderRightWidth: 0,
        borderBottomWidth: 0,
        borderLeftWidth: width,
        borderTopColor: 'transparent',
        borderRightColor: 'transparent',
        borderBottomColor: 'transparent',
        borderLeftColor: color,
      };
    } else if (direction === 'down-right') {
      return {
        borderTopWidth: 0,
        borderRightWidth: 0,
        borderBottomWidth: height,
        borderLeftWidth: width,
        borderTopColor: 'transparent',
        borderRightColor: 'transparent',
        borderBottomColor: color,
        borderLeftColor: 'transparent',
      };
    } else {
      return {};
    }
  };

  return (
    <View
      testID={_Triangle.displayName}
      style={[styles.triangle, _borderStyles(), UNSAFE_style]}
    />
  );
};

const styles = StyleSheet.create({
  triangle: {
    width: 0,
    height: 0,
    backgroundColor: 'transparent',
    borderStyle: 'solid',
  },
});

_Triangle.displayName = '_Triangle';

export {_Triangle};
