import React from 'react';

import {
  componentButtonContainerSizeLargeFontSize,
  componentButtonContainerSizeMediumFontSize,
  componentButtonContainerSizeSmallFontSize,
} from '@livingdesign/tokens/dist/react-native/light/regular/components/Button';
import {fireEvent, render} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import PrimaryButton from './primary-button';

jest.useFakeTimers({legacyFakeTimers: true});

describe('PrimaryButton', () => {
  test('Should render Primary button', async () => {
    const mockFn = jest.fn();

    const {findByRole} = render(
      <PrimaryButton onPress={mockFn}>Test</PrimaryButton>,
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
      <PrimaryButton disabled onPress={jest.fn()}>
        Test
      </PrimaryButton>,
    );

    expect(queryByRole('button')).toBeDisabled();

    update(<PrimaryButton onPress={jest.fn()}>Test</PrimaryButton>);

    expect(queryByRole('button')).toBeEnabled();
  });

  test('Should render children correctly.', async () => {
    const {findByRole} = render(
      <PrimaryButton onPress={jest.fn()}>Test button</PrimaryButton>,
    );

    expect(await findByRole('button')).toHaveTextContent('Test button');
  });

  test('Should render icon correctly.', async () => {
    const {findByRole, queryByTestId} = render(
      <PrimaryButton icon={<Icons.CheckIcon />} onPress={jest.fn()}>
        Test button
      </PrimaryButton>,
    );

    const iconElement = queryByTestId('CheckIcon');

    expect(await findByRole('button')).toContainElement(iconElement);
  });

  test('Should render selected correctly.', async () => {
    const {findByRole} = render(
      <PrimaryButton onPress={jest.fn()} selected>
        Test
      </PrimaryButton>,
    );

    expect(await findByRole('button')).toHaveProp('accessibilityState', {
      selected: true,
    });
  });

  test('Should render small size primary button correctly.', async () => {
    const {findByText} = render(
      <PrimaryButton onPress={jest.fn()} size="small">
        Small Primary Button
      </PrimaryButton>,
    );
    expect(await findByText('Small Primary Button')).toHaveStyle({
      fontSize: componentButtonContainerSizeSmallFontSize,
    });
  });

  test('Should render medium size primary button correctly.', async () => {
    const {findByText} = render(
      <PrimaryButton onPress={jest.fn()} size="medium">
        Medium Primary Button
      </PrimaryButton>,
    );
    expect(await findByText('Medium Primary Button')).toHaveStyle({
      fontSize: componentButtonContainerSizeMediumFontSize,
    });
  });

  test('Should render large size primary button correctly.', async () => {
    const {findByText} = render(
      <PrimaryButton onPress={jest.fn()} size="large">
        Large Primary Button
      </PrimaryButton>,
    );
    expect(await findByText('Large Primary Button')).toHaveStyle({
      fontSize: componentButtonContainerSizeLargeFontSize,
    });
  });
});

test('Should render style fullWidth correctly.', async () => {
  const {getByText} = render(
    <PrimaryButton onPress={jest.fn()} isFullWidth>
      Test FullWidth
    </PrimaryButton>,
  );
  expect(await getByText('Test FullWidth')).toHaveStyle({
    flexGrow: 1,
  });
});
