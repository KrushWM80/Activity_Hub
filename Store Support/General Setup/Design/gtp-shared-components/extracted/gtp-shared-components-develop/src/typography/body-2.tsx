import * as React from 'react';

import TextBase, {TextBaseExternalProps} from './base/text';

export type Body2Props = TextBaseExternalProps;

/**
 * @deprecated use <Body weight="700" /> instead
 */
const Body2 = (props: Body2Props) => <TextBase type="body2" {...props} />;
Body2.displayName = 'Body2';
export default Body2;
