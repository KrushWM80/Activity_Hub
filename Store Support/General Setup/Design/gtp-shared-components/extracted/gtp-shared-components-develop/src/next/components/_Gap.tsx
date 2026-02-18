import * as React from 'react';
import {Children} from 'react';
import {StyleSheet, View, ViewStyle} from 'react-native';

import flattenChildren from 'react-keyed-flatten-children';

import {Divider} from './Divider';

export type Direction = 'horizontal' | 'vertical';
export type GapProps = {
  gap?: number;
  direction?: Direction;
  style?: ViewStyle;
  showSeparator?: boolean;
  children?: React.ReactNode;
};

/**
 * @internal
 */
const _Gap: React.FC<GapProps> = (props) => {
  const {
    children,
    gap = 16,
    direction = 'horizontal',
    style = {},
    showSeparator = false,
  } = props;
  const kids = flattenChildren(children);

  /**
   * Currently the Divider supports vertical only
   */
  const _showSeparator = (index: number) => {
    if (
      direction === 'vertical' &&
      showSeparator &&
      index !== kids.length - 1
    ) {
      return <Divider />;
    }
    return null;
  };

  return (
    <View
      testID={_Gap.displayName}
      style={[ss(gap, direction).container, style]}>
      {Children.map(kids, (child, index) => {
        return (
          <>
            <View style={ss(gap, direction).child}>
              {child}
              {_showSeparator(index)}
            </View>
          </>
        );
      })}
    </View>
  );
};

const ss = (gap: number, direction: Direction) => {
  let flexDirection;
  let padding;
  if (direction === 'vertical') {
    flexDirection = 'column';
    padding = {paddingHorizontal: gap / -2};
  } else {
    flexDirection = 'row';
    padding = {paddingVertical: gap / -2};
  }

  return StyleSheet.create({
    container: {
      flexDirection,
      ...padding,
    } as ViewStyle,
    child: {
      marginHorizontal: gap / 2,
    },
  });
};

_Gap.displayName = '_Gap';
export {_Gap};
