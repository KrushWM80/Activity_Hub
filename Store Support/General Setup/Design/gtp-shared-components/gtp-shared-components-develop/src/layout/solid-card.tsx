import * as React from 'react';

import Card, {SolidCardBaseProps} from './card';

export type SolidCardProps = Omit<SolidCardBaseProps, 'type'>;

export type SolidCardExternalProps = SolidCardProps;
/**
 * @deprecated use <strong><Card ... /></strong> instead
 */
const SolidCard = ({...props}: SolidCardProps) => (
  <Card type="solid" {...props} />
);

export default SolidCard;
