import * as React from 'react';
import {
  GestureResponderEvent,
  KeyboardTypeOptions,
  NativeSyntheticEvent,
  Platform,
  StyleProp,
  StyleSheet,
  Text,
  TextInput,
  TextInputFocusEventData,
  TextInputProps,
  TextStyle,
  View,
  ViewStyle,
} from 'react-native';

import * as taToken from '@livingdesign/tokens/dist/react-native/light/regular/components/TextArea';
import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/TextField';
import {Icons, IconSize} from '@walmart/gtp-shared-icons';

import {getFont, Weights} from '../../theme/font';
import {a11yRole, useSimpleReducer} from '../utils';

import {
  _LeadingTrailing as Leading,
  _LeadingTrailing as Trailing,
} from './_LeadingTrailing';
// ---------------
// Props
// ---------------
export type TextFieldSize = 'small' | 'large';
export const TEXT_FIELD_VERTICAL_SPACE = 2;
// this is used for keyboardType
export type TextFieldInputType =
  | 'email'
  | 'number'
  | 'password'
  | 'tel'
  | 'text'
  | 'search'
  | 'url';

export type TextFieldRef = TextInput;

export type TextFieldProps = Omit<
  React.ComponentPropsWithRef<typeof TextInput>,
  | 'onChangeText'
  | 'value'
  | 'defaultValue'
  | 'placeholder'
  | 'style'
  | 'onBlur'
  | 'onFocus'
  | 'readOnly'
