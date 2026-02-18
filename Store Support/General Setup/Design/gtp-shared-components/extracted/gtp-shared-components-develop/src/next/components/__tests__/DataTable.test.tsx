import * as React from 'react';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/DataTable';
import {fireEvent, render} from '@testing-library/react-native';

import {DataTable} from '../DataTable';
import {DataTableBody} from '../DataTableBody';
import {DataTableCell} from '../DataTableCell';
import {DataTableCellStatus} from '../DataTableCellStatus';
import {DataTableHead} from '../DataTableHead';
import {DataTableHeader, DataTableHeaderSortType} from '../DataTableHeader';
import {DataTableRow} from '../DataTableRow';
import {Tag} from '../Tag';

let mockSortFn: jest.Mock | ((value: DataTableHeaderSortType) => void);
beforeAll(() => {
  mockSortFn = jest.fn();
});
const renderTable = () => {
  return render(
    <DataTable>
      <DataTableHead>
        <DataTableRow>
          <DataTableHeader
            alignment={'right'}
            sort={'ascending'}
            onSort={mockSortFn}>
            {'Heading_1'}
          </DataTableHeader>
          <DataTableHeader>{'Heading_2'}</DataTableHeader>
        </DataTableRow>
      </DataTableHead>
      <DataTableBody>
        <DataTableRow>
          <DataTableCell>{'Cell_1'}</DataTableCell>
          <DataTableCell variant="numeric">{'Cell_2'}</DataTableCell>
        </DataTableRow>
      </DataTableBody>
    </DataTable>,
  );
};

test('Test DataTableHead section', async () => {
  const dataTable = renderTable();
  const tableHead = await dataTable.findByTestId('DataTableHead');
  const arrowUp = await dataTable.findByTestId('ArrowUpIcon');
  //TableHead Contains only one TableRow
  expect(tableHead.children.length).toEqual(1);
  const tableHeaderRow = dataTable.queryAllByTestId('DataTableRow');
  expect(tableHeaderRow[0].children.length).toEqual(2);
  expect(arrowUp).toBeDefined();
  const _dataTableHeader = dataTable.queryAllByTestId('DataTableHeader');
  fireEvent.press(_dataTableHeader[0]);
  expect(mockSortFn).toHaveBeenCalledTimes(1);
  const arrowDown = dataTable.queryByTestId('ArrowDownIcon');
  expect(arrowDown).toBeNull();
  const _heading1 = await dataTable.findByText('Heading_1');
  expect(_heading1.props.style[1][0].textAlign).toEqual('right');
  const _heading2 = await dataTable.findByText('Heading_2');
  expect(_heading2.props.style[1][0].textAlign).toEqual('left');
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
  expect(_dataTableCell[1]).toHaveStyle({
    flexDirection: 'row',
    padding: token.componentDataTableCellPadding,
    width: '50%',
  });
  const _cell1 = await dataTable.findByText('Cell_1');
  expect(_cell1.props.style[1].textAlign).toEqual('left');
  const _cell2 = await dataTable.findByText('Cell_2');
  expect(_cell2.props.style[1].textAlign).toEqual('right');
});
const renderStatusTable = () => {
  return render(
    <DataTable>
      <DataTableHead>
        <DataTableRow>
          <DataTableHeader
            alignment={'right'}
            sort={'ascending'}
            onSort={mockSortFn}>
            {'Heading_1'}
          </DataTableHeader>
          <DataTableHeader>{'Status'}</DataTableHeader>
        </DataTableRow>
      </DataTableHead>
      <DataTableBody>
        <DataTableRow>
          <DataTableCell>{'Cell_1'}</DataTableCell>
          <DataTableCellStatus>
            <Tag color={'green'} variant={'tertiary'}>
              {'Inprogress'}
            </Tag>
          </DataTableCellStatus>
        </DataTableRow>
      </DataTableBody>
    </DataTable>,
  );
};
test('Test DataTableCellStatus section', async () => {
  const dataTable = renderStatusTable();
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
  const _dataTableCellStatus = await dataTable.findByTestId(
    'DataTableCellStatus',
  );
  expect(_dataTableCellStatus).toHaveStyle({
    alignItems: 'flex-start',
    padding: token.componentDataTableCellPadding,
    width: '50%',
  });
});
