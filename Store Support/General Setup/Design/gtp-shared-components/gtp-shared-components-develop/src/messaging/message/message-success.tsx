import * as React from 'react';

import MessageBase, {MessageBaseExternalProps} from './base/message';

export type MessageSuccessProps = MessageBaseExternalProps;

/**
 * @deprecated use <strong>\<Alert variant="success" \/\></strong> instead
 */
export const MessageSuccess = ({...props}: MessageSuccessProps) => (
  <MessageBase type="success" {...props} />
);

export default MessageSuccess;
