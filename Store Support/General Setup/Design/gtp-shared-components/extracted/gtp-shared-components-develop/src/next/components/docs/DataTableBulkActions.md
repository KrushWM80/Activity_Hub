### DataTable With BulkActions

```js
import {
  DataTable,
  DataTableBody,
  DataTableCell,
  DataTableHead,
  DataTableHeader,
  DataTableHeaderSelect,
  DataTableCellSelect,
  DataTableBulkActions,
  DataTableRow,
  ButtonGroup,
  Button,
} from '@walmart/gtp-shared-components';

const bulkHeader = ['ID', 'Name'];
const bulkData = [
  {id: 1, name: 'Banana'},
  {id: 2, name: 'Peach'},
  {id: 3, name: 'Strawberry'},
];
const [simpleCellChecked, setSimpleCellChecked] = React.useState([]);
const onHeaderChecked = () => {
  if (simpleCellChecked.length < 3) {
    setSimpleCellChecked([1, 2, 3]);
  } else {
    setSimpleCellChecked([]);
  }
};
const selectAll = () => {
  setSimpleCellChecked([1, 2, 3]);
};
const clearAll = () => {
  setSimpleCellChecked([]);
};
<>
  <DataTableBulkActions
    actionContent={
      <ButtonGroup>
        <Button
          onPress={() =>
            displayPopupAlert('Action 1', `Selected Ids ${simpleCellChecked}`)
          }>
          Custom Action 1
        </Button>
        <Button
          onPress={() =>
            displayPopupAlert('Action 2', `Selected Ids ${simpleCellChecked}`)
          }>
          Custom Action 2
        </Button>
      </ButtonGroup>
    }
    count={simpleCellChecked.length}
    onClearSelected={clearAll}
    onSelectAll={selectAll}
  />
  <DataTable>
    <DataTableHead>
      <DataTableRow>
        <DataTableHeaderSelect
          onChange={onHeaderChecked}
          indeterminate={
            simpleCellChecked.length !== 0 && simpleCellChecked.length < 3
          }
          checked={simpleCellChecked.length === 3}
        />
        {bulkHeader.map((header, index) => (
          <DataTableHeader alignment={index === 2 ? 'right' : 'left'}>
            {header}
          </DataTableHeader>
        ))}
      </DataTableRow>
    </DataTableHead>
    <DataTableBody hor>
      {bulkData.map((item) => {
        const {id, name, isEdit} = item;
        return (
          <DataTableRow>
            <DataTableCellSelect
              checked={simpleCellChecked.includes(id)}
              onChange={() => {
                if (simpleCellChecked.includes(id)) {
                  const removed = simpleCellChecked.filter(
                    (item) => item !== id,
                  );
                  setSimpleCellChecked(removed);
                } else {
                  setSimpleCellChecked([...simpleCellChecked, id]);
                }
              }}
            />
            <DataTableCell>{id}</DataTableCell>
            <DataTableCell key={'name'}>{name}</DataTableCell>
          </DataTableRow>
        );
      })}
    </DataTableBody>
  </DataTable>
</>;
```