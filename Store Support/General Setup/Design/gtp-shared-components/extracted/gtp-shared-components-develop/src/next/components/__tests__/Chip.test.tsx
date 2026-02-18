import * as React from 'react';

import {fireEvent, render, screen} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';
import renderer from 'react-test-renderer';

import {Chip, ChipId} from '../Chip';

const mockFn = jest.fn((chipId: ChipId) => {
  return chipId;
});

describe('Test Chip', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('Should match snapshot correctly.', async () => {
    const chip = renderer
      .create(
        <Chip size="small" children="Sam's Choice" id={0} onPress={mockFn} />,
      )
      .toJSON();
    expect(chip).toMatchSnapshot();
  });

  test('Should trigger onPress correctly.', async () => {
    render(
      <Chip id={0} onPress={mockFn} size="small" children="Sam'sChoice" />,
    );
    expect(mockFn).toHaveBeenCalledTimes(0);
    const button = await screen.findByText("Sam'sChoice");
    fireEvent.press(button);
    expect(mockFn).toHaveBeenCalledTimes(1);
    expect(mockFn).toHaveLastReturnedWith(0);
  });

  test('Should trigger onPress with string as ID', async () => {
    render(
      <Chip id="myId" onPress={mockFn} size="small" children="Sam'sChoice" />,
    );
    expect(mockFn).toHaveBeenCalledTimes(0);
    const button = await screen.findByText("Sam'sChoice");
    fireEvent.press(button);
    expect(mockFn).toHaveBeenCalledTimes(1);
    expect(mockFn).toHaveLastReturnedWith('myId');
  });

  test('Should not trigger onPress when disabled.', async () => {
    render(
      <Chip
        id={0}
        onPress={mockFn}
        size="small"
        children="Sam's Choice"
        disabled
      />,
    );
    expect(mockFn).toHaveBeenCalledTimes(0);
    const button = await screen.findByText("Sam's Choice");
    fireEvent.press(button);
    expect(mockFn).toHaveBeenCalledTimes(0);

    fireEvent.press(button);
    expect(mockFn).toHaveBeenCalledTimes(0);
  });

  test('Should render leading icon correctly.', async () => {
    render(
      <Chip
        testID="samschoice"
        id={0}
        leading={<Icons.CheckIcon />}
        onPress={mockFn}
        size="small"
        children="Sam's Choice"
      />,
    );
    const button = await screen.findByTestId('samschoice');
    const iconElement = screen.queryByTestId('CheckIcon');
    expect(button).toContainElement(iconElement);
  });

  test('Should render trailing icon correctly.', async () => {
    render(
      <Chip
        testID="samschoice"
        id={0}
        trailing={<Icons.CheckIcon />}
        onPress={mockFn}
        size="small"
        children="Sam's Choice"
      />,
    );
    const button = await screen.findByTestId('samschoice');
    const iconElement = screen.queryByTestId('CheckIcon');
    expect(button).toContainElement(iconElement);
  });
  test('Should not trigger onPress when disableOnPress is True.', async () => {
    render(
      <Chip
        id={0}
        onPress={mockFn}
        size="small"
        children="Sam's Choice"
        disableOnPress
      />,
    );
    expect(mockFn).toHaveBeenCalledTimes(0);
    const button = await screen.findByText("Sam's Choice");
    fireEvent.press(button);
    expect(mockFn).toHaveBeenCalledTimes(0);
  });
});
