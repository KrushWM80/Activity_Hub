import * as React from 'react';

import {CheckboxExternalProps} from './checkbox';
import CheckboxItem from './checkbox-item';

type CheckboxItemProps = Omit<CheckboxExternalProps, 'onChange'> & {
  label: string;
  id: string;
};

export type CheckboxItemGroupProps = {
  selectedIds?: Array<string>;
  onSelect?: (ids: Array<string>) => void;
  items: Array<CheckboxItemProps>;
};

const toggleItem = (items: Array<string>, item: string) => {
  if (items.includes(item)) {
    return items.filter((i) => i !== item);
  }
  return [...items, item];
};

/**
 * @deprecated use FormGroup instead
 */
const CheckboxItemGroup = ({
  items,
  selectedIds,
  onSelect,
}: CheckboxItemGroupProps) => (
  <>
    {items.map((item, i) => {
      const {label, id, ...rest} = item;
      return (
        <CheckboxItem
          key={`CheckboxItem_${i}_${id}`}
          label={label}
          value={selectedIds?.includes(id)}
          onChange={() => onSelect?.(toggleItem(selectedIds ?? [], id))}
          {...rest}
        />
      );
    })}
  </>
);

export default CheckboxItemGroup;
