import * as React from 'react';

import {
  act,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react-native';

import {colors} from '../../../next/utils';
import {FilterTag} from '../FilterTag';

describe('FilterTag', () => {
  jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');
  jest.useFakeTimers({legacyFakeTimers: true});

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should render default successfully', () => {
    render(<FilterTag>Test Filter</FilterTag>);
    const filter = screen.getByTestId('FilterTag');
    expect(filter).toHaveTextContent('Test Filter');
    expect(filter).toBeOnTheScreen();
    expect(filter).toBeVisible();
    expect(filter).toHaveStyle({
      borderWidth: 0,
      borderRadius: 4,
      backgroundColor: colors.blue['5'], // '#F2F8FD',
    });
  });

  test('should render pressed style when pressed', () => {
    render(<FilterTag testOnly_pressed>Test Filter</FilterTag>);
    const filter = screen.getByTestId('FilterTag');
    expect(filter).toHaveStyle({
      borderWidth: 0,
      borderRadius: 4,
      backgroundColor: colors.blue['20'], // '#CCE3F8',
    });
  });

  test('should render disabled style when disabled', () => {
    render(<FilterTag disabled>Test Filter</FilterTag>);
    const filter = screen.getByTestId('FilterTag');
    expect(filter).toBeDisabled();
    expect(filter).toHaveStyle({
      borderWidth: 1,
      borderColor: colors.gray['50'], // '#BABBBE',
      backgroundColor: colors.white, // '#FFFFFF',
    });
  });

  test('should have correct accessibility', () => {
    render(<FilterTag>Test Filter</FilterTag>);
    const filter = screen.getByTestId('FilterTag');
    expect(filter).toHaveProp('accessibilityRole', 'togglebutton');
    expect(filter).toHaveProp('accessibilityState', {disabled: false});
    expect(filter).toHaveAccessibleName('Remove filter: Test Filter');
  });

  test('should call onPress when clicked', async () => {
    const mockFn = jest.fn();
    render(<FilterTag onPress={mockFn}>Test Filter</FilterTag>);
    const filter = screen.getByTestId('FilterTag');
    fireEvent.press(filter);
    act(() => {
      jest.runAllTimers();
    });
    await waitFor(() => {
      expect(mockFn).toHaveBeenCalled();
    });
  });

  test('should not call onPress when disabled', async () => {
    const mockFn = jest.fn();
    render(
      <FilterTag onPress={mockFn} disabled>
        Test Filter
      </FilterTag>,
    );
    const filter = screen.getByTestId('FilterTag');
    fireEvent.press(filter);
    act(() => {
      jest.runAllTimers();
    });
    await waitFor(() => {
      expect(mockFn).not.toHaveBeenCalled();
    });
  });
});