> & {
  /**
   * This is the size of the TextField.
   * Valid values: 'small' | 'large'
   * @default large
   */
  size?: TextFieldSize;
  /**
   * If the text field is disabled.
   * @default false
   */
  disabled?: boolean;
  /**
   * The error text for the text field.
   */
  error?: React.ReactNode;
  /**
   * The helper text for the text field.
   */
  helperText?: React.ReactNode;
  /**
   * The label for the text field.
   */
  label: React.ReactNode;
  /**
   * The leading content for the text field.
   *
   * If you pass an icon from our collection (Icons) we take care of the styling (size, color, layout)
   * If you pass anything else, you are responsible for the styling.
   * Examples:
   *
   * ```
   * leading={<Icons.EmailIcon />} // <-- we style
   * leading={<Icons.SparkIcon />} // <-- we style
   * leading={<SomeComponent {...props}/>} // <-- you style
   * leading={(isAwesome? <SomeComponent {...props}/>: null)} <-- you style
   * ```
   */
  leading?: React.ReactNode;
  /**
   * The trailing content for the text field.
   *
   * If you pass an icon from our collection (Icons) we take care of the styling (size, color, layout)
   * If you pass anything else, you are responsible for the styling.
   * Examples:
   *
   * ```
   * trailing={<Icons.CloseIcon />} // <-- we style
   * trailing={<Icons.HomeIcon />} // <-- we style
   * trailing={<SomeComponent {...props}/>} // <-- you style
   * trailing={(isAwesome? <SomeComponent {...props}/>: null)} // <-- you style
   * ```
   */
  trailing?: React.ReactNode;
  /**
   * The callback fired when the text field requests to change.
   * Made optional for backwards compatibility
   */
  onChangeText?: (value: React.SetStateAction<string>) => void;
  /**
   * The callback fired when the text field requests to onBlur.
   */
  onBlur?: (value: NativeSyntheticEvent<TextInputFocusEventData>) => void;
  /**
   * The callback fired when the text field requests to onFocus.
   */
  onFocus?: (args: NativeSyntheticEvent<TextInputFocusEventData>) => void;
  /**
   * The placeholder for the text field.
   */
  placeholder?: string;
  /**
   * The props spread to the TextInput element.
   *
   * @default {}
   */
  textInputProps?: TextInputProps;
  /**
   * Whether the text field is read only.
   */
  readOnly?: boolean;
  /**
   * The type for the text field.
   * Valid values are: 'email' | 'number' | 'password' | 'tel' | 'text' | 'url'
   *
   * @default text
   */
  type?: TextFieldInputType;
  /**
   * The value for the text field.  Providing the value will turn this component
   * into a controlled component, which means the native value will be forced to
   * reflect this value if it changes.  For most use cases, this works fine,
   * but in some cases you might want to use the `defaultValue` prop instead.
   *
   * Example: If you have a controlled component:
   *
   * ```
   * import {TextField} from '@walmart/gtp-shared-components';
   * const [value, setValue] = React.useState('I am a controlled TextField');
   * <TextField
   *   label="Controlled TextField"
   *   helperText="Use value prop and onChangeText prop"
   *   value={value}
   *   onChangeText={setValue}
   * />
   * ```
   */
  value?: string;
  /**
   * Provides an initial value that will change when the user starts typing.
   * Useful for use-cases where you do not want to deal with listening to events
   * and updating the value prop to keep the controlled state in sync.
   *
   * Example: If you have an uncontrolled component:
   *
   * ```
   * import {TextField} from '@walmart/gtp-shared-components';
   * <TextField
   *   label="Uncontrolled TextField"
   *   helperText="Init with defaultValue, capture with onSubmitEditing"
   *   defaultValue="I am an uncontrolled TextField"
   *   onSubmitEditing={event =>
   *     // Update your state
   *   }
   * />
   * ```
   */
  defaultValue?: string;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
  /**
   * <strong>NOTE</strong> the actual name of this prop is <strong>ref</strong>. We had to rename
   * it here because of a quirk in the docs generator
   *
   * Internal reference for the TextInput component.
   * You can use this to trigger internal methods: focus(), blur(), clear(), isFocused()
   * from the parent component
   * Example: if you want to force a TextField to be in focus when entering a screen
   *
   * ```
   * import {useFocusEffect} from '@react-navigation/native';
   * import {TextField, TextFieldRef} from '@walmart/gtp-shared-components';
   * . . .
   * const inputRef = React.useRef<TextFieldRef | null>(null);
   *
   * useFocusEffect(
   *   React.useCallback(() => {
   *     if (inputRef.current) {
   *       inputRef.current.focus();
   *     }
   *   }, [inputRef.current]
   * );
   * . . .
   * <TextField
   *   ref={inputRef}
   *   // ... other props ...
   * />
   * ```
   */
  ref_?: React.RefObject<TextInput>;

  // -----------------------------
  // Backwards compatibility props
  // -----------------------------
  /**
   * @deprecated use <strong>leading</strong> instead
   * It has no effect
   */
  leadingIcon?: React.ReactNode;
  /**
   * @deprecated use <strong>trailing</strong> instead
   * It has no effect
   */
  trailingIcon?: React.ReactNode;
  /**
   * @deprecated use <strong>trailing</strong> instead
   * It has no effect
   */
  trailingLink?: string;
  /**
   * @deprecated use <strong>trailing</strong> instead
   * It has no effect
   */
  onTrailingIconPress?: (event: GestureResponderEvent) => void;
  /**
   * @deprecated use <strong>trailing</strong> instead
   */
  onLinkPress?: (event: GestureResponderEvent) => void;
  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  state?: 'success' | 'error';
  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  successMessage?: string;
  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  stateIcon?: boolean;
  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  counter?: boolean;
  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  helperTextImportantForA11y?: 'yes' | 'no';
  /**
   * @deprecated use <strong>onChangeText</strong> instead
   */
  onTextChange?: (value?: string) => void;
};

type TextFieldState = {
  focused: boolean;
  containerBorderColor: string;
  containerBorderWidth: number;
  containerPaddingVertical: number;
  containerPaddingHorizontal: number;
  textColor: string;
  labelTextColor: string;
  helperTextColor: string;
};

