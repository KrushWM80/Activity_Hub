import * as React from 'react';

import TagBase, {TagBaseExternalProps} from './base/tag';

export type SecondaryTagProps = TagBaseExternalProps;

/**
 * @deprecated use Tag instead
 */
export const SecondaryTag = ({...props}: SecondaryTagProps) => (
  <TagBase type="secondary" {...props} />
);

SecondaryTag.displayName = 'SecondaryTag';
