import * as React from 'react';

import BaseBadge, {BaseBadgeProps} from './base/badge';

export type InformationalBadgeProps = BaseBadgeProps;

/**
 * This badge is for use on product tiles to display ratings for digital products.
 * #### Badges are used to draw a customer’s focus to item traits such as availability, status, media rating or count. Items may be  products, fulfillment slots or something else. They are visual only and non-interactive.
 *
 * ```js
 * import {InformationalBadge} from '@walmart/gtp-shared-components';
 * ```
 */
/**
 * @deprecated: use <Badge .../> instead
 */
const InformationalBadge = ({...props}: InformationalBadgeProps) => (
  <BaseBadge type="informational" {...props} />
);

InformationalBadge.displayName = 'InformationalBadge';

export default InformationalBadge;
