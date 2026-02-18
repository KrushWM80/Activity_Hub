import * as React from 'react';
import {StyleProp, StyleSheet, View, ViewProps, ViewStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Divider';

import {a11yRole} from '../utils';

// ---------------
// Props
// ---------------
export type DividerProps = ViewProps & {
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  block?: boolean;
  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  color?: string;
};

/**
 * Divider is used to visually separate content.
 *
 * ## Usage
 * ```js
 * import {Divider} from '@walmart/gtp-shared-components`;
 *
 * <Divider/>
 * ```
 */
const Divider: React.FC<DividerProps> = (props: DividerProps) => {
  const {UNSAFE_style, block, color, ...rest} = props;

  // ---------------
  // Rendering
  // ---------------
  return (
    <View
      accessibilityRole={a11yRole('none')}
      testID={Divider.displayName}
      style={[styles.defaultContainer, UNSAFE_style]}
      {...rest}
    />
  );
};

// ---------------
// StyleSheet
// ---------------
const styles = StyleSheet.create({
  defaultContainer: {
    flex: 1,
    height: 1,
    borderBottomColor: token.componentDividerSeparatorColor,
    borderBottomWidth: token.componentDividerSeparatorWidth,
  },
});

Divider.displayName = 'Divider';
export {Divider};
