import * as React from 'react';
import {GestureResponderEvent} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/DataTable';
import {fireEvent, render} from '@testing-library/react-native';

import {colors} from '../../utils';
import {Button} from '../Button';
import {ButtonGroup} from '../ButtonGroup';
import {DataTableBulkActions} from '../DataTableBulkActions';
let mockFn: jest.Mock | ((value: GestureResponderEvent) => void);
let count = 0;
beforeAll(() => {
  mockFn = jest.fn();
});
const onSelectAll = () => {
  count = 3;
};
const onClearAll = () => {
  count = 0;
};
const renderTable = () => {
  return render(
    <DataTableBulkActions
      actionContent={
        <ButtonGroup>
          <Button onPress={mockFn}>Custom Action 1</Button>
          <Button onPress={mockFn}>Custom Action 2</Button>
        </ButtonGroup>
      }
      count={count}
      onClearSelected={onClearAll}
      onSelectAll={onSelectAll}
    />,
  );
};

test('Test DataTableBulkActions section', async () => {
  const dataTable = renderTable();
  const bulkActions = await dataTable.findByTestId('DataTableBulkActions');

  expect(bulkActions.props.style[0]).toEqual({
    marginVertical: token.componentDataTableBulkActionsContainerGap,
    padding: token.componentDataTableBulkActionsContainerPadding,
    backgroundColor:
      token.componentDataTableBulkActionsContainerBackgroundColor,
    borderColor: token.componentDataTableBulkActionsContainerBorderColor,
    borderWidth: token.componentDataTableBulkActionsContainerBorderWidth,
    borderRadius: token.componentDataTableBulkActionsContainerBorderRadius,
    alignItems: token.componentDataTableBulkActionsContentAlignVertical,
    justifyContent:
      token.componentDataTableBulkActionsContainerAlignHorizontalBS,
    shadowColor: colors.black,
    shadowOpacity: 0.1,
    shadowRadius: 5,
    shadowOffset: {width: 0, height: 3},
  });
  const selectAll = await dataTable.findByTestId('selectAll');
  fireEvent.press(selectAll);
  expect(count).toEqual(3);
  const clearAll = await dataTable.findByTestId('clearSelected');
  fireEvent.press(clearAll);
  expect(count).toEqual(0);
  const _action1 = await dataTable.findByText('Custom Action 1');
  fireEvent.press(_action1);
  expect(mockFn).toHaveBeenCalledTimes(1);
  const _action2 = await dataTable.findByText('Custom Action 2');
  fireEvent.press(_action2);
  expect(mockFn).toHaveBeenCalledTimes(2);
});
