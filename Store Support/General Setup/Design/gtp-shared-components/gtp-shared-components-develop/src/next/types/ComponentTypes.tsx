import {
  ModalBaseProps,
  PanResponderGestureState,
  PressableProps,
  ScrollViewProps,
  TextProps,
  ViewProps,
} from 'react-native';

import type {
  GestureResponderEvent,
  ModalProps as RNModalProps,
} from 'react-native-modal';
declare type OrNull<T> = null | T;
type CommonOmitProps = 'children' | 'style';
type ViewOmitProps = CommonOmitProps | 'id';
type ScrollViewOmitProps = CommonOmitProps;
type PressableOmitProps = CommonOmitProps | 'id' | 'disabled' | 'onPress';
type TextOmitProps = CommonOmitProps | 'weight';
type RNModalOmitProps =
  | 'children'
  | 'style'
  | 'animationIn'
  | 'animationOut'
  | 'animationInTiming'
  | 'animationOutTiming'
  | 'avoidKeyboard'
  | 'coverScreen'
  | 'hasBackdrop'
  | 'backdropColor'
  | 'backdropOpacity'
  | 'backdropTransitionInTiming'
  | 'backdropTransitionOutTiming'
  | 'customBackdrop'
  | 'useNativeDriver'
  | 'deviceHeight'
  | 'deviceWidth'
  | 'hideModalContentWhileAnimating'
  | 'propagateSwipe'
  | 'isVisible'
  | 'panResponderThreshol'
  | 'swipeThreshold'
  | 'onModalShow'
  | 'onModalWillShow'
  | 'onModalHide'
  | 'onModalWillHide'
  | 'onBackdropPress'
  | 'onBackButtonPress'
  | 'scrollTo'
  | 'scrollOffset'
  | 'scrollOffsetMax'
  | 'scrollHorizontal'
  | 'statusBarTranslucent'
  | 'supportedOrientations';
export type CommonRNModalBaseProps = {
  animationInTiming?: number;
  animationOutTiming?: number;
  avoidKeyboard?: boolean;
  coverScreen?: boolean;
  hasBackdrop?: boolean;
  backdropColor?: string;
  backdropOpacity?: number;
  backdropTransitionInTiming?: number;
  backdropTransitionOutTiming?: number;
  customBackdrop?: React.ReactNode;
  useNativeDriver?: boolean;
  deviceHeight?: number | null;
  deviceWidth?: number | null;
  hideModalContentWhileAnimating?: boolean;
  propagateSwipe?:
    | boolean
    | ((
        event: GestureResponderEvent,
        gestureState: PanResponderGestureState,
      ) => boolean);
  isVisible?: boolean;
  panResponderThreshold?: number;
  swipeThreshold?: number;
  onModalShow?: () => void;
  onModalWillShow?: () => void;
  onModalHide?: () => void;
  onModalWillHide?: () => void;
  onBackdropPress?: () => void;
  onBackButtonPress?: () => void;
  scrollTo?: OrNull<(e: any) => void>;
  scrollOffset?: number;
  scrollOffsetMax?: number;
  scrollHorizontal?: boolean;
  statusBarTranslucent?: boolean;
  supportedOrientations?: (
    | 'landscape'
    | 'portrait'
    | 'portrait-upside-down'
    | 'landscape-left'
    | 'landscape-right'
  )[];
};
export type CommonViewProps = Omit<ViewProps, ViewOmitProps>;
export type CommonScrollViewProps = Omit<ScrollViewProps, ScrollViewOmitProps>;
export type CommonPressableProps = Omit<PressableProps, PressableOmitProps>;
export type CommonTextProps = Omit<TextProps, TextOmitProps>;
export type CommonModalBaseProps = Omit<
  ModalBaseProps,
  'transparent' | 'visible'
>;
export type CommonModalProps = Omit<RNModalProps, RNModalOmitProps>;
