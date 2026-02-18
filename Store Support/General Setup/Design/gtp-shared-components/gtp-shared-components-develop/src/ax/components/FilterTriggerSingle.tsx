import * as React from 'react';
import {
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
export type FilterTriggerSingleProps = CommonPressableProps & {
  /**
   * The text content for the filter.
   */
  children: string;
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
   * If the filter select trigger is applied.
   * @default false
   */
  isApplied?: boolean;
  /**
   * If the filter select trigger is open.
   * @default false
   */
  isOpen?: boolean;
  /**
   * The leading content for the filter.
   * (typically an icon)
   */
  leading?: React.ReactElement;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with
   * `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Show/hide a quick filter that has 3< options.
 * - Use when needing to quickly apply a simple boolean filter to a data set or results list.
 * - Don't use when what you really need is a tab that changes your data/results to a different view
 *   without actually filtering down the list.
 *
 * ## Usage
 * ```js
 * import {FilterTriggerSingle, Icons} from '@walmart/gtp-shared-components/ax`;
 *
 * <FilterTriggerSingle leading={<Icons.TruckIcon />}>
 *   Closed
 * </FilterTriggerSingle>
 * <FilterTriggerSingle leading={<Icons.TruckIcon />} isOpen>
 *   Opened
 * </FilterTriggerSingle>
 * <FilterTriggerSingle leading={<Icons.TruckIcon />} isApplied>
 *   Closed Applied
 * </FilterTriggerSingle>
 * <FilterTriggerSingle leading={<Icons.TruckIcon />} isApplied isOpen>
 *   Open Applied
 * </FilterTriggerSingle>
 * ```
 */
const FilterTriggerSingle: React.FC<FilterTriggerSingleProps> = (props) => {
  const {
    children,
    disabled = false,
    onPress,
    isApplied = false,
    isOpen = false,
    leading,
    UNSAFE_style,
    ...rest
  } = props;

  const ss = styles();

  // ---------------
  // Rendering
  // ---------------
  const renderTrailing = () => {
    return <Icons.ChevronDownIcon color={disabled ? '#BABBBE' : undefined} />;
  };

  const renderStyle = () => {
    if (disabled) {
      return;
    }
    if (isApplied) {
      if (isOpen) {
        return ss.openAppliedStyle;
      } else {
        return;
      }
    } else {
      if (isOpen) {
        return ss.openDefaultStyle;
      } else {
        return;
      }
    }
  };

  const accessibilityLabel = `Filter by ${children}, ${
    isApplied ? 'applied' : 'not applied'
  }, activate to change filter`;

  return (
    <_FilterBase
      testID={FilterTriggerSingle.displayName}
      accessibilityRole="button"
      accessibilityState={{disabled}}
      accessibilityLabel={accessibilityLabel}
      leading={leading}
      trailing={renderTrailing()}
      applied={isApplied}
      disabled={disabled}
      onPress={onPress}
      UNSAFE_style={[UNSAFE_style, renderStyle()]}
      containerPressedStyle={
        isApplied
          ? isOpen
            ? ss.containerPressedOpenedAppliedStyle
            : ss.containerPressedDefaultAppliedStyle
          : undefined
      }
      {...rest}>
      {children}
    </_FilterBase>
  );
};

// ---------------
// Styles
// ---------------
const styles = () => {
  return StyleSheet.create({
    openDefaultStyle: {
      borderColor: colors.gray['160'], // '#2E2F32',
    },
    openAppliedStyle: {
      borderColor: colors.blue['160'], // '#002D58',
    },
    containerPressedDefaultAppliedStyle: {
      borderColor: colors.blue['100'], // '#0071DC',
      backgroundColor: colors.blue['5'], // '#F2F8FD',
    },
    containerPressedOpenedAppliedStyle: {
      borderColor: colors.blue['160'], // '#002D58',
      backgroundColor: colors.blue['5'], // '#F2F8FD',
    },
  });
};

FilterTriggerSingle.displayName = 'FilterTriggerSingle';
export {FilterTriggerSingle};
