import * as React from 'react';
import {
  Animated,
  GestureResponderEvent,
  KeyboardAvoidingView,
  LayoutChangeEvent,
  Modal,
  PanResponder,
  PanResponderGestureState,
  PanResponderInstance,
  Platform,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
  View,
} from 'react-native';

import {Icons} from '@walmart/gtp-shared-icons';

import {IconButton} from '../next/components/IconButton';
import {getThemeFrom, ThemeContext, ThemeObject} from '../theme/theme-provider';
import {Title} from '../typography';

import {composed as defaultTheme} from './theme';

export type BottomSheetProps = {
  children?: any;
  /** The title for this bottom sheet. */
  title?: string;
  /** Dismiss event handler. */
  onDismiss?: () => void;
  /**
   * Back button press event handler.  If set, will display a back chevron.
   *
   * **Note:** If the bottom sheet is resizable, the back icon will not be visible.
   */
  onBackPress?: () => void;
  /**
   * Resize event handler.
   * this will be called with `height` as argument
   * so it can be used to get the current height of
   * the BottomSheet
   */
  onResize?: (height?: number | undefined) => void;
  /** Minimum content height.*/
  minimumContentHeight: number;
  /** Height of the swipe-to-dismiss area. */
  dismissAreaHeight: number;
  /**
   * Whether bottom sheet should display the close icon.
   *
   * **Note:** If the bottom sheet is resizable, the close icon will not be visible.
   */
  dismissable: boolean;
  /** Whether the bottom sheet allows resizing. */
  resizable: boolean;
  /** The bottom sheet size. */
  size: number | 'auto' | 'small' | 'medium' | 'large';
  /** Whether dismissing by dragging to bottom changes opacity as you drag. */
  dismissingChangesOpacity: boolean;
  /** Whether the bottom sheet is visible. */
  visible: boolean;
  /** Whether to avoid the keyboard. */
  avoidKeyboard?: boolean;
  /**
   * This is the distance between the top of the user screen and the react native view,
   * may be non-zero in some use cases.
   */
  keyboardVerticalOffset?: number;
  /**
   * This determines whether the keyboard should stay visible after a tap when using a textInput inside the bottomSheet
   */
  keyboardShouldPersistTaps?: 'never' | 'always' | 'handled';
};

type BottomSheetState = {
  isDragging: boolean;
  offset: number;

  /** Height manually set by user */
  userHeight?: number;

  /** Heights for all sheet areas */
  wrapperHeight?: number;
  gripHeight?: number;
  titleHeight?: number;
  contentHeight?: number;

  initialHeight: number;
  pan: Animated.ValueXY;

  transitionWhenReady: boolean;
  transition: Animated.Value;
  transitioning: boolean;
  dismissing: boolean;
  props: BottomSheetProps;
};

/**
 * Bottom sheets are elevated surfaces containing supplementary content. They are anchored to the bottom of the screen. They are similar to modals in content and behavior. They animate up from the bottom of the screen, over the main content.
 *
 * **Note:** This is an alpha-level component. Its API is subject to change.
 */
export default class BottomSheet extends React.Component<
  BottomSheetProps,
  BottomSheetState
