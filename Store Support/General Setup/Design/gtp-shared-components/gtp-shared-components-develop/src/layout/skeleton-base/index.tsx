import * as React from 'react';
import {Animated, ViewProps} from 'react-native';

import {ThemeObject} from '../../theme/theme-provider';

export type SkeletonBaseProps = ViewProps & {
  theme: ThemeObject;
  height: number;
  width?: string | number;
  rounded: boolean;
  animator: Animated.Value;
};

/**
 * @internal
 */
export default class SkeletonBase extends React.Component<SkeletonBaseProps> {
  render() {
    const {height, width, rounded, theme, animator, style, ...rootProps} =
      this.props;
    return (
      <Animated.View
        {...rootProps}
        style={[
          theme.part('item'),
          {height, width},
          rounded && {borderRadius: height / 2},
          style,
          {
            backgroundColor: animator.interpolate({
              inputRange: [0, 1, 2],
              outputRange: [
                theme.part('colorFrom'),
                theme.part('colorTo'),
                theme.part('colorFrom'),
              ],
            }),
          },
        ]}
      />
    );
  }
}
