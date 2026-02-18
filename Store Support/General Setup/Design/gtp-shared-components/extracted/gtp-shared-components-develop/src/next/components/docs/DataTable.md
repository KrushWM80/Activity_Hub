### DataTable Sort

```js
import {
  DataTable,
  DataTableBody,
  DataTableCell,
  DataTableHead,
  DataTableHeader,
  DataTableRow,
  useSimpleReducer,
} from '@walmart/gtp-shared-components';

const actData = [
  {id: 1, name: 'Banana', quantity: 20},
  {id: 2, name: 'Peach', quantity: 30},
  {id: 3, name: 'Strawberry', quantity: 40},
];

const [sortOrder,setSortOrder]=React.useState('ascending');

const sortData=()=>{
  if(sortOrder !== 'none'){
    const sortedArray=actData.sort((a,b)=> sortOrder === 'descending' ? b.quantity - a.quantity : a.quantity - b.quantity);
    return sortedArray;
  }
  return actData;
};

const renderDataBody=()=>{
  const data=sortData();
 return data.map((item)=>{
    const {id,name,quantity}=item;
    return <DataTableRow>
      <DataTableCell>{id}</DataTableCell>
      <DataTableCell>{name}</DataTableCell>
      <DataTableCell variant="numeric">{quantity}</DataTableCell>
    </DataTableRow>
  })
};

<DataTable>
  <DataTableHead>
    <DataTableRow>
      <DataTableHeader>{'ID'}</DataTableHeader>
      <DataTableHeader>{'Name'}</DataTableHeader>
      <DataTableHeader
      alignment={'right'}
      sort={sortOrder}
      onSort={type =>setSortOrder(type)}>{'Count'}</DataTableHeader>
    </DataTableRow>
  </DataTableHead>
  <DataTableBody>
  {renderDataBody(sortOrder)}
  </DataTableBody>
</DataTable>;
```
### DataTable With HorizontalScroll

```js
import {
  DataTable,
  DataTableBody,
  DataTableCell,
  DataTableHead,
  DataTableHeader,
  DataTableRow,
  useSimpleReducer,
} from '@walmart/gtp-shared-components';

const headers = ['Item number', 'Item name', 'Quantity (lb)', 'Delivery date'];
const rowData = [
  {
    itemNumber: 51259338,
    itemName: 'Organic Bananas, Bunch',
    quantity: '24,500',
    dDate: 'Oct 5, 2022',
  },
  {
    itemNumber: 51259339,
    itemName: 'Organic Tomato, Bunch',
    quantity: '2,300',
    dDate: 'Oct 5, 2022',
  },
  {
    itemNumber: 51259349,
    itemName: 'Organic Apple, Bunch',
    quantity: '2,000',
    dDate: 'Oct 5, 2022',
  },
  {
    itemNumber: 44391605,
    itemName: 'Fresh Strawberries, 1 lb',
    quantity: '13,758',
    dDate: 'Oct 10, 2022',
  },
];

<DataTable horizontalScroll={true}>
  <DataTableHead>
    <DataTableRow>
      {headers.map((header, index) => (
        <DataTableHeader alignment={index === 2 ? 'right' : 'left'}>
          {header}
        </DataTableHeader>
      ))}
    </DataTableRow>
  </DataTableHead>
  <DataTableBody hor>
    {rowData.map((item) => {
      const {itemNumber, itemName, quantity, dDate} = item;
      return (
        <DataTableRow>
          <DataTableCell>{itemNumber}</DataTableCell>
          <DataTableCell>{itemName}</DataTableCell>
          <DataTableCell variant="numeric">{quantity}</DataTableCell>
          <DataTableCell>{dDate}</DataTableCell>
        </DataTableRow>
      );
    })}
  </DataTableBody>
</DataTable>;

```