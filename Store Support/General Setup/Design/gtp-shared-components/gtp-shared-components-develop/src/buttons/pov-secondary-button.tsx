import * as React from 'react';

import {
  BaseButtonExternalSmallProps,
  BaseButtonLoadingProps,
} from './base/button';
import ThemedButton from './base/themed-button';

export type POVSecondaryButtonProps = BaseButtonExternalSmallProps &
  BaseButtonLoadingProps;

/**
 * @deprecated this is not in the LD specs
 */
const POVSecondaryButton = ({small, ...props}: POVSecondaryButtonProps) => (
  <ThemedButton type={`povSecondary${small ? 'Small' : ''}`} {...props} />
);

POVSecondaryButton.displayName = 'POVSecondaryButton';

export default POVSecondaryButton;
