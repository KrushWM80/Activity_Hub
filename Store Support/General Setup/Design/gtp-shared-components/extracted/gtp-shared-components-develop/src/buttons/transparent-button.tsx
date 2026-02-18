import * as React from 'react';

import {
  BaseButtonExternalSizeProps,
  BaseButtonExternalSmallProps,
  BaseButtonLoadingProps,
} from './base/button';
import ThemedButton from './base/themed-button';

export type TransparentButtonProps = BaseButtonExternalSizeProps &
  BaseButtonExternalSmallProps &
  BaseButtonLoadingProps;

/**
 * @deprecated use <Button variant="secondary" .../> instead
 */
const TransparentButton = ({size, ...props}: TransparentButtonProps) => (
  <ThemedButton
    type={`transparent${
      size === 'medium' ? 'Medium' : size === 'large' ? 'Large' : 'Small'
    }`}
    {...props}
  />
);

TransparentButton.displayName = 'TransparentButton';

export default TransparentButton;
