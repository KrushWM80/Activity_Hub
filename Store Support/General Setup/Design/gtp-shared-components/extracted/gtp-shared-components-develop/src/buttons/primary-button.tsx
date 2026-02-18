import * as React from 'react';

import ThemedButton, {
  ThemedButtonExternalSizeProps,
  ThemedButtonExternalSmallProps,
  ThemedButtonLoadingProps,
} from './base/themed-button';

export type PrimaryButtonProps = ThemedButtonExternalSizeProps &
  ThemedButtonExternalSmallProps &
  ThemedButtonLoadingProps;

/**
 * @deprecated Use <Button variant="primary"... /> instead
 */
const PrimaryButton = ({size, ...props}: PrimaryButtonProps) => (
  <ThemedButton
    type={`primary${
      size === 'medium' ? 'Medium' : size === 'large' ? 'Large' : 'Small'
    }`}
    {...props}
  />
);

PrimaryButton.displayName = 'PrimaryButton';

export default PrimaryButton;
