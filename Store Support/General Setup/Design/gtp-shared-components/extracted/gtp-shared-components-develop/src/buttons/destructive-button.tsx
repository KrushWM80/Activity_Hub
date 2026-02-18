import * as React from 'react';

import ThemedButton, {
  ThemedButtonExternalSizeProps,
  ThemedButtonExternalSmallProps,
  ThemedButtonLoadingProps,
} from './base/themed-button';

export type DestructiveButtonProps = ThemedButtonExternalSizeProps &
  ThemedButtonExternalSmallProps &
  ThemedButtonLoadingProps;

/**
 * @deprecated: use <Button variant="destructive" .../> instead
 */
const DestructiveButton = ({size, ...props}: DestructiveButtonProps) => (
  <ThemedButton
    type={`destructive${
      size === 'medium' ? 'Medium' : size === 'large' ? 'Large' : 'Small'
    }`}
    {...props}
  />
);

DestructiveButton.displayName = 'DestructiveButton';

export default DestructiveButton;
