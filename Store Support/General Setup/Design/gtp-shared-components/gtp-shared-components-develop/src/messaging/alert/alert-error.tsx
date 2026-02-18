import * as React from 'react';

import AlertBase, {AlertExternalProps} from './base/alert';

export type AlertErrorProps = AlertExternalProps;

/**
 * @deprecated use <strong><Banner variant="error"/></strong> instead
 */
const AlertError = ({...props}: AlertErrorProps) => (
  <AlertBase type="error" {...props} />
);

export default AlertError;
