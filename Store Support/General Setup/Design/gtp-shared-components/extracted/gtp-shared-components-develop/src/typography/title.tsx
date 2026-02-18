import * as React from 'react';

import TextBase, {TextBaseExternalProps} from './base/text';

export type TitleProps = TextBaseExternalProps;

/**
 * @deprecated use <Heading /> instead
 */
const Title = (props: TitleProps) => <TextBase type="title" {...props} />;

Title.displayName = 'Title';

export default Title;
