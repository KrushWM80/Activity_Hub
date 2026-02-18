import * as React from 'react';

import {ToggleExternalProps} from './toggle';
import ToggleItem from './toggle-item';

type ToggleItemProps = Omit<ToggleExternalProps, 'onValueChange'> & {
  label: string;
  id: string;
};

export type ToggleItemGroupProps = {
  selectedIds?: Array<string>;
  onSelect?: (ids: Array<string>) => void;
  items: Array<ToggleItemProps>;
};

const toggleItem = (items: Array<string>, item: string) => {
  if (items.includes(item)) {
    return items.filter((i) => i !== item);
  }
  return [...items, item];
};

/**
 * @deprecated use Switch instead
 */
const ToggleItemGroup = ({
  items,
  selectedIds,
  onSelect,
}: ToggleItemGroupProps) => (
  <>
    {items.map((item, i) => {
      const {label, id, ...rest} = item;
      return (
        <ToggleItem
          key={`ToggleItem_${i}_${id}`}
          value={selectedIds?.includes(id)}
          onValueChange={() => onSelect?.(toggleItem(selectedIds ?? [], id))}
          {...rest}>
          {label}
        </ToggleItem>
      );
    })}
  </>
);

export default ToggleItemGroup;
