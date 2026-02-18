import * as React from 'react';
import {
  Animated,
  GestureResponderEvent,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  ViewProps,
} from 'react-native';

import {interpolateStyles, mergeStyles} from '../../next/utils';
import {ThemeObject} from '../../theme/theme-provider';

export type BaseButtonExternalProps = ViewProps & {
  /** Whether to display this Button full-width
   * @deprecated This prop is deprecated. Default value is false. Use 'isFullWidth' prop instead.
   */
  block?: boolean;
  /** Whether to display this Button full-width
   * @default false
   */
  isFullWidth?: boolean;
  /** Icon to show on this Button */
  icon?: React.ReactElement;
  /** Whether to show the icon on the right */
  iconRight?: boolean;
  /** This Button's content (usually a string) */
  children?: React.ReactNode;
  /** Whether this Button is disabled */
  disabled?: boolean;
  /** Whether this Button is selected */
  selected?: boolean;
  /** This Button's press event handler */
  onPress: (event: GestureResponderEvent) => void;
};

export type BaseButtonLoadingProps = {
  /** Whether this Button should show the loading indicator */
  loading?: boolean;
  /** Whether this Button should allow presses while the loading indicator is shown */
  allowPressWhileLoading?: boolean;
};

export type BaseButtonExternalSmallProps = BaseButtonExternalProps & {
  /** Whether to use the `small` variant
   * @deprecated This prop is deprecated. Default button size is small. Use 'size' prop instead.
   */
  small?: boolean;
};

export type BaseButtonExternalSizeProps = BaseButtonExternalProps & {
  /**
   * Whether to use the `size` variant
   * @default "small"
   */
  size?: 'small' | 'medium' | 'large';
};

type BaseButtonProps = ViewProps &
  BaseButtonExternalSmallProps &
  BaseButtonExternalSizeProps &
  BaseButtonLoadingProps & {
    theme: ButtonTheme;
    textProps: {
      numberOfLines?: number;
      ellipsizeMode?: 'head' | 'middle' | 'tail' | 'clip';
    };
    /** @ignore */
    loadingIndicator: React.ReactElement;
    /** @ignore */
    iconNoMargin?: boolean;
  };

type State = {
  pressing: boolean;
  press: Animated.Value;
};

type StateTheme = {
  face: Record<string, any>;
  text: Record<string, any>;
  image: Record<string, any>;
};

export type ButtonTheme = ThemeObject & {
  disabled: StateTheme;
  default: StateTheme;
  pressed: StateTheme;
};

export type BaseButtonTheme = ButtonTheme;

/**
 * @internal
 */
export default class BaseButton extends React.Component<
  BaseButtonProps,
  State
