import * as React from 'react';
import {GestureResponderEvent, Text} from 'react-native';

import {fireEvent, render} from '@testing-library/react-native';

import {Link} from '../Link';

jest.useFakeTimers({legacyFakeTimers: true});
let mockFn: jest.Mock | ((event: GestureResponderEvent) => void);
beforeAll(() => {
  mockFn = jest.fn();
});
describe('Test Link', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('Should trigger onPress correctly.', async () => {
    const rootQueries = render(
      <Link children="This is a Link" color="default" onPress={mockFn} />,
    );
    expect(mockFn).toHaveBeenCalledTimes(0);
    const button = await rootQueries.findByText('This is a Link');
    fireEvent.press(button);
    expect(mockFn).toHaveBeenCalledTimes(1);
  });

  test('Should not trigger onPress when disabled.', async () => {
    const rootQueries = render(
      <Link
        children="This is a disabled Link"
        color="default"
        onPress={mockFn}
        disabled
      />,
    );
    const button = await rootQueries.findByText('This is a disabled Link');
    fireEvent.press(button);
    expect(mockFn).toHaveBeenCalledTimes(0);
  });

  test('Should trigger onPress when embedded.', async () => {
    const rootQueries = render(
      <Text>
        {'This '}
        <Link testID="link" children="link" color="default" onPress={mockFn} />
        {' is embedded'}
      </Text>,
    );
    const button = await rootQueries.findByTestId('link');
    fireEvent.press(button);
    expect(mockFn).toHaveBeenCalledTimes(1);
  });
});
