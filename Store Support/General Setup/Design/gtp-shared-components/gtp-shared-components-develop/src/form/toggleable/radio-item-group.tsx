import * as React from 'react';

import {RadioExternalProps} from './radio';
import RadioItem from './radio-item';

export type RadioItemGroupItemProps = Omit<RadioExternalProps, 'onChange'> & {
  label: string;
  id: string;
};

export type RadioItemGroupProps = {
  selectedId?: string;
  onSelect?: (id: string) => void;
  items: Array<RadioItemGroupItemProps>;
};

/**
 * @deprecated use FormGroup instead
 */
const RadioItemGroup = ({items, selectedId, onSelect}: RadioItemGroupProps) => (
  <>
    {items.map((item, i) => {
      const {label, id, ...rest} = item;
      return (
        <RadioItem
          key={`RadioItem_${i}_${id}`}
          label={item.label}
          value={item.id === selectedId}
          onChange={() => onSelect?.(item.id)}
          {...rest}
        />
      );
    })}
  </>
);

export default RadioItemGroup;
