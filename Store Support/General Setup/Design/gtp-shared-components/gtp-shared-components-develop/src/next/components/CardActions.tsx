import * as React from 'react';
import {StyleProp, StyleSheet, View, ViewStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Card';

import type {CommonViewProps} from '../types/ComponentTypes';

import {CardContext, CardSize} from './Card';

// ---------------
// Props
// ---------------
export type CardActionsProps = CommonViewProps & {
  /**
   * Typically a ButtonGroup bellow the CardContent
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
 * Card subcomponent, providing a set of buttons below CardContent
 *
 * ## Usage
 * ```js
 * import {CardActions} from '@walmart/gtp-shared-components`;
 * ```
 */
const CardActions: React.FC<CardActionsProps> = (props) => {
  const {children, UNSAFE_style, ...rest} = props;
  const {cardSize} = React.useContext(CardContext);

  // ---------------
  // Rendering
  // ---------------
  return (
    <View
      testID={CardActions.displayName}
      style={[ss(cardSize).container, UNSAFE_style]}
      {...rest}>
      <View style={ss(cardSize).innerContainer}>{children}</View>
    </View>
  );
};

// ---------------
// Styles
// ---------------
const ss = (size: CardSize) => {
  return StyleSheet.create({
    container: {
      width: '90%',
      alignItems: 'center',
      justifyContent: 'flex-end',
      borderTopColor: token.componentCardActionsContainerBorderColorTop,
      borderTopWidth: token.componentCardActionsContainerBorderWidthTop,
      marginVertical:
        size === 'small'
          ? token.componentCardActionsContainerSizeSmallMarginVertical
          : token.componentCardActionsContainerSizeLargeMarginVertical,
      paddingHorizontal:
        size === 'small'
          ? token.componentCardActionsContainerSizeSmallPaddingHorizontal
          : token.componentCardActionsContainerSizeLargePaddingHorizontal,
    },
    innerContainer: {
      alignSelf: 'flex-end',
      marginRight: size === 'small' ? '-9%' : '-12%',
      marginTop:
        size === 'small'
          ? token.componentCardActionsContainerSizeSmallMarginVertical
          : token.componentCardActionsContainerSizeLargeMarginVertical,
    },
  });
};

CardActions.displayName = 'CardActions';
export {CardActions};
