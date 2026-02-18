import * as React from 'react';
import {StyleProp, StyleSheet, Text, TextStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Text';

import {getFont, Weights} from '../../theme/font';
import {CommonTextProps} from '../types/ComponentTypes';
import {a11yRole, formatColor, TypographyColors} from '../utils';

// ---------------
// Props
// ---------------
export type BodySize = 'large' | 'medium' | 'small';
const weight400 = token.componentTextBodyWeight400FontWeight.toString();
const weight700 = token.componentTextBodyWeight700FontWeight.toString();
export type BodyWeight =
  | typeof weight400
  | typeof weight700
  // the following are for backwards compatibility
  | 'thin'
  | 'light'
  | 'normal'
  | 'medium'
  | 'bold'
  | 'black'

  // the following are for backwards compatibility
  | Extract<Weights, 'thin' | 'light' | 'medium' | 'normal' | 'bold' | 'black'>;

export type BodyProps = CommonTextProps & {
  /**
   * The text of the body.
   */
  children: React.ReactNode;
  /**
   * If the body is displayed in monospace.
   *
   * @default false
   */
  isMonospace?: boolean;
  /**
   * The size for the body.
   * Valid values: 'large' | 'medium' | 'small'
   *
   * @default 'medium'
   */
  size?: BodySize;
  /**
   * The weight for the body.
   * Valid values: '400' | '700'
   *
   * 'thin' | 'light' | 'normal' are deprecated, internally translated to '400'
   *
   * 'medium' | 'bold' | 'black' are deprecated, internally translated to '700'
   *
   * @default '400'
   */
  weight?: BodyWeight;
  /**
   * The color for the caption
   * Valid values are 'black' | 'blue5' | 'blue10' | 'blue20' | 'blue30' | 'blue40' | 'blue50' | 'blue60' | 'blue70' | 'blue80' | 'blue90' | 'blue100' | 'blue110' | 'blue120' | 'blue130' | 'blue140' | 'blue150' | 'blue160' | 'blue170' | 'blue180' | 'gray5' | 'gray10' | 'gray20' | 'gray30' | 'gray40' | 'gray50' | 'gray60' | 'gray70' | 'gray80' | 'gray90' | 'gray100' | 'gray110' | 'gray120' | 'gray130' | 'gray140' | 'gray150' | 'gray160' | 'gray170' | 'gray180' | 'green5' | 'green10' | 'green20' | 'green30' | 'green40' | 'green50' | 'green60' | 'green70' | 'green80' | 'green90' | 'green100' | 'green110' | 'green120' | 'green130' | 'green140' | 'green150' | 'green160' | 'green170' | 'green180' | 'orange5' | 'orange10' | 'orange20' | 'orange30' | 'orange40' | 'orange50' | 'orange60' | 'orange70' | 'orange80' | 'orange90' | 'orange100' | 'orange110' | 'orange120' | 'orange130' | 'orange140' | 'orange150' | 'orange160' | 'orange170' | 'orange180' | 'pink5' | 'pink10' | 'pink20' | 'pink30' | 'pink40' | 'pink50' | 'pink60' | 'pink70' | 'pink80' | 'pink90' | 'pink100' | 'pink110' | 'pink120' | 'pink130' | 'pink140' | 'pink150' | 'pink160' | 'pink170' | 'pink180' | 'purple5' | 'purple10' | 'purple20' | 'purple30' | 'purple40' | 'purple50' | 'purple60' | 'purple70' | 'purple80' | 'purple90' | 'purple100' | 'purple110' | 'purple120' | 'purple130' | 'purple140' | 'purple150' | 'purple160' | 'purple170' | 'purple180' | 'red5' | 'red10' | 'red20' | 'red30' | 'red40' | 'red50' | 'red60' | 'red70' | 'red80' | 'red90' | 'red100' | 'red110' | 'red120' | 'red130' | 'red140' | 'red150' | 'red160' | 'red170' | 'red180' | 'spark5' | 'spark10' | 'spark20' | 'spark30' | 'spark40' | 'spark50' | 'spark60' | 'spark70' | 'spark80' | 'spark90' | 'spark100' | 'spark110' | 'spark120' | 'spark130' | 'spark140' | 'spark150' | 'spark160' | 'spark170' | 'spark180' | 'yellow5' | 'yellow10' | 'yellow20' | 'yellow30' | 'yellow40' | 'yellow50' | 'yellow60' | 'yellow70' | 'yellow80' | 'yellow90' | 'yellow100' | 'yellow110' | 'yellow120' | 'yellow130' | 'yellow140' | 'yellow150' | 'yellow160' | 'yellow170' | 'yellow180' | 'white'
   *
   * @default gray160
   */
  color?: TypographyColors;
  /**
   * If provided, the <strong>style</strong> to provide to the Text element (children).
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<TextStyle>;
  /**
   * @deprecated has no effect. If you need to apply a color to the text, use e.g. UNSAFE_style=`{color: 'green'}`
   */
  inheritColor?: boolean;
  /**
   * @deprecated has no effect. Italics are not supported in LD3
   */
  italic?: boolean;
};

/**
 * Body text is used as the main content on a page or section.
 *
 * ## Usage
 * ```js
 * import {Body} from '@walmart/gtp-shared-components`;
 *
 * <Body>Lorem ipsum dolor sit amet</Body>
 * <Body size="small" weight="400">Lorem ipsum dolor sit amet</Body>
 * <Body isMonospace>Lorem ipsum dolor sit amet</Body>
 * ```
 */
const Body = React.forwardRef<Text, BodyProps>((props, ref) => {
  const {
    children,
    isMonospace = false,
    size = 'medium',
    weight = weight400,
    color = 'gray160', //token.componentTextBodyTextColor
    UNSAFE_style = {},
    ...rest
  } = props;
  let localWeight = weight;
  // Backwards compatibility logic
  if (['thin', 'light', 'normal'].includes(weight as string)) {
    localWeight = weight400;
  } else if (['medium', 'bold', 'black'].includes(weight as string)) {
    localWeight = weight700;
  }

  const localColor = formatColor(color) as TypographyColors;

  // ---------------
  // Rendering
  // ---------------
  return (
    <Text
      accessibilityRole={a11yRole('text')}
      testID={Body.displayName}
      ref={ref}
      style={[
        ss(localWeight as Weights, size, localColor, isMonospace).text,
        UNSAFE_style,
      ]}
      {...rest}>
      {children}
    </Text>
  );
});

//exporting testing purpose
const _getFontSize = (size: BodySize) => {
  if (size === 'small') {
    return token.componentTextBodySizeSmallFontSize;
  } else if (size === 'large') {
    return token.componentTextBodySizeLargeFontSize;
  }
  return token.componentTextBodySizeMediumFontSize;
};

//exporting testing purpose
const _getLineHeight = (size: BodySize) => {
  if (size === 'small') {
    return token.componentTextBodySizeSmallLineHeight;
  } else if (size === 'large') {
    return token.componentTextBodySizeLargeLineHeight;
  }
  return token.componentTextBodySizeMediumLineHeight;
};
// ---------------
// Styles
// ---------------
const ss = (
  weight: Weights,
  size: BodySize,
  colors: TypographyColors,
  isMonospace: boolean,
) => {
  const fontSize = _getFontSize(size);
  const lineHeight = _getLineHeight(size);
  const style = StyleSheet.create({
    text: {
      ...getFont(weight, isMonospace),
      fontSize,
      lineHeight,
      color: colors,
    } as TextStyle,
  });
  return style;
};

Body.displayName = 'Body';
export {Body};
export {_getFontSize, _getLineHeight};
