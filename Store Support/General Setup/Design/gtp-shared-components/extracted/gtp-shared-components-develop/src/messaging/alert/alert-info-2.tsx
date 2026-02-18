import * as React from 'react';

import AlertBase, {AlertExternalProps} from './base/alert';

export type AlertInfo2Props = AlertExternalProps;

/**
 * @deprecated use <strong><Banner variant="info"/></strong> instead
 */
const AlertInfo2 = ({...props}: AlertInfo2Props) => (
  <AlertBase type="info2" {...props} />
);

export default AlertInfo2;
