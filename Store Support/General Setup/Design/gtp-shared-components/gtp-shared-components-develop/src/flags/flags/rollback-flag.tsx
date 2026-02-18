import * as React from 'react';

import BaseFlag, {BaseFlagExternalProps} from './base/flag';

export type RollbackFlagProps = BaseFlagExternalProps;

/**
 * @deprecated use Tag instead
 */
export const RollbackFlag = ({...props}: RollbackFlagProps) => (
  <BaseFlag type="rollback" {...props} />
);

RollbackFlag.displayName = 'RollbackFlag';
