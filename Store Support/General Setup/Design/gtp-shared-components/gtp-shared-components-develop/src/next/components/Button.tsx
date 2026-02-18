import * as React from 'react';
import {
  GestureResponderEvent,
  ImageStyle,
  Pressable,
  PressableProps,
  StyleProp,
  StyleSheet,
  Text,
  TextStyle,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Button';

import {getFont, Weights} from '../../theme/font';
import type {CommonPressableProps} from '../types/ComponentTypes';
import {a11yRole} from '../utils';

import {
  _LeadingTrailing as _Leading,
  _LeadingTrailing as _Trailing,
} from './_LeadingTrailing';
import {Spinner, SpinnerColor} from './Spinner';

// ---------------
// Props
// ---------------
export type ButtonVariant =
  | 'destructive'
  | 'primary'
  | 'secondary'
  | 'tertiary';
export type ButtonSize = 'small' | 'medium' | 'large';
type ButtonInteractionState = 'Default' | 'Disabled';

// TODO: check with LD team for combinations of props which should
// prohibited, for example: both leading and trailing passed
export type ButtonProps = Omit<
  CommonPressableProps,
  'hitSlop' | 'onPress' | 'disabled'
> & {
  /**
   * Type of button. Valid values:
   * | 'primary'
   * | 'secondary'
   * | 'tertiary'
   * | 'destructive'
   * @default secondary
   */
  variant?: ButtonVariant;
  /**
   * This Button's string title
   */
  children?: React.ReactNode;
  /**
   * This Button's press event handler
   */
  onPress: (event: GestureResponderEvent) => void;
  /**
   * Size of the button;
   * Valid values: 'small' | 'medium' | 'large'
   * @default small
   */
  size?: ButtonSize;
  /**
   * The leading content for the button.
   * (typically an icon)
   */
  leading?: React.ReactElement;
  /**
   * The trailing content for the button.
   * (typically an icon)
   */
  trailing?: React.ReactElement;
  /**
   * Whether this Button is disabled
   * @default false
   */
  disabled?: boolean;
  /**
   * Whether this Button should show the loading indicator
   * @default false
   */
  isLoading?: boolean;
  /**
   * Whether to display this Button full-width
   * @default false
   */
  isFullWidth?: boolean;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   *
   * NOTE: for this component, you can also pass the following to customize the title:
   *
   * fontSize, fontWeight, lineHeight, color
   *
   * Again, we strongly recommend against this, since it deviates from the LD specs.
   */
  UNSAFE_style?: StyleProp<ViewStyle> & Partial<TextStyle>;
  /**
   * Allows defining a larger area for press
   */
  hitSlop?: Extract<PressableProps, 'hitSlop'>;
};

/**
 * A button allows users to take actions and make choices, with a single
 * press or a tap. Buttons are used as calls-to-action (CTA) across the experience.
 * They are organized in the order or their importance:
 * <strong>variant: primary, secondary, tertiary</strong>
 *
 * ## Usage
 * ```js
 * import {Button} from '@walmart/gtp-shared-components';
 *
 * <Button
 *   variant="primary"
 *   onPress={() => console.log('Pressed')}
 *   size="small"
 *   isLoading={false}
 * />
 * ```
 */
const Button = React.forwardRef<View, ButtonProps>((props, ref) => {
  const {
    variant = 'secondary',
    children,
    onPress,
    size = 'small',
    leading,
    trailing,
    disabled = false,
    isLoading = false,
    isFullWidth = false,
    UNSAFE_style,
    hitSlop,
    ...rest
  } = props;

  const [interactionState, setInteractionState] =
    React.useState<ButtonInteractionState>('Default');

  // ---------------
  // Interactions
  // ---------------
  const handlePress = (event: GestureResponderEvent) => {
    if (!isLoading) {
      if (!disabled) {
        onPress(event);
      }
    }
  };

  React.useEffect(() => {
    if (disabled) {
      setInteractionState('Disabled');
    } else {
      setInteractionState('Default');
    }
  }, [disabled]);

  // ---------------
  // Styles
  // ---------------
  let spinnerColor: SpinnerColor;
  if (variant !== 'secondary') {
    spinnerColor = 'white';
  } else {
    spinnerColor = 'gray';
  }
  if (interactionState === 'Disabled') {
    spinnerColor = 'gray';
  }

  const unsafeExtraFontStyle = React.useMemo(() => {
    let retObject = {};
    const fontSize = (UNSAFE_style as TextStyle)?.fontSize;
    const fontWeight = (UNSAFE_style as TextStyle)?.fontWeight;
    const lineHeight = (UNSAFE_style as TextStyle)?.lineHeight;
    const color = (UNSAFE_style as TextStyle)?.color;
    if (fontSize) {
      retObject = {...retObject, fontSize};
    }
    if (fontWeight) {
      retObject = {...retObject, fontWeight};
    }
    if (lineHeight) {
      retObject = {...retObject, lineHeight};
    }
    if (color) {
      retObject = {...retObject, color};
    }
    return retObject;
  }, [UNSAFE_style]);

  // Three dimensions which determine styling:
  // - elements that need styles (container, text, image, spinner)
  // - interaction states (default, pressed, disabled)
  // - incoming props (variant, size, isFullWidth)
  // e.g. [primaryDefaultContainer, smallContainer]
  const resolveInnerContainerStyle = React.useCallback(() => {
    return [
      styles.innerContainer,
      styles[
        `${variant}${interactionState}InnerContainer` as keyof typeof styles
      ],
      styles[`${size}InnerContainer` as keyof typeof styles],
      isFullWidth ? styles.fullWidthInnerContainer : {},
    ];
  }, [variant, interactionState, size, isFullWidth]);

  const resolveTextStyle = React.useCallback(() => {
    return [
      styles.text,
      styles[`${variant}${interactionState}Text` as keyof typeof styles],
      styles[`${size}Text` as keyof typeof styles],
      isFullWidth ? styles.textFullWidth : {},
      isLoading ? styles.transparent : {},
      unsafeExtraFontStyle,
    ];
  }, [
    interactionState,
    isFullWidth,
    isLoading,
    size,
    unsafeExtraFontStyle,
    variant,
  ]);

  const resolveImageStyle = React.useCallback(() => {
    return [
      styles[`${variant}${interactionState}Image`] ?? {},
      styles[`${size}Image` as keyof typeof styles],
    ] as ImageStyle;
  }, [variant, interactionState, size]);

  const resolveSpinnerContainerStyle = React.useCallback(() => {
    return [
      styles.spinnerContainer,
      styles[`${size}SpinnerContainer` as keyof typeof styles],
    ] as ViewStyle;
  }, [size]);

  // --------------
  // Rendering
  // --------------
  const renderLeading = (pressed: boolean, node: React.ReactNode) => {
    let lStyle = [styles.leading, resolveImageStyle()];
    if (pressed) {
      lStyle = [lStyle, styles[`${variant}PressedImage`]];
    }
    return (
      <_Leading
        node={node}
        iconProps={{
          UNSAFE_style: lStyle as ImageStyle,
        }}
      />
    );
  };

  const renderTrailing = (pressed: boolean, node: React.ReactNode) => {
    let tStyle = [styles.trailing, resolveImageStyle()];
    if (pressed) {
      tStyle = [tStyle, styles[`${variant}PressedImage`]];
    }
    return (
      <_Trailing
        node={node}
        iconProps={{
          UNSAFE_style: tStyle as ImageStyle,
        }}
      />
    );
  };

  const renderLoading = () => {
    return (
      <View style={resolveSpinnerContainerStyle()}>
        {isLoading && <Spinner size="small" color={spinnerColor} />}
      </View>
    );
  };

  const renderButtonText = (pressed: boolean) => {
    let tStyle = resolveTextStyle();
    if (pressed) {
      tStyle = [...resolveTextStyle(), styles[`${variant}PressedText`]];
    }
    return (
      <Text numberOfLines={1} ellipsizeMode="tail" style={tStyle}>
        {children}
      </Text>
    );
  };

  return (
    <Pressable
      ref={ref}
      accessibilityRole={a11yRole('button')}
      accessibilityState={{disabled, busy: isLoading}}
      testID={Button.displayName}
      onPress={handlePress}
      hitSlop={hitSlop}
      style={[styles.container, UNSAFE_style]}
      disabled={disabled || isLoading}
      {...rest}>
      {({pressed}) => (
        <View
          style={
            pressed
              ? [
                  resolveInnerContainerStyle(),
                  styles[`${variant}PressedInnerContainer`],
                ]
              : resolveInnerContainerStyle()
          }>
          {leading ? renderLeading(pressed, leading) : null}
          {renderButtonText(pressed)}
          {trailing ? renderTrailing(pressed, trailing) : null}
          {renderLoading()}
        </View>
      )}
    </Pressable>
  );
});

// ---------------
// StyleSheet
// ---------------
const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'center',
    overflow: 'visible',
  },
  innerContainer: {
    flexShrink: 1,
    flexDirection: 'row',
    borderRadius: token.componentButtonContainerBorderRadius,
    alignItems: token.componentButtonContainerAlignVertical,
    justifyContent: token.componentButtonContainerAlignHorizontal,
    overflow: 'hidden',
    borderWidth: 1,
  } as TextStyle,
  fullWidthInnerContainer: {
    flex: 1,
  },
  leading: {
    marginRight: token.componentButtonLeadingIconMarginEnd,
  },
  trailing: {
    marginLeft: token.componentButtonTrailingIconMarginStart,
  },
  text: {
    ...getFont('bold'),
    textAlign: 'center',
  } as TextStyle,
  textFullWidth: {
    flexGrow: 0,
  },
  spinnerContainer: {
    position: 'absolute',
    alignSelf: 'center',
    width: '100%',
    left: 16,
  },
  transparent: {
    opacity: 0,
  },
  //------------------------
  // Sizes
  //------------------------
  // Small
  //------------------------
  smallInnerContainer: {
    paddingHorizontal: token.componentButtonContainerSizeSmallPaddingHorizontal,
    paddingVertical: token.componentButtonContainerSizeSmallPaddingVertical,
  },
  smallText: {
    fontSize: token.componentButtonTextLabelSizeSmallFontSize,
    lineHeight: token.componentButtonTextLabelSizeSmallLineHeight,
  },
  smallImage: {},
  smallSpinner: {},
  smallSpinnerContainer: {
    left: 15,
    marginVertical: 3,
  },
  //------------------------
  // Medium
  //------------------------
  mediumInnerContainer: {
    paddingHorizontal:
      token.componentButtonContainerSizeMediumPaddingHorizontal,
    paddingVertical: token.componentButtonContainerSizeMediumPaddingVertical,
  },
  mediumText: {
    fontSize: token.componentButtonTextLabelSizeMediumFontSize,
    lineHeight: token.componentButtonTextLabelSizeMediumLineHeight,
  },
  mediumImage: {},
  mediumSpinner: {},
  mediumSpinnerContainer: {
    left: 22,
    marginVertical: 3,
  },
  //------------------------
  // Large
  //------------------------
  largeInnerContainer: {
    paddingHorizontal: token.componentButtonContainerSizeLargePaddingHorizontal,
    paddingVertical: token.componentButtonContainerSizeLargePaddingVertical,
  },
  largeText: {
    fontSize: token.componentButtonTextLabelSizeLargeFontSize,
    lineHeight: token.componentButtonTextLabelSizeLargeLineHeight,
  },
  largeImage: {},
  largeSpinner: {},
  largeSpinnerContainer: {
    left: 22,
    marginVertical: 3,
  },
  //------------------------
  // Primary
  //------------------------
  primaryDefaultInnerContainer: {
    backgroundColor:
      token.componentButtonContainerVariantPrimaryBackgroundColorDefault,
    borderColor:
      token.componentButtonContainerVariantPrimaryBackgroundColorDefault,
  },
  primaryDefaultText: {
    color: token.componentButtonTextLabelVariantPrimaryTextColorDefault,
    ...getFont(
      token.componentButtonTextLabelVariantPrimaryFontWeight.toString() as Weights,
    ),
  } as TextStyle,
  primaryDefaultImage: {
    tintColor: token.componentButtonTextLabelVariantPrimaryTextColorDefault,
  },
  primaryDefaultSpinner: {
    color: token.componentButtonTextLabelVariantPrimaryTextColorDefault,
  },
  primaryDefaultSpinnerContainer: {},

  primaryPressedInnerContainer: {
    backgroundColor:
      token.componentButtonContainerVariantPrimaryBackgroundColorActive,
  },
  primaryPressedText: {
    color: token.componentButtonTextLabelVariantPrimaryTextColorActive,
  },
  primaryPressedImage: {
    tintColor: token.componentButtonTextLabelVariantPrimaryTextColorActive,
  },
  primaryPressedSpinner: {},
  primaryPressedSpinnerContainer: {},

  primaryDisabledInnerContainer: {
    backgroundColor:
      token.componentButtonContainerVariantPrimaryBackgroundColorDisabled,
    borderColor:
      token.componentButtonContainerVariantPrimaryBackgroundColorDisabled,
  },
  primaryDisabledText: {
    color: token.componentButtonTextLabelVariantPrimaryTextColorDisabled,
    ...getFont(
      token.componentButtonTextLabelVariantPrimaryFontWeight.toString() as Weights,
    ),
  } as TextStyle,
  primaryDisabledImage: {
    tintColor: token.componentButtonTextLabelVariantPrimaryTextColorDisabled,
  },
  primaryDisabledSpinner: {
    color: token.componentButtonTextLabelVariantPrimaryTextColorDisabled,
  },
  primaryDisabledSpinnerContainer: {},

  //------------------------
  // Secondary
  //------------------------
  secondaryDefaultInnerContainer: {
    borderWidth:
      token.componentButtonContainerVariantSecondaryBorderWidthDefault,
    borderColor:
      token.componentButtonContainerVariantSecondaryBorderColorDefault,
    backgroundColor:
      token.componentButtonContainerVariantSecondaryBackgroundColorDefault,
  },
  secondaryDefaultText: {
    color: token.componentButtonTextLabelVariantSecondaryTextColorDefault,
    ...getFont(
      token.componentButtonTextLabelVariantSecondaryFontWeight.toString() as Weights,
    ),
  } as TextStyle,
  secondaryDefaultImage: {
    tintColor: token.componentButtonTextLabelVariantSecondaryTextColorDefault,
  },
  secondaryDefaultSpinner: {
    color: token.componentButtonTextLabelVariantSecondaryTextColorDefault,
  },
  secondaryDefaultSpinnerContainer: {},

  secondaryPressedInnerContainer: {
    borderWidth:
      // token.componentButtonContainerVariantSecondaryBorderWidthActive, // TODO: this doesn't seem to have the right value, Cory to check
      1,
    backgroundColor:
      token.componentButtonContainerVariantSecondaryBackgroundColorActive,
    borderColor:
      token.componentButtonContainerVariantSecondaryBorderColorActive,
  },
  secondaryPressedText: {
    color: token.componentButtonTextLabelVariantSecondaryTextColorActive,
  },
  secondaryPressedImage: {
    tintColor: token.componentButtonTextLabelVariantSecondaryTextColorActive,
  },
  secondaryPressedSpinner: {},
  secondaryPressedSpinnerContainer: {},

  secondaryDisabledInnerContainer: {
    borderColor:
      token.componentButtonContainerVariantSecondaryBorderColorDisabled,
    backgroundColor:
      token.componentButtonContainerVariantSecondaryBackgroundColorDisabled,
  },
  secondaryDisabledText: {
    color: token.componentButtonTextLabelVariantSecondaryTextColorDisabled,
  },
  secondaryDisabledImage: {
    tintColor: token.componentButtonTextLabelVariantSecondaryTextColorDisabled,
  },
  secondaryDisabledSpinner: {
    color: token.componentButtonTextLabelVariantSecondaryTextColorDisabled,
  },
  secondaryDisabledSpinnerContainer: {},

  //------------------------
  // Tertiary
  //------------------------
  tertiaryDefaultInnerContainer: {
    backgroundColor:
      token.componentButtonContainerVariantTertiaryBackgroundColor,
    borderWidth: 0,
  },
  tertiaryDefaultText: {
    ...getFont(
      token.componentButtonTextLabelVariantTertiaryFontWeight.toString() as Weights,
    ),
    fontSize: 16,
    lineHeight: 24,
    textAlign: 'center',
    color: token.componentButtonTextLabelVariantTertiaryTextColorDefault,
    textDecorationLine:
      token.componentButtonTextLabelVariantTertiaryTextDecorationDefault,
  } as TextStyle,
  tertiaryDefaultImage: {},
  tertiaryDefaultSpinner: {},
  tertiaryDefaultSpinnerContainer: {},

  tertiaryPressedInnerContainer: {
    borderWidth: 0,
  },
  tertiaryPressedText: {
    color: token.componentButtonTextLabelVariantTertiaryTextColorActive,
    textDecorationLine:
      token.componentButtonTextLabelVariantTertiaryTextDecorationActive,
  } as TextStyle,
  tertiaryPressedImage: {},
  tertiaryPressedSpinner: {},

  tertiaryDisabledInnerContainer: {
    borderWidth: 0,
  },
  tertiaryDisabledText: {
    color: token.componentButtonTextLabelVariantTertiaryTextColorDisabled,
    textDecorationLine:
      token.componentButtonTextLabelVariantTertiaryTextDecorationDisabled,
  } as TextStyle,
  tertiaryDisabledImage: {},
  tertiaryDisabledSpinner: {},

  //------------------------
  // Destructive
  //------------------------
  destructiveDefaultInnerContainer: {
    backgroundColor:
      token.componentButtonContainerVariantDestructiveBackgroundColorDefault,
    borderColor:
      token.componentButtonContainerVariantDestructiveBackgroundColorDefault,
  },
  destructiveDefaultText: {
    color: token.componentButtonTextLabelVariantDestructiveTextColorDefault,
    ...getFont(
      token.componentButtonTextLabelVariantDestructiveFontWeight.toString() as Weights,
    ),
  } as TextStyle,
  destructiveDefaultImage: {
    tintColor: token.componentButtonTextLabelVariantDestructiveTextColorDefault,
  },
  destructiveDefaultSpinner: {
    color: token.componentButtonTextLabelVariantDestructiveTextColorDefault,
  },
  destructiveDefaultSpinnerContainer: {},

  destructivePressedInnerContainer: {
    backgroundColor:
      token.componentButtonContainerVariantDestructiveBackgroundColorActive,
  },
  destructivePressedText: {
    color: token.componentButtonTextLabelVariantDestructiveTextColorActive,
  },
  destructivePressedImage: {
    tintColor: token.componentButtonTextLabelVariantDestructiveTextColorActive,
  },
  destructivePressedSpinner: {},
  destructivePressedSpinnerContainer: {},

  destructiveDisabledInnerContainer: {
    backgroundColor:
      token.componentButtonContainerVariantDestructiveBackgroundColorDisabled,
    borderColor:
      token.componentButtonContainerVariantDestructiveBackgroundColorDisabled,
  },
  destructiveDisabledText: {
    color: token.componentButtonTextLabelVariantDestructiveTextColorDisabled,
  },
  destructiveDisabledImage: {
    tintColor:
      token.componentButtonTextLabelVariantDestructiveTextColorDisabled,
  },
  destructiveDisabledSpinner: {
    color: token.componentButtonTextLabelVariantDestructiveTextColorDisabled,
  },
  destructiveDisabledSpinnerContainer: {},
});

Button.displayName = 'Button';
export {Button};
