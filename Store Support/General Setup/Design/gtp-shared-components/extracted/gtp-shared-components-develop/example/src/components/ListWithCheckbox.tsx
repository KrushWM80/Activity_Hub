import * as React from 'react';
import {List, Checkbox, Icons, ListItem} from '@walmart/gtp-shared-components';

// ---------------
// Props
// ---------------
export type ListWithCheckboxProps = {
  selectedIds?: Array<number>;
  onSelect?: (ids: Array<number>) => void;
};

const ListWithCheckbox: React.FC<ListWithCheckboxProps> = (
  props: ListWithCheckboxProps,
) => {
  const {
    selectedIds = [],
    onSelect = () => {
      console.log;
    },
  } = props;

  const listSize = 4;
  const idOfOptionAll = 0;

  const resolveSelectedIds = (ids: Array<number>, id: number) => {
    if (id === idOfOptionAll) {
      if (ids.includes(id)) {
        return [];
      } else {
        return [...Array(listSize).keys()];
      }
    } else {
      if (ids.includes(id)) {
        return ids.filter(i => i !== id && i !== idOfOptionAll);
      } else {
        if (ids.length === listSize - 2) {
          return [...ids, id, idOfOptionAll];
        } else {
          return [...ids, id];
        }
      }
    }
  };

  // ---------------
  // Rendering
  // ---------------
  return (
    <>
      <List>
        <ListItem
          title="All Entertainment Associates"
          leading={<Icons.StarFillIcon />}
          trailing={
            <Checkbox
              checked={selectedIds?.includes(0)}
              onPress={() =>
                onSelect?.(resolveSelectedIds(selectedIds ?? [], 0))
              }
            />
          }>
          All Entertainment Associates
        </ListItem>
        <ListItem
          title="Amanda Jones"
          leading={<Icons.StarFillIcon />}
          trailing={
            <Checkbox
              checked={selectedIds?.includes(1)}
              onPress={() =>
                onSelect?.(resolveSelectedIds(selectedIds ?? [], 1))
              }
            />
          }>
          Entertainment TA\n8:00am - 5:00pm
        </ListItem>
        <ListItem
          title="Angela Reyes"
          leading={<Icons.StarFillIcon />}
          trailing={
            <Checkbox
              checked={selectedIds?.includes(2)}
              onPress={() =>
                onSelect?.(resolveSelectedIds(selectedIds ?? [], 2))
              }
            />
          }>
          Entertainment TA\n8:00am - 5:00pm
        </ListItem>
        <ListItem
          title="Chris Crawford"
          leading={<Icons.StarFillIcon />}
          trailing={
            <Checkbox
              checked={selectedIds?.includes(3)}
              onPress={() =>
                onSelect?.(resolveSelectedIds(selectedIds ?? [], 3))
              }
            />
          }>
          Entertainment TA\n8:00am - 5:00pm
        </ListItem>
      </List>
    </>
  );
};

ListWithCheckbox.displayName = 'ListWithCheckbox';
export {ListWithCheckbox};
