import React from 'react';

import {fireEvent, render} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import BaseButton, {BaseButtonTheme} from './button';

jest.useFakeTimers({legacyFakeTimers: true});

const mockTheme = {
  part() {
    return {};
  },
} as unknown as BaseButtonTheme;

describe('BaseButton', () => {
  test('Should trigger onPress correctly.', async () => {
    const mockFn = jest.fn();

    const {findByRole} = render(
      <BaseButton onPress={mockFn} theme={mockTheme}>
        Test
      </BaseButton>,
    );

    expect(mockFn).toHaveBeenCalledTimes(0);

    const button = await findByRole('button');

    fireEvent.press(button);

    expect(mockFn).toHaveBeenCalledTimes(1);
  });

  test('Should render disabled correctly.', () => {
    /**
     * @note Use `queryByRole` to get around an async `act()` error.
     * https://github.com/callstack/react-native-testing-library/issues/379#issuecomment-720734366
     */
    const {queryByRole, update} = render(
      <BaseButton disabled onPress={jest.fn()} theme={mockTheme}>
        Test
      </BaseButton>,
    );

    expect(queryByRole('button')).toBeDisabled();

    update(
      <BaseButton onPress={jest.fn()} theme={mockTheme}>
        Test
      </BaseButton>,
    );

    expect(queryByRole('button')).toBeEnabled();
  });

  test('Should render children correctly.', async () => {
    const {findByRole} = render(
      <BaseButton onPress={jest.fn()} theme={mockTheme}>
        Test button
      </BaseButton>,
    );

    expect(await findByRole('button')).toHaveTextContent('Test button');
  });

  test('Should render icon correctly.', async () => {
    const {findByRole, queryByTestId} = render(
      <BaseButton
        icon={<Icons.CheckIcon />}
        onPress={jest.fn()}
        theme={mockTheme}>
        Test
      </BaseButton>,
    );

    const iconElement = queryByTestId('CheckIcon');

    expect(await findByRole('button')).toContainElement(iconElement);
  });

  test('Should render selected correctly.', async () => {
    const {findByRole} = render(
      <BaseButton onPress={jest.fn()} selected theme={mockTheme}>
        Test
      </BaseButton>,
    );

    expect(await findByRole('button')).toHaveProp('accessibilityState', {
      selected: true,
    });
  });
});
