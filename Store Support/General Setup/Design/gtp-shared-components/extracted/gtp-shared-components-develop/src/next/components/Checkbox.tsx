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

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Checkbox';
import {Icons} from '@walmart/gtp-shared-icons';

import {getFont} from '../../theme/font';
import {a11yRole, iconSizes} from '../utils';

// ---------------
// Props
// ---------------
export type CheckboxProps = PressableProps & {
  /**
   * If the checkbox is checked
   */
  checked?: boolean;
  /**
   * If the checkbox is disabled
   */
  disabled?: boolean;
  /**
   * If the checkbox is indeterminate
   */
  indeterminate?: boolean;
  /**
   * The label for the checkbox
   */
  label?: React.ReactNode;
  /**
   * This Checkbox's press event handler
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
 * Checkboxes are used for a list of options where the user may select multiple options, including all or none.
 *
 * ## Usage
 * ```js
 * import {Checkbox} from '@walmart/gtp-shared-components`;
 *
 * <Checkbox label="Unchecked" />
 * <Checkbox label="Checked" checked />
 * <Checkbox label="Indeterminate" indeterminate />
 * <Checkbox label="Unchecked (disabled)" disabled />
 * <Checkbox label="Checked (disabled)" checked disabled />
 * <Checkbox label="Indeterminate (disabled)" indeterminate disabled />
 *
 * ```
 */
const Checkbox: React.FC<CheckboxProps> = (props) => {
  const {
    checked = false,
    disabled = false,
    indeterminate = false,
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

  const renderIcon = () => {
    if (indeterminate) {
      return (
        <Icons.MinusIcon
          size={
            iconSizes[
              token.componentCheckboxInputIconStateIndeterminateIconSize
            ]
          }
          color={token.componentCheckboxInputIconStateIndeterminateIconColor}
        />
      );
    }
    if (checked) {
      return (
        <Icons.CheckIcon
          size={iconSizes[token.componentCheckboxInputIconStateCheckedIconSize]}
          color={token.componentCheckboxInputIconStateCheckedIconColor}
        />
      );
    }
    return null;
  };

  const _accessibilityLabel = `${
    typeof label === 'string' ? label : ''
  } ${a11yRole('checkbox')}`;

  // ---------------
  // Rendering
  // ---------------
  return (
    <Pressable
      testID={Checkbox.displayName}
      accessibilityState={{checked, disabled}}
      accessibilityLabel={_accessibilityLabel}
      onPress={handlePress}
      style={[ss(disabled, checked, indeterminate).container, UNSAFE_style]}
      {...rest}>
      <View style={ss(disabled, checked, indeterminate).iconContainer}>
        {renderIcon()}
      </View>
      {label && (
        <Text style={ss(disabled, checked, indeterminate).label}>{label}</Text>
      )}
    </Pressable>
  );
};

// ---------------
// Styles
// ---------------
const ss = (disabled: boolean, checked: boolean, indeterminate: boolean) => {
  // Default
  let iconContainerState = {
    borderColor: token.componentCheckboxInputBorderColorDefault,
    borderWidth: token.componentCheckboxInputBorderWidthDefault,
    backgroundColor: token.componentCheckboxInputBackgroundColorDefault,
  } as ViewStyle;
  let labelState = {
    ...getFont(),
    color: token.componentCheckboxLabelTextColorDefault,
  } as TextStyle;
  if (checked) {
    // Default Checked
    if (!disabled) {
      iconContainerState = {
        borderColor: token.componentCheckboxInputBorderColorDefault,
        borderWidth: token.componentCheckboxInputBorderWidthDefault,
        backgroundColor:
          token.componentCheckboxInputStateCheckedBackgroundColorDefault,
      } as ViewStyle;
      labelState = {
        ...getFont('bold'),
        color: token.componentCheckboxLabelTextColorDefault,
      } as TextStyle;
    }
    // Disabled Checked
    else {
      iconContainerState = {
        borderColor: token.componentCheckboxInputBorderColorDisabled,
        borderWidth: token.componentCheckboxInputBorderWidthDisabled,
        backgroundColor:
          token.componentCheckboxInputStateCheckedBackgroundColorDisabled,
      } as ViewStyle;
      labelState = {
        ...getFont('bold'),
        color: token.componentCheckboxLabelTextColorDisabled,
      } as TextStyle;
    }
  } else if (indeterminate) {
    // Default Indeterminate
    if (!disabled) {
      iconContainerState = {
        borderColor: token.componentCheckboxInputBorderColorDefault,
        borderWidth: token.componentCheckboxInputBorderWidthDefault,
        backgroundColor:
          token.componentCheckboxInputStateIndeterminateBackgroundColorDefault,
      } as ViewStyle;
      labelState = {
        ...getFont('bold'),
        color: token.componentCheckboxLabelTextColorDefault,
      } as TextStyle;
    }
    // Disabled Indeterminate
    else {
      iconContainerState = {
        borderColor: token.componentCheckboxInputBorderColorDisabled,
        borderWidth: token.componentCheckboxInputBorderWidthDisabled,
        backgroundColor:
          token.componentCheckboxInputStateIndeterminateBackgroundColorDisabled,
      } as ViewStyle;
      labelState = {
        ...getFont('bold'),
        color: token.componentCheckboxLabelTextColorDisabled,
      } as TextStyle;
    }
  } else {
    // Default disabled
    if (disabled) {
      iconContainerState = {
        borderColor: token.componentCheckboxInputBorderColorDisabled,
        borderWidth: token.componentCheckboxInputBorderWidthDisabled,
        backgroundColor: token.componentCheckboxInputBackgroundColorDisabled,
      } as ViewStyle;
      labelState = {
        ...getFont(),
        color: token.componentCheckboxLabelTextColorDisabled,
      } as TextStyle;
    }
  }

  const style = StyleSheet.create({
    container: {
      flexDirection: 'row',
      alignItems: 'flex-start',
    },
    iconContainer: {
      justifyContent: 'center',
      alignItems: 'center',
      borderStyle: 'solid', // Check with Cory: can't find this token value
      borderRadius: token.componentCheckboxInputBorderRadius,
      height: token.componentCheckboxInputHeight,
      width: token.componentCheckboxInputWidth,
      margin: token.componentCheckboxInputMargin,
      ...iconContainerState,
    },
    label: {
      flexShrink: 1,
      marginLeft: token.componentCheckboxLabelMarginStart,
      fontSize: token.componentCheckboxLabelFontSize,
      lineHeight: token.componentCheckboxLabelLineHeight,
      ...labelState,
    },
  });
  return style;
};

Checkbox.displayName = 'Checkbox';
export {Checkbox};
