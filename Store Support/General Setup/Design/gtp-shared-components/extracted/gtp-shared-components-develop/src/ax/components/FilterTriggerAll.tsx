import * as React from 'react';
import {
  Animated,
  Easing,
  GestureResponderEvent,
  StyleProp,
  StyleSheet,
  Text,
  TextStyle,
  ViewStyle,
} from 'react-native';

import {Icons} from '@walmart/gtp-shared-icons';

import type {CommonPressableProps} from '../../next/types/ComponentTypes';
import {colors} from '../../next/utils/colors';
import {getFont} from '../../theme/font';

import {_FilterBase} from './_FilterBase';

// ---------------
// Props
// ---------------
export type FilterTriggerAllProps = CommonPressableProps & {
  /**
   * The text content for the filter.
   */
  children?: string;
  /**
   * If the filter settings trigger is disabled.
   * @default false
   */
  disabled?: boolean;
  /**
   * The function to call when the filter is pressed.
   */
  onPress?: (event: GestureResponderEvent) => void;
  /**
   * The applied count for the filter settings trigger.
   */
  appliedCount?: React.ReactNode;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with
   * `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Show/hide a full/large list of available filters.
 * - Use when reducing large data sets with 3+ filtering methods into subsets of data.
 * - Don't use when there's less than 3 filtering methods and can be quickly filtered
 *   by a Filter Toggle or Filter Trigger Single.
 *
 * ## Usage
 * ```js
 * import {FilterTriggerAll} from '@walmart/gtp-shared-components/ax`;
 *
 * <FilterTriggerAll>
 * <FilterTriggerAll>Filters</FilterTriggerAll>
 * <FilterTriggerAll appliedCount={0}/>
 * <FilterTriggerAll appliedCount={1}/>
 * <FilterTriggerAll appliedCount={1}>Filters</FilterTriggerAll>
 * ```
 */
const FilterTriggerAll: React.FC<FilterTriggerAllProps> = (props) => {
  const {
    children,
    disabled = false,
    onPress,
    appliedCount,
    UNSAFE_style,
    ...rest
  } = props;

  const [showIndicator, setShowIndicator] = React.useState(false);
  const fadeAnim = React.useRef(new Animated.Value(0)).current;

  const hasAppliedCount =
    typeof appliedCount !== 'boolean' &&
    appliedCount !== null &&
    typeof appliedCount !== 'undefined' &&
    fadeAnim !== null;

  const ss = styles(disabled);

  React.useEffect(() => {
    if (hasAppliedCount) {
      setShowIndicator(true);
      Animated.timing(fadeAnim, {
        toValue: 1, // Target opacity value
        easing: Easing.bezier(0.77, 0, 0.175, 1), // LD token timingEaseInOut100 from: https://livingdesign.walmart.com/resources/design-tokens/#timing
        duration: 200, // Animation duration in milliseconds
        useNativeDriver: true, // Enable native driver for better performance
      }).start();
    } else {
      Animated.timing(fadeAnim, {
        toValue: 0, // Target opacity value
        easing: Easing.bezier(0.77, 0, 0.175, 1), // LD token timingEaseInOut100 from: https://livingdesign.walmart.com/resources/design-tokens/#timing
        duration: 200, // Animation duration in milliseconds
        useNativeDriver: true, // Enable native driver for better performance
      }).start(() => {
        setShowIndicator(false);
      });
    }
  }, [fadeAnim, hasAppliedCount]);

  // ---------------
  // Rendering
  // ---------------
  const renderLeading = () => {
    return (
      <Icons.SlidersIcon
        testID={FilterTriggerAll.displayName + '-slidersIcon'}
        UNSAFE_style={[
          children ? ss.leadingStyle : undefined,
          disabled ? ss.disabledIcon : undefined,
        ]}
      />
    );
  };

  const renderIndicator = () => {
    if (showIndicator) {
      return (
        <Animated.View
          testID={FilterTriggerAll.displayName + '-appliedCount'}
          style={[
            ss.appliedCountContainer,
            ss.trailingStyle,
            {opacity: fadeAnim},
          ]}>
          <Text style={ss.appliedCountText}>{appliedCount}</Text>
        </Animated.View>
      );
    }
  };

  const accessibilityLabel = `${children ?? 'Filters'}, ${
    hasAppliedCount ? appliedCount : 'none'
  } applied, activate to change filter settings`;

  return (
    <_FilterBase
      testID={FilterTriggerAll.displayName}
      accessibilityRole="button"
      accessibilityState={{disabled}}
      accessibilityLabel={accessibilityLabel}
      leading={renderLeading()}
      trailing={renderIndicator()}
      applied={hasAppliedCount}
      disabled={disabled}
      onPress={onPress}
      UNSAFE_style={UNSAFE_style}
      {...rest}>
      {children}
    </_FilterBase>
  );
};

// ---------------
// Styles
// ---------------
const styles = (disabled: boolean) => {
  return StyleSheet.create({
    appliedCountContainer: {
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: disabled ? colors.gray['50'] : colors.blue['130'], // '#BABBBE' : '#004F9A',
      borderRadius: 1000,
      width: 16,
      height: 16,
    },
    appliedCountText: {
      ...getFont('700'),
      color: 'white',
      fontSize: 12,
      lineHeight: 16,
      textAlign: 'center',
    } as TextStyle,
    trailingStyle: {
      marginLeft: 8,
    },
    leadingStyle: {
      marginRight: 8,
    },
    disabledIcon: {
      tintColor: colors.gray['50'], // '#BABBBE',
    },
  });
};

FilterTriggerAll.displayName = 'FilterTriggerAll';
export {FilterTriggerAll};
