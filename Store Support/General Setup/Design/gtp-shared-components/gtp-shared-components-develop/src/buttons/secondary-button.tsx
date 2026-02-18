import * as React from 'react';

import {
  BaseButtonExternalSizeProps,
  BaseButtonExternalSmallProps,
  BaseButtonLoadingProps,
} from './base/button';
import ThemedButton from './base/themed-button';

export type SecondaryButtonProps = BaseButtonExternalSizeProps &
  BaseButtonExternalSmallProps &
  BaseButtonLoadingProps;

/**
 * @deprecated: use <Button variant="secondary" .../> instead
 */
const SecondaryButton = ({size, ...props}: SecondaryButtonProps) => (
  <ThemedButton
    type={`secondary${
      size === 'medium' ? 'Medium' : size === 'large' ? 'Large' : 'Small'
    }`}
    {...props}
  />
);

SecondaryButton.displayName = 'SecondaryButton';

export default SecondaryButton;
