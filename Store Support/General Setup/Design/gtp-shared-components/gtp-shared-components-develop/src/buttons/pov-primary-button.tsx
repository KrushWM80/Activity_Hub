import * as React from 'react';

import {
  BaseButtonExternalSmallProps,
  BaseButtonLoadingProps,
} from './base/button';
import ThemedButton from './base/themed-button';

export type POVPrimaryButtonProps = BaseButtonExternalSmallProps &
  BaseButtonLoadingProps;

/**
 * @deprecated this is not in the LD specs
 */
const POVPrimaryButton = ({small, ...props}: POVPrimaryButtonProps) => (
  <ThemedButton type={`povPrimary${small ? 'Small' : ''}`} {...props} />
);

POVPrimaryButton.displayName = 'POVPrimaryButton';

export default POVPrimaryButton;
