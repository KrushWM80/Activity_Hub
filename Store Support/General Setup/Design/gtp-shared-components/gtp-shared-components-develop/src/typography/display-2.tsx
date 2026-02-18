import * as React from 'react';

import TextBase, {TextBaseExternalProps} from './base/text';

export type Display2Props = TextBaseExternalProps;

/**
 * @deprecated use <Display /> instead
 */
const Display2 = (props: Display2Props) => (
  <TextBase type="display2" {...props} />
);
Display2.displayName = 'Display2';
export default Display2;
