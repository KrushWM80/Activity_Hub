import * as React from 'react';

import AlertBase, {AlertExternalProps} from './base/alert';

export type AlertInfoProps = AlertExternalProps;

/**
 * @deprecated use <strong><Banner variant="info"/></strong> instead
 */
const AlertInfo = ({...props}: AlertInfoProps) => (
  <AlertBase type="info" {...props} />
);

export default AlertInfo;