> {
  static defaultProps: BottomSheetProps = {
    dismissable: true,
    dismissAreaHeight: 50,
    dismissingChangesOpacity: true,
    minimumContentHeight: 136,
    resizable: true,
    size: 'auto',
    visible: true,
    avoidKeyboard: false,
    keyboardVerticalOffset: 33,
  };

  state: BottomSheetState = {
    isDragging: false,
    offset: 0,
    userHeight: undefined,
    initialHeight: 0,
    contentHeight: undefined,
    wrapperHeight: undefined,
    gripHeight: undefined,
    titleHeight: undefined,
    pan: new Animated.ValueXY(),

    transitionWhenReady: this.props.visible,
    transition: new Animated.Value(0),
    transitioning: false,
    dismissing: false,
    props: BottomSheet.defaultProps,
  };

  static contextTypes = ThemeContext;

  _panResponder: PanResponderInstance;
  _theme?: ThemeObject;
  constructor(props: BottomSheetProps) {
    super(props);

    this.state = {
      ...this.state,
      props,
    };

    this._panResponder = PanResponder.create({
      onStartShouldSetPanResponder: () => true,
      onMoveShouldSetPanResponderCapture: () => true,
      onPanResponderGrant: () => {
        const {userHeight} = this.state;
        const initialHeight =
          userHeight ?? this.getInitialSheetHeight(this.sheetHeight());
        this.setState({
          initialHeight,
          isDragging: true,
        });
      },
      onPanResponderMove: (
        _e: GestureResponderEvent,
        gestureState: PanResponderGestureState,
      ) => {
        const {initialHeight, wrapperHeight, userHeight} = this.state;
        const {dismissAreaHeight} = this.props;

        const topHeight =
          this._theme?.extend('default').part('top').minHeight ?? 0;
        const desiredHeight = Math.min(
          (wrapperHeight ?? 0) - topHeight,
          Math.max(1, Math.ceil(initialHeight - gestureState.dy)),
        );
        if (userHeight !== desiredHeight) {
          this.setState({
            userHeight: desiredHeight,
            dismissing: desiredHeight <= dismissAreaHeight,
          });
        }
      },
      onPanResponderRelease: () => {
        const height = this.state.userHeight ?? this.state.initialHeight;
        this.setState({
          userHeight: this.state.dismissing
            ? height
            : Math.max(this.state.props.minimumContentHeight, height),
          isDragging: false,
        });
      },
    });
  }

  componentDidUpdate(prevProps: BottomSheetProps) {
    if (this.props.visible && this.props !== prevProps) {
      this.setState({props: this.props});
    }
    if (prevProps.visible !== this.props.visible && !this.props.visible) {
      this.setState(
        {
          contentHeight: undefined,
          gripHeight: undefined,
          titleHeight: undefined,
          transitionWhenReady: !this.state.dismissing,
        },
        () => {
          if (!this.state.dismissing) {
            this.setTransitioning(!this.state.dismissing, this.props);
          }
        },
      );
    }
    if (
      this.state.wrapperHeight !== undefined &&
      this.state.contentHeight !== undefined &&
      this.state.gripHeight !== undefined &&
      this.state.titleHeight !== undefined &&
      this.state.transitionWhenReady
    ) {
      this.setState({transitionWhenReady: false}, () => {
        this.setTransitioning(!this.state.dismissing, this.props);
      });
    }
  }

  setTransitioning = (transitioning: boolean, props: BottomSheetProps) => {
    if (transitioning) {
      this.state.transition.setValue(props.visible ? 0 : 1);
      this.setState({transitioning, dismissing: false}, () => {
        Animated.timing(this.state.transition, {
          useNativeDriver: true,
          duration: this._theme?.part('static.animationDuration'),
          toValue: props.visible ? 1 : 0,
        }).start(() => {
          this.setTransitioning(false, props);
        });
      });
    } else {
      this.setState({
        transitioning,
        transitionWhenReady: false,
        props,
        dismissing: false,
        userHeight: undefined,
      });
    }
  };

  getInitialSheetHeight = (height: number) => {
    const {wrapperHeight} = this.state;
    const {size, minimumContentHeight} = this.props;

    if (size === 'auto') {
      return Math.max(minimumContentHeight, height);
    }
    if (size === 'small') {
      return Math.min(
        Math.max(height, minimumContentHeight),
        (wrapperHeight ?? 0) * 0.3,
      );
    }
    if (size === 'medium') {
      return (wrapperHeight ?? 0) * 0.5;
    }
    if (size === 'large') {
      return Math.min((wrapperHeight ?? 0) * 0.9);
    }
    return size;
  };

  handleLayoutEvent =
    (part: 'grip' | 'title' | 'content' | 'wrapper') =>
    (event: LayoutChangeEvent) => {
      const newHeight = Math.ceil(event.nativeEvent.layout.height);
      if (
        newHeight === 0 ||
        !this.state[`${part}Height` as keyof BottomSheetState] ||
        ((part === 'wrapper' || part === 'content') &&
          this.state[`${part}Height` as keyof BottomSheetState] !== newHeight)
      ) {
        this.setState<never>({[`${part}Height`]: newHeight});
      }
    };

  renderGrip = () => {
    const {resizable} = this.state.props;
    const {isDragging} = this.state;
    const themeState = this._theme?.extend(isDragging ? 'active' : 'default');

    if (resizable) {
      return (
        <View
          onLayout={this.handleLayoutEvent('grip')}
          style={themeState.part('grip')}
          {...this._panResponder.panHandlers}>
          <View style={themeState.part('gripIndicator')} />
        </View>
      );
    }
    return (
      <Animated.View
        onLayout={this.handleLayoutEvent('grip')}
        style={themeState.part('nonGrip')}
      />
    );
  };

  calculateOpacity = (height: number, minHeight: number) => {
    const {dismissAreaHeight, dismissingChangesOpacity} = this.state.props;
    const {transition, transitioning, transitionWhenReady} = this.state;

    if (transitioning || transitionWhenReady) {
      return transition.interpolate({inputRange: [0, 1], outputRange: [0, 1]});
    }
    if (dismissingChangesOpacity) {
      if (height > minHeight) {
        return 1;
      }
      if (height > dismissAreaHeight) {
        return (height - dismissAreaHeight) / (minHeight - dismissAreaHeight);
      }
      return 0;
    }
    return 1;
  };

  sheetHeight = () => {
    const {contentHeight, gripHeight, titleHeight} = this.state;
    return (gripHeight ?? 0) + (titleHeight ?? 0) + (contentHeight ?? 0);
  };

  handleOnDismiss = () => {
    this.props.onResize?.(0);
    this.props.onDismiss?.();
    this.props.onBackPress?.();
  };

  render() {
    const {
      children,
      title,
      onDismiss,
      onBackPress,
      onResize,
      minimumContentHeight,
      dismissAreaHeight,
      dismissable,
      dismissingChangesOpacity,
      resizable,
      visible,
      avoidKeyboard,
      keyboardVerticalOffset,
      keyboardShouldPersistTaps,
      ...viewProps
    } = this.state.props;
    const {transition, transitioning, userHeight, wrapperHeight} = this.state;

    if (userHeight && userHeight < dismissAreaHeight) {
      this.handleOnDismiss();
      return null;
    }

    if (!(visible || transitioning)) {
      return null;
    }

    this._theme = getThemeFrom(
      this.context,
      defaultTheme,
      'layout',
      'bottomSheet',
    );
    const themeState = this._theme.extend('default');

    const fullHeight = this.getInitialSheetHeight(this.sheetHeight());
    const scrollEnabled = (userHeight ?? fullHeight) < this.sheetHeight();

    const opacity = this.calculateOpacity(
      userHeight ?? fullHeight,
      minimumContentHeight,
    );
    const viewStyle = transitioning && {
      transform: [
        {
          translateY: transition.interpolate({
            inputRange: [0, 1],
            outputRange: [wrapperHeight ?? 0, 0],
          }),
        },
      ],
    };

    return (
      <Modal
        onRequestClose={() => dismissable && this.handleOnDismiss()}
        transparent>
        <Animated.View
          {...viewProps}
          style={[themeState.part('wrapper'), {opacity: opacity}]}>
          <SafeAreaView style={themeState.part('safeArea')}>
            <Animated.View
              style={themeState.part('safeArea')}
              onLayout={this.handleLayoutEvent('wrapper')}>
              <Animated.View style={themeState.part('top')}>
                <TouchableOpacity
                  style={themeState.part('dismissArea')}
                  onPress={this.handleOnDismiss}>
                  <Animated.View style={themeState.part('dismissArea')} />
                </TouchableOpacity>
              </Animated.View>
              <KeyboardAvoidingView
                onLayout={(event: LayoutChangeEvent) =>
                  this.props.onResize?.(
                    Math.ceil(event.nativeEvent.layout.height),
                  )
                }
                behavior={Platform.OS === 'ios' ? 'padding' : undefined}
                enabled={avoidKeyboard}
                style={[!transitioning && themeState.part('keyboardContainer')]}
                keyboardVerticalOffset={keyboardVerticalOffset}>
                <Animated.View style={viewStyle}>
                  <Animated.View
                    style={[
                      themeState.part('contentContainer'),
                      {height: userHeight ?? fullHeight},
                    ]}>
                    {onBackPress && !resizable ? (
                      <IconButton
                        UNSAFE_style={themeState.part('backButton')}
                        onPress={() => onBackPress()}
                        children={<Icons.ChevronLeftIcon size={24} />}
                      />
                    ) : null}
                    {dismissable && !resizable ? (
                      <IconButton
                        UNSAFE_style={themeState.part('closeButton')}
                        onPress={() => onDismiss?.()}
                        children={<Icons.CloseIcon size={24} />}
                      />
                    ) : null}
                    {this.renderGrip()}
                    {title || (!resizable && (dismissable || onBackPress)) ? (
                      <Title
                        style={themeState.part('title')}
                        onLayout={this.handleLayoutEvent('title')}>
                        {title}
                      </Title>
                    ) : (
                      <Animated.View
                        onLayout={this.handleLayoutEvent('title')}
                      />
                    )}
                    <ScrollView
                      style={themeState.part('scrollableArea')}
                      bounces={scrollEnabled}
                      scrollEnabled={scrollEnabled}
                      showsVerticalScrollIndicator={scrollEnabled}
                      keyboardShouldPersistTaps={keyboardShouldPersistTaps}>
                      <Animated.View style={themeState.part('content')}>
                        <Animated.View
                          style={themeState.part('contentInner')}
                          onLayout={this.handleLayoutEvent('content')}
                          collapsable={false}>
                          {this.state.props.children}
                        </Animated.View>
                      </Animated.View>
                    </ScrollView>
                  </Animated.View>
                </Animated.View>
              </KeyboardAvoidingView>
            </Animated.View>
          </SafeAreaView>
          <SafeAreaView style={themeState.part('safeAreaBackground')} />
        </Animated.View>
      </Modal>
    );
  }
}
