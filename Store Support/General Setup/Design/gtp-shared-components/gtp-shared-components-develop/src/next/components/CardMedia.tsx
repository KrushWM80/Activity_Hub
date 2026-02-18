import * as React from 'react';
import {StyleProp, StyleSheet, View, ViewStyle} from 'react-native';

import type {CommonViewProps} from '../types/ComponentTypes';
import {a11yRole} from '../utils';

// ---------------
// Props
// ---------------
export type CardMediaProps = CommonViewProps & {
  /**
   * Typically an image above the CardHeader
   */
  children: React.ReactElement;
  /**
   * If provided, the `style` to provide to the root element.
   * @note This property is prefixed with `UNSAFE` as its use often
   * results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Card subcomponent, typically providing an image above CardHeader
 *
 * ## Usage
 * ```js
 * import {CardMedia} from '@walmart/gtp-shared-components`;
 * ```
 */
const CardMedia: React.FC<CardMediaProps> = (props) => {
  const {children, UNSAFE_style, ...rest} = props;

  // ---------------
  // Rendering
  // ---------------
  return (
    <View
      accessibilityRole={a11yRole('image')}
      testID={CardMedia.displayName}
      style={[ss.container, UNSAFE_style]}
      {...rest}>
      {children}
    </View>
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  container: {
    justifyContent: 'center',
    alignItems: 'center',
    width: '100%',
    overflow: 'hidden',
  },
});

CardMedia.displayName = 'CardMedia';
export {CardMedia};