/**
 * Text fields allow users to enter and edit text.
 *
 * ## Usage
 * ```js
 * import {TextField, Icons} from '@walmart/gtp-shared-components`;
 *
 * <TextField
 *   label="Label text"
 *   helperText="Helper text"
 *   placeholder="Placeholder text"
 *   leading={[<Icons.EmailIcon />, true]}
 *   onSubmitEditing={event =>
 *     console.log('TextField value captured:', event.nativeEvent.text)
 *   }
 * />
 * ```
 */
const TextField = React.forwardRef<TextInput, TextFieldProps>((props, ref) => {
  const {
    size = 'small',
    disabled = false,
    error,
    label,
    helperText,
    placeholder,
    readOnly = false,
    textInputProps,
    leading,
    onChangeText,
    onBlur,
    onFocus,
    trailing,
    type = 'text',
    value,
    defaultValue,
    UNSAFE_style,
    ...rest
  } = props;

  const resolvedContainerBorderColor = (isFocused: boolean = false) => {
    let borderColor: string =
      token.componentTextFieldContainerBorderColorDefault;
    if (disabled) {
      borderColor = token.componentTextFieldContainerBorderColorDisabled;
    } else if (error) {
      borderColor = token.componentTextFieldContainerStateErrorBorderColorFocus;
    } else if (readOnly) {
      borderColor =
        token.componentTextFieldContainerStateReadOnlyBorderColorDefault;
    } else if (isFocused) {
      borderColor = token.componentTextFieldContainerBorderColorFocus;
    }
    return borderColor;
  };
  const resolvedContainerBorderWidth = (isFocused: boolean = false) => {
    if (disabled) {
      return token.componentTextFieldContainerBorderWidthDisabled;
    } else if (isFocused) {
      return token.componentTextFieldContainerBorderWidthFocus;
    } else {
      return token.componentTextFieldContainerBorderWidthDefault;
    }
  };
  const resolvedContainerPaddingVertical = () => {
    let paddingVertical: number =
      token.componentTextFieldContainerSizeSmallPaddingVertical;
    if (size === 'large') {
      paddingVertical =
        token.componentTextFieldContainerSizeLargePaddingVertical -
        TEXT_FIELD_VERTICAL_SPACE;
    }
    return (
      paddingVertical - token.componentTextFieldContainerBorderWidthDefault
    );
  };
  const resolvedContainerPaddingHorizontal = () => {
    let paddingHorizontal: number =
      token.componentTextFieldContainerSizeSmallPaddingHorizontal;
    if (size === 'large') {
      paddingHorizontal =
        token.componentTextFieldContainerSizeLargePaddingHorizontal;
    }
    return (
      paddingHorizontal - token.componentTextFieldContainerBorderWidthDefault
    );
  };
  const resolvedTextColor = (isFocused: boolean = false) => {
    if (disabled) {
      return token.componentTextFieldValueTextColorDisabled;
    } else if (isFocused) {
      return token.componentTextFieldValueTextColorFocus;
    } else {
      return token.componentTextFieldValueTextColorDefault;
    }
  };
  const resolveIconColor = (isFocused: boolean = false) => {
    if (disabled || readOnly) {
      return token.componentTextFieldLeadingIconIconColorDisabled; // @cory this is missing for trailing ...TrailingIconIconColorDisabled
    } else if (isFocused) {
      return token.componentTextFieldLeadingIconIconColorFocus; // @cory: token missing for trailing ...TrailingIconIconColorFocus
    } else {
      return token.componentTextFieldLeadingIconIconColorDefault; // @cory: token missing for trailing ...TrailingIconIconColorDefault?
    }
  };
  const resolvePlaceHolderTextColor = () => {
    if (disabled) {
      return token.componentTextFieldValueTextColorDisabled;
    } else {
      return token.componentTextFieldValuePlaceholderTextColor;
    }
  };
  const initialState: TextFieldState = {
    focused: false,
    containerBorderColor: resolvedContainerBorderColor(),
    containerBorderWidth: resolvedContainerBorderWidth(),
    containerPaddingVertical: resolvedContainerPaddingVertical(),
    containerPaddingHorizontal: resolvedContainerPaddingHorizontal(),
    textColor: resolvedTextColor(),
    labelTextColor: resolvedTextColor(),
    helperTextColor: resolvedTextColor(),
  };

  const [state, setState] = useSimpleReducer<TextFieldState>(initialState);

  React.useLayoutEffect(() => {
    // initialize value if passed in the props
    setState(
      'containerBorderColor',
      resolvedContainerBorderColor(state.focused as boolean),
    );
    setState(
      'containerBorderWidth',
      resolvedContainerBorderWidth(state.focused as boolean),
    );
    setState('containerPaddingVertical', resolvedContainerPaddingVertical());
    setState(
      'containerPaddingHorizontal',
      resolvedContainerPaddingHorizontal(),
    );
    setState('textColor', resolvedTextColor(state.focused as boolean));

    setState('labelTextColor', resolvedTextColor());
    setState('helperTextColor', resolvedTextColor());
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    setState,
    disabled,
    error,
    state.focused,
    state.containerBorderWidth,
    size,
    readOnly,
  ]);

  const handleOnFocus = (
    args: NativeSyntheticEvent<TextInputFocusEventData>,
  ) => {
    if (disabled || rest?.editable === false) {
      return;
    }
    setState('focused', true);
    onFocus?.(args);
  };

  const handleOnBlur = (
    args: NativeSyntheticEvent<TextInputFocusEventData>,
  ) => {
    if (rest?.editable === false) {
      return;
    }
    setState('focused', false);
    onBlur?.(args);
  };

  const handleChangeText = (_value: string) => {
    if (disabled || rest?.editable === false) {
      return;
    }
    onChangeText?.(_value);
  };

  const resolveSecureTextEntry = (_type: TextFieldInputType) => {
    if (rest?.secureTextEntry) {
      return {
        secureTextEntry: rest?.secureTextEntry,
      };
    } else if (_type === 'password') {
      return {
        secureTextEntry: true,
      };
    } else {
      return {
        secureTextEntry: false,
      };
    }
  };

  const resolveBlurOnSubmit = (_error: React.ReactNode) => {
    if (_error) {
      return {
        blurOnSubmit: false,
      };
    }
  };

  // ---------------
  // Rendering
  // ---------------
  const renderLeading = (node: React.ReactNode) => {
    return (
      <Leading
        node={node}
        iconProps={{
          UNSAFE_style: ss(size).leading,
          color: resolveIconColor(state.focused as boolean),
          size: token.componentTextFieldLeadingIconIconSize as IconSize, // "medium"
        }}
      />
    );
  };

  const renderTrailing = (node: React.ReactNode) => {
    return (
      <Trailing
        node={node}
        iconProps={{
          UNSAFE_style: ss(size).trailing,
          color: resolveIconColor(state.focused as boolean),
          size: token.componentTextFieldLeadingIconIconSize as IconSize, // "medium"  // @cory: token missing for trailing ...TrailingIconIconSize?
        }}
      />
    );
  };

  const renderLabel = (
    _size: TextFieldSize,
    _state: TextFieldState,
    _label: React.ReactNode,
  ) => {
    return (
      <View style={ss(_size).labelContainer}>
        <Text
          accessible
          accessibilityRole={a11yRole('text')}
          nativeID={`${TextField.displayName}-label`}
          style={[
            ss(_size).label,
            {color: _state.labelTextColor} as TextStyle,
          ]}>
          {_label}
        </Text>
      </View>
    );
  };

  const renderHelperText = (_helperText: React.ReactNode) => (
    <Text
      accessibilityRole={a11yRole('text')}
      style={[
        ss(size).helperText,
        {color: state.helperTextColor} as TextStyle,
      ]}>
      {_helperText}
    </Text>
  );

  const renderError = (_error: React.ReactNode) => (
    <View style={ss(size).errorContainer}>
      <Icons.ExclamationCircleFillIcon color="red" />
      <Text style={ss(size).errorText}>{_error}</Text>
    </View>
  );

  const renderHelperTextOrError = (
    _error: React.ReactNode,
    _helperText: React.ReactNode,
  ) => {
    if (_error) {
      return renderError(_error);
    } else if (_helperText) {
      return renderHelperText(_helperText);
    } else {
      return null;
    }
  };

  return (
    <View
      accessibilityState={{disabled: disabled as boolean}}
      testID={TextField.displayName}
      style={[ss(size).container, UNSAFE_style]}>
      {renderLabel(size, state as TextFieldState, label)}
      <View
        testID={TextField.displayName! + '-input-container'}
        style={[
          ss(size).inputContainer,
          {
            color: state.textColor,
            borderColor: state.containerBorderColor,
            borderWidth: state.containerBorderWidth,
            paddingVertical: state.containerPaddingVertical,
            paddingHorizontal: state.containerPaddingHorizontal,
          } as TextStyle,
        ]}>
        {leading ? renderLeading(leading) : null}
        <TextInput
          accessibilityState={{disabled}}
          accessible
          testID={TextField.displayName! + '-input'}
          ref={ref}
          style={[
            ss(size).textInput,
            {
              color: state.textColor as string,
            },
          ]}
          placeholderTextColor={resolvePlaceHolderTextColor()}
          value={value}
          defaultValue={defaultValue}
          editable={!(readOnly || disabled || rest?.editable === false)}
          onChangeText={handleChangeText}
          onFocus={handleOnFocus}
          onBlur={handleOnBlur}
          onSubmitEditing={rest?.onSubmitEditing}
          placeholder={placeholder}
          underlineColorAndroid="transparent"
          autoCapitalize="none"
          showSoftInputOnFocus
          spellCheck={false}
          {...resolveKeyboardType(type)}
          {...resolveSecureTextEntry(type)}
          {...resolveAutoCompleteProps(type)}
          {...resolveBlurOnSubmit(error)}
          {...textInputProps}
          {...rest}
        />
        {trailing ? renderTrailing(trailing) : null}
      </View>
      {renderHelperTextOrError(error, helperText)}
    </View>
  );
});

