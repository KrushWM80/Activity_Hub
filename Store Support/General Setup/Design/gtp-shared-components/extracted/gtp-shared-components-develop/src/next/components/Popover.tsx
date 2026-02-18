/* c8 ignore start */
import React, {
  FC,
  ReactNode,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react';
import {
  Dimensions,
  LayoutChangeEvent,
  LayoutRectangle,
  StyleProp,
  StyleSheet,
  Text,
  TextStyle,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Popover';
import DropShadow from 'react-native-drop-shadow';
import RNModal from 'react-native-modal';

import {getFont} from '../../theme/font';
import type {CommonViewProps} from '../types/ComponentTypes';
import {
  colors,
  resolveNubbinAlignmentStyle,
  resolvePopUpPositionStyle,
  resolveSpotlightContainerStyle,
} from '../utils';

import {_Triangle, TriangleDirection} from './_Triangle';

export type PopoverPosition =
  | 'bottomCenter'
  | 'bottomLeft'
  | 'bottomRight'
  | 'left'
  | 'right'
  | 'topCenter'
  | 'topLeft'
  | 'topRight';

// ---------------
// Constants
// ---------------
const CONTAINER_OFFSET =
  token.componentPopoverLayoutContainerPositionBottomCenterOffsetTop;
const NUBBIN_OFFSET = token.componentPopoverNubbinPositionBottomLeftOffsetStart;
const NUBBIN_WIDTH = 16;
const MAX_WIDTH = Dimensions.get('screen').width;

// ---------------
// Props
// ---------------
export type PopoverProps = CommonViewProps & {
  /**
   * The content for the popover.
   */
  content: ReactNode;
  /**
   * The trigger for the popover
   */
  children: ReactNode;
  /**
   * If the popover is open.
   *
   * @default false
   */
  isOpen?: boolean;
  /**
   * If the popover has a nubbin.
   *
   * @default false
   */
  hasNubbin?: boolean;
  /**
   * If the popover has a spotlight.
   *
   * @default false
   */
  hasSpotlight?: boolean;
  /**
   * The color of the spotlight background.  Only applied if hasSpotlight is true.
   * @default "#fff"
   */
  spotlightColor?: string;
  /**
   * The callback fired when the popover requests to close.
   */
  onClose?: (() => void) | undefined;
  /**
   * The position for the popover.
   * Valid values: "bottomCenter" | "bottomLeft" | "bottomRight" | "left" | "right" | "topCenter" | "topLeft" | "topRight"
   * @default "bottomCenter"
   */
  position?: PopoverPosition;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Popovers are overlays that display contextual content on demand.
 *
 * ## Usage
 * ```js
 * import {Popover} from '@walmart/gtp-shared-components`;
 *
 * const [isOpen, setIsOpen] = useState(false);
 *
 * <Popover
 *  content={'Example Popover content.'}
 *  isOpen={isOpen}
 *  onClose={() => setIsOpen(false)}
 *  position="topLeft">
 *   <Link
 *     onPress={() => setIsOpen(!isOpen)}>
 *     Top{'\n'}Left
 *   </Link>
 * </Popover>
 * ```
 */
const Popover: FC<PopoverProps> = (props) => {
  const {
    children,
    content,
    hasNubbin = false,
    hasSpotlight = false,
    isOpen = false,
    spotlightColor = '#fff',
    onClose,
    position = 'bottomCenter',
    UNSAFE_style,
    ...rest
  } = props;

  let triggerRef = useRef<View | null>(null).current;

  const [childrenLayout, setChildrenLayout] = useState<
    LayoutRectangle | undefined
  >();
  const [popoverLayout, setPopoverLayout] = useState<
    LayoutRectangle | undefined
  >();

  const [modalPositionStyle, setModalPositionStyle] = useState<
    ViewStyle | undefined
  >();

  const resolveTriangle = () => {
    let direction: TriangleDirection = 'up',
      width = 16,
      height = 8,
      color = token.componentPopoverNubbinBackgroundColor, // "#fff"
      style = {};

    switch (position) {
      case 'right':
        direction = 'left';
        width = 8;
        height = 16;
        break;
      case 'left':
        direction = 'right';
        width = 8;
        height = 16;
        break;
      case 'topRight':
        direction = 'down';
        style = {
          marginLeft: token.componentPopoverNubbinPositionTopRightOffsetEnd, // 24
        };
        break;
      case 'topCenter':
        direction = 'down';
        break;
      case 'topLeft':
        direction = 'down';
        style = {
          marginRight: token.componentPopoverNubbinPositionTopLeftOffsetStart, // 24
        };
        break;
      case 'bottomRight':
        style = {
          marginLeft: token.componentPopoverNubbinPositionBottomRightOffsetEnd, // 24
        };
        break;
      case 'bottomLeft':
        style = {
          marginRight:
            token.componentPopoverNubbinPositionBottomLeftOffsetStart, // 24
        };
        break;
      case 'bottomCenter':
      default:
        break; // use defaults
    }

    return (
      <_Triangle
        width={width}
        height={height}
        direction={direction}
        color={color}
        UNSAFE_style={style}
      />
    );
  };

  const handleContentStyle = () => {
    if (popoverLayout) {
      let left;
      let right;
      if (popoverLayout.x < 0) {
        left = Math.abs(popoverLayout.x) + 10;
      } else if (popoverLayout.x + popoverLayout.width > MAX_WIDTH) {
        right = popoverLayout.x + popoverLayout.width + 10 - MAX_WIDTH;
      }

      return {left, right};
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

  useEffect(() => {
    if (isOpen) {
      triggerRef?.measure((x, y, width, height, pageX, pageY) => {
        if (popoverLayout) {
          const resolvedStyle = resolvePopUpPositionStyle(
            position,
            pageX,
            pageY,
            width,
            height,
            popoverLayout.width,
            popoverLayout.height,
            CONTAINER_OFFSET,
            NUBBIN_OFFSET,
            NUBBIN_WIDTH,
            hasSpotlight,
          );
          setModalPositionStyle(resolvedStyle);
        }
      });
    }
  }, [position, triggerRef, isOpen, popoverLayout, hasSpotlight]);

  const spotlightContainerStyle = useMemo(
    () => [
      {
        backgroundColor: spotlightColor,
        height: childrenLayout?.height,
        width: childrenLayout?.width,
      },
      position !== 'left' && position !== 'right' ? {flex: 1} : undefined,
      resolveSpotlightContainerStyle(
        position,
        childrenLayout,
        NUBBIN_WIDTH,
        NUBBIN_OFFSET,
      ),
    ],
    [position, childrenLayout, spotlightColor],
  );

  // ---------------
  // Rendering
  // ---------------
  return (
    <>
      <RNModal
        testID={Popover.displayName}
        onLayout={(event: LayoutChangeEvent) => {
          const layout = event.nativeEvent.layout;
          setPopoverLayout(layout);
        }}
        style={[ss.container, modalPositionStyle, UNSAFE_style]}
        isVisible={isOpen}
        onBackdropPress={() => onClose?.()}
        backdropColor={hasSpotlight ? undefined : 'transparent'}
        animationIn="fadeIn"
        animationInTiming={500} // @cory no LD token for animation timing in/out
        animationOut="fadeOut"
        animationOutTiming={500} // @cory no LD token for animation timing in/out
        useNativeDriver={true}
        hideModalContentWhileAnimating={true} // Fixes flicker bug when useNativeDriver: https://github.com/react-native-modal/react-native-modal/issues/268#issuecomment-494768894
        {...rest}>
        <DropShadow style={ss.outerShadow}>
          <DropShadow
            testID={Popover.displayName + '-container'}
            style={[
              ss.innerShadow,
              resolveNubbinAlignmentStyle(position),
              hideIfModalPositionNotReady(),
            ]}>
            {hasSpotlight && (
              <View
                testID={Popover.displayName + '-spotlight'}
                onTouchEnd={onClose}
                style={spotlightContainerStyle}>
                {children}
              </View>
            )}
            {hasNubbin && resolveTriangle()}
            <View
              testID={Popover.displayName + '-content'}
              style={[ss.content, handleContentStyle()]}>
              {typeof content === 'string' ? (
                <Text style={ss.contentText}>{content}</Text>
              ) : (
                content
              )}
            </View>
          </DropShadow>
        </DropShadow>
      </RNModal>

      <View
        testID={Popover.displayName + '-trigger'}
        ref={(element) => (triggerRef = element)}
        onLayout={(event) => setChildrenLayout(event.nativeEvent.layout)}>
        {children}
      </View>
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
    zIndex: parseInt(token.componentPopoverLayoutContainerZIndex, 10), // @cory should be number instead of string
  },
  outerShadow: {
    // Extracted from token.componentPopoverContainerElevation
    shadowColor: colors.black, // rgba(0, 0, 0, 0.15)
    shadowOpacity: 0.15, // rgba(0, 0, 0, 0.15)
    shadowRadius: 5, // blurRadius":"5px"
    shadowOffset: {
      width: 0, // offsetX
      height: 3, // offsetY
    },
  },
  innerShadow: {
    // Extracted from token.componentPopoverContainerElevation
    shadowColor: colors.black, // rgba(0, 0, 0, 0.15)
    shadowOpacity: 0.1, // rgba(0, 0, 0, 0.15)
    shadowRadius: 3, // blurRadius":"5px"
    shadowOffset: {
      width: 0, // offsetX
      height: -1, // offsetY
    },
  },
  content: {
    minWidth: 100, // At least enough space for nubbin offset
    backgroundColor: token.componentPopoverContainerBackgroundColor, // "#fff"
    borderRadius: token.componentPopoverContainerBorderRadius, // 4
    paddingHorizontal: token.componentPopoverContainerPaddingHorizontal, // 16
    paddingVertical: token.componentPopoverContainerPaddingVertical, // 16
  },
  contentText: {
    ...getFont(),
    lineHeight: 20,
  } as TextStyle,
});

Popover.displayName = 'Popover';
export {Popover};
/* c8 ignore stop */
