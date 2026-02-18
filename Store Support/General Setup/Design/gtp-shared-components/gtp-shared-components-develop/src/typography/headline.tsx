import * as React from 'react';

import TextBase, {TextBaseExternalProps} from './base/text';

export type HeadlineProps = TextBaseExternalProps;

/**
 * @deprecated use <Heading /> instead
 */
const Headline = (props: HeadlineProps) => (
  <TextBase type="headline" {...props} />
);
Headline.displayName = 'Headline';
export default Headline;
