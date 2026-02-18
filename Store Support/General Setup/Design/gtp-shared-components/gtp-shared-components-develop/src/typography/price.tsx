import * as React from 'react';

import {capitalize} from '../next/utils';

import TextBase, {TextBaseExternalProps} from './base/text';

export type PriceProps = TextBaseExternalProps;
type Size = 'small' | 'medium' | 'large';

/**
 * @deprecated use <Body isMonospace={true} />
 */
const Price = ({size, ...props}: PriceProps & {size: Size}) => (
  <TextBase type={`price${capitalize(size)}`} {...props} />
);

Price.displayName = 'Price';

export default Price;
