import * as React from 'react';
import {StyleProp, StyleSheet, View, ViewProps, ViewStyle} from 'react-native';

import {Body} from './Body';

// ---------------
// Props
// ---------------

export type VariantsProps = ViewProps & {
  /**
   * Array of variants.  When using color variants, these will show up as colored pips.
   */
  variants: Array<string>;
  /**
   * Whether these variants are colors.
   */
  colors?: boolean;
  /**
   * Content for the Variants.
   * It is marked as optional for backwards compatibility only
   */
  children?: React.ReactNode;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Variant indicators show customers that an item is available in multiple styles or colors.
 * They are informative and not actionable.
 *
 * ## Usage
 * ```js
 * import {Variants} from '@walmart/gtp-shared-components';
 *
 * <Variants variants={[colors.blue['100'], colors.green['100']]} />;
 * ```
 */

const Variants: React.FC<VariantsProps> = (props) => {
  /**
   * Maximum Variants displayed on Screen - 4.
   */
  const MAX_VARIANTS = 4;

  const {variants, colors = true, children, UNSAFE_style = {}, ...rest} = props;

  // ---------------
  // Rendering
  // ---------------

  const _renderVariant = (backgroundColor: string, index: number) => {
    if (index < MAX_VARIANTS) {
      return (
        <View
          key={`Variant_${index}`}
          style={[
            ss.pip,
            {backgroundColor},
            index === variants.length - 1 && ss.lastPip,
          ]}
        />
      );
    }
    return null;
  };

  const _renderRemainingCaption = () => {
    if (variants.length > MAX_VARIANTS) {
      return (
        <Body UNSAFE_style={ss.caption}>+{variants.length - MAX_VARIANTS}</Body>
      );
    }
    return null;
  };

  const _renderNoColorCaption = () => {
    return (
      <View {...rest} style={[ss.container, UNSAFE_style]}>
        <Body UNSAFE_style={ss.caption}>{variants.length} options</Body>
      </View>
    );
  };

  return colors ? (
    <View testID={Variants.displayName} style={[ss.container, UNSAFE_style]}>
      {variants.map((backgroundColor, index) =>
        _renderVariant(backgroundColor, index),
      )}
      {_renderRemainingCaption()}
    </View>
  ) : (
    _renderNoColorCaption()
  );
};

// ---------------
// Styles
// ---------------

const ss = StyleSheet.create({
  container: {
    alignSelf: 'center',
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
  },
  pip: {
    height: 8,
    width: 8,
    marginVertical: 4,
    borderRadius: 4,
    marginRight: 8,
    flexDirection: 'row',
  },
  lastPip: {
    height: 8,
    width: 8,
    marginVertical: 4,
    borderRadius: 4,
    marginRight: 0,
    flexDirection: 'row',
  },
  caption: {
    fontSize: 12,
    lineHeight: 16,
    color: '#74767c',
  },
});

Variants.displayName = 'Variants';
export {Variants};
