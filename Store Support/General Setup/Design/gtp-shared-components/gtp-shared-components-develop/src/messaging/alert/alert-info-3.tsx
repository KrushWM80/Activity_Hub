import * as React from 'react';

import AlertBase, {AlertExternalProps} from './base/alert';

export type AlertInfo3Props = AlertExternalProps;

/**
 * @deprecated use <strong><Banner variant="info"/></strong> instead
 */
const AlertInfo3 = ({...props}: AlertInfo3Props) => (
  <AlertBase type="info3" {...props} />
);

export default AlertInfo3;
