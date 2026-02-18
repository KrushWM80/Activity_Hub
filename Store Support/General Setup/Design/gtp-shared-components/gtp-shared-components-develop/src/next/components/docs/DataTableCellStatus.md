### DataTable With Status

```js
import {
  DataTable,
  DataTableBody,
  DataTableCell,
  DataTableHead,
  DataTableHeader,
  DataTableCellStatus,
  DataTableRow,
  Tag,
} from '@walmart/gtp-shared-components';

const statusHeader = ['Name', 'Status'];
const statusData = [
  {id: 1, name: 'Freyja Atli', status: 'Healthy'},
  {id: 2, name: 'Borghildr Sigurdr', status: 'Upset stomach'},
  {id: 3, name: 'Brynhild Idun', status: 'Unamused'},
];
const renderTag = (status, id) => {
  const color = id === 1 ? 'green' : id === 2 ? 'purple' : 'gray';
  return (
    <Tag color={color} variant={'tertiary'}>
      {status}
    </Tag>
  );
};

<DataTable>
  <DataTableHead>
    <DataTableRow>
      {statusHeader.map((header, index) => (
        <DataTableHeader>{header}</DataTableHeader>
      ))}
    </DataTableRow>
  </DataTableHead>
  <DataTableBody>
    {statusData.map((item) => {
      const {id, name, status} = item;
      return (
        <DataTableRow>
          <DataTableCell>{name}</DataTableCell>
          <DataTableCellStatus>{renderTag(status, id)}</DataTableCellStatus>
        </DataTableRow>
      );
    })}
  </DataTableBody>
</DataTable>;
```