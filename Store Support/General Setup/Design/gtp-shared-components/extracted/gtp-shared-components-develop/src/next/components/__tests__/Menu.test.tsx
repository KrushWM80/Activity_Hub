import * as React from 'react';
import {GestureResponderEvent} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Menu';
import {fireEvent, render, screen} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import {IconButton} from '../IconButton';
import {Menu, MenuPosition} from '../Menu';
import {MenuItem} from '../MenuItem';

jest.useFakeTimers({legacyFakeTimers: true});
jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');
let mockFn: jest.Mock | ((event: GestureResponderEvent) => void);
beforeAll(() => {
  mockFn = jest.fn();
});
beforeEach(() => {
  jest.clearAllMocks();
});
const MenuApp = ({position}: {position: MenuPosition}) => {
  const [isOpen, setIsOpen] = React.useState<boolean>(false);
  return (
    <Menu
      isOpen={isOpen}
      onClose={() => setIsOpen(false)}
      position={position}
      trigger={
        <IconButton
          onPress={() => setIsOpen(!isOpen)}
          children={<Icons.MoreIcon />}
        />
      }>
      <MenuItem leading={<Icons.PencilIcon />} onPress={mockFn}>
        {'Edit'}
      </MenuItem>
    </Menu>
  );
};

beforeEach(() => {
  jest.clearAllMocks();
});
describe.each<MenuPosition>([
  'bottomLeft',
  'bottomRight',
  'topLeft',
  'topRight',
])('Test Menu with position ', (position) => {
  describe.each<boolean>([true, false])('each', () => {
    test(`Menu render position: ${position} `, async () => {
      render(<MenuApp position={position} />);
      const trigger = await screen.findByTestId('MoreIcon');

      // Menu display only after trigger is pressed
      const modalNotVisible = screen.queryByTestId('Menu');
      expect(modalNotVisible).not.toBeTruthy();

      fireEvent.press(trigger);
      const modalVisible = screen.queryByTestId('Menu');
      expect(modalVisible).toBeTruthy();

      const menuItem = await screen.findByTestId('MenuItem');
      expect(menuItem).toHaveStyle({
        flexDirection: 'row',
        alignItems: token.componentMenuItemContainerAlignVertical, //"center"
        paddingHorizontal: token.componentMenuItemContainerPaddingHorizontal, //16
        paddingVertical: token.componentMenuItemContainerPaddingVertical, //8
      });
      fireEvent.press(menuItem);
      expect(mockFn).toHaveBeenCalledTimes(1);
      const menuItemLabel = await screen.findByText('Edit');
      expect(menuItemLabel).toHaveStyle({
        lineHeight: token.componentMenuItemTextLabelLineHeight, //20
        fontSize: token.componentMenuItemTextLabelFontSize, //14
        textDecorationLine:
          token.componentMenuItemTextLabelTextDecorationDefault, //"underline"
        color: token.componentMenuItemTextLabelTextColorDefault, //"#2e2f32"
        flexWrap: token.componentMenuItemTextLabelTextWrap ? 'wrap' : 'nowrap',
      });
    });
  });
});
