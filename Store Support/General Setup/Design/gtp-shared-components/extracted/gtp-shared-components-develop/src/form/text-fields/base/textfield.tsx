import * as React from 'react';
import {
  GestureResponderEvent,
  NativeSyntheticEvent,
  Platform,
  StyleProp,
  TextInput,
  TextInputContentSizeChangeEventData,
  TextInputProps,
  TouchableHighlight,
  TouchableOpacity,
  View,
  ViewStyle,
} from 'react-native';

import {Icons} from '@walmart/gtp-shared-icons';

import {LinkButton} from '../../../buttons';
import {Caption} from '../../../next/components/Caption';
import {ThemeObject} from '../../../theme/theme-provider';

export type TextFieldBaseExternalProps = Omit<
  TextInputProps,
  'maxLength' | 'multiline' | 'numberOfLines' | 'onChangeText' | 'hitSlop'
> & {
  /**
   * Leading icon serves for aesthetic purposes.  These icons will indicate what the user needs to input; for example, an envelope will indicate an email address, a geo-pin will indicate an address. Leading icons can be dynamic. For example, credit card icon is replaced by a credit card image once the first four digits are validated.
   */
  leadingIcon?: React.ReactElement;
  /**
   * Label text is used to inform users as to what information is requested for a text field. Every text field should have a label.
   */
  label: string;
  /**
   * Helper text is used to inform users as to what information is requested for a text field.
   */
  helperText?: string;
  /**
   * Whether this text field is disabled.
   */
  disabled?: boolean;
  /**
   * This text field's text change handler.
   */
  onTextChange?: (value?: string) => void;
  /**
   * This text field's message to be displayed when it is in an `error` state.
   */
  errorMessage?: string;
  /**
   * This text field's message to be displayed when it is in an `success` state.
   */
  successMessage?: string;
  /**
   * Whether to show the appropriate state icon when in `error` or `success` state.
   */
  stateIcon?: boolean;
  /**
   * This text field's state.
   */
  state?: 'success' | 'error';
  /**
   * Limits the maximum number of characters that can be entered.
   */
  maxLength?: number;
  /**
   * Whether to show the character counter (when `maxLength` is set).
   */
  counter?: boolean;
  /**
   * Internal reference for the TextInput component.
   */
  inputRef?: React.RefObject<TextInput>;
  /**
   * Whether helper text is important for accessibility
   */
  helperTextImportantForA11y?: 'yes' | 'no';
} & (
    | {
        trailingIcon?: never;
        onTrailingIconPress?: never;
        trailingLink?: never;
        onLinkPress?: never;
      }
    | {
        /**
         * A trailing icon allows the user to control text fields.  A text field may have either a trailing icon or a trailing link, but never both.
         */
        trailingIcon: React.ReactElement;
        /**
         * This text field's trailing icon press handler.
         */
        onTrailingIconPress: (event: GestureResponderEvent) => void;
        trailingLink?: never;
        onLinkPress?: never;
      }
    | {
        trailingIcon?: never;
        onTrailingIconPress?: never;
        /**
         * A trailing link allows the user to control text fields.  A text field may have either a trailing link or a trailing icon, but never both.
         */
        trailingLink: string;
        /**
         * This text field's trailing icon press handler.
         */
        onLinkPress: (event: GestureResponderEvent) => void;
      }
  );

export type TextFieldLineProps = {
  autoSize?: boolean;
  multiline?: boolean;
  numberOfLines?: number;
  active?: boolean;
};

type TextFieldContainerProps = {
  style: StyleProp<ViewStyle>;
  disabled?: boolean;
  children: React.ReactNode;
  onPress?: (event: GestureResponderEvent) => void;
};

export type TextFieldBaseProps = TextFieldBaseExternalProps &
  TextFieldLineProps &
  Omit<TextFieldContainerProps, 'disabled' | 'children' | 'style'> & {
    theme: ThemeObject;
  };

type TextFieldBaseState = {
  inputState?: 'active';
  value?: string;
  lines?: number;
};

