import * as React from 'react';
import {GestureResponderEvent} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/DataTable';
import {fireEvent, render} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons/dist';

import {DataTable} from '../DataTable';
import {DataTableBody} from '../DataTableBody';
import {DataTableCell} from '../DataTableCell';
import {DataTableCellActions} from '../DataTableCellActions';
import {DataTableHead} from '../DataTableHead';
import {DataTableHeader} from '../DataTableHeader';
import {DataTableRow} from '../DataTableRow';
import {IconButton} from '../IconButton';
let mockFn: jest.Mock | ((value: GestureResponderEvent) => void);
beforeAll(() => {
  mockFn = jest.fn();
});
const renderTable = () => {
  return render(
    <DataTable>
      <DataTableHead>
        <DataTableRow>
          <DataTableHeader>{'Heading_1'}</DataTableHeader>
          <DataTableHeader alignment={'right'}>{'Actions'}</DataTableHeader>
        </DataTableRow>
      </DataTableHead>
      <DataTableBody>
        <DataTableRow>
          <DataTableCell>{'Cell_1'}</DataTableCell>
          <DataTableCellActions alignment="right" width={'30%'}>
            <IconButton
              children={<Icons.PencilIcon />}
              size="small"
              onPress={mockFn}
            />
            <IconButton
              children={<Icons.TrashCanIcon />}
              size="small"
              onPress={mockFn}
            />
          </DataTableCellActions>
        </DataTableRow>
      </DataTableBody>
    </DataTable>,
  );
};

test('Test DataTableHead section', async () => {
  const dataTable = renderTable();
  const tableHead = await dataTable.findByTestId('DataTableHead');
  //TableHead Contains only one TableRow
  expect(tableHead.children.length).toEqual(1);
  const tableHeaderRow = dataTable.queryAllByTestId('DataTableRow');
  expect(tableHeaderRow[0].children.length).toEqual(2);
  const arrowDown = dataTable.queryByTestId('ArrowDownIcon');
  expect(arrowDown).toBeNull();
  const _heading1 = await dataTable.findByText('Heading_1');
  expect(_heading1.props.style[1][0].textAlign).toEqual('left');
  const _heading2 = await dataTable.findByText('Actions');
  expect(_heading2.props.style[1][0].textAlign).toEqual('right');
});
test('Test DataTableBody section', async () => {
  const dataTable = renderTable();
  const tableHead = await dataTable.findByTestId('DataTableBody');

  //DataTableBody Contains only one TableRow
  expect(tableHead.children.length).toEqual(1);
  const tableHeaderRow = dataTable.queryAllByTestId('DataTableRow');
  expect(tableHeaderRow[0].children.length).toEqual(2);
  const _dataTableCell = dataTable.queryAllByTestId('DataTableCell');
  expect(_dataTableCell[0]).toHaveStyle({
    flexDirection: 'row',
    padding: token.componentDataTableCellPadding,
    width: '50%',
  });

  const _cell1 = await dataTable.findByText('Cell_1');
  expect(_cell1.props.style[1].textAlign).toEqual('left');
  const actionsCell = await dataTable.findByTestId('DataTableCellActions');
  expect(actionsCell).toBeDefined();
  const PencilIcon = await dataTable.findByTestId('PencilIcon');
  fireEvent.press(PencilIcon);
  expect(mockFn).toHaveBeenCalledTimes(1);
  const TrashCanIcon = await dataTable.findByTestId('TrashCanIcon');
  fireEvent.press(TrashCanIcon);
  expect(mockFn).toHaveBeenCalledTimes(2);
});
