import * as React from 'react';

import BaseFlag, {BaseFlagExternalProps} from './base/flag';

export type FilledFlagProps = BaseFlagExternalProps;

/**
 * @deprecated use Tag instead
 */
export const FilledFlag = ({...props}: FilledFlagProps) => (
  <BaseFlag type="filled" {...props} />
);
