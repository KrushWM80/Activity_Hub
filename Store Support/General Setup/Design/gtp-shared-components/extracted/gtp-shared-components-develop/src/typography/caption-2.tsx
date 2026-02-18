import * as React from 'react';

import TextBase, {TextBaseExternalProps} from './base/text';

export type Caption2Props = TextBaseExternalProps;

/**
 * @deprecated use <Caption weight="700"/> instead
 */
const Caption2 = (props: Caption2Props) => (
  <TextBase type="caption2" {...props} />
);
Caption2.displayName = 'Caption2';
export default Caption2;
