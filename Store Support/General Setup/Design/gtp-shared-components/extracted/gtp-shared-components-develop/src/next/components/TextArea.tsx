import * as React from 'react';
import {
  FlexStyle,
  NativeSyntheticEvent,
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

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/TextArea';
import {Icons} from '@walmart/gtp-shared-icons';

import {getFont, Weights} from '../../theme/font';
import {a11yRole, useSimpleReducer} from '../utils';

// ---------------
// Props
// ---------------
export type TextAreaSize = 'small' | 'large';

// this is used for keyboardType
export type TextAreaInputType =
  | 'email'
  | 'number'
  | 'password'
  | 'tel'
  | 'text'
  | 'search'
  | 'url';

export type TextAreaRef = TextInput;

export type TextAreaProps = Omit<
  React.ComponentPropsWithRef<typeof TextInput>,
  | 'onChangeText'
  | 'maxLength'
  | 'value'
  | 'defaultValue'
  | 'placeholder'
  | 'style'
  | 'onBlur'
  | 'onFocus'
  | 'readOnly'
> & {
  /**
   * This is the size of the TextArea.
   * Valid values: 'small' | 'large'
   * @default large
   */
  size?: TextAreaSize;
  /**
   * If the text area is disabled.
   * @default false
   */
  disabled?: boolean;
  /**
   * The error text for the text area.
   */
  error?: React.ReactNode;
  /**
   * The helper text for the text area.
   */
  helperText?: React.ReactNode;
  /**
   * The label for the text area.
   */
  label: React.ReactNode;
  /**
   * The maximum length for the text area (includes character counter).
   * If this prop is passed, a counter will be displayed at the bottom
   * right (e.g. 12/140 meaning 12 chars of 140 max)
   */
  maxLength?: number;
  /**
   * The callback fired when the text area requests to change.
   * Made optional for backwards compatibility
   */
  onChangeText?: ((text: string) => void) | undefined;
  /**
   * The callback fired when the text field requests to onBlur.
   */
  onBlur?: (value: NativeSyntheticEvent<TextInputFocusEventData>) => void;
  /**
   * The callback fired when the text field requests to onFocus.
   */
  onFocus?: (args: NativeSyntheticEvent<TextInputFocusEventData>) => void;
  /**
   * The placeholder for the text area.
   */
  placeholder?: string;
  /**
   * If the text area is read only.
   */
  readOnly?: boolean;
  /**
   * The props spread to the underlying TextInput element.
   *
   * @default {}
   */
  textAreaProps?: TextInputProps;
  /**
   * The value for the text area.  Providing the value will turn this component
   * into a controlled component, which means the native value will be forced to
   * reflect this value if it changes.  For most use cases, this works fine,
   * but in some cases you might want to use the `defaultValue` prop instead.
   *
   * Example: If you have a controlled component:
   *
   * ```
   * import {TextArea} from '@walmart/gtp-shared-components';
   * const [value, setValue] = React.useState('I am a controlled TextArea');
   * <TextArea
   *   label="Controlled TextArea"
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
   * import {TextArea} from '@walmart/gtp-shared-components';
   * <TextArea
   *   label="Uncontrolled TextArea"
   *   helperText="Init with defaultValue, capture with onSubmitEditing"
   *   defaultValue="I am an uncontrolled TextArea"
   *   onSubmitEditing={event =>
   *     // Update your state
   *   }
   *   onBlur={event =>
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
   * Internal reference for the underlying TextInput component.
   * You can use this to trigger internal methods: focus(), blur(), clear(), isFocused()
   * from the parent component
   * Example: if you want to force a TextArea to be in focus when entering a screen
   *
   * ```
   * import {useFocusEffect} from '@react-navigation/native';
   * import {TextArea, TextAreaRef} from '@walmart/gtp-shared-components';
   * . . .
   * const inputRef = React.useRef<TextAreaRef | undefined | null>();
   *
   * useFocusEffect(
   *   React.useCallback(() => {
   *     if (inputRef.current) {
   *       inputRef.current.focus();
   *     }
   *   }, [inputRef.current]
   * );
   * . . .
   * <TextArea
   *   ref={inputRef}
   *   // ... other props ...
   * />
   * ```
   */
  ref_?: React.RefObject<TextInput>;
};

export type TextAreaState = {
  focused: boolean;
  containerBorderColor: string;
  containerBorderWidth: number;
  containerPaddingVertical: number;
  containerPaddingHorizontal: number;
  textColor: string;
  labelTextColor: string;
  helperTextColor: string;
  nrOfCharacters: number;
  counterColor: string;
};

/**
 * Text fields allow users to enter and edit text.
 *
 * ## Usage
 * ```js
 * import {TextArea} from '@walmart/gtp-shared-components`;
 *
 * <TextArea
 *   label="Label text"
 *   helperText="Helper text"
 *   placeholder="Placeholder text"
 *   onSubmitEditing={event =>
 *     console.log('TextArea value captured:', event.nativeEvent.text)
 *   }
 * />
 * ```
 */
const TextArea = React.forwardRef<TextInput, TextAreaProps>((props, ref) => {
  const {
    size = 'small',
    disabled = false,
    error,
    label,
    helperText,
    maxLength,
    readOnly = false,
    placeholder,
    textAreaProps,
    onChangeText,
    onBlur,
    onFocus,
    value,
    defaultValue,
    UNSAFE_style,
    ...rest
  } = props;

  const resolvedContainerBorderColor = (isFocused: boolean = false) => {
    let borderColor: string =
      token.componentTextAreaContainerBorderColorDefault;
    if (disabled) {
      borderColor = token.componentTextAreaContainerBorderColorDisabled;
    } else if (error) {
      borderColor = token.componentTextAreaContainerStateErrorBorderColorFocus;
    } else if (readOnly) {
      borderColor =
        token.componentTextAreaContainerStateReadOnlyBorderColorDefault;
    } else if (isFocused) {
      borderColor = token.componentTextAreaContainerBorderColorFocus;
    }
    return borderColor;
  };
  const resolvedContainerBorderWidth = (isFocused: boolean = false) => {
    if (disabled) {
      return token.componentTextAreaContainerBorderWidthDisabled;
    } else if (isFocused) {
      return token.componentTextAreaContainerBorderWidthFocus;
    } else {
      return token.componentTextAreaContainerBorderWidthDefault;
    }
  };
  const resolvedContainerPaddingVertical = () => {
    let paddingVertical: number =
      token.componentTextAreaContainerSizeSmallPaddingVertical;
    if (size === 'large') {
      paddingVertical =
        token.componentTextAreaContainerSizeLargePaddingVertical;
    }
    return paddingVertical - token.componentTextAreaContainerBorderWidthDefault;
  };
  const resolvedContainerPaddingHorizontal = () => {
    let paddingHorizontal: number =
      token.componentTextAreaContainerSizeSmallPaddingHorizontal;
    if (size === 'large') {
      paddingHorizontal =
        token.componentTextAreaContainerSizeLargePaddingHorizontal;
    }
    return (
      paddingHorizontal - token.componentTextAreaContainerBorderWidthDefault
    );
  };
  const resolvedTextColor = (isFocused: boolean = false) => {
    if (disabled) {
      return token.componentTextAreaValueTextColorDisabled;
    } else if (isFocused) {
      return token.componentTextAreaValueTextColorFocus;
    } else {
      return token.componentTextAreaValueTextColorDefault;
    }
  };
  const resolveCounterColor = () => {
    if (disabled) {
      return token.componentTextAreaMaxLengthTextColorDisabled;
    } else {
      return token.componentTextAreaMaxLengthTextColorDefault;
    }
  };
  const resolvePlaceHolderTextColor = () => {
    if (disabled) {
      return token.componentTextAreaValueTextColorDisabled;
    } else {
      return token.componentTextAreaValuePlaceholderTextColor;
    }
  };

  const initialState: TextAreaState = {
    focused: false,
    containerBorderColor: resolvedContainerBorderColor(),
    containerBorderWidth: resolvedContainerBorderWidth(),
    containerPaddingVertical: resolvedContainerPaddingVertical(),
    containerPaddingHorizontal: resolvedContainerPaddingHorizontal(),
    textColor: resolvedTextColor(),
    labelTextColor: resolvedTextColor(),
    helperTextColor: resolvedTextColor(),
    nrOfCharacters: value?.length ?? defaultValue?.length ?? 0,
    counterColor: token.componentTextAreaMaxLengthTextColorDefault,
  };

  const [state, setState] = useSimpleReducer<TextAreaState>(initialState);

  React.useEffect(() => {
    if (value === undefined) {
      return;
    }
    setState('nrOfCharacters', value?.length ?? 0);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [value]);

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
    setState('counterColor', resolveCounterColor());
    setState('labelTextColor', resolvedTextColor());
    setState('helperTextColor', resolvedTextColor());

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    disabled,
    error,
    readOnly,
    setState,
    size,
    state.containerBorderWidth,
    state.focused,
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
    setState('nrOfCharacters', _value.length);
    onChangeText?.(_value);
  };

  const resolveBlurOnSubmit = (_error: React.ReactNode) => {
    if (_error) {
      return {
        blurOnSubmit: false,
      };
    }
  };

  const resolveEditable = () => {
    if (disabled || readOnly || rest?.editable === false) {
      return false;
    }
    return true;
  };

  // ---------------
  // Rendering
  // ---------------
  return (
    <View
      accessibilityState={{disabled: disabled as boolean}}
      testID={TextArea.displayName}
      style={[ss(size).container, UNSAFE_style]}>
      {renderLabel(size, state as TextAreaState, label)}
      <View
        testID={TextArea.displayName + '-input-container'}
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
        <TextInput
          accessibilityState={{disabled}}
          accessible
          testID={TextArea.displayName + '-input'}
          ref={ref}
          multiline
          maxLength={maxLength ? maxLength : undefined}
          numberOfLines={8}
          style={[
            ss(size).textInput,
            {
              paddingHorizontal: state.paddingHorizontal as number,
              color: state.textColor as string,
            },
          ]}
          placeholderTextColor={resolvePlaceHolderTextColor()}
          value={value}
          defaultValue={defaultValue}
          editable={resolveEditable()}
          onChangeText={handleChangeText}
          onFocus={handleOnFocus}
          onBlur={handleOnBlur}
          onSubmitEditing={rest?.onSubmitEditing}
          placeholder={placeholder}
          underlineColorAndroid="transparent"
          autoCapitalize="none"
          showSoftInputOnFocus
          spellCheck={false}
          {...resolveBlurOnSubmit(error)}
          {...textAreaProps}
          {...rest}
        />
      </View>
      {renderHelperTextAndError(
        size,
        state as TextAreaState,
        error,
        helperText,
        maxLength,
      )}
    </View>
  );
});

// ---------------
// Styles
// ---------------
const ss = (size: TextAreaSize) => {
  return StyleSheet.create({
    container: {
      flex: 1,
      justifyContent: 'center',
    },
    labelContainer: {
      marginBottom: token.componentTextAreaTextLabelMarginBottom, // 4
    },
    label: {
      ...getFont('bold'), // @cory token missing
      fontSize: size === 'small' ? 12 : 14, // @cory Label FontSize is missing,
      lineHeight: size === 'small' ? 16 : 20, // @cory Label line hight is missing,
    } as TextStyle,
    inputContainer: {
      flexDirection: 'row',
      alignItems: 'center',
      ...getFont(),
      backgroundColor: token.componentTextAreaContainerBackgroundColor,
      borderRadius: token.componentTextAreaContainerBorderRadius, // 4
    },
    textInput: {
      width: '100%',
      ...getFont(token.componentTextAreaValueFontWeight.toString() as Weights),
      lineHeight:
        size === 'large'
          ? token.componentTextAreaValueSizeLargeLineHeight // 24,
          : token.componentTextAreaValueSizeSmallLineHeight, // 20,
      fontSize:
        size === 'large'
          ? token.componentTextAreaValueSizeLargeFontSize // 16,
          : token.componentTextAreaValueSizeSmallFontSize, // 14,
      height:
        size === 'large'
          ? token.componentTextAreaContainerSizeLargeMinHeight // 128
          : token.componentTextAreaContainerSizeSmallMinHeight, // 100
      minHeight:
        size === 'large'
          ? token.componentTextAreaContainerSizeLargeMinHeight // 128
          : token.componentTextAreaContainerSizeSmallMinHeight, // 100
      textAlignVertical: 'top',
      color: token.componentTextAreaValueTextColorDefault,
    } as TextStyle,
    helperTextAndErrorContainer: {
      flexDirection: 'row',
      justifyContent:
        token.componentTextAreaHelperTextContainerAlignHorizontal as Extract<
          // @cory incorrect TS type here
          FlexStyle,
          'justifyContent'
        >, // "space-between",
      paddingHorizontal: 4,
      // token.componentTextAreaHelperTextContainerPaddingHorizontal, // @cory token missing
      marginTop: token.componentTextAreaHelperTextContainerMarginTop, // 4,
    },
    counter: {
      ...getFont(),
      fontSize: token.componentTextAreaMaxLengthFontSize, // 12
      lineHeight: token.componentTextAreaMaxLengthLineHeight, // 16,
      marginLeft: token.componentTextAreaMaxLengthMarginStart, // 16,
      marginTop: token.componentTextAreaHelperTextContainerMarginTop, // 4
    } as TextStyle,
    errorContainer: {
      flex: 1,
      flexDirection: 'row',
      justifyContent: 'flex-start',
      alignItems: 'center',
    },
    helperText: {
      ...getFont(
        token.componentTextAreaMaxLengthFontWeight.toString() as Weights,
      ), // "400" // @cory token missing
      fontSize: token.componentTextAreaMaxLengthFontSize, // 12 // @cory token missing
      lineHeight: token.componentTextAreaMaxLengthLineHeight, // 16, // @cory token missing
      marginTop: token.componentTextAreaHelperTextContainerMarginTop, // 4
    } as TextStyle,
    errorText: {
      ...getFont(
        token.componentTextAreaMaxLengthFontWeight.toString() as Weights,
      ), // "400"
      fontSize: token.componentTextAreaMaxLengthFontSize, // 12 // @cory token missing
      color: token.componentTextAreaContainerStateErrorBorderColorDefault, // "#de1c24" // @cory token missing
      marginHorizontal:
        token.componentTextAreaHelperTextContainerMarginHorizontal, // 4
    },
  });
};

TextArea.displayName = 'TextArea';
export {TextArea};

// ---------------
// Render helpers
// (extracted and exported separately to facilitate testing)
// ---------------
export const renderLabel = (
  size: TextAreaSize,
  state: TextAreaState,
  label: React.ReactNode,
) => {
  return (
    <View
      testID={TextArea.displayName + '-label-container'}
      style={ss(size).labelContainer}
      accessible>
      <Text
        style={[ss(size).label, {color: state.labelTextColor} as TextStyle]}
        nativeID={`${TextArea.displayName}-label`}>
        {label}
      </Text>
    </View>
  );
};

export const renderHelperTextAndError = (
  size: TextAreaSize,
  state: TextAreaState,
  error: React.ReactNode,
  helperText: React.ReactNode,
  maxLength?: number,
) => {
  return (
    <>
      <View style={ss(size).helperTextAndErrorContainer} accessible>
        {error ? (
          <View style={ss(size).errorContainer} accessible>
            <Icons.ExclamationCircleFillIcon color="red" />
            <Text
              accessibilityRole={a11yRole('text')}
              style={ss(size).errorText as TextStyle}>
              {error}
            </Text>
          </View>
        ) : helperText ? (
          <Text
            accessibilityRole={a11yRole('text')}
            style={[
              ss(size).helperText,
              {color: state.helperTextColor} as TextStyle,
            ]}>
            {helperText}
          </Text>
        ) : null}
        {maxLength ? renderCounter(size, state, maxLength) : null}
      </View>
    </>
  );
};

export const renderCounter = (
  size: TextAreaSize,
  state: TextAreaState,
  maxLength: number,
) => {
  return (
    <Text
      accessibilityRole={a11yRole('text')}
      style={[ss(size).counter, {color: state.counterColor} as TextStyle]}>
      {state.nrOfCharacters}
      {'/'}
      {maxLength}
    </Text>
  );
};
