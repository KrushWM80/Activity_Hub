import * as React from 'react';
import {
  Animated,
  Dimensions,
  FlexStyle,
  Keyboard,
  LayoutAnimation,
  LayoutChangeEvent,
  Modal,
  PanResponder,
  Pressable,
  ScrollView,
  StyleProp,
  StyleSheet,
  Text,
  TextStyle,
  useWindowDimensions,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/BottomSheet';
import {Icons} from '@walmart/gtp-shared-icons';

import {getFont, Weights} from '../../theme/font';
import type {
  CommonRNModalBaseProps,
  CommonViewProps,
} from '../types/ComponentTypes';
import {a11yRole, colors, getBSPaddingBottomBasedOnRNVersion} from '../utils';
import {useKeyboard} from '../utils/useKeyboard';

import {_BottomSheetContent} from './_BottomSheetContent';
import {IconButton, IconButtonProps} from './IconButton';

// ---------------
// Props
// ---------------
export type BottomSheetProps = CommonRNModalBaseProps &
  CommonViewProps & {
    /**
     * The actions for the BottomSheet
     * Typically, this will be a ButtonGroup
     *
     * ```
     *  actions={
     *     <ButtonGroup>
     *       <Button variant="tertiary" onPress={handleCancel}>
     *         Cancel
     *       </Button>
     *       <Button variant="primary" onPress={handleContinue}>
     *         Continue
     *       </Button>
     *     </ButtonGroup>
     *   }
     * ```
     */
    actions?: React.ReactNode;
    /**
     * The content of the BottomSheet
     */
    children: React.ReactNode;
    /**
     * The props spread to the BottomSheet's close button
     */
    closeButtonProps?: IconButtonProps;
    /**
     * Whether the BottomSheet is open
     * @default false
     */
    isOpen?: boolean;
    /**
     * The callback fired when the BottomSheet open start.
     */
    onOpen?: () => void;
    /**
     * The callback fired when the BottomSheet open completed.
     */
    onOpened?: () => void;
    /**
     * The callback fired when the BottomSheet requests to close.
     */
    onClose?: () => void;
    /**
     * The callback fired when the BottomSheet close transition has ended.
     */
    onClosed?: () => void;
    /**
     * @deprecated it has no effect. Provided just for API backwards compatibility.
     */
    onBackButtonPress?: (() => void) | undefined;
    /**
     * The title for the BottomSheet
     * If you pass a string, we take care of the styling.
     * If you pass a component, you are responsible for the styling.
     * (Note: this is not recommended to be used. There is an LD ticket in the backlog
     * to investigate this: https://jira.walmart.com/browse/LD-1829
     * Added because of popular demand (e.g. CustomerTransaction/Returns team))
     * For example:
     *
     * ```
     *  title={
     *     <View style={styles.titleContainer}>
     *       <IconButton
     *         size="large"
     *         onPress={() => console.log("Modal action 'Back' was tapped")}
     *         UNSAFE_style={styles.iconButton}>
     *           <ChevronLeftIcon />
     *       </IconButton>
     *       <Text style={styles.title}>Confirmation</Text>
     *     </View>
     *   }
     * ```
     * where styles are:
     *
     * ```
     * titleContainer: {
     *  flexDirection: 'row',
     *  justifyContent: 'space-between',
     *  alignItems: 'center',
     *  paddingRight: '27%',
     * },
     * title: {
     *  ...getFont('700'),
     *  fontSize: 18,
     *  lineHeight: 24,
     *  textAlign: 'center',
     *  color: '#2e2f32',
     * } as TextStyle,
     * iconButton: {
     *  marginLeft: -12,
     * },
     * ```
     */
    title?: React.ReactNode;
    /**
     * Accessibility label for the title, use this to override the title
     * for screen readers. This is useful when the title is a component
     * and you want to provide a different label for screen readers.
     *
     * ```
     * <BottomSheet
     *   title={<View><Text>Confirmation</Text></View>}
     *   accessibilityTitleLabel="Confirmation"
     * />
     * ```
     */
    accessibilityTitleLabel?: string;
    /**
     * If provided, the <strong>style</strong> to provide to the content
     * container inside the BottomSheet.
     * This property is prefixed with <strong>UNSAFE</strong> as its use
     * often results in <strong>unintended side effects</strong>.
     */
    UNSAFE_style?: StyleProp<ViewStyle>;
    /**
     * Resize event handler.
     * this will be called with `height` as argument
     * so it can be used to get the current height of
     * the BottomSheet
     */
    onResize?: (height?: number | undefined) => void;
    /**
     * Whether to show the swipe down to close handle
     * on top of the title. Note: this is not specified
     * in LD3, hence the default: false
     * @default false
     */
    showCloseHandle?: boolean;
    /**
     * This determines whether the keyboard should stay visible after a tap when using a
     * TextField or TextArea inside the BottomSheet
     *
     * 'always' - tapping inside the bottom sheet and outside the text input will not dismiss the keyboard.  tapping outside the bottom sheet will dismiss both the keyboard and bottom sheet.
     *
     * 'never' - tapping inside the bottom sheet and outside the text input will dismiss the keyboard.  tapping outside the bottom sheet will dismiss the keyboard if up, and dismiss the bottom sheet if the keyboard is down.
     *
     * 'handled' - tapping inside the bottom sheet and outside the text input will dismiss the keyboard.  tapping outside the bottom sheet will dismiss both the keyboard and bottom sheet.
     *
     * Valid values: 'never' | 'always' | 'handled'
     * @default always
     */
    keyboardShouldPersistTaps?: 'never' | 'always' | 'handled';

    // ---------------
    // Deprecated Props
    // ---------------
    /**
     * @deprecated use <strong>onClose</strong> instead.
     * Still wired in for now.
     */
    onDismiss?: () => void;
    /**
     * @deprecated it has no effect. Provided just for API backwards compatibility.
     */
    onBackPress?: () => void;
    /**
     * @deprecated it has no effect. Provided just for API backwards compatibility.
     */
    minimumContentHeight?: number;
    /**
     * @deprecated it has no effect. Provided just for API backwards compatibility.
     */
    dismissAreaHeight?: number;
    /**
     * @deprecated it has no effect. Provided just for API backwards compatibility.
     */
    dismissable?: boolean;
    /**
     * @deprecated it has no effect. Provided just for API backwards compatibility.
     */
    resizable?: boolean;
    /**
     * @deprecated it has no effect. Provided just for API backwards compatibility.
     */
    size?: number | 'auto' | 'small' | 'medium' | 'large';
    /**
     * @deprecated it has no effect. Provided just for API backwards compatibility.
     */
    dismissingChangesOpacity?: boolean;
    /**
     * @deprecated use <strong>isOpen</strong> instead.
     * Still wired in for now.
     */
    visible?: boolean;
    /**
     * @deprecated it has no effect.This feature is now baked in.
     */
    avoidKeyboard?: boolean;
    /**
     * @deprecated it has no effect. Provided just for API backwards compatibility.
     */
    keyboardVerticalOffset?: number;
    /**
     * Internal prop, used for unit testing
     * @ignore
     */
    useNativeDriver?: boolean;
    ///*** NON LD PROPS */
    /**
     * Whether to hide the X (close IconButton)
     * @default false
     */
    hideCloseIcon?: boolean;
    /**
     * Whether to hide the title
     * @default false
     */
    hideHeader?: boolean;
    /**
     * By default, the content (children) is already embedded in a ScrollView. To prevent nesting ScrollViews,
     * set this prop to true if your content (children) contains a scrollable type component (ScrollView,FlatList,SectionList,List).
     * We also suggest you set the <strong>contentContainerStyle</strong> of your ScrollView,FlatList, SectionList, List or VirtualizedList to
     * <strong>{height: '100%'}</strong>
     * Example:
     * ```js
     *  <SectionList
     *     contentContainerStyle={{height: '100%'}}
     *     sections={data}
     *     ...
     * ```
     * @default false
     */
    childrenContainScrollableComponent?: boolean;
    /**
     * A ref to the ScrollView that wraps the content (children) of the BottomSheet.
     * This will have no effect if <strong>childrenContainScrollableComponent</strong> is set to true.
     * This is useful if you want to scroll to a specific position in the content (children) of the BottomSheet.
     * Example:
     *
     * ```
     * const innerScrollViewRef = useRef<ScrollView>(null);
     * ...
     * <BottomSheet
     *  innerScrollViewRef={innerScrollViewRef}
     * ...
     * ```
     * Then you can use the ref to scroll to a specific position in the content (children) of the BottomSheet.
     *
     * ```
     * innerScrollViewRef.current?.scrollTo({x: 0, y: 0, animated: true});
     * ```
     */
    innerScrollViewRef?: React.RefObject<ScrollView>;
    /**
     * Indicates whether the component will be wrapped with RN Modal. Setting to false means
     * the application consumer is responsible for presentation, such as displaying above other
     * screen components, opening, and dismissing the BottomSheet.
     * (see https://jira.walmart.com/browse/CEEMP-3502)
     * @default true
     */
    withRNModal?: boolean;
  };

/**
 * Bottom Sheets are surfaces anchored to the bottom of the screen that contain supplementary content.
 *
 * ## Usage
 * ```js
 * import {BottomSheet} from '@walmart/gtp-shared-components`;
 *
 * const [modalIsOpen, setModalIsOpen] = React.useState(false);
 *
 * <BottomSheet
 *   isOpen={modalIsOpen}
 *   onOpen={() => setModalIsOpen(true)}
 *   onClose={() => setModalIsOpen(false)}
 *   title="Confirmation"
 *   actions={
 *     <ButtonGroup>
 *       <Button variant="tertiary" onPress={() => setModalIsOpen(false)}>
 *         Cancel
 *       </Button>
 *       <Button variant="primary" onPress={() => setModalIsOpen(false)}>
 *         Continue
 *       </Button>
 *     </ButtonGroup>
 *   }>
 *   Lorem ipsum dolor sit amet
 * </BottomSheet>
 * ```
 */
const BottomSheet: React.FC<BottomSheetProps> = (props) => {
  const {
    actions,
    children,
    closeButtonProps,
    isOpen = false,
    onOpen,
    onOpened,
    onClose,
    onClosed,
    title,
    accessibilityTitleLabel,
    childrenContainScrollableComponent = false,
    innerScrollViewRef,
    UNSAFE_style,
    keyboardShouldPersistTaps = 'always',
    hideCloseIcon = false,
    hideHeader = false,
    withRNModal = true,
    // deprecated
    onDismiss,
    visible = false,
    ...rest
  } = props;

  const _accessibilityTitleLabel = accessibilityTitleLabel || title;
  const RNVersion = require('react-native/package.json').version;
  const accessibilityLabelText = props.title
    ? `${_accessibilityTitleLabel} ${BottomSheet.displayName}`
    : `${BottomSheet.displayName}`;

  const unsafeStyle = UNSAFE_style as ViewStyle;
  const paddingHorizontal: number =
    unsafeStyle && unsafeStyle.paddingHorizontal === 0
      ? 0
      : token.componentBottomSheetContentPaddingHorizontalBS;
  const UNSAFE_HEIGHT =
    unsafeStyle && unsafeStyle?.height ? unsafeStyle.height : 0;

  const paddingBottom = () => {
    // ButtonGroup actions already has padding so no additional padding required for actions.
    if ((unsafeStyle && unsafeStyle?.paddingBottom === 0) || actions) {
      return 0;
    }

    return token.componentBottomSheetContentPaddingBottomBS;
  };

  const restSpread = () => {
    if (rest) {
      return {...rest};
    }
  };

  const handleBackdropPress = () => {
    if (isKeyboardVisible) {
      Keyboard.dismiss();
    } else {
      closeBottomSheet();
    }
  };

  const {width: deviceWidth} = useWindowDimensions();
  const {isKeyboardVisible, keyboardHeight, keyboardEvent} = useKeyboard();

  const [bottomHeight, setBottomHeight] = React.useState(0);

  const [customStyle, setCustomStyle] = React.useState({});

  const [isModalVisible, setIsModalVisible] = React.useState(false);

  React.useEffect(() => {
    const styleCustom = {...(UNSAFE_style as any)};
    delete styleCustom?.height;
    delete styleCustom?.minHeight;
    delete styleCustom?.maxHeight;

    setCustomStyle(styleCustom);
  }, [UNSAFE_style]);

  React.useEffect(() => {
    if (isModalVisible && bottomHeight !== keyboardHeight) {
      if (keyboardEvent) {
        // Taken from React Native KeyboardAvoidingView source:
        // https://github.com/facebook/react-native/blob/947751fbe4fd72c67538260df0136a2e184bb4fb/Libraries/Components/Keyboard/KeyboardAvoidingView.js#L145
        // Notes: android duration is always 0, so it will never run on Android
        const {duration, easing} = keyboardEvent;

        if (duration && easing) {
          LayoutAnimation.configureNext({
            // We have to pass the duration equal to minimal accepted duration defined here: RCTLayoutAnimation.m
            duration: duration > 10 ? duration : 10,
            update: {
              duration: duration > 10 ? duration : 10,
              type: LayoutAnimation.Types[easing] || 'keyboard',
            },
          });
        }
      }

      setBottomHeight(keyboardHeight);
    }
  }, [keyboardEvent, keyboardHeight, bottomHeight, isModalVisible]);

  const {height: SCREEN_HEIGHT} = Dimensions.get('window');
  const maxHeight = SCREEN_HEIGHT;
  const animatedValue = React.useRef(new Animated.Value(maxHeight)).current;
  const isOpenRef = React.useRef(false);

  const panResponder = React.useRef(
    PanResponder.create({
      onStartShouldSetPanResponder: () => true,
      onPanResponderMove: (_, gestureState) => {
        const newValue = Math.max(0, gestureState.dy);
        animatedValue.setValue(newValue);
      },
      onPanResponderRelease: (_, gestureState) => {
        if (gestureState.dy > 50 || gestureState.vy > 0.5) {
          closeBottomSheet();
        } else {
          openBottomSheet();
        }
      },
    }),
  ).current;

  const handleOpen = React.useCallback(() => {
    if (!isOpenRef.current) {
      onOpen?.();
      isOpenRef.current = true;
    }
  }, [onOpen]);

  // Track the bottom sheet closing state to determine when the bottom sheet is closing
  const closingBottomSheet = React.useRef(false);

  const handleClose = React.useCallback(() => {
    if (isOpenRef.current) {
      setIsModalVisible(false);
      isOpenRef.current = false;
      closingBottomSheet.current = false; // The bottom sheet has been closed, reset the closing state
      onClosed?.();
    }
  }, [onClosed]);

  const openBottomSheet = React.useCallback(() => {
    setIsModalVisible(true);
    Animated.spring(animatedValue, {
      toValue: 0,
      useNativeDriver: true,
      bounciness: 0,
    }).start();
    handleOpen();
  }, [animatedValue, handleOpen, setIsModalVisible]);

  const closeBottomSheet = React.useCallback(() => {
    if (closingBottomSheet.current) {
      return; // The bottom sheet is closing, don't close again
    }
    closingBottomSheet.current = true; // Start closing the bottom sheet
    if (onClose || onDismiss) {
      onClose?.();
      onDismiss?.();
    }
    Animated.timing(animatedValue, {
      toValue: maxHeight,
      useNativeDriver: true,
      duration: 500,
    }).start(() => {
      handleClose();
    });
  }, [animatedValue, handleClose, maxHeight, onClose, onDismiss]);

  const isOpenOrVisible = isOpen || visible;
  const previousOpenOrVisible = React.useRef(isOpenOrVisible);
  React.useEffect(() => {
    if (isOpenOrVisible) {
      openBottomSheet();
    } else {
      // Only close the bottom sheet if it's open
      if (previousOpenOrVisible.current !== isOpenOrVisible) {
        closeBottomSheet();
      }
    }
    previousOpenOrVisible.current = isOpenOrVisible;
  }, [openBottomSheet, closeBottomSheet, isOpenOrVisible]);

  const translateY = animatedValue.interpolate({
    inputRange: [0, maxHeight],
    outputRange: [0, maxHeight],
    extrapolate: 'clamp',
  });

  const backdropOpacity = animatedValue.interpolate({
    inputRange: [0, maxHeight],
    outputRange: [1, 0],
    extrapolate: 'clamp',
  });

  // ---------------
  // Render helpers
  // (extracted and exported separately to facilitate testing)
  // ---------------
  const renderHeader = () => {
    const size = 'medium';
    const length = 32;
    return (
      <>
        {props.showCloseHandle ? <View style={ss.closeHandle} /> : null}
        <View
          testID={BottomSheet.displayName + '-header'}
          style={[
            ss.header,
            {paddingHorizontal},
            !props.title && !hideCloseIcon
              ? {paddingTop: token.componentBottomSheetTitleMarginTop}
              : {},
            props.title ? ss.headerMarginTop : {},
          ]}
          {...panResponder.panHandlers}>
          {!hideCloseIcon && (
            <View style={ss.closeIconPadding}>
              <IconButton
                testID={BottomSheet.displayName + '-close-button'}
                size={size}
                accessibilityRole={a11yRole('button')}
                accessibilityLabel={`close ${accessibilityLabelText}`}
                onPress={closeBottomSheet}
                UNSAFE_style={{
                  width: length,
                  height: length,
                }}
                hitSlop={16}
                {...props.closeButtonProps}>
                <Icons.CloseIcon />
              </IconButton>
            </View>
          )}
          <View style={ss.titleContainer}>
            {typeof props.title === 'string' ? (
              <Text
                accessibilityRole="header"
                testID={BottomSheet.displayName + '-title'}
                style={ss.title}>
                {props.title}
              </Text>
            ) : (
              <>{props.title}</>
            )}
          </View>
        </View>
      </>
    );
  };

  const renderContent = () => {
    return (
      <View
        testID={BottomSheet.displayName + '-container'}
        pointerEvents="box-none"
        style={[
          ss.outerContainer,
          getBSPaddingBottomBasedOnRNVersion(RNVersion, bottomHeight),
        ]}>
        <View
          testID={BottomSheet.displayName + '-sub-container'}
          onLayout={(event: LayoutChangeEvent) => {
            const height = Math.ceil(event.nativeEvent.layout.height);
            props.onResize?.(height);
          }}
          style={[
            ss.innerContainer,
            {maxWidth: deviceWidth, paddingBottom: paddingBottom()},
            customStyle,
          ]}>
          {!hideHeader && renderHeader()}
          <_BottomSheetContent
            externalBottomPadding={bottomHeight}
            keyboardShouldPersistTaps={
              keyboardShouldPersistTaps === 'always'
                ? keyboardShouldPersistTaps
                : 'never'
            }
            headerTitle={title}
            UNSAFE_HEIGHT={UNSAFE_HEIGHT as number}
            contentExtraStyle={{paddingHorizontal}}
            actionsExtraStyle={{paddingHorizontal}}
            componentName={BottomSheet.displayName}
            childrenContainScrollableComponent={
              childrenContainScrollableComponent
            }
            innerScrollViewRef={innerScrollViewRef}
            actions={actions}>
            {typeof children === 'string' ? (
              children
            ) : (
              <View style={ss.childrenContainer}>{children}</View>
            )}
          </_BottomSheetContent>
        </View>
      </View>
    );
  };

  return !withRNModal && isModalVisible ? (
    <View testID={BottomSheet.displayName} style={ss.withRNModalContainer}>
      {renderContent()}
    </View>
  ) : (
    <Modal
      testID={BottomSheet.displayName}
      accessibilityState={{expanded: isModalVisible}}
      accessibilityRole={
        rest?.accessibilityRole ? rest.accessibilityRole : ('dialog' as any)
      }
      accessibilityLabel={
        rest?.accessibilityLabel
          ? rest.accessibilityLabel
          : accessibilityLabelText
      }
      visible={isModalVisible}
      transparent
      onShow={onOpened}
      animationType="none"
      onRequestClose={closeBottomSheet}
      statusBarTranslucent
      backdropOpacity={0.5}
      {...restSpread()}>
      <Pressable
        accessible
        accessibilityLabel={
          rest?.accessibilityLabel
            ? rest.accessibilityLabel
            : accessibilityLabelText
        }
        accessibilityActions={[
          {name: 'activate', label: `close ${accessibilityLabelText}`},
        ]}
        testID={BottomSheet.displayName + '-outside-body-button'}
        style={ss.bottomSheetOuterContainer}
        onPress={handleBackdropPress}>
        <Animated.View
          style={[
            ss.backdrop,
            {
              backgroundColor: token.componentBottomSheetScrimBackgroundColor,
              opacity: backdropOpacity,
            },
          ]}
        />
      </Pressable>
      <Animated.View
        style={[
          ss.bottomSheetContainer,
          {
            transform: [{translateY}],
            maxHeight: maxHeight,
            paddingBottom: paddingBottom(),
          },
        ]}>
        {renderContent()}
      </Animated.View>
    </Modal>
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  wrapper: {
    justifyContent: 'flex-end',
    margin: 0,
  },
  outerContainer: {
    margin: 0,
    flex: 1,
    justifyContent: 'flex-end',
  },
  innerContainer: {
    zIndex: parseInt(token.componentBottomSheetContainerZIndex, 10),
    paddingTop: token.componentBottomSheetContentPaddingTop,
    backgroundColor: token.componentBottomSheetContainerBackgroundColor,
    borderTopLeftRadius:
      token.componentBottomSheetContainerBorderRadiusTopStart,
    borderTopRightRadius: token.componentBottomSheetContainerBorderRadiusTopEnd,
    width: token.componentBottomSheetContainerWidth,
  },
  header: {
    justifyContent: 'flex-start',
    flexDirection: token.componentBottomSheetHeaderDirection as Extract<
      FlexStyle,
      'justifyContent'
    >,
    alignItems: 'center',
  },
  headerMarginTop: {
    padding: token.componentBottomSheetHeaderPaddingBM,
  },
  titleContainer: {
    flex: 1,
    justifyContent: 'flex-start',
  },
  title: {
    ...getFont(token.componentBottomSheetTitleFontWeight.toString() as Weights),
    fontSize: token.componentBottomSheetTitleFontSize,
    lineHeight: token.componentBottomSheetTitleLineHeight,
    textAlign: token.componentBottomSheetTitleTextAlign,
    paddingLeft: token.componentBottomSheetTitlePaddingStart,
    color: token.componentBottomSheetTitleTextColor,
  } as TextStyle,
  closeHandle: {
    alignSelf: 'center',
    height: 4,
    width: 32,
    backgroundColor: colors.gray['30'],
    borderRadius: 4,
  },
  closeIconPadding: {
    paddingLeft: token.componentBottomSheetHeaderPaddingBS,
    marginRight: -6,
  },
  backdrop: {
    ...StyleSheet.absoluteFillObject,
  },
  bottomSheetContainer: {
    flex: 1,
    position: 'absolute',
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'white',
    justifyContent: 'center',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: -2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  bottomSheetOuterContainer: {
    flex: 1,
  },
  childrenContainer: {
    height: '100%',
  },
  withRNModalContainer: {
    flex: 1,
  },
});

BottomSheet.displayName = 'BottomSheet';
export {BottomSheet};
