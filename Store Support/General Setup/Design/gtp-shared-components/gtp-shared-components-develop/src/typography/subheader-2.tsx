import * as React from 'react';

import TextBase, {TextBaseExternalProps} from './base/text';

export type Subheader2Props = TextBaseExternalProps;

/**
 * @deprecated use <Heading /> instead
 */
const Subheader2 = (props: Subheader2Props) => (
  <TextBase type="subheader2" {...props} />
);

Subheader2.displayName = 'Subheader2';

export default Subheader2;
