import * as React from 'react';

import TagBase, {TagBaseExternalProps} from './base/tag';

export type TertiaryTagProps = TagBaseExternalProps;

/**
 * @deprecated use Tag instead
 */
export const TertiaryTag = ({...props}: TertiaryTagProps) => (
  <TagBase type="tertiary" {...props} />
);

TertiaryTag.displayName = 'TertiaryTag';
