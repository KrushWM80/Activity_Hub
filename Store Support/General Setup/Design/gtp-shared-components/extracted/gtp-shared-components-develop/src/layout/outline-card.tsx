import * as React from 'react';

import Card, {OutlineCardBaseProps} from './card';

export type OutlineCardProps = Omit<OutlineCardBaseProps, 'type' | 'elevation'>;
/**
 * @deprecated use <strong><Card ... /></strong> instead
 */
const OutlineCard = ({...props}: OutlineCardProps) => (
  <Card elevation={undefined} type="outline" {...props} />
);

export default OutlineCard;