> {
  static defaultProps: Partial<BaseButtonProps> = {
    block: false,
    isFullWidth: false,
    disabled: false,
    iconRight: false,
    allowPressWhileLoading: false,
  };

  state: State = {
    pressing: false,
    press: new Animated.Value(0),
  };

  static ANIMATION_DURATION = 100;

  animatedText: any;
  animatedView: any;

  /**
   * Set the `Animated.Text` ref.
   * @private
   */
  setAnimatedTextRef = (component: any) => {
    this.animatedText = component;
  };

  /**
   * Set the `Animated.View` ref.
   * @private
   */
  setAnimatedViewRef = (component: any) => {
    this.animatedView = component;
  };

  /**
   * Set `state.pressing`
   * @private
   *
   * @param {boolean} pressing
   * @param {boolean} reset
   */
  setPressing = (pressing: boolean, reset = false) => {
    /**
     * The `Animated.Text` and `Animated.View` ref checks fixes a bug where
     * React removes the `LDBaseButton` instance before an animation finishes.
     * `LDBaseButton#setPressing` is called after the unmound, causing an error
     * in the `ReactNative.Animated` internals.
     */
    if (this.animatedText && this.animatedView) {
      this.setState({
        pressing,
        press: !reset ? this.state.press : new Animated.Value(0),
      });
    }
  };

  /**
   * Set `state.pressing` to `false`
   * @private
   */
  setPressingOff = () => {
    this.setPressing(false);
  };

  /**
   * Set `state.pressing` to `true`
   * @private
   */
  setPressingOn = () => {
    this.setPressing(true);
  };

  /**
   * Do press-in animation.
   * @private
   */
  doPressInAnimation = () => {
    this.setPressingOn();
    Animated.timing(this.state.press, {
      duration: BaseButton.ANIMATION_DURATION,
      toValue: 1,
      useNativeDriver: false,
    }).start(this.setPressingOff);
  };

  /**
   * Do press-out animation.
   * @private
   */
  doPressOutAnimation = () => {
    this.setPressingOn();
    Animated.timing(this.state.press, {
      duration: BaseButton.ANIMATION_DURATION,
      toValue: 0,
      useNativeDriver: false,
    }).start(this.setPressingOff);
  };

  handlePress = (event: GestureResponderEvent) => {
    const {disabled, onPress, loading, allowPressWhileLoading} = this.props;

    if (!loading || allowPressWhileLoading) {
      if (!disabled) {
        onPress(event);
      }

      this.handlePressOut();
    }
  };

  handlePressIn = () => {
    const {loading, allowPressWhileLoading} = this.props;
    if (!loading || allowPressWhileLoading) {
      if (!this.state.pressing) {
        this.doPressInAnimation();
      } else {
        this.state.press.stopAnimation(this.doPressInAnimation);
      }
    }
  };

  handlePressOut = () => {
    const {loading, allowPressWhileLoading} = this.props;
    if (!loading || allowPressWhileLoading) {
      if (!this.state.pressing) {
        this.doPressOutAnimation();
      } else {
        this.state.press.stopAnimation(this.doPressOutAnimation);
      }
    }
  };

  componentDidUpdate(prevProps: BaseButtonProps) {
    const {disabled} = this.props;

    if (prevProps.disabled !== disabled) {
      this.state.press.stopAnimation();
      this.setPressing(false, true);
    }
  }

  render() {
    const {
      block,
      isFullWidth,
      children,
      disabled,
      selected,
      style,
      theme,
      icon,
      iconNoMargin,
      iconRight,
      hitSlop,
      textProps,
      loading,
      loadingIndicator,
      ...rootProps
    } = this.props;
    const {press} = this.state;
    const rootStyles = mergeStyles(
      block || isFullWidth ? styles.containerBlock : styles.container,
      style,
    );
    const blockStyle =
      block || isFullWidth ? styles.buttonBlock : styles.button;
    const textStyle = block || isFullWidth ? styles.textBlock : undefined;

    if (disabled) {
      return (
        <TouchableOpacity
          activeOpacity={1}
          accessibilityRole={
            !process.env.STYLEGUIDIST_ENV ? 'button' : undefined
          }
          {...rootProps}
          onPress={this.handlePress}
          onPressIn={this.handlePressIn}
          onPressOut={this.handlePressOut}
          accessibilityState={{disabled: true}}
          hitSlop={hitSlop}
          style={rootStyles}>
          <View style={[blockStyle, theme.part('disabled.face')]}>
            {icon &&
              !iconRight &&
              React.cloneElement(icon, {
                style: [
                  iconNoMargin ? styles.iconNoMargin : styles.icon,
                  theme.part('disabled.image'),
                ],
              })}
            {loading && (
              <Animated.View
                style={theme.part(
                  selected ? 'selected' : 'default',
                  'spinnerContainer',
                )}>
                {React.cloneElement(loadingIndicator, {
                  style: theme.part('disabled.spinner'),
                  color: theme.part('disabled.spinner').color,
                })}
              </Animated.View>
            )}
            <Text
              {...textProps}
              style={[
                textStyle,
                theme.part('disabled.text'),
                loading && styles.transparent,
              ]}>
              {children}
            </Text>
            {icon &&
              iconRight &&
              React.cloneElement(icon, {
                style: [
                  iconNoMargin ? styles.iconNoMargin : styles.iconRight,
                  theme.part('disabled.image'),
                ],
              })}
          </View>
        </TouchableOpacity>
      );
    }

    const parts = ['face', 'text', 'image', 'spinner'];
    const partStyles: Record<string, any> = {};

    parts.forEach((part) => {
      partStyles[part] = interpolateStyles(
        press,
        theme.part(selected ? 'selected' : 'default', part),
        theme.part(selected ? 'selectedpressed' : 'pressed', part),
      );
    });

    return (
      <TouchableOpacity
        activeOpacity={1}
        accessibilityRole={!process.env.STYLEGUIDIST_ENV ? 'button' : undefined}
        {...rootProps}
        onPress={this.handlePress}
        onPressIn={this.handlePressIn}
        onPressOut={this.handlePressOut}
        accessibilityState={{selected}}
        hitSlop={hitSlop}
        style={rootStyles}>
        <Animated.View
          ref={this.setAnimatedViewRef}
          style={[
            blockStyle,
            partStyles.face.cleaned,
            partStyles.face.interpolated,
          ]}>
          {icon &&
            !iconRight &&
            React.cloneElement(icon, {
              style: [
                iconNoMargin ? styles.iconNoMargin : styles.icon,
                partStyles.image.cleaned,
                partStyles.image.interpolated,
              ],
            })}
          {loading && (
            <Animated.View
              style={theme.part(
                selected ? 'selected' : 'default',
                'spinnerContainer',
              )}>
              {React.cloneElement(loadingIndicator, {
                style: [
                  partStyles.spinner.interpolated,
                  partStyles.spinner.cleaned,
                ],
                color:
                  partStyles.spinner.interpolated.color ||
                  partStyles.spinner.cleaned.color,
              })}
            </Animated.View>
          )}
          <Animated.Text
            {...textProps}
            ref={this.setAnimatedTextRef}
            style={[
              textStyle,
              partStyles.text.cleaned,
              partStyles.text.interpolated,
              loading && styles.transparent,
            ]}>
            {children}
          </Animated.Text>
          {icon &&
            iconRight &&
            React.cloneElement(icon, {
              style: [
                iconNoMargin ? styles.iconNoMargin : styles.iconRight,
                partStyles.image.cleaned,
                partStyles.image.interpolated,
              ],
            })}
        </Animated.View>
      </TouchableOpacity>
    );
  }
}

const styles = StyleSheet.create({
  button: {
    flexShrink: 1,
    flexDirection: 'row',
  },
  buttonBlock: {
    flex: 1,
    flexDirection: 'row',
  },
  iconNoMargin: {
    alignSelf: 'center',
  },
  icon: {
    alignSelf: 'center',
    marginRight: 7,
  },
  iconRight: {
    alignSelf: 'center',
    marginLeft: 7,
  },
  container: {
    flexDirection: 'row',
    justifyContent: 'center',
    overflow: 'visible',
  },
  containerBlock: {
    flexDirection: 'row',
    justifyContent: 'center',
    overflow: 'visible',
  },
  textBlock: {
    flexGrow: 1,
  },
  transparent: {
    opacity: 0,
  },
});
