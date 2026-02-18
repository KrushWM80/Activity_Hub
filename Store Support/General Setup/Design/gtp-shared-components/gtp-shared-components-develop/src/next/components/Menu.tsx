import * as React from 'react';
import {
  LayoutChangeEvent,
  LayoutRectangle,
  StyleProp,
  StyleSheet,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Menu';
import DropShadow from 'react-native-drop-shadow';
import RNModal from 'react-native-modal';

import type {CommonViewProps} from '../types/ComponentTypes';
import {colors, resolvePopUpPositionStyle} from '../utils';

// ---------------
// Props
// ---------------
export type MenuPosition =
  | 'bottomLeft'
  | 'bottomRight'
  | 'topLeft'
  | 'topRight';
export type MenuProps = CommonViewProps & {
  /**
   * The content for the menu.
   */
  children: React.ReactNode;
  /**
   * If the menu is open.
   * @default false
   */
  isOpen?: boolean;
  /**
   * The callback fired when the menu requests to close.
   */
  onClose?: (() => void) | undefined;
  /**
   * The position for the menu.
   * @default bottomLeft
   */
  position: MenuPosition;
  /**
   * The trigger for the menu.
   */
  trigger?: React.ReactElement;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * A Menu is a container with items for user-triggered actions.
 *
 * ## Usage
 * ```js
 * import {IconButton, Menu} from '@walmart/gtp-shared-components`;
 *
 * const [isOpen, setIsOpen] = React.useState(false);
 *
 * <Menu
 *   isOpen={isOpen}
 *   onClose={() => setIsOpen(false)}
 *   position="bottomLeft"
 *   trigger={<IconButton icon="more" onPress={() => setIsOpen(true)} />}
 * >
 *   <MenuItem>Item 1</MenuItem>
 *   <MenuItem>Item 2</MenuItem>
 * </Menu>
 * ```
 */
const Menu: React.FC<MenuProps> = (props) => {
  const {
    children,
    UNSAFE_style,
    isOpen = false,
    onClose,
    position = 'bottomLeft',
    trigger,
    ...rest
  } = props;

  let triggerRef = React.useRef<View | null>(null).current;

  const [menuLayout, setMenuLayout] = React.useState<
    LayoutRectangle | undefined
  >();

  const [modalPositionStyle, setModalPositionStyle] = React.useState<
    ViewStyle | undefined
  >();

  const containerOffset = (_position: MenuPosition) => {
    switch (_position) {
      case 'bottomLeft':
        return token.componentMenuLayoutContainerPositionBottomLeftOffsetTop; //8
      case 'bottomRight':
        return token.componentMenuLayoutContainerPositionBottomRightOffsetTop; //8
      case 'topLeft':
        return token.componentMenuLayoutContainerPositionBottomLeftOffsetTop; //8
      case 'topRight':
        return token.componentMenuLayoutContainerPositionBottomRightOffsetTop; //8
    }
  };

  // Modal position depends on layout async calls, if not calculated yet
  // set style opacity: 0 to hide it till completed.
  const hideIfModalPositionNotReady = (): ViewStyle => {
    if (!modalPositionStyle) {
      return {opacity: 0};
    } else {
      return {};
    }
  };

  React.useEffect(() => {
    if (isOpen) {
      triggerRef?.measure((x, y, width, height, pageX, pageY) => {
        if (menuLayout) {
          const distanceY =
            token.componentMenuContainerStateExitActivePositionTopTranslateY; // 8,
          const distanceX = 10; //10
          const resolvedStyle = resolvePopUpPositionStyle(
            position,
            pageX,
            pageY,
            width,
            height,
            menuLayout.width,
            menuLayout.height,
            containerOffset(position), //8
          );
          let adjustedMenuStyle;
          switch (position) {
            case 'bottomLeft':
              adjustedMenuStyle = {
                left: resolvedStyle?.left + distanceX,
                top: resolvedStyle?.top - distanceY,
              };
              break;
            case 'bottomRight':
              adjustedMenuStyle = {
                left: resolvedStyle?.left - distanceX,
                top: resolvedStyle?.top - distanceY,
              };
              break;
            case 'topLeft':
              adjustedMenuStyle = {
                left: resolvedStyle?.left + distanceX,
                top: resolvedStyle?.top + distanceY,
              };
              break;
            case 'topRight':
              adjustedMenuStyle = {
                left: resolvedStyle?.left - distanceX,
                top: resolvedStyle?.top + distanceY,
              };
              break;
            default:
              adjustedMenuStyle = resolvedStyle;
              break;
          }

          setModalPositionStyle(adjustedMenuStyle);
        }
      });
    }
  }, [position, triggerRef, isOpen, menuLayout]);

  // ---------------
  // Rendering
  // ---------------
  return (
    <>
      <View
        testID={`${Menu.displayName}-trigger`}
        ref={(element) => (triggerRef = element)}>
        {trigger}
      </View>
      <RNModal
        testID={`${Menu.displayName}`}
        onLayout={(event: LayoutChangeEvent) => {
          const layout = event.nativeEvent.layout;
          setMenuLayout(layout);
        }}
        style={[ss.container, modalPositionStyle, UNSAFE_style]}
        isVisible={isOpen}
        onBackdropPress={() => onClose?.()}
        backdropColor="transparent"
        animationIn="fadeIn"
        animationInTiming={500} // @cory no LD token for animation timing in/out
        animationOut="fadeOut"
        animationOutTiming={500} // @cory no LD token for animation timing in/out
        useNativeDriver={true}
        hideModalContentWhileAnimating={true} // Fixes flicker bug when useNativeDriver: https://github.com/react-native-modal/react-native-modal/issues/268#issuecomment-494768894
        {...rest}>
        <DropShadow style={ss.outerShadow}>
          <DropShadow style={[ss.innerShadow, hideIfModalPositionNotReady()]}>
            <View testID={`${Menu.displayName}_container`} style={ss.content}>
              {children}
            </View>
          </DropShadow>
        </DropShadow>
      </RNModal>
    </>
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  container: {
    position: 'absolute',
    margin: 0, // Removes default margin on react-native-modal
    zIndex: parseInt(token.componentMenuLayoutContainerZIndex, 10), // @cory should be number instead of string // 300
  },

  outerShadow: {
    // Extracted from token.componentMenuContainerElevation
    //{"blurRadius": "10px", "color": "rgba(0, 0, 0, 0.15)", "offsetX": 0, "offsetY": "5px", "spreadRadius": "3px"}
    shadowColor: colors.black,
    shadowOpacity: 0.15,
    shadowRadius: 10,
    shadowOffset: {
      width: 0, // offsetX
      height: 5, // offsetY
    },
  },
  innerShadow: {
    // Extracted from token.componentMenuContainerElevation
    //{"blurRadius": "4px", "color": "rgba(0, 0, 0, 0.10)", "offsetX": 0, "offsetY": "-1px", "spreadRadius": 0}
    shadowColor: colors.black,
    shadowOpacity: 0.1,
    shadowRadius: 4,
    shadowOffset: {
      width: 0, // offsetX
      height: -1, // offsetY
    },
  },
  content: {
    backgroundColor: token.componentMenuContainerBackgroundColor,
    borderRadius: token.componentMenuContainerBorderRadius,
    paddingHorizontal: token.componentMenuContainerPaddingHorizontal, //0
    paddingVertical: token.componentMenuContainerPaddingVertical, //8
  },
});

Menu.displayName = 'Menu';
export {Menu};
