import * as React from 'react';
import {
  Animated,
  Easing,
  FlexStyle,
  Platform,
  Pressable,
  StyleProp,
  StyleSheet,
  Text,
  TextStyle,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Switch';

import {getFont} from '../../theme/font';
import {CommonPressableProps} from '../types/ComponentTypes';
import {a11yRole} from '../utils';

// ---------------
// Props
// ---------------
export type SwitchProps = Omit<CommonPressableProps, 'disabled'> & {
  /**
   * If the switch is on
   * @default false
   */
  isOn?: boolean;
  /**
   * If the switch is disabled
   * @default false
   */
  disabled?: boolean;
  /**
   * The label for the switch
   */
  label?: React.ReactNode;
  /**
   * Callback called with the new value when it changes.
   */
  onValueChange?: (value: boolean) => void;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  small?: boolean;
};

/**
 * Switches are generally used to activate or deactivate (on/off) a specific setting.
 *
 * ## Usage
 * ```js
 * import {SpinnerOverlay, Switch} from '@walmart/gtp-shared-components`;
 *
 * const SwitchComponent = () => {
 *   const [isEnabled, setIsEnabled] = useState(false);
 *   const [isLoading, setIsLoading] = useState(false);
 *   const onToggleSwitch = async () => {
 *     setIsLoading(true);
 *     try {
 *       const response = await fetch('https://<Your URL>/toggleSwitch', {
 *         method: 'POST',
 *         body: JSON.stringify({isEnabled: !isEnabled}),
 *         headers: {
 *           'Content-Type': 'application/json',
 *         },
 *       });
 *       const data = await response.json();
 *       setIsEnabled(data.isEnabled);
 *     } catch (error) {
 *       console.error(error);
 *     } finally {
 *       setIsLoading(false);
 *     }
 *   };
 *   return (
 *     <View>
 *       <Text>Toggle Switch: </Text>
 *       {isLoading && <SpinnerOverlay visible={true} />}
 *       <Switch isOn={isEnabled} onValueChange={onToggleSwitch} disabled={isLoading} />
 *     </View>
 *   );
 * }
 *
 * export default SwitchComponent;
 * ```
 */
const Switch: React.FC<SwitchProps> = (props) => {
  const {
    isOn = false,
    disabled = false,
    label,
    onValueChange,
    UNSAFE_style,
    ...rest
  } = props;

  const handleMarginLeftOff = token.componentSwitchHandleOffsetStart; // 3
  const handleMarginLeftOn = // 44 - 18 - 3 = 23
    token.componentSwitchTrackWidth -
    token.componentSwitchHandleWidth -
    token.componentSwitchHandleOffsetStart;

  const isAnimating = React.useRef(false);
  const previousIsOn = React.useRef(false);
  const switchAnim = React.useRef(
    new Animated.Value(handleMarginLeftOff),
  ).current;

  React.useEffect(() => {
    if (previousIsOn.current !== isOn) {
      isAnimating.current = true; // save isAnimating state to prevent taps during animatino
      if (isOn) {
        // Values extracted from token.componentSwitchHandleTransition
        Animated.timing(switchAnim, {
          toValue: handleMarginLeftOn,
          duration: 100,
          easing: Easing.bezier(0.77, 0, 0.174, 1),
          useNativeDriver: false, // paddingLeft not supported by Native Driver
        }).start(() => (isAnimating.current = false));
      } else {
        // Values extracted from token.componentSwitchHandleTransition
        Animated.timing(switchAnim, {
          toValue: handleMarginLeftOff,
          duration: 100,
          easing: Easing.bezier(0.77, 0, 0.174, 1),
          useNativeDriver: false, // paddingLeft not supported by Native Driver
        }).start(() => (isAnimating.current = false));
      }
    }
    previousIsOn.current = isOn; // Save the previous value
  }, [
    isOn,
    switchAnim,
    handleMarginLeftOff,
    handleMarginLeftOn,
    previousIsOn,
    isAnimating,
  ]);

  // ---------------
  // Interactions
  // ---------------
  const handleSwitch = () => {
    if (!disabled && onValueChange && !isAnimating.current) {
      onValueChange(isOn);
    }
  };

  const resolveThumbColor = () => {
    if (disabled) {
      return isOn
        ? token.componentSwitchHandleStateIsOnBackgroundColorDisabled // "#babbbe"
        : token.componentSwitchHandleBackgroundColorDisabled; // "#babbbe"
    } else {
      return isOn
        ? token.componentSwitchHandleStateIsOnBackgroundColorDefault // "#fff"
        : token.componentSwitchHandleBackgroundColorDefault; // "#f1f1f2"
    }
  };

  const resolveTrackColor = () => {
    if (disabled) {
      return isOn
        ? token.componentSwitchTrackStateIsOnBackgroundColorDisabled // "#e3e4e5"
        : token.componentSwitchTrackBackgroundColorDisabled; // "#e3e4e5"
    } else {
      return isOn
        ? token.componentSwitchTrackStateIsOnBackgroundColorDefault // "#0071dc"
        : token.componentSwitchTrackBackgroundColorDefault; // "#74767c"
    }
  };

  // ---------------
  // Rendering
  // ---------------
  return (
    <Pressable
      accessibilityRole={a11yRole('switch')}
      accessibilityState={{checked: isOn, disabled}}
      testID={Switch.displayName}
      onPress={handleSwitch}
      disabled={disabled}
      style={[ss.container, UNSAFE_style]}
      {...rest}>
      <Animated.View
        testID={Switch.displayName + '-track'}
        style={[ss.track, {backgroundColor: resolveTrackColor()}]}>
        <Animated.View
          testID={Switch.displayName + '-thumb'}
          style={[
            ss.handle,
            !disabled ? ss.handleShadow : null,
            {backgroundColor: resolveThumbColor(), marginLeft: switchAnim},
          ]}
        />
      </Animated.View>
      {!!label && <Text style={ss.label}>{label}</Text>}
    </Pressable>
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: token.componentSwitchContainerAlignVertical as Extract<
      FlexStyle,
      'alignItems'
    >,
  },
  label: {
    ...getFont(),
    flexShrink: 1,
    marginLeft: token.componentSwitchTextLabelMarginStart,
    fontSize: token.componentSwitchTextLabelFontSize,
    lineHeight: token.componentSwitchTextLabelLineHeight,
    color: token.componentSwitchTextLabelTextColor,
  } as TextStyle,
  track: {
    justifyContent: 'center',
    width: token.componentSwitchTrackWidth, // 44
    height: token.componentSwitchTrackHeight, // 24
    borderRadius: token.componentSwitchTrackBorderRadius, // 1000
  },
  handle: {
    width: token.componentSwitchHandleWidth, // 18
    height: token.componentSwitchHandleHeight, // 18
    borderRadius: token.componentSwitchHandleBorderRadius, // 1000
  },
  handleShadow: {
    ...Platform.select({
      // token.componentSwitchHandleElevation
      // @cory several issues with token, multi shadows, px values, spreadRadius not supported by RN
      android: {
        elevation: 1,
      },
      ios: {
        shadowColor: 'black', // corresponds to rgb(0,0,0,0.15) from figma
        shadowOpacity: 0.15, // corresponds to rgb(0,0,0,0.15) from figma
        shadowRadius: 2, // corresponds to blurRadius from figma
        shadowOffset: {
          height: 1, // corresponds to offsetY from figma
          width: 0, // corresponds to offsetX from figma
        },
      },
    }),
  },
});

Switch.displayName = 'Switch';
export {Switch};
