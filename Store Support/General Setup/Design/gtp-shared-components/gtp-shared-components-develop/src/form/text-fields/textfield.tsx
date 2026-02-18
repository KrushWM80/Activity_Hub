import * as React from 'react';

import ThemedTextField, {
  ThemedTextFieldExternalProps,
} from './base/themed-textfield';

export type TextFieldProps = ThemedTextFieldExternalProps;

/**
 * Text Fields allow users to enter and edit text.
 *
 */
export const TextField = ({...props}: TextFieldProps) => (
  <ThemedTextField type={'textField'} {...props} />
);

export default TextField;
