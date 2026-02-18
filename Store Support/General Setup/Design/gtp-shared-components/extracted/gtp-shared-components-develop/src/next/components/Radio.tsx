import * as React from 'react';
import {
  GestureResponderEvent,
  Pressable,
  PressableProps,
  StyleProp,
  StyleSheet,
  Text,
  TextStyle,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Radio';

import {getFont} from '../../theme/font';
import {a11yRole} from '../utils';

// ---------------
// Props
// ---------------
export type RadioProps = PressableProps & {
  /**
   * If the radio is checked
   */
  checked?: boolean;
  /**
   * If the radio is disabled
   */
  disabled?: boolean;
  /**
   * The label for the radio
   */
  label?: React.ReactNode;
  /**
   * This Radio's press event handler
   */
  onPress?: (event: GestureResponderEvent) => void;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
  /**
   * @deprecated it has no effect. use <strong>checked</strong> instead..
   */
  value?: boolean;
  /**
   * @deprecated it has no effect. use <strong>onPress</strong> instead..
   */
  onChange?: (value: boolean) => void;
};

/**
 * Radio buttons represent a group of mutually exclusive choices, compared to
 * checkboxes that allow users to make one or more selections from a group.
 * In use cases where only one selection of a group is allowed, use the radio
 * button component instead of the checkbox.
 *
 * ## Usage
 * ```js
 * import {Radio} from '@walmart/gtp-shared-components`;
 *
 * <Radio label="Unselected" />
 * <Radio label="Selected" checked />
 * <Radio label="Unselected (disabled)" disabled />
 * <Radio label="Selected (disabled)" checked disabled />
 * <Radio />
 * <Radio checked />
 * <Radio disabled />
 * <Radio checked disabled />
 * ```
 */
const Radio: React.FC<RadioProps> = (props) => {
  const {
    checked = false,
    disabled = false,
    label,
    onPress,
    UNSAFE_style,
    ...rest
  } = props;

  // ---------------
  // Interactions
  // ---------------
  const handlePress = (event: GestureResponderEvent) => {
    if (!disabled && onPress) {
      onPress(event);
    }
  };

  // ---------------
  // Rendering
  // ---------------
  return (
    <Pressable
      testID={Radio.displayName}
      accessible={true}
      accessibilityRole={a11yRole('radio')}
      accessibilityState={{disabled, checked}}
      accessibilityLabel={typeof label === 'string' ? label : undefined}
      onPress={handlePress}
      style={[ss(disabled, checked).container, UNSAFE_style]}
      {...rest}>
      <View
        testID={Radio.displayName + '-buttonOuter'}
        style={ss(disabled, checked).outer}>
        <View
          testID={Radio.displayName + '-buttonInner'}
          style={ss(disabled, checked).inner}
        />
      </View>
      {label && <Text style={ss(disabled, checked).label}>{label}</Text>}
    </Pressable>
  );
};

// ---------------
// Styles
// ---------------
const ss = (disabled: boolean, checked: boolean) => {
  // Default states
  let innerState = {
    backgroundColor: token.componentRadioInputInnerBackgroundColorDefault,
  } as ViewStyle;
  let outerState = {
    borderWidth: token.componentRadioInputOuterBorderWidthDefault,
    borderColor: token.componentRadioInputOuterBorderColorDefault,
  } as ViewStyle;
  let labelState = {
    ...getFont(),
    color: token.componentRadioTextLabelTextColorDefault,
  } as TextStyle;

  if (checked) {
    // Checked and Disabled
    if (disabled) {
      innerState = {
        backgroundColor:
          token.componentRadioInputInnerStateCheckedBackgroundColorDisabled,
      } as ViewStyle;
      outerState = {
        borderWidth: token.componentRadioInputOuterBorderWidthDisabled,
        borderColor: token.componentRadioInputOuterBorderColorDisabled,
      } as ViewStyle;
      labelState = {
        ...getFont('bold'),
        color: token.componentRadioTextLabelTextColorDisabled,
      } as TextStyle;
    }
    // Checked and not Disabled
    else {
      innerState = {
        backgroundColor:
          token.componentRadioInputInnerStateCheckedBackgroundColorDefault,
      } as ViewStyle;
      outerState = {
        borderWidth: token.componentRadioInputOuterBorderWidthDefault,
        borderColor: token.componentRadioInputOuterBorderColorDefault,
      } as ViewStyle;
      labelState = {
        ...getFont('bold'),
        color: token.componentRadioTextLabelTextColorDefault,
      } as TextStyle;
    }
  } else {
    // Unchecked and Disabled
    if (disabled) {
      innerState = {
        backgroundColor: token.componentRadioInputInnerBackgroundColorDisabled,
      } as ViewStyle;
      outerState = {
        borderWidth: token.componentRadioInputOuterBorderWidthDisabled,
        borderColor: token.componentRadioInputOuterBorderColorDisabled,
      } as ViewStyle;
      labelState = {
        ...getFont(),
        color: token.componentRadioTextLabelTextColorDisabled,
      } as TextStyle;
    }
    // else: Unchecked and not Disabled (Default, original state)
  }

  const style = StyleSheet.create({
    container: {
      flexDirection: 'row',
      alignItems: 'flex-start',
    },
    inner: {
      borderRadius: token.componentRadioInputInnerRadius,
      height: 12, // Check with Cory: missing from LD token
      width: 12, // Check with Cory: missing from LD token
      ...innerState,
    },
    outer: {
      justifyContent: 'center',
      alignItems: 'center',
      margin: 1, // Check with Cory: missing from Radio LD token, exists in Checkbox but not here
      borderRadius: token.componentRadioInputOuterRadius,
      borderStyle: 'solid', // Check with Cory: missing from LD token
      backgroundColor: token.componentRadioInputOuterBackgroundColor,
      height: token.componentRadioInputHeight,
      width: token.componentRadioInputWidth,
      ...outerState,
    },
    label: {
      flexShrink: 1,
      marginLeft: token.componentRadioTextLabelMarginStart,
      fontSize: token.componentRadioTextLabelFontSize,
      lineHeight: token.componentRadioTextLabelLineHeight,
      ...labelState,
    },
  });
  return style;
};

Radio.displayName = 'Radio';
export {Radio};
