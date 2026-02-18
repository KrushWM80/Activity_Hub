import * as React from 'react';
import {Animated, View, ViewProps} from 'react-native';

import {getThemeFrom, ThemeContext} from '../theme/theme-provider';

import SkeletonBase from './skeleton-base';
import {composed as defaultTheme} from './theme';

export type SkeletonProps = ViewProps &
  (
    | {
        /** Height of the skeleton */
        height?: number;
        /** Width of the skeleton */
        width?: number | string;
        /** Whether to use the rounded variant */
        rounded?: boolean;
        /** Value animator.  If not supplied, a default value animator will be used. */
        animator?: Animated.Value | SkeletonAnimator;
        /** Number of lines in the skeleton */
        lines?: never;
      }
    | {
        height?: never;
        width?: never;
        rounded?: never;
        animator?: Animated.Value | SkeletonAnimator;
        lines: number;
      }
  );

type State = {
  animator: Animated.Value;
};

type SkeletonAnimator = {
  animator: Animated.Value;
  animation: Animated.CompositeAnimation;
};

/**
 * @deprecated use <strong><Skeleton ... /></strong> instead
 */
export default class Skeleton extends React.Component<SkeletonProps, State> {
  static contextTypes = ThemeContext;

  static createAnimator = () => {
    const animator = new Animated.Value(0);
    const animation = Animated.loop(
      Animated.timing(animator, {
        toValue: 2,
        duration: 1500,
        useNativeDriver: false,
      }),
    );
    animation.start();
    return {animator, animation} as SkeletonAnimator;
  };

  constructor(props: SkeletonProps) {
    super(props);
    if (props.animator && 'animator' in props.animator) {
      this.state = {
        animator: props.animator.animator,
      };
    } else {
      this.state = {
        animator: props.animator ?? Skeleton.createAnimator().animator,
      };
    }
  }

  render() {
    const {height, width, lines, rounded, style, ...rootProps} = this.props;
    const {animator} = this.state;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'layout',
      'skeleton',
      lines ? 'lines' : 'default',
    );
    return (
      <View {...rootProps} style={theme.part('container')}>
        {Array.from(new Array(Math.max(lines ?? 1, 1))).map((val, i) => (
          <SkeletonBase
            key={`Skeleton_${i}`}
            animator={animator}
            rounded={!!rounded}
            theme={theme}
            height={height ?? theme.part('height')}
            width={width ?? theme.part('width')}
          />
        ))}
      </View>
    );
  }
}