// ---------------
// Styles
// ---------------
const ss = (size: TextFieldSize) => {
  const resolvedMarginLeftForTextInput = () => {
    if (process.env.STYLEGUIDIST_ENV) {
      return 8;
    } else if (Platform.OS === 'android') {
      return -3;
    }
    return undefined;
  };

  return StyleSheet.create({
    container: {
      flex: 1,
      justifyContent: 'center',
    },
    labelContainer: {
      marginBottom: token.componentTextFieldTextLabelMarginBottom, // 4,
    },
    label: {
      ...getFont('bold'),
      fontSize: size === 'small' ? 12 : 14, // @cory Label FontSize is missing,
      lineHeight: size === 'small' ? 16 : 20, // @cory Label line hight is missing,
      marginBottom: token.componentTextFieldTextLabelMarginBottom,
    } as TextStyle,
    inputContainer: {
      flexDirection: 'row',
      height: size === 'large' ? 56 : 40,
      alignItems: 'center',
      ...getFont(),
      backgroundColor: token.componentTextFieldContainerBackgroundColor,
      borderWidth: token.componentTextFieldContainerBorderWidthDefault, // 1
      borderRadius: token.componentTextFieldContainerBorderRadius, // 4
    },
    textInput: {
      flex: 1,
      ...getFont(),
      fontWeight: token.componentTextFieldValueFontWeight.toString(), // "400",
      fontSize:
        size === 'large'
          ? token.componentTextFieldValueSizeLargeFontSize // 16,
          : token.componentTextFieldValueSizeSmallFontSize, // 14,
      ...Platform.select({
        android: {
          paddingVertical: size === 'large' ? 3 : 2,
        },
        ios: {
          paddingVertical: size === 'large' ? 1 : 3,
        },
      }),
      color: token.componentTextFieldValueTextColorDefault,
      marginLeft: resolvedMarginLeftForTextInput(),
    } as TextStyle,
    helperTextContainer: {
      paddingHorizontal: 4,
      // token.componentTextFieldHelperTextContainerPaddingHorizontal, // @cory this is missing in 0.58
      marginTop: token.componentTextFieldHelperTextMarginTop, // 4,
    },
    errorContainer: {
      flexDirection: 'row',
      alignItems: 'center',
      paddingHorizontal:
        // token.componentTextFieldHelperTextContainerPaddingHorizontal, // @cory this is missing in 0.58
        4,
      marginTop: token.componentTextFieldHelperTextMarginTop, // 4,
    },
    errorText: {
      // @cory I had to pull the error font tokens from TextArea
      ...getFont(
        taToken.componentTextAreaMaxLengthFontWeight.toString() as Weights,
      ), // "400"
      fontSize: taToken.componentTextAreaMaxLengthFontSize, // 12 // @cory token missing
      color: token.componentTextFieldContainerStateErrorBorderColorDefault, // "#de1c24" // @cory missing token for this one?
      marginHorizontal: 4, // @cory missing error tokens
    } as TextStyle,
    helperText: {
      // @cory I had to pull the helper text font tokens from TextArea
      ...getFont(
        taToken.componentTextAreaMaxLengthFontWeight.toString() as Weights,
      ), // "400" // @cory token missing
      fontSize: taToken.componentTextAreaMaxLengthFontSize, // 12 // @cory token missing
      lineHeight: taToken.componentTextAreaMaxLengthLineHeight, // 16, // @cory token missing
      marginTop: taToken.componentTextAreaHelperTextContainerMarginTop, // 4
    } as TextStyle,
    leading: {
      marginRight:
        // token.componentTextFieldLeadingIconMarginRight, // @cory this is missing in 0.58
        size === 'large' ? 12 : 8,
    },
    trailing: {
      // marginHorizontal: token.componentTextFieldTrailingMarginHorizontal, // @cory this token doesn't exist anymore in 0.58
      marginLeft: size === 'large' ? 16 : 12,
      //0.74 added
      // verticalAlign: token.componentTextFieldTrailingAlignVertical,
    },
  });
};

