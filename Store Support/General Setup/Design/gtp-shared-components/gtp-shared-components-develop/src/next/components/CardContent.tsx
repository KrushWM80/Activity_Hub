import * as React from 'react';
import {StyleProp, StyleSheet, View, ViewStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Card';

import type {CommonViewProps} from '../types/ComponentTypes';

import {CardContext, CardSize} from './Card';

// ---------------
// Props
// ---------------
export type CardContentProps = CommonViewProps & {
  /**
   * Typically text that gets displayed bellow CardHeader
   */
  children: React.ReactElement | string;
  /**
   * If provided, the `style` to provide to the root element.
   * @note This property is prefixed with `UNSAFE` as its use often
   * results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Card subcomponent, providing the content of the card
 * below CardHeader
 *
 * ## Usage
 * ```js
 * import {CardContent} from '@walmart/gtp-shared-components`;
 * ```
 */
const CardContent: React.FC<CardContentProps> = (props) => {
  const {children, UNSAFE_style, ...rest} = props;
  const {cardSize} = React.useContext(CardContext);

  // ---------------
  // Rendering
  // ---------------
  return (
    <View
      testID={CardContent.displayName}
      style={[ss(cardSize).container, UNSAFE_style]}
      {...rest}>
      {children}
    </View>
  );
};

// ---------------
// Styles
// ---------------
const ss = (size: CardSize) => {
  return StyleSheet.create({
    container: {
      justifyContent: 'center',
      alignItems: 'center',
      alignSelf: 'flex-start',
      marginVertical:
        size === 'small'
          ? token.componentCardContentContainerSizeSmallMarginVertical
          : token.componentCardContentContainerSizeLargeMarginVertical,
      paddingHorizontal:
        size === 'small'
          ? token.componentCardContentContainerSizeSmallPaddingHorizontal
          : token.componentCardContentContainerSizeLargePaddingHorizontal,
    },
  });
};

CardContent.displayName = 'CardContent';
export {CardContent};
