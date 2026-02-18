import * as React from 'react';

import BaseBadge, {BaseBadgeProps} from './base/badge';

export type CountBadgeProps = BaseBadgeProps;

/**
 * This badge is for showing the number of items selected or included.
 * #### Badges are used to draw a customer’s focus to item traits such as availability, status, media rating or count. Items may be  products, fulfillment slots or something else. They are visual only and non-interactive.
 *
 * ```js
 * import {CountBadge} from '@walmart/gtp-shared-components';
 * ```
 * */

/**
 * @deprecated: use <Badge .../> instead
 */
const CountBadge = ({...props}: CountBadgeProps) => (
  <BaseBadge type="count" {...props} />
);

CountBadge.displayName = 'CountBadge';

export default CountBadge;