TextField.displayName = 'TextField';
export {TextField};

// ---------------
// Render helpers
// (extracted and exported separately to facilitate testing)
// ---------------
export const resolveKeyboardType = (
  _type: TextFieldInputType,
  platformOS = Platform.OS,
): {keyboardType: KeyboardTypeOptions} => {
  let keyboardType;
  switch (_type) {
    case 'text':
    case 'password':
      keyboardType = 'default';
      break;
    case 'email':
      keyboardType = 'email-address';
      break;
    case 'number':
      keyboardType = 'numeric'; // or number-pad, decimal-pad, numbers-and-punctuation (iOS only)?
      break;
    case 'tel':
      keyboardType = 'phone-pad';
      break;
    case 'url':
      keyboardType = platformOS === 'android' ? 'default' : 'url';
      break;
    case 'search':
      keyboardType = platformOS === 'android' ? 'default' : 'web-search';
      break;
    default:
      keyboardType = 'default';
      break;
  }
  return {keyboardType: keyboardType as KeyboardTypeOptions};
};

export const resolveAutoCompleteProps = (
  _type: TextFieldInputType,
  platformOS = Platform.OS,
): TextInputProps => {
  switch (_type) {
    case 'url':
      return platformOS === 'android'
        ? {
            autoComplete: 'off',
          }
        : {
            textContentType: 'URL',
          };
    case 'email':
      return platformOS === 'android'
        ? {
            autoComplete: 'email',
          }
        : {
            textContentType: 'emailAddress',
          };
    case 'tel':
      return platformOS === 'android'
        ? {
            autoComplete: 'tel',
          }
        : {
            textContentType: 'telephoneNumber',
          };
    case 'text':
    case 'number':
      return platformOS === 'android'
        ? {
            autoComplete: 'off',
          }
        : {
            textContentType: 'none',
          };
    default:
      return {};
  }
};
