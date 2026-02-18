import * as React from 'react';

import ThemedTextField, {
  ThemedTextFieldExternalProps,
} from './base/themed-textfield';

export type MultiLineTextFieldProps = ThemedTextFieldExternalProps & {
  /** The maximum number of lines to show. */
  numberOfLines?: number;
};

/**
 * @deprecated use <strong><TextField /></strong> instead
 */
const MultilineTextField = ({...props}: MultiLineTextFieldProps) => (
  <ThemedTextField multiline autoSize type={'textField'} {...props} />
);

export default MultilineTextField;
