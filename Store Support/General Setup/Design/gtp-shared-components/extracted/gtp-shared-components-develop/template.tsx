import * as React from 'react';
import {StyleProp, StyleSheet, Text, View, ViewStyle} from 'react-native';

import type {CommonViewProps} from '../types/ComponentTypes';

// ---------------
// Props
// ---------------
type MyComponentSize = 'small' | 'medium' | 'large';
export type MyComponentProps = CommonViewProps & {
  /**
   * This is the description for prop size
   */
  size: MyComponentSize;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with
   * `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * This is the description for MyComponent
 *
 * ```js
 * import {MyComponent} from '@walmart/bluesteel-rn-components`;
 * ```
 */
const MyComponent: React.FC<MyComponentProps> = (props) => {
  const {size, UNSAFE_style} = props;

  // ---------------
  // Rendering
  // ---------------
  return (
    <View testID={MyComponent.displayName} style={[ss.container, UNSAFE_style]}>
      <Text>{size}</Text>
    </View>
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

MyComponent.displayName = 'MyComponent';
export {MyComponent};
