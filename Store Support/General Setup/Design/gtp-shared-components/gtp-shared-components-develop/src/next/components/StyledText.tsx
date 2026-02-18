import * as React from 'react';
import {
  FlexStyle,
  StyleProp,
  StyleSheet,
  Text,
  TextStyle,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/StyledText';
import {IconSize} from '@walmart/gtp-shared-icons';

import {getFont} from '../../theme/font';
import type {CommonViewProps} from '../types/ComponentTypes';
import {a11yRole} from '../utils';

import {_LeadingTrailing as _Leading} from './_LeadingTrailing';

// ---------------
// Props
// ---------------
export type StyledTextSize = 'small' | 'large';
export type StyledTextColor = 'blue' | 'gray' | 'green';

export type StyledTextProps = CommonViewProps & {
  /**
   * The content for the styled text.
   * Typically a string.
   */
  children: React.ReactNode;
  /**
   * This size of the StyledText
   *
   * Valid values: 'small' | 'large'
   * @default 'small'
   */
  size?: StyledTextSize;
  /**
   * The color for the StyledText
   *
   * Valid values: 'blue' | 'gray' | 'green'
   * @default 'gray'
   */
  color?: StyledTextColor;
  /**
   * The leading content for the styled text.
   * Typically an icon.
   */
  leading?: React.ReactNode;
  /**
   * If provided, the `style` to provide to the root element. @note This property
   * is prefixed with `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Styled text visually enhances copy and can help convey meaning by
 * adding color and/or an optional icon.
 *
 * ## Usage
 * ```js
 * import {StyledText} from '@walmart/gtp-shared-components`;
 *
 * <StyledText>Styled Text</StyledText>
 * <StyledText size="small" color="blue" leading={<Icons.CheckIcon />}>
 *   Blue small StyledText with Check Icon
 * </StyledText>
 * <StyledText size="large" color="green" leading={<Icons.CheckIcon />}>
 *   Green large StyledText with Check Icon
 * </StyledText>
 * <StyledText size="large" color="gray" leading={<Icons.CheckIcon />}>
 *   Gray large StyledText with Check Icon
 * </StyledText>
 * ```
 */
const StyledText: React.FC<StyledTextProps> = (props) => {
  const {
    children,
    size = 'small',
    color = 'gray',
    leading,
    UNSAFE_style,
    ...rest
  } = props;

  const iconTintColor =
    color === 'blue'
      ? token.componentStyledTextLeadingIconColorBlueIconColor
      : color === 'gray'
      ? token.componentStyledTextLeadingIconColorGrayIconColor
      : token.componentStyledTextLeadingIconColorGreenIconColor;

  const iconSize =
    size === 'small'
      ? (token.componentStyledTextLeadingIconSizeSmallIconSize as IconSize)
      : (token.componentStyledTextLeadingIconSizeLargeIconSize as IconSize);

  // ---------------
  // Rendering
  // ---------------
  const renderLeading = (node: React.ReactNode) => {
    return (
      <_Leading
        node={node}
        iconProps={{
          UNSAFE_style: {
            marginRight: token.componentStyledTextLeadingIconMarginEnd,
          },
          color: iconTintColor,
          size: iconSize,
        }}
      />
    );
  };

  return (
    <View
      testID={StyledText.displayName}
      style={[ss(color, size).container, UNSAFE_style]}
      {...rest}>
      {leading ? renderLeading(leading) : null}
      <Text
        accessibilityRole={a11yRole('text')}
        testID={StyledText.displayName + '-content'}
        style={ss(color, size).content}>
        {children}
      </Text>
    </View>
  );
};

// ---------------
// Styles
// ---------------
const ss = (color: StyledTextColor, size: StyledTextSize) => {
  return StyleSheet.create({
    container: {
      flexDirection: 'row',
      justifyContent:
        token.componentStyledTextContainerAlignVertical as Extract<
          FlexStyle,
          'justifyContent'
        >,
      alignItems: 'center',
    },
    content: {
      ...getFont(),
      fontWeight: token.componentStyledTextTextLabelFontWeight.toString(),
      fontSize:
        size === 'small'
          ? token.componentStyledTextTextLabelSizeSmallFontSize
          : token.componentStyledTextTextLabelSizeLargeFontSize,
      color:
        color === 'blue'
          ? token.componentStyledTextTextLabelColorBlueTextColor
          : color === 'gray'
          ? token.componentStyledTextTextLabelColorGrayTextColor
          : token.componentStyledTextTextLabelColorGreenTextColor,
      lineHeight: token.componentStyledTextTextLabelLineHeight,
      paddingTop: size === 'small' ? 4 : 3,
    } as TextStyle,
  });
};

StyledText.displayName = 'StyledText';
export {StyledText};
