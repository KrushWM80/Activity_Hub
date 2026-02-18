import * as React from 'react';

import BaseBadge, {BaseBadgeProps} from './base/badge';

export type AvailabilityBadgeProps = BaseBadgeProps;

/**
 * This badge is for use with product tiles to give customers insight into how quickly an item can be fullfilled.
 * #### Badges are used to draw a customer’s focus to item traits such as availability, status, media rating or count. Items may be  products, fulfillment slots or something else. They are visual only and non-interactive.
 *
 * ```js
 * import {AvailabilityBadge} from '@walmart/gtp-shared-components';
 * ```
 */
/**
 * @deprecated: use <Badge .../> instead
 */
const AvailabilityBadge = ({...props}: AvailabilityBadgeProps) => (
  <BaseBadge type="availability" {...props} />
);

AvailabilityBadge.displayName = 'AvailabilityBadge';

export default AvailabilityBadge;
