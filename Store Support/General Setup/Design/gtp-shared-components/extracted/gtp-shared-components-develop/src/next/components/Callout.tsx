import * as React from 'react';
import {
  LayoutChangeEvent,
  LayoutRectangle,
  StyleProp,
  StyleSheet,
  Text,
  TextStyle,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Callout';
import DropShadow from 'react-native-drop-shadow';
import RNModal from 'react-native-modal';

import {getFont, Weights} from '../../theme/font';
import type {CommonViewProps} from '../types/ComponentTypes';
import {
  colors,
  resolveNubbinAlignmentStyle,
  resolvePopUpPositionStyle,
} from '../utils';

import {_Triangle, TriangleDirection} from './_Triangle';
import {Link} from './Link';

export type CalloutPosition =
  | 'bottomCenter'
  | 'bottomLeft'
  | 'bottomRight'
  | 'left'
  | 'right'
  | 'topCenter'
  | 'topLeft'
  | 'topRight';

// ---------------
// Props
// ---------------
export type CalloutProps = CommonViewProps & {
  /**
   * The content for the callout.
   */
  content: React.ReactNode;
  /**
   * The trigger for the callout
   */
  children: React.ReactNode;
  /**
   * If the callout is open.
   *
   * @default false
   */
  isOpen?: boolean;
  /**
   * The callback fired when the callout requests to close.
   */
  onClose?: (() => void) | undefined;
  /**
   * The position for the callout.
   * Valid values: "bottomCenter" | "bottomLeft" | "bottomRight" | "left" | "right" | "topCenter" | "topLeft" | "topRight"
   * @default "bottomCenter"
   */
  position?: CalloutPosition;
  /**
   * The text for the close button
   * @default 'Close'
   */
  closeText?: string;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Callouts are overlays that display contextual content on demand.
 *
 * ## Usage
 * ```js
 * import {Callout} from '@walmart/gtp-shared-components`;
 *
 * const [isOpen, setIsOpen] = React.useState(false);
 *
 * <Callout
 *   content={'Example Callout content.'}
 *   isOpen={isOpen}
 *   onClose={() => setIsOpen(false)}
 *   position="bottomRight">
 *   <Link
 *     onPress={() => setIsOpen(false)}>
 *     Bottom{'\n'}Right
 *   </Link>
 * </Callout>
 * ```
 */
const Callout: React.FC<CalloutProps> = (props) => {
  const {
    children,
    content,
    isOpen = false,
    onClose,
    position = 'bottomCenter',
    closeText = 'Close',
    UNSAFE_style,
    ...rest
  } = props;

  let triggerRef = React.useRef<View | null>(null).current;

  const [calloutLayout, setCalloutLayout] = React.useState<
    LayoutRectangle | undefined
  >();

  const [modalPositionStyle, setModalPositionStyle] = React.useState<
    ViewStyle | undefined
  >();

  const resolveTriangle = () => {
    let direction: TriangleDirection = 'up',
      width: number = token.componentCalloutNubbinWidth,
      height: number = token.componentCalloutNubbinHeight / 2,
      color: string = token.componentCalloutNubbinBackgroundColor,
      style = {};

    switch (position) {
      case 'right':
        direction = 'left';
        width = token.componentCalloutNubbinWidth / 2;
        height = token.componentCalloutNubbinHeight;
        break;
      case 'left':
        direction = 'right';
        width = token.componentCalloutNubbinWidth / 2;
        height = token.componentCalloutNubbinHeight;
        break;
      case 'topRight':
        direction = 'down';
        style = {
          marginLeft: token.componentCalloutNubbinPositionTopRightOffsetStart,
        };
        break;
      case 'topCenter':
        direction = 'down';
        break;
      case 'topLeft':
        direction = 'down';
        style = {
          marginRight: token.componentCalloutNubbinPositionTopLeftOffsetEnd,
        };
        break;
      case 'bottomRight':
        style = {
          marginLeft:
            token.componentCalloutNubbinPositionBottomRightOffsetStart,
        };
        break;
      case 'bottomLeft':
        style = {
          marginRight: token.componentCalloutNubbinPositionBottomLeftOffsetEnd,
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
    if (isOpen && calloutLayout) {
      triggerRef?.measure((x, y, width, height, pageX, pageY) => {
        const containerOffset = 4; // @cory token.componentCalloutLayoutContainerPositionBottomOffsetTop is different from Figma
        const nubbinOffset =
          token.componentCalloutNubbinPositionBottomLeftOffsetEnd;
        const nubbinWidth = token.componentCalloutNubbinWidth;
        const resolvedStyle = resolvePopUpPositionStyle(
          position,
          pageX,
          pageY,
          width,
          height,
          calloutLayout.width,
          calloutLayout.height,
          containerOffset,
          nubbinOffset,
          nubbinWidth,
        );
        setModalPositionStyle(resolvedStyle);
      });
    }
  }, [position, triggerRef, isOpen, calloutLayout]);

  // ---------------
  // Rendering
  // ---------------
  return (
    <>
      <View
        testID={Callout.displayName + '-trigger'}
        ref={(element) => (triggerRef = element)}>
        {children}
      </View>
      <RNModal
        testID={Callout.displayName}
        onLayout={(event: LayoutChangeEvent) => {
          const layout = event.nativeEvent.layout;
          setCalloutLayout(layout);
        }}
        style={[ss.container, modalPositionStyle, UNSAFE_style]}
        isVisible={isOpen}
        backdropColor="transparent"
        animationIn="fadeIn"
        animationInTiming={400} // token.componentCalloutContainerStateEnterActiveTransition: 0.2s
        animationOut="fadeOut"
        animationOutTiming={400} // token.componentCalloutContainerStateExitActiveTransition: 0.2s
        useNativeDriver={true}
        hideModalContentWhileAnimating={true} // Fixes flicker bug when useNativeDriver: https://github.com/react-native-modal/react-native-modal/issues/268#issuecomment-494768894
        {...rest}>
        <DropShadow style={ss.outerShadow}>
          <DropShadow
            testID={Callout.displayName + '-container'}
            style={[
              ss.innerShadow,
              resolveNubbinAlignmentStyle(position),
              hideIfModalPositionNotReady(),
            ]}>
            {resolveTriangle()}
            <View
              testID={Callout.displayName + '-content'}
              style={[ss.content]}>
              {typeof content === 'string' ? (
                <Text style={ss.contentText}>{content}</Text>
              ) : (
                content
              )}
              <Link
                color="white" // token.componentCalloutCloseButtonTextColor, can't pass hex to Link color prop
                hitSlop={ss.hitSlop}
                UNSAFE_style={ss.closeButton}
                onPress={() => onClose?.()}
                {...rest}>
                {closeText}
              </Link>
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
    zIndex: parseInt(token.componentCalloutLayoutContainerZIndex, 10), // @cory should be number instead of string
  },
  outerShadow: {
    // Extracted from token.componentCalloutContainerElevation
    shadowColor: colors.black, // rgba(0, 0, 0, 0.15)
    shadowOpacity: 0.15, // rgba(0, 0, 0, 0.15)
    shadowRadius: 5, // blurRadius":"5px"
    shadowOffset: {
      width: 0, // offsetX
      height: 3, // offsetY
    },
  },
  innerShadow: {
    // Extracted from token.componentCalloutContainerElevation
    shadowColor: colors.black, // rgba(0, 0, 0, 0.10)
    shadowOpacity: 0.1, // rgba(0, 0, 0, 0.10)
    shadowRadius: 3, // blurRadius":"5px"
    shadowOffset: {
      width: 0, // offsetX
      height: -1, // offsetY
    },
  },
  content: {
    minWidth: token.componentCalloutContainerWidth,
    backgroundColor: token.componentCalloutContainerBackgroundColor,
    borderRadius: token.componentCalloutContainerBorderRadius,
    paddingVertical: token.componentCalloutContainerPaddingVertical,
  },
  contentText: {
    ...getFont(token.componentCalloutTextLabelFontWeight.toString() as Weights),
    fontSize: token.componentCalloutTextLabelFontSize,
    lineHeight: token.componentCalloutTextLabelLineHeight,
    color: token.componentCalloutTextLabelTextColor,
    paddingHorizontal: token.componentCalloutTextLabelPaddingHorizontal,
    paddingTop: token.componentCalloutTextLabelPaddingTop,
    paddingBottom: token.componentCalloutTextLabelPaddingBottom,
  } as TextStyle,
  closeButton: {
    alignSelf: 'flex-end',
    fontSize: token.componentCalloutCloseButtonFontSize,
    lineHeight: token.componentCalloutCloseButtonLineHeight,
    paddingHorizontal: token.componentCalloutCloseButtonPaddingHorizontal,
  },
  hitSlop: {
    left: 16,
    top: 16,
    right: 16,
    bottom: 16,
  },
});

Callout.displayName = 'Callout';
export {Callout};
