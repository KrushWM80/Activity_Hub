import * as React from 'react';

import AlertBase, {AlertExternalProps} from './base/alert';

export type AlertProps = AlertExternalProps;

/**
 * @deprecated use <strong><Banner /></strong> instead
 */
const Alert = ({...props}: AlertProps) => <AlertBase {...props} />;

export default Alert;
