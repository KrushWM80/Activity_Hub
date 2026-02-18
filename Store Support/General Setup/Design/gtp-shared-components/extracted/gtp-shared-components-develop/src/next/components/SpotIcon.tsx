import * as React from 'react';
import {ImageStyle, StyleProp, StyleSheet, View, ViewStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/SpotIcon';

import type {CommonViewProps} from '../types/ComponentTypes';
import {a11yRole, iconSizes, IconSizesKey} from '../utils';

import {_LeadingTrailing as _Icon} from './_LeadingTrailing';

// ---------------
// Props
// ---------------
export type SpotIconSize = 'small' | 'large';
export type SpotIconColor = 'blue' | 'white';

export type SpotIconProps = CommonViewProps & {
  /**
   * The icon for the spot icon.
   */
  children: React.ReactNode;
  /**
   * The color for the spot icon.
   * Valid values: 'blue' | 'white'
   * @default blue
   */
  color?: SpotIconColor;
  /**
   * The size for the spot icon.
   * Valid values: 'small' | 'large'
   * @default small
   */
  size?: SpotIconSize;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with `UNSAFE`
   * as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Spot Icons are decorative elements that add visual interest to messaging or other screen elements such
 * as list items.
 *
 * ## Usage
 * ```js
 * import {Icons, SpotIcon} from '@walmart/gtp-shared-components`;
 *
 * <SpotIcon>
 *   <Icons.CheckIcon />
 * </SpotIcon>
 * <SpotIcon color="white">
 *   <Icons.CheckIcon />
 * </SpotIcon>
 * <SpotIcon size="large">
 *   <Icons.CheckIcon />
 * </SpotIcon>
 * <SpotIcon color="white" size="large">
 *   <Icons.CheckIcon />
 * </SpotIcon>
 * ```
 */
const SpotIcon: React.FC<SpotIconProps> = (props) => {
  const {
    children,
    color = 'blue',
    size = 'small',
    UNSAFE_style = {},
    ...rest
  } = props;

  // ---------------
  // Rendering
  // ---------------
  const renderChild = (node: React.ReactNode) => {
    return (
      <_Icon
        node={node}
        iconProps={{
          UNSAFE_style: ss(size, color).icon,
        }}
      />
    );
  };

  return (
    <View
      accessibilityRole={a11yRole('image')}
      testID={SpotIcon.displayName}
      style={[ss(size, color).container, UNSAFE_style]}
      {...rest}>
      {renderChild(children)}
    </View>
  );
};

// ---------------
// Styles
// ---------------
const ss = (size: SpotIconSize, color: SpotIconColor) => {
  const containerSize =
    size === 'small'
      ? token.componentSpotIconContainerSizeSmallHeight
      : token.componentSpotIconContainerSizeLargeHeight;
  const iconSize =
    size === 'small'
      ? iconSizes[
          token.componentSpotIconIconSizeSmallIconSize as IconSizesKey // medium
        ]
      : iconSizes[
          token.componentSpotIconIconSizeLargeIconSize as IconSizesKey // large
        ];
  const borderRadius =
    size === 'small'
      ? token.componentSpotIconContainerSizeSmallBorderRadius
      : token.componentSpotIconContainerSizeLargeBorderRadius;

  return StyleSheet.create({
    container: {
      alignItems: token.componentSpotIconContainerAlignHorizontal,
      justifyContent: token.componentSpotIconContainerAlignVertical,
      borderRadius: borderRadius,
      backgroundColor:
        color === 'blue'
          ? token.componentSpotIconContainerColorBlueBackgroundColor
          : token.componentSpotIconContainerColorWhiteBackgroundColor,
      height: containerSize,
      width: containerSize,
    } as ViewStyle,
    icon: {
      height: iconSize,
      width: iconSize,
    } as ImageStyle,
  });
};

SpotIcon.displayName = 'SpotIcon';
export {SpotIcon};
