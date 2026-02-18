import * as React from 'react';

import CollapseBase, {CollapseBaseProps} from './collapse-base';

/**
 * Collapse is refactored to current coding standards and moved to the next folder
 * Collapse is not in the LD3 specs but will be preserved for backwards compatibility
 */
const Collapse = ({...props}: Omit<CollapseBaseProps, 'simple'>) => (
  <CollapseBase {...props} />
);
export default Collapse;
