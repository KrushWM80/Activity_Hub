import * as React from 'react';

import MessageBase, {MessageBaseExternalProps} from './base/message';

export type MessageWarningProps = MessageBaseExternalProps;

/**
 * @deprecated use <strong>\<Alert variant="warning" \/\></strong> instead
 */
const MessageWarning = ({...props}: MessageWarningProps) => (
  <MessageBase type="warning" {...props} />
);

export default MessageWarning;
