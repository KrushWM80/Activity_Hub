import * as React from 'react';
import {
  Animated,
  Easing,
  GestureResponderEvent,
  StyleProp,
  StyleSheet,
  ViewStyle,
} from 'react-native';

import {Icons} from '@walmart/gtp-shared-icons';

import type {CommonPressableProps} from '../../next/types/ComponentTypes';
import {colors} from '../../next/utils/colors';

import {_FilterBase} from './_FilterBase';

// ---------------
// Props
// ---------------
export type FilterTagProps = CommonPressableProps & {
  /**
   * The text label for the filter tag.
   */
  children: string;
  /**
   * If the filter tag is disabled.
   * @default false
   */
  disabled?: boolean;
  /**
   * The function to call when the filter is pressed.
   */
  onPress?: (event: GestureResponderEvent) => void;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with
   * `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Only shown once a filter is being applied.
 * - Use when a filter is applied and a tag is needed to show what has been selected.
 * - Use when interacting with complex data such that a user would often apply multiple filters at
 *   once and require visibility of all applied filter parameters.
 *
 * ## Usage
 * ```js
 * import {FilterTag} from '@walmart/gtp-shared-components/ax`;
 *
 * <FilterTag onPress={() => {}}>Filter Tag</FilterTag>
 * <FilterTag disabled>Filter Tag</FilterTag>
 *
 * ```
 */
const FilterTag: React.FC<FilterTagProps> = (props) => {
  const {
    children,
    disabled = false,
    onPress = undefined, // Default to undefined so animation is not triggered if no onPress is provided
    UNSAFE_style,
    ...rest
  } = props;

  const translateX = React.useRef(new Animated.Value(-100)).current;

  React.useEffect(() => {
    // Slide in animation
    Animated.timing(translateX, {
      toValue: 0,
      duration: 200,
      easing: Easing.bezier(0.77, 0, 0.175, 1), // LD token timingEaseInOut100 from: https://livingdesign.walmart.com/resources/design-tokens/#timing
      useNativeDriver: true,
    }).start();
  }, [translateX]);

  const handlePress = (event: GestureResponderEvent) => {
    // TODO: Unmounting a component happens before the animation completes, revisit later
    // if (onPress) {
    //   // Slide out animation
    //   Animated.timing(translateX, {
    //     toValue: -100,
    //     duration: 200,
    //     easing: Easing.bezier(0.77, 0, 0.175, 1), // LD token timingEaseInOut100 from: https://livingdesign.walmart.com/resources/design-tokens/#timing
    //     useNativeDriver: true,
    //   }).start(() => {
    onPress?.(event);
    //   });
    // }
  };

  // ---------------
  // Rendering
  // ---------------
  const renderTrailing = React.useCallback(() => {
    return <Icons.CloseIcon />;
  }, []);

  return (
    <Animated.View
      style={{
        transform: [{translateX}], // Slide-in from left to right
      }}>
      <_FilterBase
        testID={FilterTag.displayName}
        accessibilityRole="togglebutton"
        accessibilityLabel={`Remove filter: ${children}`}
        disabled={disabled}
        trailing={renderTrailing()}
        onPress={handlePress}
        UNSAFE_style={[ss.container, UNSAFE_style]}
        containerPressedStyle={ss.containerPressed}
        containerDisabledStyle={ss.containerDisabled}
        {...rest}>
        {children}
      </_FilterBase>
    </Animated.View>
  );
};

const ss = StyleSheet.create({
  container: {
    borderWidth: 0,
    borderRadius: 4,
    backgroundColor: colors.blue['5'], // '#F2F8FD',
  },
  containerPressed: {
    borderWidth: 0,
    borderRadius: 4,
    backgroundColor: colors.blue['20'], // '#CCE3F8',
  },
  containerDisabled: {
    borderWidth: 1,
    borderColor: colors.gray['50'], // '#BABBBE',
    backgroundColor: colors.white, // '#FFFFFF',
  },
});

FilterTag.displayName = 'FilterTag';
export {FilterTag};
