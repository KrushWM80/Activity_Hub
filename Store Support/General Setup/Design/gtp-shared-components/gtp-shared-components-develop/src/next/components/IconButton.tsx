import * as React from 'react';
import {
  FlexStyle,
  GestureResponderEvent,
  Pressable,
  StyleProp,
  StyleSheet,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/IconButton';
import {Icons, IconSize} from '@walmart/gtp-shared-icons';

import {CommonPressableProps} from '../types/ComponentTypes';
import {a11yRole} from '../utils';
// ---------------
// Props
// ---------------
export type IconButtonSize = 'large' | 'medium' | 'small';
type LinkInteractionState = 'default' | 'disabled';

export type IconButtonProps = Omit<
  CommonPressableProps,
  'onPress' | 'disabled' | 'color'
> & {
  /**
   * The callback fired when the link is pressed.
   */
  onPress: (event: GestureResponderEvent) => void;

  /**
   * The accessibility label for the icon button.
   */
  a11yLabel?: string;
  /**
   * The content for the icon button.
   * Typically an icon e.g. <strong>\<Icons.PlusIcon \/\></strong>
   * It is marked as optional for backwards compatibility only
   */
  children?: React.ReactElement;

  /**
   * Whether the icon button is disabled.
   * @default false
   */
  disabled?: boolean;
  /**
   * The size for the icon button.
   * Valid values: <strong>'large' | 'medium' |  'small'</strong>.
   * @default small
   */
  size?: IconButtonSize;
  /**
   * If provided, the additional style to provide to the root element.
   * Note: this property is prefixed with `UNSAFE` as its use often
   * results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
  /**
   * Undocumented prop (this is not in the LD3 specs)
   * Change the icon color
   * @ignore
   */
  color?: string;
  /**
   * Undocumented prop (this is not in the LD3 specs)
   * Change the icon disabled color
   * @ignore
   */
  disabledColor?: string;
  /**
   * @deprecated it has no effect
   */
  type?: string;
  /**
   * @deprecated use <strong>children</strong> prop instead
   */
  icon?: React.ReactElement;
};

/**
 * This button is an action that allows adding content into another flow or screen.
 *
 * ## Usage
 * ```js
 * import {Icons, IconButton} from '@walmart/gtp-shared-components';
 *
 * <IconButton
 *   size="small"
 *   icon={<Icons.HomeIcon />}
 *   onPress={() => {}}
 * />
 * <IconButton
 *   size="medium"
 *   icon={<Icons.HomeIcon />}
 *   onPress={() => {}}
 * />
 * <IconButton
 *   size="large"
 *   icon={<Icons.HomeIcon />}
 *   onPress={() => {}}
 * />
 * <IconButton
 *   size="large"
 *   icon={<Icons.HomeIcon />}
 *   onPress={() => {}}
 *   UNSAFE_style={{
 *     backgroundColor: 'yellow',
 *     height: 42,
 *     width: 42,
 *     borderRadius: 21,
 *   }}
 * />
 * ```
 */
const IconButton: React.FC<IconButtonProps> = (props: IconButtonProps) => {
  const {
    children,
    icon,
    size = 'small',
    disabled = false,
    UNSAFE_style,
    onPress,
    ...rest
  } = props;

  const [interactionState, setInteractionState] =
    React.useState<LinkInteractionState>('default');

  // ---------------
  // Styles
  // ---------------
  const resolveIconSize = (_size: IconButtonSize): IconSize => {
    switch (_size) {
      case 'small':
        return token.componentIconButtonIconSizeSmallIconSize as IconSize;
      case 'medium':
        return token.componentIconButtonIconSizeMediumIconSize as IconSize;
      case 'large':
        return token.componentIconButtonIconSizeLargeIconSize as IconSize;
      default:
        return token.componentIconButtonIconSizeSmallIconSize as IconSize;
    }
  };

  const resolveIconColor = (pressed: boolean): string => {
    if (pressed) {
      return token.componentIconButtonIconIconColorActive; // "#000"
    } else if (interactionState === 'disabled') {
      return (
        rest.disabledColor ?? token.componentIconButtonIconIconColorDisabled // "#babbbe"
      );
    } else {
      return rest.color ?? token.componentIconButtonIconIconColorDefault; // "#000"
    }
  };

  const defaultContainerStyle = [
    ss(size).container,
    {
      backgroundColor: disabled
        ? token.componentIconButtonContainerBackgroundColorDisabled // "transparent"
        : token.componentIconButtonContainerBackgroundColorDefault, // "transparent"
      borderColor: disabled
        ? token.componentIconButtonContainerBorderColorDisabled // "transparent",
        : token.componentIconButtonContainerBorderColorDefault, // "transparent",
      borderWidth: disabled
        ? token.componentIconButtonContainerBorderWidthDisabled // 0,
        : token.componentIconButtonContainerBorderWidthDefault, // 0,
    },
    UNSAFE_style,
  ];

  // Interactions
  // ---------------
  React.useEffect(() => {
    if (disabled) {
      setInteractionState('disabled');
    } else {
      setInteractionState('default');
    }
  }, [disabled]);

  const handleOnPress = (event: GestureResponderEvent): void => {
    if (interactionState !== 'disabled') {
      onPress(event);
    }
  };

  // ---------------
  // Rendering
  // ---------------
  // For backwards compatibility, render icon if provided
  const renderChildren = (pressed: boolean) => {
    let element;
    if (children && React.isValidElement(children)) {
      element = children as React.ReactElement;
    } else if (icon) {
      element = icon;
    } else {
      element = <Icons.CloseIcon />;
    }
    return (
      <>
        {React.cloneElement(element, {
          size: element?.props?.size ?? resolveIconSize(size),
          color: element?.props?.color ?? resolveIconColor(pressed),
        })}
      </>
    );
  };

  return (
    <Pressable
      accessibilityRole={a11yRole('imagebutton')}
      accessibilityState={{disabled}}
      testID={IconButton.displayName}
      style={({pressed}) => {
        if (pressed) {
          return [ss(size).container, UNSAFE_style, ss(size).containerPressed];
        }
        return defaultContainerStyle;
      }}
      onPress={handleOnPress}
      disabled={disabled}
      {...rest}>
      {({pressed}) => renderChildren(pressed)}
    </Pressable>
  );
};

// ---------------
// Stylesheet
// ---------------
const ss = (size: IconButtonSize) => {
  return StyleSheet.create({
    container: {
      justifyContent:
        token.componentIconButtonContainerAlignHorizontal as Extract<
          FlexStyle,
          'alignItems'
        >, // "center"
      alignItems: token.componentIconButtonContainerAlignVertical as Extract<
        FlexStyle,
        'alignItems'
      >, // "center",
      width:
        size === 'small'
          ? token.componentIconButtonContainerSizeSmallWidth // 32
          : size === 'medium'
          ? token.componentIconButtonContainerSizeMediumWidth // 40
          : token.componentIconButtonContainerSizeLargeWidth, // 48
      height:
        size === 'small'
          ? token.componentIconButtonContainerSizeSmallHeight // 32
          : size === 'medium'
          ? token.componentIconButtonContainerSizeMediumHeight // 40
          : token.componentIconButtonContainerSizeLargeHeight, // 48
      borderRadius:
        size === 'small'
          ? token.componentIconButtonContainerSizeSmallBorderRadius // 1000
          : size === 'medium'
          ? token.componentIconButtonContainerSizeMediumBorderRadius // 1000
          : token.componentIconButtonContainerSizeLargeBorderRadius, // 1000
    },
    containerPressed: {
      backgroundColor: token.componentIconButtonContainerBackgroundColorActive,
      borderWidth: token.componentIconButtonContainerBorderWidthActive, // 1,
    },
  });
};

IconButton.displayName = 'IconButton';
export {IconButton};
