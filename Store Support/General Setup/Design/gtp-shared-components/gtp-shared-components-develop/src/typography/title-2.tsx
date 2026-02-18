import * as React from 'react';

import TextBase, {TextBaseExternalProps} from './base/text';

export type Title2Props = TextBaseExternalProps;

/**
 * @deprecated use </Heading /> instead
 */
const Title2 = (props: Title2Props) => <TextBase type="title2" {...props} />;

Title2.displayName = 'Title2';

export default Title2;
