import * as React from 'react';
import {StyleProp, StyleSheet, View, ViewProps, ViewStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Skeleton';

import {Skeleton} from './Skeleton';
// ---------------
// Props
// ---------------
export type SkeletonTextProps = ViewProps & {
  /**
   * The number of lines for the skeleton text.
   *
   * @default 3
   */
  lines?: number;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * SkeletonText is used to show multiple Skeleton lines of text
 *
 * ## Usage
 * ```js
 * import {SkeletonText} from '@walmart/gtp-shared-components`;
 *
 * <SkeletonText lines={3} />
 * ```
 */
const SkeletonText: React.FC<SkeletonTextProps> = (props) => {
  const {lines = 3, UNSAFE_style, ...rest} = props;

  // ---------------
  // Rendering
  // ---------------
  return (
    <View
      testID={SkeletonText.displayName}
      style={[ss.container, UNSAFE_style]}
      {...rest}>
      {Array.from(new Array(lines)).map((_, index) => (
        <Skeleton
          UNSAFE_style={{marginBottom: token.componentSkeletonTextGap}}
          key={index}
        />
      ))}
    </View>
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  container: {
    marginBottom: token.componentSkeletonTextContainerGap, // 8
  },
});

SkeletonText.displayName = 'SkeletonText';
export {SkeletonText};
