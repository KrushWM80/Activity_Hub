import React from 'react';

import {
  componentButtonContainerSizeLargeFontSize,
  componentButtonContainerSizeMediumFontSize,
  componentButtonContainerSizeSmallFontSize,
} from '@livingdesign/tokens/dist/react-native/light/regular/components/Button';
import {fireEvent, render} from '@testing-library/react-native';

import TertiaryButton from './TertiaryButton';

jest.useFakeTimers({legacyFakeTimers: true});

describe('TertiaryButton', () => {
  test('Should render Tertiary button', async () => {
    const mockFn = jest.fn();

    const {findByRole} = render(
      <TertiaryButton onPress={mockFn}>Test</TertiaryButton>,
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
      <TertiaryButton disabled onPress={jest.fn()}>
        Test
      </TertiaryButton>,
    );

    expect(queryByRole('button')).toBeDisabled();

    update(<TertiaryButton onPress={jest.fn()}>Test</TertiaryButton>);

    expect(queryByRole('button')).toBeEnabled();
  });

  test('Should render children correctly.', async () => {
    const {findByRole} = render(
      <TertiaryButton onPress={jest.fn()}>Test button</TertiaryButton>,
    );

    expect(await findByRole('button')).toHaveTextContent('Test button');
  });

  test('Should render selected correctly.', async () => {
    const {findByRole} = render(
      <TertiaryButton onPress={jest.fn()} selected>
        Test
      </TertiaryButton>,
    );

    expect(await findByRole('button')).toHaveProp('accessibilityState', {
      selected: true,
    });
  });

  test('Should render small size tertiary button correctly.', async () => {
    const {findByText} = render(
      <TertiaryButton onPress={jest.fn()} size="small">
        Small Tertiary Button
      </TertiaryButton>,
    );
    expect(await findByText('Small Tertiary Button')).toHaveStyle({
      fontSize: componentButtonContainerSizeSmallFontSize,
    });
  });

  test('Should render medium size tertiary button correctly.', async () => {
    const {findByText} = render(
      <TertiaryButton onPress={jest.fn()} size="medium">
        Medium Tertiary Button
      </TertiaryButton>,
    );
    expect(await findByText('Medium Tertiary Button')).toHaveStyle({
      fontSize: componentButtonContainerSizeMediumFontSize,
    });
  });

  test('Should render large size tertiary button correctly.', async () => {
    const {findByText} = render(
      <TertiaryButton onPress={jest.fn()} size="large">
        Large Tertiary Button
      </TertiaryButton>,
    );
    expect(await findByText('Large Tertiary Button')).toHaveStyle({
      fontSize: componentButtonContainerSizeLargeFontSize,
    });
  });
});

test('Should render style fullWidth correctly.', async () => {
  const {getByText} = render(
    <TertiaryButton onPress={jest.fn()} isFullWidth>
      Test FullWidth
    </TertiaryButton>,
  );
  expect(await getByText('Test FullWidth')).toHaveStyle({
    flexGrow: 1,
  });
});
