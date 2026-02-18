import * as React from 'react';
import {GestureResponderEvent} from 'react-native';

import {fireEvent, render, screen} from '@testing-library/react-native';
import renderer from 'react-test-renderer';

import {Snackbar} from '../Snackbar';

jest.useFakeTimers({legacyFakeTimers: true});
let mockFn: jest.Mock | ((event: GestureResponderEvent) => void);
beforeAll(() => {
  mockFn = jest.fn();
});

describe('Test Snackbar', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('Should match snapshot correctly.', async () => {
    const snackbar = renderer.create(<Snackbar>Test</Snackbar>).toJSON();
    expect(snackbar).toMatchSnapshot();
  });

  test('Should match snapshot of closeButton correctly.', async () => {
    const snackbar = renderer
      .create(<Snackbar closeButton={{onPress: mockFn}}>Test</Snackbar>)
      .toJSON();
    expect(snackbar).toMatchSnapshot();
  });

  test('Should trigger actionButton onPress correctly.', async () => {
    render(
      <Snackbar actionButton={{caption: 'Action Button', onPress: mockFn}}>
        Test
      </Snackbar>,
    );
    expect(mockFn).toHaveBeenCalledTimes(0);
    const button = await screen.findByTestId('Snackbar-actionButton');
    fireEvent.press(button);
    expect(mockFn).toHaveBeenCalledTimes(1);
    fireEvent.press(button);
    expect(mockFn).toHaveBeenCalledTimes(2);
  });

  test('Should trigger closeButton onPress correctly.', async () => {
    render(<Snackbar closeButton={{onPress: mockFn}}>Test</Snackbar>);
    expect(mockFn).toHaveBeenCalledTimes(0);
    const button = await screen.findByTestId('IconButton');
    fireEvent.press(button);
    expect(mockFn).toHaveBeenCalledTimes(1);
    fireEvent.press(button);
    expect(mockFn).toHaveBeenCalledTimes(2);
  });
});
