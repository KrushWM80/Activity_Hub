import * as React from 'react';
import {
  Animated,
  Easing,
  StyleProp,
  StyleSheet,
  ViewProps,
  ViewStyle,
} from 'react-native';

import SparkLeafLarge from '../../../assets/images/SparkLeafLarge.png';
import SparkLeafSmall from '../../../assets/images/SparkLeafSmall.png';
import {colors} from '../utils';

// ---------------
// Props
// ---------------
export type SpinnerSize = 'small' | 'large';
export type SpinnerColor = 'gray' | 'white';

export type SpinnerProps = ViewProps & {
  /**
   * Color for the foreground of the spinner
   * valid values: <strong>'gray' | 'white'</strong>.
   * @default gray
   */
  color?: SpinnerColor;
  /**
   * The size of the spinner
   * valid values: <strong>'small' | 'large'</strong>.
   * @default large
   */
  size?: SpinnerSize;
  /**
   * If provided, the `style` to provide to the root element.
   * This property is prefixed with `UNSAFE` as its use
   * often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle> | undefined;
  /**
   * @deprecated it has no effect. Use <strong>size="small"</strong> instead.
   */
  small?: boolean;
};

/**
 * Spinners inform users of the processes, including retrieval
 * of data, loading state and saving.
 *
 * Visually expresses an undetermined wait time, or unquantifiable task.
 * The spinner dismisses when the process is completed.
 * Spinners are not interactive.
 *
 * ## Usage
 * ```js
 * import {Spinner} from '@walmart/gtp-shared-components';
 *
 * <Spinner />
 * <Spinner size="small" />
 * <Spinner color="white" />
 * <Spinner color="white" size="small" />
 * ```
 */
const Spinner: React.FC<SpinnerProps> = (props: SpinnerProps) => {
  const {current: animator} = React.useRef<Animated.Value>(
    new Animated.Value(0),
  );
  const {current: fade} = React.useRef<Animated.Value>(new Animated.Value(0));
  const rotation = React.useRef<Animated.CompositeAnimation | undefined>(
    undefined,
  );
  const ANIMATION_DURATION = 1300;

  const {color = 'gray', size = 'large', UNSAFE_style, ...rest} = props;

  const containerStyle =
    size === 'large' ? styles.largeContainer : styles.smallContainer;

  const startRotation = React.useCallback(() => {
    Animated.timing(fade, {
      duration: ANIMATION_DURATION,
      toValue: 1,
      isInteraction: false,
      useNativeDriver: true,
    }).start();

    if (rotation.current) {
      animator.setValue(0);
      Animated.loop(rotation.current).start();
    }
  }, [animator, fade]);

  React.useEffect(() => {
    if (rotation.current === undefined) {
      rotation.current = Animated.timing(animator, {
        toValue: 2,
        duration: ANIMATION_DURATION,
        easing: Easing.linear,
        isInteraction: false,
        useNativeDriver: true,
      });
    }
    startRotation();
  }, [fade, startRotation, animator]);

  /** Default SpinnerColor - `gray` */
  const resolveSpinnerColor = (inputColor: string | undefined) => {
    return inputColor === colors.white || inputColor === 'white'
      ? 'white'
      : 'gray';
  };

  // ---------------
  // Rendering
  // ---------------
  const renderLeaf = (index: number) => {
    const interpolate = animator.interpolate({
      inputRange: [0, 1, 2],
      outputRange: ['0deg', `${60 * index}deg`, '360deg'],
    });

    return (
      <Animated.Image
        key={index.toString()}
        style={[
          styles.leaf,
          {transform: [{rotate: interpolate}]},
          resolveSpinnerColor(color) && {
            tintColor: resolveSpinnerColor(color),
          },
        ]}
        source={size === 'small' ? SparkLeafSmall : SparkLeafLarge}
      />
    );
  };

  return (
    <Animated.View
      collapsable={false}
      testID={Spinner.displayName}
      {...rest}
      style={[containerStyle, UNSAFE_style]}>
      {[...Array(6).keys()].map((i) => renderLeaf(i))}
    </Animated.View>
  );
};

// ---------------
// StyleSheet
// ---------------
const styles = StyleSheet.create({
  largeContainer: {
    height: 48,
    width: 48,
    alignSelf: 'center',
  },
  smallContainer: {
    height: 24,
    width: 24,
    alignSelf: 'center',
  },
  leaf: {
    position: 'absolute',
    tintColor: colors.gray['100'],
  },
});

Spinner.displayName = 'Spinner';
export {Spinner};
