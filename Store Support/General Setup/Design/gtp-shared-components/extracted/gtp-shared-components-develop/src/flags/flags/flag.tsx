import * as React from 'react';

import BaseFlag, {BaseFlagExternalProps} from './base/flag';

export type FlagProps = BaseFlagExternalProps;

/**
 * @deprecated use Tag instead
 */
export const Flag = ({...props}: FlagProps) => (
  <BaseFlag type="general" {...props} />
);

Flag.displayName = 'Flag';
