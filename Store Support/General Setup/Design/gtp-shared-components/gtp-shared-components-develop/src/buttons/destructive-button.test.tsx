import React from 'react';

import {
  componentButtonContainerSizeLargeFontSize,
  componentButtonContainerSizeMediumFontSize,
  componentButtonContainerSizeSmallFontSize,
} from '@livingdesign/tokens/dist/react-native/light/regular/components/Button';
import {fireEvent, render} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import DestructiveButton from './destructive-button';
jest.useFakeTimers({legacyFakeTimers: true});

describe('DestructiveButton', () => {
  test('Should render Destructive Button', async () => {
    const mockFn = jest.fn();

    const {findByRole} = render(
      <DestructiveButton onPress={mockFn}>Test</DestructiveButton>,
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
      <DestructiveButton disabled onPress={jest.fn()}>
        Test
      </DestructiveButton>,
    );

    expect(queryByRole('button')).toBeDisabled();

    update(<DestructiveButton onPress={jest.fn()}>Test</DestructiveButton>);

    expect(queryByRole('button')).toBeEnabled();
  });

  test('Should render children correctly.', async () => {
    const {findByRole} = render(
      <DestructiveButton onPress={jest.fn()}>Test button</DestructiveButton>,
    );

    expect(await findByRole('button')).toHaveTextContent('Test button');
  });

  test('Should render icon correctly.', async () => {
    const {findByRole, queryByTestId} = render(
      <DestructiveButton icon={<Icons.CheckIcon />} onPress={jest.fn()}>
        Test button
      </DestructiveButton>,
    );

    const iconElement = queryByTestId('CheckIcon');

    expect(await findByRole('button')).toContainElement(iconElement);
  });

  test('Should render selected correctly.', async () => {
    const {findByRole} = render(
      <DestructiveButton onPress={jest.fn()} selected>
        Test
      </DestructiveButton>,
    );

    expect(await findByRole('button')).toHaveProp('accessibilityState', {
      selected: true,
    });
  });

  test('Should render small size Destructive Button correctly.', async () => {
    const {findByText} = render(
      <DestructiveButton onPress={jest.fn()} size="small">
        Small Destructive Button
      </DestructiveButton>,
    );
    expect(await findByText('Small Destructive Button')).toHaveStyle({
      fontSize: componentButtonContainerSizeSmallFontSize,
    });
  });

  test('Should render medium size Destructive Button correctly.', async () => {
    const {findByText} = render(
      <DestructiveButton onPress={jest.fn()} size="medium">
        Medium Destructive Button
      </DestructiveButton>,
    );
    expect(await findByText('Medium Destructive Button')).toHaveStyle({
      fontSize: componentButtonContainerSizeMediumFontSize,
    });
  });

  test('Should render large size Destructive Button correctly.', async () => {
    const {findByText} = render(
      <DestructiveButton onPress={jest.fn()} size="large">
        Large Destructive Button
      </DestructiveButton>,
    );
    expect(await findByText('Large Destructive Button')).toHaveStyle({
      fontSize: componentButtonContainerSizeLargeFontSize,
    });
  });
});

test('Should render style fullWidth correctly.', async () => {
  const {getByText} = render(
    <DestructiveButton onPress={jest.fn()} isFullWidth>
      Test FullWidth
    </DestructiveButton>,
  );
  expect(await getByText('Test FullWidth')).toHaveStyle({
    flexGrow: 1,
  });
});
