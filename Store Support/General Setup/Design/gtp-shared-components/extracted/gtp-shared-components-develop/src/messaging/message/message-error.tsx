import * as React from 'react';

import MessageBase, {MessageBaseExternalProps} from './base/message';

export type MessageErrorProps = MessageBaseExternalProps;

/**
 * @deprecated use <strong>\<Alert variant="error" \/\></strong> instead
 */
const MessageError = ({...props}: MessageErrorProps) => (
  <MessageBase type="error" {...props} />
);

export default MessageError;
