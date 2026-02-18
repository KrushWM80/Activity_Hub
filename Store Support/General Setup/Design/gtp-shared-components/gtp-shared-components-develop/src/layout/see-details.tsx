import * as React from 'react';

import CollapseBase, {CollapseBaseProps} from './collapse-base';

export type SeeDetailsProps = Omit<
  CollapseBaseProps,
  'icon' | 'simple' | 'title' | 'subtitle'
> & {
  /** Title text for this SeeDetails while hiding content.  If not set, "See Details" will be used. */
  showText?: string;
  /** Title text for this SeeDetails while showing content  If not set, "Hide Details" will be used.. */
  hideText?: string;
};

/**
 * SeeDetails is Refactored (aligned to current coding standards) and moved to the next folder
 * SeeDetails is not in the LD3 specs but will be preserved for backwards compatibility
 */
const SeeDetails = ({hideText, showText, ...props}: SeeDetailsProps) => (
  <CollapseBase
    simple
    title={
      props.expanded ? hideText ?? 'Hide Details' : showText ?? 'See Details'
    }
    {...props}
  />
);

export default SeeDetails;
