import * as React from 'react';
import {
  FlexAlignType,
  StyleProp,
  StyleSheet,
  View,
  ViewProps,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Card';

import {a11yRole} from '../utils';

import {
  _LeadingTrailing as _Leading,
  _LeadingTrailing as _Trailing,
} from './_LeadingTrailing';
import {CardContext, CardSize} from './Card';
import {Heading} from './Heading';

// ---------------
// Props
// ---------------
export type CardHeaderProps = ViewProps & {
  /**
   * The leading content for the card header.
   * (typically an icon)
   */
  leading?: React.ReactElement;
  /**
   * The title for the card header.
   * Typically a Text element.
   */
  title: React.ReactNode;
  /**
   * The trailing content for the card header.
   * Typically a Link.
   */
  trailing?: React.ReactElement;
  /**
   * If provided, the `style` to provide to the root element.
   * @note This property is prefixed with `UNSAFE` as its use often
   * results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Card subcomponent, providing a title
 * below CardMedia
 *
 * ## Usage
 * ```js
 * import {CardHeader} from '@walmart/gtp-shared-components`;
 * ```
 */
const CardHeader: React.FC<CardHeaderProps> = (props) => {
  const {leading, title, trailing, UNSAFE_style, ...rest} = props;
  const {cardSize} = React.useContext(CardContext);

  const renderLeading = (node: React.ReactNode) => (
    <_Leading
      node={node}
      iconProps={{
        UNSAFE_style: ss(cardSize).leading,
      }}
    />
  );

  const renderTrailing = (node: React.ReactNode) => (
    <_Trailing
      node={node}
      iconProps={{
        UNSAFE_style: ss(cardSize).trailing,
      }}
    />
  );

  return (
    <View
      accessibilityRole={a11yRole('header')}
      testID={CardHeader.displayName}
      style={[ss(cardSize).container, UNSAFE_style]}
      {...rest}>
      <View style={ss(cardSize).leftGroup}>
        {leading ? renderLeading(leading) : null}
        <Heading children={title} weight="700" />
      </View>
      {trailing ? renderTrailing(trailing) : null}
    </View>
  );
};

// ---------------
// Styles
// ---------------
const ss = (size: CardSize) => {
  return StyleSheet.create({
    container: {
      width: '100%',
      flexDirection: 'row',
      justifyContent: 'space-between',
      backgroundColor: token.componentCardContainerBackgroundColor,
      alignItems:
        token.componentCardHeaderContainerAlignVertical as FlexAlignType,
      marginVertical:
        size === 'small'
          ? token.componentCardHeaderContainerSizeSmallMarginVertical
          : token.componentCardContentContainerSizeLargeMarginVertical,
      paddingHorizontal:
        size === 'small'
          ? token.componentCardHeaderContainerSizeSmallPaddingHorizontal
          : token.componentCardHeaderContainerSizeLargePaddingHorizontal,
    },
    leading: {
      marginRight: token.componentCardHeaderLeadingIconMarginEnd,
    },
    trailing: {
      marginRight: token.componentCardHeaderTrailingMarginStart,
    },
    leftGroup: {
      flexDirection: 'row',
      alignItems: 'center',
    },
  });
};

CardHeader.displayName = 'CardHeader';
export {CardHeader};
