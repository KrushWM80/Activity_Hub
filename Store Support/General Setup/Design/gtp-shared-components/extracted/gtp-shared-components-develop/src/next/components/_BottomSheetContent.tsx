import * as React from 'react';
import {
  findNodeHandle,
  FlexStyle,
  LayoutChangeEvent,
  LayoutRectangle,
  ScrollView,
  StyleProp,
  StyleSheet,
  Text,
  TextStyle,
  TouchableHighlight,
  useWindowDimensions,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/BottomSheet';
// @ts-ignore: internal module
import TextInputState from 'react-native/Libraries/Components/TextInput/TextInputState';
import DeviceInfo from 'react-native-device-info';

import {getFont} from '../../theme/font';
import {calculateBSContainerPercentageValue, colors} from '../utils';

const STATUS_BAR_HEIGHT = 150;

export type BottomSheetContentProps = {
  children: React.ReactNode;
  keyboardShouldPersistTaps: 'never' | 'always' | 'handled';
  componentName: string | undefined;
  headerTitle?: React.ReactNode;
  actions?: React.ReactNode;
  contentExtraStyle?: StyleProp<ViewStyle>;
  actionsExtraStyle?: StyleProp<ViewStyle>;
  childrenContainScrollableComponent?: boolean;
  externalBottomPadding?: number;
  innerScrollViewRef?: React.RefObject<ScrollView>;
  UNSAFE_HEIGHT?: string | number;
};

/**
 * @internal
 */
const _BottomSheetContent = (props: BottomSheetContentProps) => {
  const {
    children,
    keyboardShouldPersistTaps,
    componentName,
    headerTitle,
    actions,
    childrenContainScrollableComponent = false,
    contentExtraStyle = {},
    actionsExtraStyle = {},
    externalBottomPadding = 0, // Usually the keyboard height
    innerScrollViewRef,
    UNSAFE_HEIGHT = 0,
  } = props;

  //validating the ios device contains notch or not then adjusting the style of SafeAreaView
  const safeAreaViewStyle = {marginBottom: DeviceInfo.hasNotch() ? 16 : 12};

  const {height: deviceHeight} = useWindowDimensions();
  const contentPadding = headerTitle
    ? 0 //16
    : token.componentBottomSheetContentPaddingBottomBS;
  const [containerLayout, setContainerLayout] = React.useState<
    LayoutRectangle | undefined
  >();

  const [actionsLayout, setActionsLayout] = React.useState<
    LayoutRectangle | undefined
  >();

  const [containerHeight, setContainerHeight] = React.useState(0);

  React.useEffect(() => {
    /* c8 ignore next */
    const maxHeight = deviceHeight - STATUS_BAR_HEIGHT; // Max Height excludes status bar
    let currentHeight = maxHeight; // Start with max height
    if (UNSAFE_HEIGHT) {
      currentHeight = calculateBSContainerPercentageValue(
        deviceHeight,
        UNSAFE_HEIGHT,
        token.componentBottomSheetContentPaddingBottomBS,
        actionsLayout?.height,
      );
    }
    // External bottom padding is typically keyboardHeight from the calling the parent
    // If it exists subtract that.  If not, subtract just the actions height
    // Actions won't be shown when the keyboard is up
    if (externalBottomPadding > 0) {
      currentHeight -= externalBottomPadding;
    } else {
      if (actionsLayout) {
        currentHeight -=
          actionsLayout.height +
          token.componentBottomSheetContentPaddingBottomBS / 2;
      }
    }

    // Just set height of childrenContainScrollableComponent to maximum allowed height and
    // never try to resize it smaller.  Trying to resize it smaller will cause the scrollable
    // component's parent view to repeatedly call onLayout while the list is populating.  Also,
    // we are strongly recommending they set the contentContainerStyle to 100% height anyway.
    if (childrenContainScrollableComponent) {
      setContainerHeight(currentHeight);
    } else if (containerLayout) {
      // Adjust bottom sheet to content size if smaller than max height
      if (containerLayout.height < currentHeight) {
        currentHeight =
          containerLayout.height +
          token.componentBottomSheetContentPaddingBottomBS;
      }
      setContainerHeight(currentHeight);
    }
  }, [
    deviceHeight,
    actionsLayout,
    containerLayout,
    externalBottomPadding,
    UNSAFE_HEIGHT,
    childrenContainScrollableComponent,
  ]);

  const renderActions = () => {
    return (
      <View
        onLayout={(event: LayoutChangeEvent) => {
          const layout = event.nativeEvent.layout;
          setActionsLayout(layout);
        }}
        testID={componentName + '-actions'}
        style={[ss.actions, safeAreaViewStyle, actionsExtraStyle]}>
        {actions}
      </View>
    );
  };

  /* c8 ignore start */
  React.useEffect(() => {
    if (!process.env.STYLEGUIDIST_ENV) {
      const currentlyFocusedInput = TextInputState.currentlyFocusedInput();
      // Get the scroll responder, either from the innerScrollViewRef if passed or else use the _innerRef
      const responder = innerScrollViewRef
        ? innerScrollViewRef?.current?.getScrollResponder()
        : _innerRef?.current?.getScrollResponder();
      // Check both the input and the scroll responder exist and that the keyboard is up
      if (currentlyFocusedInput && responder && externalBottomPadding !== 0) {
        // Measure the input and scroll to it if it is below the keyboard
        currentlyFocusedInput.measureInWindow(
          (_x: number, y: number, _width: number, height: number) => {
            // Measure the input as it's y position plus its height minus the status bar height
            if (y + height - STATUS_BAR_HEIGHT > externalBottomPadding) {
              responder?.scrollResponderScrollNativeHandleToKeyboard(
                findNodeHandle(currentlyFocusedInput),
                200, // Add extra height to get input comfortably above keyboard
                true,
              );
            }
          },
        );
      }
    }
  }, [externalBottomPadding, innerScrollViewRef]);
  /* c8 ignore stop */

  const _innerRef = React.useRef<ScrollView>(null);

  // To add some bottom spaces when actoion section not available
  const getContentStyle = !actions ? safeAreaViewStyle : {};

  return (
    <View>
      {childrenContainScrollableComponent ? (
        <View
          style={[
            ss.scrollableStyle,
            {height: containerHeight},
            getContentStyle,
            contentExtraStyle,
          ]}>
          {typeof children === 'string' ? (
            <Text style={ss.contentText}>{children}</Text>
          ) : (
            children
          )}
        </View>
      ) : (
        <View
          testID={componentName + '-content'}
          style={[
            ss.content,
            {height: containerHeight},
            getContentStyle,
            contentExtraStyle,
          ]}>
          <ScrollView
            ref={innerScrollViewRef || _innerRef} // If innerScrollViewRef is passed in, use that, otherwise use _innerRef
            style={[ss.innerContent, {paddingBottom: contentPadding}]}
            showsVerticalScrollIndicator={false}
            keyboardShouldPersistTaps={keyboardShouldPersistTaps}>
            <TouchableHighlight
              accessible={false}
              onLayout={(event: LayoutChangeEvent) => {
                const layout = event.nativeEvent.layout;
                setContainerLayout(layout);
              }}>
              {typeof children === 'string' ? (
                <Text style={ss.contentText}>{children}</Text>
              ) : (
                children
              )}
            </TouchableHighlight>
          </ScrollView>
        </View>
      )}
      {externalBottomPadding === 0 && actions && renderActions()}
    </View>
  );
};
_BottomSheetContent.displayName = '_BottomSheetContent';

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  content: {
    width: token.componentBottomSheetLayoutContainerWidth, // "100%",
    alignItems:
      token.componentBottomSheetLayoutContainerAlignHorizontal as Extract<
        FlexStyle,
        'alignItems'
      >, //'center'
  },
  innerContent: {
    width: '100%',
  },
  scrollableStyle: {
    width: token.componentBottomSheetLayoutContainerWidth, // "100%",
  },
  contentText: {
    ...getFont(),
    lineHeight: 20,
    color: colors.black,
  } as TextStyle,
  actions: {
    width: '100%',
    flexDirection: 'row',
    justifyContent:
      //token.componentBottomSheetActionContentAlignHorizontal as Extract  // "end" // Cory, wrong value here
      'flex-end',
    alignItems: 'flex-end',
    borderTopColor: token.componentBottomSheetActionContentBorderColorTop, // "#e3e4e5",
    borderTopWidth: token.componentBottomSheetActionContentBorderWidthTop, // 1,
    paddingVertical: token.componentBottomSheetActionContentPaddingBS, // 16,
  },
});

export {_BottomSheetContent};
