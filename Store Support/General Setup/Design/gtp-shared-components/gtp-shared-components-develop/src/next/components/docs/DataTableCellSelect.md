### DataTableCellSelect

```js
import {
  DataTable,
  DataTableBody,
  DataTableCell,
  DataTableHead,
  DataTableHeader,
  DataTableHeaderSelect,
  DataTableCellSelect,
  DataTableRow,
} from '@walmart/gtp-shared-components';

const selectHeader = ['ID', 'Name'];
const selectData = [
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
<DataTable>
  <DataTableHead>
    <DataTableRow>
      {selectHeader.map((header, index) => (
        <DataTableHeader>{header}</DataTableHeader>
      ))}
      <DataTableHeaderSelect
        alignment={'right'}
        onChange={onHeaderChecked}
        indeterminate={
          simpleCellChecked.length !== 0 && simpleCellChecked.length < 3
        }
        checked={simpleCellChecked.length === 3}
      />
    </DataTableRow>
  </DataTableHead>
  <DataTableBody hor>
    {selectData.map((item) => {
      const {id, name} = item;
      return (
        <DataTableRow>
          <DataTableCell>{id}</DataTableCell>
          <DataTableCell>{name}</DataTableCell>
          <DataTableCellSelect
            variant="numeric"
            checked={simpleCellChecked.includes(id)}
            onChange={() => {
              if (simpleCellChecked.includes(id)) {
                const removed = simpleCellChecked.filter((item) => item !== id);
                setSimpleCellChecked(removed);
              } else {
                setSimpleCellChecked([...simpleCellChecked, id]);
              }
            }}
          />
        </DataTableRow>
      );
    })}
  </DataTableBody>
</DataTable>;
```