const Container = (props: TextFieldContainerProps) => {
  const {onPress, disabled, style, children} = props;
  if (onPress) {
    return (
      <TouchableOpacity
        activeOpacity={1}
        disabled={disabled}
        onPress={onPress}
        style={style}>
        <View pointerEvents="none">{children}</View>
      </TouchableOpacity>
    );
  }
  return <View style={style}>{children}</View>;
};

export default class TextFieldBase extends React.Component<
  TextFieldBaseProps,
  TextFieldBaseState
> {
  state: TextFieldBaseState = {
    value: this.props.value ?? this.props.defaultValue,
  };
  static defaultProps: Partial<TextFieldBaseProps> = {
    stateIcon: true,
  };
  private inputRef = React.createRef<TextInput>();
  currentState = () => {
    if (this.props.disabled) {
      return 'disabled';
    }
    if (this.props.state === 'success') {
      if (this.state.inputState === 'active' || this.props.active) {
        return 'successActive';
      }
      if (this.state.value) {
        return 'successFilled';
      }
      return 'success';
    }
    if (this.props.state === 'error') {
      if (this.state.inputState === 'active' || this.props.active) {
        return 'errorActive';
      }
      if (this.state.value) {
        return 'errorFilled';
      }
      return 'error';
    }
    if (this.state.inputState === 'active' || this.props.active) {
      return 'active';
    }
    if (this.state.value) {
      return 'filled';
    }
    return 'default';
  };
  private setValue = (value?: string) => {
    this.setState({value}, () => {
      this.props.onTextChange?.(value);
    });
  };
  private setSize =
    (lineheight: number) =>
    (event: NativeSyntheticEvent<TextInputContentSizeChangeEventData>) => {
      this.setState(
        {lines: Math.ceil(event.nativeEvent.contentSize.height / lineheight)},
        () => this.props.onContentSizeChange?.(event),
      );
    };
  private helperMessage = () => {
    if (this.props.state === 'error') {
      return this.props.errorMessage ?? this.props.helperText;
    }
    if (this.props.state === 'success') {
      return this.props.successMessage ?? this.props.helperText;
    }
    return this.props.helperText;
  };
  private getRef = () => {
    return this.props.inputRef ?? this.inputRef;
  };
  public focus = () => {
    this.getRef().current?.focus();
  };
  componentDidUpdate(prevProps: TextFieldBaseProps) {
    if (prevProps.value !== this.props.value) {
      this.setState({value: this.props.value ?? this.props.defaultValue});
    }
  }
  render() {
    const {
      leadingIcon,
      trailingIcon,
      trailingLink,
      onLinkPress,
      label,
      placeholder,
      helperText,
      maxLength,
      counter,
      disabled,
      editable,
      theme,
      stateIcon,
      multiline,
      autoSize,
      numberOfLines,
      onTrailingIconPress,
      onPress,
      style,
      ...props
    } = this.props;
    const themeState = this.currentState();
    return (
      <Container
        onPress={onPress}
        disabled={disabled}
        style={[theme.part(themeState, 'container'), style]}>
        <View style={theme.part(themeState, 'fieldContainer')}>
          {leadingIcon && (
            <View style={theme.part(themeState, 'leadingIconContainer')}>
              {React.cloneElement(leadingIcon, {
                size: theme.part('static.iconSize'),
                style: theme.part(themeState, 'leadingIcon'),
              })}
            </View>
          )}
          <View style={theme.part(themeState, 'inputContainer')}>
            <View
              style={[
                theme.part(themeState, 'labelContainer'),
                leadingIcon &&
                  theme.part(themeState, 'labelContainerWithLeadingIcon'),
              ]}>
              <Caption
                numberOfLines={theme.part('static.iconSize')}
                UNSAFE_style={theme.part(themeState, 'label')}>
                {label}
              </Caption>
            </View>
            <TextInput
              {...props}
              hitSlop={theme.part(themeState, 'inputHitSlop')}
              ref={this.getRef()}
              maxLength={maxLength ? maxLength : undefined}
              editable={!disabled && editable}
              placeholder={themeState !== 'active' ? placeholder || label : ''}
              onChangeText={this.setValue}
              onContentSizeChange={
                Platform.OS === 'android' && autoSize
                  ? this.setSize(theme.part('static.lineHeight'))
                  : props.onContentSizeChange
              }
              onFocus={(e) =>
                this.setState({inputState: 'active'}, () => props.onFocus?.(e))
              }
              onBlur={(e) =>
                this.setState({inputState: undefined}, () => props.onBlur?.(e))
              }
              multiline={multiline}
              numberOfLines={numberOfLines}
              style={[
                theme.part(themeState, 'input'),
                multiline &&
                  numberOfLines &&
                  !autoSize && {
                    height: theme.part('static.lineHeight') * numberOfLines,
                  },
                multiline &&
                  numberOfLines && {
                    maxHeight: theme.part('static.lineHeight') * numberOfLines,
                  },
                Platform.OS === 'android' &&
                  this.state.lines && {
                    height:
                      theme.part('static.lineHeight') *
                      (numberOfLines
                        ? Math.min(numberOfLines, this.state.lines || 1)
                        : Math.max(1, this.state.lines || 1)),
                  },
              ]}
              placeholderTextColor={theme.part(themeState, 'placeholder')}
              underlineColorAndroid="transparent"
            />
          </View>
          {trailingLink && onLinkPress && (
            <View style={theme.part(themeState, 'trailingLinkContainer')}>
              <LinkButton
                small
                onPress={onLinkPress}
                style={theme.part(themeState, 'trailingLink')}>
                {trailingLink}
              </LinkButton>
            </View>
          )}
          {trailingIcon && (
            <TouchableHighlight
              underlayColor={theme.part('static.underlayColor')}
              accessibilityRole={
                !process.env.STYLEGUIDIST_ENV ? 'button' : undefined
              }
              style={theme.part(themeState, 'trailingIconContainer')}
              onPress={onTrailingIconPress}>
              {React.cloneElement(trailingIcon, {
                size: theme.part('static.iconSize'),
                style: theme.part(themeState, 'trailingIcon'),
              })}
            </TouchableHighlight>
          )}
          {!trailingIcon && this.props.state === 'success' && (
            <View style={theme.part(themeState, 'trailingIconContainer')}>
              <Icons.CheckCircleFillIcon
                size={theme.part('static.iconSize')}
                UNSAFE_style={[
                  theme.part(themeState, 'trailingIcon'),
                  theme.part('static.successIcon'),
                ]}
              />
            </View>
          )}
        </View>
        {(this.helperMessage() || (this.props.state && stateIcon)) && (
          <View style={theme.part(themeState, 'helperContainer')}>
            <Caption
              importantForAccessibility={this.props.helperTextImportantForA11y}
              numberOfLines={
                theme.part('static.helperLines') > 0
                  ? theme.part('static.helperLines')
                  : undefined
              }
              UNSAFE_style={theme.part(themeState, 'helper')}>
              {this.helperMessage()}
            </Caption>
            {this.props.state === 'error' && stateIcon && (
              <View style={theme.part('static.stateIconContainer')}>
                <Icons.ExclamationCircleFillIcon
                  size={16}
                  UNSAFE_style={theme.part('static.errorIcon')}
                />
              </View>
            )}
            {this.props.state === 'success' && stateIcon && (
              <View style={theme.part('static.stateIconContainer')}>
                <Icons.CheckCircleFillIcon
                  size={16}
                  UNSAFE_style={theme.part('static.successIcon')}
                />
              </View>
            )}
            {counter && (
              <Caption UNSAFE_style={theme.part(themeState, 'counter')}>
                {this.state.value?.length ?? 0}/{this.props.maxLength}
              </Caption>
            )}
          </View>
        )}
      </Container>
    );
  }
}
