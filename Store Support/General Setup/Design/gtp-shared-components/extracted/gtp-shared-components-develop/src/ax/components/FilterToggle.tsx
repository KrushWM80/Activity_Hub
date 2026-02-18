import * as React from 'react';
import {GestureResponderEvent, StyleProp, ViewStyle} from 'react-native';

import type {CommonPressableProps} from '../../next/types/ComponentTypes';

import {_FilterBase} from './_FilterBase';

// ---------------
// Props
// ---------------
export type FilterToggleProps = CommonPressableProps & {
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
 * Apply/clear a single filter for a list of data.
 * - Use when needing to quickly apply a simple boolean filter to a data set or results list.
 * - Don't use when what you really need is a tab that changes your data/results to a different view
 * without actually filtering down the list.
 *
 * ## Usage
 * ```js
 * import {FilterToggle, Icons} from '@walmart/gtp-shared-components/ax`;
 *
 * <FilterToggle>Filter</FilterToggle>
 * <FilterToggle isApplied>Applied</FilterToggle>
 * <FilterToggle leading={<Icons.ClockIcon />}>With Icon</FilterToggle>
 * <FilterToggle leading={<Icons.ClockIcon />} isApplied>
 *   With Icon Applied
 * </FilterToggle>
 * <FilterToggle disabled>Filter</FilterToggle>
 *
 * ```
 */
const FilterToggle: React.FC<FilterToggleProps> = (props) => {
  const {
    children,
    disabled = false,
    onPress,
    isApplied = false,
    leading,
    UNSAFE_style,
    ...rest
  } = props;

  // ---------------
  // Rendering
  // ---------------
  return (
    <_FilterBase
      testID={FilterToggle.displayName}
      accessibilityRole="button"
      accessibilityState={{selected: isApplied, disabled}}
      accessibilityLabel={`Filter by ${children}, ${
        isApplied ? 'selected' : 'not selected'
      }`}
      leading={leading}
      applied={isApplied}
      disabled={disabled}
      onPress={onPress}
      UNSAFE_style={UNSAFE_style}
      {...rest}>
      {children}
    </_FilterBase>
  );
};

FilterToggle.displayName = 'FilterToggle';
export {FilterToggle};
