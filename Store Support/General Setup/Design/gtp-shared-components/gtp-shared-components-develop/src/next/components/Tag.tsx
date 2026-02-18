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

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Tag';
import {IconSize} from '@walmart/gtp-shared-icons';

import {getFont} from '../../theme/font';
import type {CommonViewProps} from '../types/ComponentTypes';
import {a11yRole} from '../utils';

import {_LeadingTrailing as _Leading} from './_LeadingTrailing';

// ---------------
// Props
// ---------------
export type TagVariant = 'primary' | 'secondary' | 'tertiary';
export type TagColor = 'red' | 'spark' | 'green' | 'blue' | 'purple' | 'gray';

export type TagProps = CommonViewProps & {
  /**
   * The content for the tag.
   * Typically a string.
   */
  children: React.ReactNode;
  /**
   * The color for the tag.
   * TagColor = 'red' | 'spark' | 'green' | 'blue' | 'purple' | 'gray'
   */
  color: TagColor;
  /**
   * The leading content for the tag.
   * Typically an icon.
   */
  leading?: React.ReactNode;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with
   * `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
  /**
   * The variant for the tag.
   * TagVariant = 'primary' | 'secondary' | 'tertiary'
   */
  variant: TagVariant;
};

/**
 * Tags are used to draw a customer’s focus to item traits such as availability, status, or media rating.
 * Items may be products, fulfillment slots, or something else. They are visual only and non-interactive.
 *
 * ## Usage
 * ```js
 * import {Tag} from '@walmart/gtp-shared-components`;
 *
 * <Tag variant="primary" color="spark" leading={<Icons.TruckIcon />}>
 *   Spark Primary Tag
 * </Tag>
 * ```
 */
const Tag: React.FC<TagProps> = (props) => {
  const {
    children,
    color = 'blue',
    leading,
    UNSAFE_style = {},
    variant = 'secondary',
    ...rest
  } = props;

  const renderLeading = (node: React.ReactNode) => {
    return (
      <_Leading
        node={node}
        iconProps={{
          UNSAFE_style: [
            {
              marginRight: token.componentTagLeadingIconMarginEnd,
            },
            ss(variant, color).iconStyle,
          ],
          size: token.componentTagLeadingIconIconSize as IconSize,
        }}
      />
    );
  };
  return (
    <View
      testID={Tag.displayName}
      style={[ss(variant, color).container, UNSAFE_style]}
      {...rest}>
      {leading ? renderLeading(leading) : null}
      <Text
        accessibilityRole={a11yRole('text')}
        testID={Tag.displayName + '-content'}
        style={[ss(variant, color).content]}>
        {children}
      </Text>
    </View>
  );
};

export const variantStyles = {
  primary: {
    blue: {
      tintColor: token.componentTagLeadingIconVariantPrimaryColorBlueIconColor,
      textColor: token.componentTagTextLabelVariantPrimaryColorBlueTextColor,
      backgroundColor:
        token.componentTagContainerVariantPrimaryColorBlueBackgroundColor,
    },
    gray: {
      tintColor: token.componentTagLeadingIconVariantPrimaryColorGrayIconColor,
      textColor: token.componentTagTextLabelVariantPrimaryColorGrayTextColor,
      backgroundColor:
        token.componentTagContainerVariantPrimaryColorGrayBackgroundColor,
    },
    green: {
      tintColor: token.componentTagLeadingIconVariantPrimaryColorGreenIconColor,
      textColor: token.componentTagTextLabelVariantPrimaryColorGreenTextColor,
      backgroundColor:
        token.componentTagContainerVariantPrimaryColorGreenBackgroundColor,
    },
    purple: {
      tintColor:
        token.componentTagLeadingIconVariantPrimaryColorPurpleIconColor,
      textColor: token.componentTagTextLabelVariantPrimaryColorPurpleTextColor,
      backgroundColor:
        token.componentTagContainerVariantPrimaryColorPurpleBackgroundColor,
    },
    red: {
      tintColor: token.componentTagLeadingIconVariantPrimaryColorRedIconColor,
      textColor: token.componentTagTextLabelVariantPrimaryColorRedTextColor,
      backgroundColor:
        token.componentTagContainerVariantPrimaryColorRedBackgroundColor,
    },
    spark: {
      tintColor: token.componentTagLeadingIconVariantPrimaryColorSparkIconColor,
      textColor: token.componentTagTextLabelVariantPrimaryColorSparkTextColor,
      backgroundColor:
        token.componentTagContainerVariantPrimaryColorSparkBackgroundColor,
    },
  },
  secondary: {
    blue: {
      tintColor:
        token.componentTagLeadingIconVariantSecondaryColorBlueIconColor,
      textColor: token.componentTagTextLabelVariantSecondaryColorBlueTextColor,
      borderColor:
        token.componentTagContainerVariantSecondaryColorBlueBorderColor,
      borderWidth:
        token.componentTagContainerVariantSecondaryColorBlueBorderWidth,
      backgroundColor:
        token.componentTagContainerVariantSecondaryBackgroundColor,
    },
    gray: {
      tintColor:
        token.componentTagLeadingIconVariantSecondaryColorGrayIconColor,
      textColor: token.componentTagTextLabelVariantSecondaryColorGrayTextColor,
      borderColor:
        token.componentTagContainerVariantSecondaryColorGrayBorderColor,
      borderWidth:
        token.componentTagContainerVariantSecondaryColorGrayBorderWidth,
      backgroundColor:
        token.componentTagContainerVariantSecondaryBackgroundColor,
    },
    green: {
      tintColor:
        token.componentTagLeadingIconVariantSecondaryColorGreenIconColor,
      textColor: token.componentTagTextLabelVariantSecondaryColorGreenTextColor,
      borderColor:
        token.componentTagContainerVariantSecondaryColorGreenBorderColor,
      borderWidth:
        token.componentTagContainerVariantSecondaryColorGreenBorderWidth,
      backgroundColor:
        token.componentTagContainerVariantSecondaryBackgroundColor,
    },
    purple: {
      tintColor:
        token.componentTagLeadingIconVariantSecondaryColorPurpleIconColor,
      textColor:
        token.componentTagTextLabelVariantSecondaryColorPurpleTextColor,
      borderColor:
        token.componentTagContainerVariantSecondaryColorPurpleBorderColor,
      borderWidth:
        token.componentTagContainerVariantSecondaryColorPurpleBorderWidth,
      backgroundColor:
        token.componentTagContainerVariantSecondaryBackgroundColor,
    },
    red: {
      tintColor: token.componentTagLeadingIconVariantSecondaryColorRedIconColor,
      textColor: token.componentTagTextLabelVariantSecondaryColorRedTextColor,
      borderColor:
        token.componentTagContainerVariantSecondaryColorRedBorderColor,
      borderWidth:
        token.componentTagContainerVariantSecondaryColorRedBorderWidth,
      backgroundColor:
        token.componentTagContainerVariantSecondaryBackgroundColor,
    },
    spark: {
      tintColor:
        token.componentTagLeadingIconVariantSecondaryColorSparkIconColor,
      textColor: token.componentTagTextLabelVariantSecondaryColorSparkTextColor,
      borderColor:
        token.componentTagContainerVariantSecondaryColorSparkBorderColor,
      borderWidth:
        token.componentTagContainerVariantSecondaryColorSparkBorderWidth,
      backgroundColor:
        token.componentTagContainerVariantSecondaryBackgroundColor,
    },
  },
  tertiary: {
    blue: {
      tintColor: token.componentTagLeadingIconVariantTertiaryColorBlueIconColor,
      textColor: token.componentTagTextLabelVariantTertiaryColorBlueTextColor,
      backgroundColor:
        token.componentTagContainerVariantTertiaryColorBlueBackgroundColor,
    },
    gray: {
      tintColor: token.componentTagLeadingIconVariantTertiaryColorGrayIconColor,
      textColor: token.componentTagTextLabelVariantTertiaryColorGrayTextColor,
      backgroundColor:
        token.componentTagContainerVariantTertiaryColorGrayBackgroundColor,
    },
    green: {
      tintColor:
        token.componentTagLeadingIconVariantTertiaryColorGreenIconColor,
      textColor: token.componentTagTextLabelVariantTertiaryColorGreenTextColor,
      backgroundColor:
        token.componentTagContainerVariantTertiaryColorGreenBackgroundColor,
    },
    purple: {
      tintColor:
        token.componentTagLeadingIconVariantTertiaryColorPurpleIconColor,
      textColor: token.componentTagTextLabelVariantTertiaryColorPurpleTextColor,
      backgroundColor:
        token.componentTagContainerVariantTertiaryColorPurpleBackgroundColor,
    },
    red: {
      tintColor: token.componentTagLeadingIconVariantTertiaryColorRedIconColor,
      textColor: token.componentTagTextLabelVariantTertiaryColorRedTextColor,
      backgroundColor:
        token.componentTagContainerVariantTertiaryColorRedBackgroundColor,
    },
    spark: {
      tintColor:
        token.componentTagLeadingIconVariantTertiaryColorSparkIconColor,
      textColor: token.componentTagTextLabelVariantTertiaryColorSparkTextColor,
      backgroundColor:
        token.componentTagContainerVariantTertiaryColorSparkBackgroundColor,
    },
  },
};
// ---------------
// Styles
// ---------------
const ss = (variant: TagVariant, color: TagColor) => {
  const iconTintColor = variantStyles[variant][color].tintColor;
  const textColor = variantStyles[variant][color].textColor;
  const backgroundColor = variantStyles[variant][color].backgroundColor;
  const containerBorderColor =
    variant === 'secondary'
      ? variantStyles.secondary[color]?.borderColor
      : undefined;
  const containerBorderWidth =
    variant === 'secondary' ? variantStyles.secondary[color]?.borderWidth : 0;

  return StyleSheet.create({
    container: {
      flexDirection: 'row',
      alignSelf: 'flex-start',
      backgroundColor: backgroundColor,
      borderRadius: token.componentTagContainerBorderRadius,
      margin: 2,
      borderColor: containerBorderColor,
      borderWidth: containerBorderWidth,
      lineHeight: token.componentTagTextLabelLineHeight,
      justifyContent: token.componentTagContainerAlignVertical as Extract<
        FlexStyle,
        'justifyContent'
      >,
      paddingHorizontal: token.componentTagContainerPaddingHorizontal,
      paddingVertical: token.componentTagContainerPaddingVertical
        ? token.componentTagContainerPaddingVertical
        : 2,
    },
    content: {
      ...getFont(),
      color: textColor,
      fontWeight: token.componentTagTextLabelFontWeight.toString(),
      fontSize: token.componentTagTextLabelFontSize,
    } as TextStyle,
    iconStyle: {
      tintColor: iconTintColor,
    },
  });
};

Tag.displayName = 'Tag';
export {Tag};
