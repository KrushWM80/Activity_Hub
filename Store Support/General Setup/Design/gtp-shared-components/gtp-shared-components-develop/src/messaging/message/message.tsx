import * as React from 'react';

import MessageBase, {MessageBaseExternalProps} from './base/message';

export type MessageProps = MessageBaseExternalProps;

/**
 * @deprecated use <strong>\<Alert \/\></strong> instead
 */
const Message = ({...props}: MessageProps) => <MessageBase {...props} />;

export default Message;
