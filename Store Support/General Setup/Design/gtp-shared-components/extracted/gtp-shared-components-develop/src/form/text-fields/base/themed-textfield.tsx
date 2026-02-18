import * as React from 'react';
import {GestureResponderEvent} from 'react-native';

import {getThemeFrom, ThemeContext} from '../../../theme/theme-provider';
import {composed as defaultTheme} from '../../theme';

import TextFieldBase, {
  TextFieldBaseExternalProps,
  TextFieldLineProps,
} from './textfield';

export type ThemedTextFieldExternalProps = TextFieldBaseExternalProps;

export type ThemedTextFieldProps = TextFieldBaseExternalProps &
  TextFieldLineProps & {
    type: string;
    onPress?: (event: GestureResponderEvent) => void;
  };

/**
 * @internal
 */
export default class ThemedTextField extends React.Component<ThemedTextFieldProps> {
  static contextTypes = ThemeContext;

  render() {
    const {type, ...props} = this.props;
    const theme = getThemeFrom(this.context, defaultTheme, 'form', type);
    return <TextFieldBase {...props} theme={theme} />;
  }
}
