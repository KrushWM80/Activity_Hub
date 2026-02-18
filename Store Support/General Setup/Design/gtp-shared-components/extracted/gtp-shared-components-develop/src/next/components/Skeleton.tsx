import * as React from 'react';
import {
  Animated,
  StyleProp,
  StyleSheet,
  ViewProps,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Skeleton';

import {
  SharedAnimator,
  useSharedLoopAnimator,
} from '../utils/useSharedLoopAnimator';

// ---------------
// Props
// ---------------
export type SkeletonVariant = 'rectangle' | 'rounded';

// TODO: Needed for deprecated prop, remove with that prop
type SkeletonAnimator = {
  animator: Animated.Value;
  animation: Animated.CompositeAnimation;
};

export type SkeletonProps = ViewProps & {
  /**
   * The variant for the skeleton.
   * Valid values: "rectangle" | "rounded"
   * @default "rectangle"
   */
  variant?: SkeletonVariant;
  /**
   * The width for the skeleton.
   * @default "100%"
   */
  width?: number | string;
  /**
   * The height for the skeleton.
   * @default 16
   */
  height?: number | string;
  /**
   * @deprecated skeleton animations are now automatically synchronized
   *
   * It has no effect
   */
  animator?: SkeletonAnimator;
  /**
   * @deprecated use <strong>variant</strong> instead
   *
   * It has no effect
   */
  rounded?: boolean;
  /**
   * @deprecated use <strong>SkeletonText</strong> instead
   *
   * It has no effect
   */
  lines?: number;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * A skeleton is a low-fidelity shape that approximates a user interface element and indicates loading of content.
 * A group of skeletons roughly matching a loaded screen can improve perceived responsiveness when loading data is slow.
 *
 * ## Usage
 * ```js
 * import {Skeleton} from '@walmart/gtp-shared-components`;
 *
 * <Skeleton />
 * <Skeleton variant="rounded" />
 * <Skeleton height={50} width={50} />
 * <Skeleton height={50} width={50} variant="rounded" />
 * <Skeleton height={50} width={100} />
 * <Skeleton height={50} width={100} variant="rounded" />
 * ```
 */
const Skeleton: React.FC<SkeletonProps> = (props) => {
  const {
    variant = 'rectangle',
    width = token.componentSkeletonContainerWidth, // 100%
    height = token.componentSkeletonContainerHeight, // 16
    UNSAFE_style,
    ...rest
  } = props;

  const ANIMATION_DURATION = 1500; // token.componentSkeletonContainerAnimationDuration (0.75s) * 2
  const sharedAnimator: SharedAnimator =
    useSharedLoopAnimator(ANIMATION_DURATION);

  const borderRadiusStyle =
    variant === 'rounded'
      ? token.componentSkeletonContainerVariantRoundedBorderRadius // 1000
      : token.componentSkeletonContainerVariantRectangleBorderRadius; // 4

  const interpolate = React.useCallback(() => {
    // Extracted from token.componentSkeletonContainerAnimationDirection: alternate
    // and token.componentSkeletonContainerAnimationTiming: linear
    return sharedAnimator.value.interpolate({
      inputRange: [0, 1, 2],
      outputRange: [
        token.componentSkeletonContainerAnimationKeyframesFromBackgroundColor, // "#f8f8f8"
        token.componentSkeletonContainerAnimationKeyframesToBackgroundColor, // "#e3e4e5"
        token.componentSkeletonContainerAnimationKeyframesFromBackgroundColor, // "#f8f8f8"
      ],
    });
  }, [sharedAnimator.value]);

  const resolveStyle = React.useCallback(() => {
    return {
      height,
      width,
      borderRadius: borderRadiusStyle,
      backgroundColor: interpolate(),
    } as unknown as StyleProp<ViewStyle>;
  }, [height, width, borderRadiusStyle, interpolate]);

  // ---------------
  // Rendering
  // ---------------
  return (
    <Animated.View
      testID={Skeleton.displayName}
      style={[ss.container, UNSAFE_style, resolveStyle()]}
      {...rest}
    />
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  container: {
    backgroundColor: token.componentSkeletonContainerBackgroundColor, // "#f8f8f8"
  },
});

Skeleton.displayName = 'Skeleton';
export {Skeleton};
