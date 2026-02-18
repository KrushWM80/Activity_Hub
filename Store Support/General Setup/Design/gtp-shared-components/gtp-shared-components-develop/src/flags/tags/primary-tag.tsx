import * as React from 'react';

import TagBase, {TagBaseExternalProps} from './base/tag';

export type PrimaryTagProps = TagBaseExternalProps;

/**
 * @deprecated use Tag instead
 */
export const PrimaryTag = ({...props}: PrimaryTagProps) => (
  <TagBase type="primary" {...props} />
);

PrimaryTag.displayName = 'PrimaryTag';
