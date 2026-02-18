import * as React from 'react';

import {act, fireEvent, render, screen} from '@testing-library/react-native';

import {convertDateToString} from '../../utils';
import {DateDropdown} from '../DateDropdown';

jest.useFakeTimers({legacyFakeTimers: true});
jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');
jest.mock('react-native-device-info', () => {
  return {
    __esModule: true,
    default: {
      hasNotch: jest.fn().mockReturnValueOnce(true).mockReturnValueOnce(false),
      ...jest.fn(() => {}),
    },
  };
});
const TestApp = ({
  value,
  disabled = false,
}: {
  value?: Date;
  disabled?: boolean;
}) => {
  const [date, setDate] = React.useState(value);
  return (
    <DateDropdown
      disabled={disabled}
      label={'Date'}
      value={date}
      onSelect={(dt) => {
        if (dt) {
          setDate(dt);
        }
      }}
    />
  );
};

const getValue = (element: any) => {
  if (element) {
    return element?.children[0]?.props.children.props.value;
  }
};

describe('DateDropdown', () => {
  test('with select current date on Done Press', async () => {
    render(<TestApp />);
    const element = screen.queryByTestId('DateDropdown');
    expect(element).toBeDefined();
    const value = getValue(element);
    expect(value).toEqual('');
    // Fire an event that updates state
    await act(() => {
      if (element) {
        fireEvent.press(element);
      }
    });
    const done = screen.queryByTestId('_LegacyDatePicker-done-button');
    await act(async () => {
      if (done) {
        fireEvent.press(done);
      }
    });
    const selectedDate = getValue(element);
    expect(selectedDate).toEqual(convertDateToString(new Date()));
  });
  test('the on press will not trigger when disabled', async () => {
    render(<TestApp disabled={true} />);
    const element = screen.queryByTestId('DateDropdown');
    expect(element).toBeDefined();
    const value = getValue(element);
    expect(value).toEqual('');
    // Fire an event that updates state
    await act(() => {
      if (element) {
        fireEvent.press(element);
      }
    });
    const done = screen.queryByTestId('_LegacyDatePicker-done-button');
    await act(async () => {
      if (done) {
        fireEvent.press(done);
      }
    });
    const selectedDate = getValue(element);
    expect(selectedDate).toEqual('');
  });
  test('render correctly for decrease button press', async () => {
    render(<TestApp value={new Date(2024, 7, 28)} />);

    const element = screen.queryByTestId('DateDropdown');
    expect(element).toBeDefined();
    const value = getValue(element);
    expect(value).toEqual(convertDateToString(new Date(2024, 7, 28)));
    // Fire an event that updates state
    await act(() => {
      if (element) {
        fireEvent.press(element);
      }
    });
    const rightIcon = screen.queryByTestId('_LegacyDatePicker-decrease-button');
    await act(() => {
      if (rightIcon) {
        fireEvent.press(rightIcon);
      }
    });
    const done = screen.queryByTestId('_LegacyDatePicker-done-button');
    await act(async () => {
      if (done) {
        fireEvent.press(done);
      }
    });
    const decreasedDate = getValue(element);
    expect(decreasedDate).toEqual(convertDateToString(new Date(2024, 7, 27)));
  });
  test('render correctly for increase button press', async () => {
    render(<TestApp value={new Date(2024, 7, 28)} />);

    const element = screen.queryByTestId('DateDropdown');
    expect(element).toBeDefined();
    const value = getValue(element);
    expect(value).toEqual(convertDateToString(new Date(2024, 7, 28)));
    // @ts-ignore
    // Fire an event that updates state
    await act(() => {
      // @ts-ignore
      fireEvent.press(element);
    });
    const rightIcon = screen.queryByTestId('_LegacyDatePicker-increase-button');
    await act(() => {
      if (rightIcon) {
        fireEvent.press(rightIcon);
      }
    });
    const done = screen.queryByTestId('_LegacyDatePicker-done-button');
    await act(async () => {
      if (done) {
        fireEvent.press(done);
      }
    });
    const increasedDate = getValue(element);
    expect(increasedDate).toEqual(convertDateToString(new Date(2024, 7, 29)));
  });
});
