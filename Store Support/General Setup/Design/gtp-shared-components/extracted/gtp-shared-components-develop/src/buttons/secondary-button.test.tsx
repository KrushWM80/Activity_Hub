import React from 'react';

import {
  componentButtonContainerSizeLargeFontSize,
  componentButtonContainerSizeMediumFontSize,
  componentButtonContainerSizeSmallFontSize,
} from '@livingdesign/tokens/dist/react-native/light/regular/components/Button';
import {fireEvent, render} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import SecondaryButton from './secondary-button';

jest.useFakeTimers({legacyFakeTimers: true});

describe('SecondaryButton', () => {
  test('Should render Secondary button', async () => {
    const mockFn = jest.fn();

    const {findByRole} = render(
      <SecondaryButton onPress={mockFn}>Test</SecondaryButton>,
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
      <SecondaryButton disabled onPress={jest.fn()}>
        Test
      </SecondaryButton>,
    );

    expect(queryByRole('button')).toBeDisabled();

    update(<SecondaryButton onPress={jest.fn()}>Test</SecondaryButton>);

    expect(queryByRole('button')).toBeEnabled();
  });

  test('Should render children correctly.', async () => {
    const {findByRole} = render(
      <SecondaryButton onPress={jest.fn()}>Test button</SecondaryButton>,
    );

    expect(await findByRole('button')).toHaveTextContent('Test button');
  });

  test('Should render icon correctly.', async () => {
    const {findByRole, queryByTestId} = render(
      <SecondaryButton icon={<Icons.CheckIcon />} onPress={jest.fn()}>
        Test button
      </SecondaryButton>,
    );

    const iconElement = queryByTestId('CheckIcon');

    expect(await findByRole('button')).toContainElement(iconElement);
  });

  test('Should render selected correctly.', async () => {
    const {findByRole} = render(
      <SecondaryButton onPress={jest.fn()} selected>
        Test
      </SecondaryButton>,
    );

    expect(await findByRole('button')).toHaveProp('accessibilityState', {
      selected: true,
    });
  });

  test('Should render small size secondary button correctly.', async () => {
    const {findByText} = render(
      <SecondaryButton onPress={jest.fn()} size="small">
        Small Secondary Button
      </SecondaryButton>,
    );
    expect(await findByText('Small Secondary Button')).toHaveStyle({
      fontSize: componentButtonContainerSizeSmallFontSize,
    });
  });

  test('Should render medium size secondary button correctly.', async () => {
    const {findByText} = render(
      <SecondaryButton onPress={jest.fn()} size="medium">
        Medium Secondary Button
      </SecondaryButton>,
    );
    expect(await findByText('Medium Secondary Button')).toHaveStyle({
      fontSize: componentButtonContainerSizeMediumFontSize,
    });
  });

  test('Should render large size secondary button correctly.', async () => {
    const {findByText} = render(
      <SecondaryButton onPress={jest.fn()} size="large">
        Large Secondary Button
      </SecondaryButton>,
    );
    expect(await findByText('Large Secondary Button')).toHaveStyle({
      fontSize: componentButtonContainerSizeLargeFontSize,
    });
  });
});

test('Should render style fullWidth correctly.', async () => {
  const {getByText} = render(
    <SecondaryButton onPress={jest.fn()} isFullWidth>
      Test FullWidth
    </SecondaryButton>,
  );
  expect(await getByText('Test FullWidth')).toHaveStyle({
    flexGrow: 1,
  });
});
