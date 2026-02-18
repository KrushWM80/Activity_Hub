import * as React from 'react';

import ThemedTextField, {
  ThemedTextFieldExternalProps,
} from './base/themed-textfield';

export type TextAreaProps = ThemedTextFieldExternalProps & {
  /** The maximum number of lines to show. */
  numberOfLines?: number;
};

/**
 * Text Areas are taller than Text Fields and wrap overflow text onto
 * a new line. They are a fixed height and scroll vertically when the
 * cursor reaches the bottom of the field.
 *
 */
const TextArea = ({...props}: TextAreaProps) => (
  <ThemedTextField multiline type={'textField'} {...props} />
);

export default TextArea;
