---
to: src/next/components/<%= componentName %>.tsx
unless_exists: true
---

import * as React from 'react';
import {StyleProp, StyleSheet, Text, View, ViewStyle} from 'react-native';

import type {CommonViewProps} from '../types/ComponentTypes';

// ---------------
// Props
// ---------------
type <%= componentName %>Size = 'small' | 'medium' | 'large';
export type <%= componentName %>Props = CommonViewProps & {
  /**
   * This is the description for prop size
   */
  size: <%= componentName %>Size;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with
   * `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * This is the description for <%= componentName %>
 *
 * ```js
 * import {<%= componentName %>} from '@walmart/gtp-shared-components`;
 * ```
 */
const <%= componentName %>: React.FC<<%= componentName %>Props> = (props) => {
  const {size, UNSAFE_style} = props;

  // ---------------
  // Rendering
  // ---------------
  return (
    <View testID={<%= componentName %>.displayName} style={[ss.container, UNSAFE_style]}>
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

<%= componentName %>.displayName = '<%= componentName %>';
export {<%= componentName %>};
