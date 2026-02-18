import * as React from 'react';

import TextBase, {TextBaseExternalProps} from './base/text';

export type Title3Props = TextBaseExternalProps;

/**
 * @deprecated use </Heading /> instead
 */
const Title3 = (props: Title3Props) => <TextBase type="title3" {...props} />;

Title3.displayName = 'Title3';

export default Title3;
