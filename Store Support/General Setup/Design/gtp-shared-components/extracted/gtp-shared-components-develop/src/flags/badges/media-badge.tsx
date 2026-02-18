import * as React from 'react';

import BaseBadge, {BaseBadgeProps} from './base/badge';

export type MediaBadgeProps = BaseBadgeProps;
/**
 * This badge is for giving non-critical, state information.
 * #### Badges are used to draw a customer’s focus to item traits such as availability, status, media rating or count. Items may be  products, fulfillment slots or something else. They are visual only and non-interactive.
 *
 * ```js
 * import {MediaBadge} from '@walmart/gtp-shared-components';
 * ```
 */
/**
 * @deprecated: use <Badge .../> instead
 */
const MediaBadge = ({...props}: BaseBadgeProps) => (
  <BaseBadge type="media" {...props} />
);

MediaBadge.displayName = 'MediaBadge';

export default MediaBadge;
