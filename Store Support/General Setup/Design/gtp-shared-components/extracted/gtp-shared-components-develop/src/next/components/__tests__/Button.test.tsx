import * as React from 'react';
import {GestureResponderEvent} from 'react-native';

import {
  componentButtonTextLabelSizeLargeFontSize,
  componentButtonTextLabelSizeMediumFontSize,
  componentButtonTextLabelSizeSmallFontSize,
} from '@livingdesign/tokens/dist/react-native/light/regular/components/Button';
import {fireEvent, render, screen, within} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import {Button, ButtonVariant} from '../Button';
jest.useFakeTimers({legacyFakeTimers: true});

let mockFn: jest.Mock | ((event: GestureResponderEvent) => void);
beforeAll(() => {
  mockFn = jest.fn();
});
beforeEach(() => {
  jest.clearAllMocks();
});

describe.each<ButtonVariant>(['primary', 'secondary', 'tertiary'])(
  'Test %s Button',
  (variant) => {
    test('Should trigger onPress correctly.', async () => {
      render(
        <Button variant={variant} size="small" onPress={mockFn}>
          Submit
        </Button>,
      );
      expect(mockFn).toHaveBeenCalledTimes(0);
      const button = await screen.findByText('Submit');
      fireEvent.press(button);
      expect(mockFn).toHaveBeenCalledTimes(1);
    });

    test('Should render disabled correctly.', async () => {
      render(
        <Button variant={variant} disabled onPress={mockFn}>
          Disabled button
        </Button>,
      );
      let button = await screen.findByText('Disabled button');
      expect(button).toBeDisabled();
      screen.update(
        <Button variant={variant} onPress={mockFn}>
          Enabled button
        </Button>,
      );
      button = await screen.findByText('Enabled button');
      expect(button).toBeEnabled();
    });

    test('Should render children correctly.', async () => {
      render(
        <Button variant={variant} onPress={mockFn}>
          Test button
        </Button>,
      );
      const button = await screen.findByTestId('Button');
      expect(button).toHaveTextContent('Test button');
    });

    test('Should render leading icon correctly.', async () => {
      render(
        <Button
          variant={variant}
          leading={<Icons.CheckIcon />}
          onPress={mockFn}>
          Button with leading icon
        </Button>,
      );
      const iconElement = screen.queryByTestId('CheckIcon');
      expect(iconElement).toBeTruthy();
    });

    test('Should render trailing icon correctly.', async () => {
      render(
        <Button
          variant={variant}
          trailing={<Icons.CheckIcon />}
          onPress={mockFn}>
          Button with leading icon
        </Button>,
      );
      const iconElement = screen.queryByTestId('CheckIcon');
      expect(iconElement).toBeTruthy();
    });

    test(`Should render small size ${variant} button correctly.`, async () => {
      render(
        <Button variant={variant} onPress={mockFn} size="small">
          Small Button
        </Button>,
      );
      const text = await screen.findByText('Small Button');
      expect(text).toHaveStyle({
        fontSize: componentButtonTextLabelSizeSmallFontSize,
      });
    });

    test(`Should render medium size ${variant} button correctly.`, async () => {
      render(
        <Button variant={variant} onPress={mockFn} size="medium">
          Medium Button
        </Button>,
      );
      const text = await screen.findByText('Medium Button');
      expect(text).toHaveStyle({
        fontSize: componentButtonTextLabelSizeMediumFontSize,
      });
    });

    test(`Should render large size ${variant} button correctly.`, async () => {
      render(
        <Button variant={variant} onPress={mockFn} size="large">
          Large Button
        </Button>,
      );
      const buttonQueries = within(await screen.findByText('Large Button'));
      const text = await buttonQueries.findByText('Large Button');
      expect(text).toHaveStyle({
        fontSize: componentButtonTextLabelSizeLargeFontSize,
      });
    });

    test('Should render style fullWidth correctly.', async () => {
      render(
        <Button variant={variant} onPress={mockFn} isFullWidth>
          FullWidth Button
        </Button>,
      );
      const buttonQueries = within(await screen.findByText('FullWidth Button'));
      const text = await buttonQueries.findByText('FullWidth Button');
      expect(text).toHaveStyle({
        flexGrow: 0,
      });
    });
  },
);
