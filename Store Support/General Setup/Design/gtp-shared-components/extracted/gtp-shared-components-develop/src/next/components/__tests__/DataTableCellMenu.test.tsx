import * as React from 'react';
import {GestureResponderEvent} from 'react-native';

import {fireEvent, render, screen} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import {DataTableCellActionsMenu} from '../DataTableCellActionsMenu';
import {DataTableCellActionsMenuItem} from '../DataTableCellActionsMenuItem';
import {IconButton} from '../IconButton';

jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');

jest.useFakeTimers({legacyFakeTimers: true});

let mockFn: jest.Mock | ((event: GestureResponderEvent) => void);
beforeAll(() => {
  mockFn = jest.fn();
});
beforeEach(() => {
  jest.clearAllMocks();
});
const DataTableMenuApp = () => {
  const [isOpen, setIsOpen] = React.useState<boolean>(false);
  return (
    <DataTableCellActionsMenu
      isOpen={isOpen}
      onClose={() => setIsOpen(false)}
      trigger={
        <IconButton
          onPress={() => setIsOpen(!isOpen)}
          children={<Icons.MoreIcon />}
        />
      }>
      <DataTableCellActionsMenuItem
        leading={<Icons.EmailIcon />}
        onPress={mockFn}>
        {'email'}
      </DataTableCellActionsMenuItem>
    </DataTableCellActionsMenu>
  );
};

beforeEach(() => {
  jest.clearAllMocks();
});

describe.each<boolean>([true, false])('each', () => {
  test(`DataTableCellActionsMenu render `, async () => {
    render(<DataTableMenuApp />);
    const trigger = await screen.findByTestId('MoreIcon');

    // DataTableCellActionsMenu display only after trigger is pressed
    const modalNotVisible = screen.queryByTestId('DataTableCellActionsMenu');
    expect(modalNotVisible).not.toBeTruthy();

    fireEvent.press(trigger);
    const modalVisible = await screen.findByTestId('DataTableCellActionsMenu');
    expect(modalVisible).toBeTruthy();

    const menuItem = await screen.findByTestId('DataTableCellActionsMenuItem');
    fireEvent.press(menuItem);
    expect(mockFn).toHaveBeenCalledTimes(1);
  });
});
