import * as React from 'react';

import TextBase, {TextBaseExternalProps} from './base/text';

export type SubheaderProps = TextBaseExternalProps;

/**
 * @deprecated use <Heading /> instead
 */
const Subheader = (props: SubheaderProps) => (
  <TextBase type="subheader" {...props} />
);

Subheader.displayName = 'Subheader';

export default Subheader;
