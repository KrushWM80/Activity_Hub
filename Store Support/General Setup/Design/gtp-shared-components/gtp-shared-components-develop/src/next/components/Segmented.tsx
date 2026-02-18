import * as React from 'react';
import {StyleProp, StyleSheet, View, ViewProps, ViewStyle} from 'react-native';

import flattenChildren from 'react-keyed-flatten-children';

import {a11yRole, colors} from '../utils';

// ---------------
// Props
// ---------------

export type SegmentSize = 'small' | 'large';

export type SegmentedProps = ViewProps & {
  /** Size of the Segment.
   * @default small
   */
  size?: SegmentSize;

  /** The index of the selected segment
   * @default 0
   */
  selectedIndex?: number;

  /**
   * The content for the Segment.
   * It is marked as optional for backwards compatibility only
   */
  children?: React.ReactNode;

  /** Whether this segmented control is disabled
   * @default false
   */
  disabled?: boolean;

  /** Segmented's change event handler */
  onChange?: (index: number) => void;

  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;

  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  small?: boolean;
};

/**
 * A Segmented control is a linear set of two or more Segments, each of which functions as a mutually exclusive button.
 * Segmented controls are often used to display different views; Segmented controls manipulate the content shown following an exclusive or “either/or” pattern.
 * It is used to toggle between two or more content sections within the same space on screen. Only one section can be shown at a time.
 *
 * ## Usage
 * ```js
 * import {Segmented, Segment} from '@walmart/gtp-shared-components';
 *
 * const [selectedSegment1, setSelectedSegment1] = React.useState(0)
 *
 * <Segmented
 *   size='small'
 *   selectedIndex={selectedSegment1}
 *   onChange={index => setSelectedSegment1(index)}>
 *   <Segment>First</Segment>
 *   <Segment>Second</Segment>
 *   <Segment>Third</Segment>
 * </Segmented>
 * ```
 */

const Segmented: React.FC<SegmentedProps> = (props) => {
  const {
    selectedIndex = 0,
    disabled = false,
    size = 'small',
    children,
    onChange,
    UNSAFE_style = {},
    ...rest
  } = props;

  const kids = flattenChildren(children);

  const _setSelected = (index: number) => {
    onChange?.(index);
  };

  // ---------------
  // Rendering
  // ---------------

  const renderChildren = () => {
    return kids.map((child, index) =>
      React.cloneElement(child as React.ReactElement, {
        key: `Segment_${index}`,
        selected: (selectedIndex ?? 0) === index,
        disabled,
        size,
        onPress: () => _setSelected(index),
      }),
    );
  };

  return (
    <View
      accessibilityRole={a11yRole('radiogroup')}
      testID={Segmented.displayName}
      style={[ss.container, UNSAFE_style]}
      {...rest}>
      {renderChildren()}
    </View>
  );
};

// ---------------
// Styles
// ---------------

const ss = StyleSheet.create({
  container: {
    borderRadius: 4,
    padding: 2,
    alignItems: 'stretch',
    flexDirection: 'row',
    backgroundColor: colors.gray['20'],
  },
});

Segmented.displayName = 'Segmented';
export {Segmented};
