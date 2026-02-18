import * as React from 'react';

import ThemedTextField, {
  ThemedTextFieldExternalProps,
} from './base/themed-textfield';

type PasswordFieldState = {
  secure?: boolean;
};

export type PasswordFieldProps = Omit<
  ThemedTextFieldExternalProps,
  'trailingIcon' | 'trailingLink' | 'onTrailingIconPress' | 'onLinkPress'
> & {
  secure?: boolean;
  defaultSecure?: boolean;
  /**
   * This password field's secure change handler.
   */
  onSecureChange?: (secure: boolean) => void;
};

/**
 * @deprecated use <strong><TextField type="password" /></strong>
 */
export default class PasswordField extends React.Component<
  PasswordFieldProps,
  PasswordFieldState
> {
  state: PasswordFieldState = {
    secure: this.props.defaultSecure,
  };
  static defaultProps: Partial<PasswordFieldProps> = {
    defaultSecure: true,
  };

  static getDerivedStateFromProps = (
    props: PasswordFieldProps,
    state: PasswordFieldState,
  ) => ({
    secure: props.secure ?? state.secure,
  });

  render() {
    const {secure, onSecureChange, ...props} = this.props;
    return (
      <ThemedTextField
        secureTextEntry={this.state.secure}
        {...props}
        type="textField"
        trailingLink={!this.state.secure ? 'Hide' : 'Show'}
        onLinkPress={() =>
          this.setState({secure: !this.state.secure}, () =>
            onSecureChange?.(!!this.state.secure),
          )
        }
      />
    );
  }
}
