import * as React from 'react';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Alert';
import {render, screen} from '@testing-library/react-native';

import {Alert, AlertVariant} from '../Alert';

const mockFn = jest.fn();
describe.each<AlertVariant>(['error', 'info', 'success', 'warning'])(
  'Test Alert Variant = %s ',
  (variant) => {
    render(
      <Alert
        variant={variant}
        children="This is an alert"
        actionButtonProps={{
          children: 'Action',
          onPress: mockFn,
        }}
      />,
    ).toJSON();
    test('Should match snapshot correctly.', async () => {
      render(
        <Alert
          variant={variant}
          children="This is an alert"
          actionButtonProps={{
            children: 'Action',
            onPress: mockFn,
          }}
        />,
      ).toJSON();
      expect(screen.toJSON()).toMatchSnapshot();
      const alertComponent = await screen.findByTestId('Alert');
      const alertContainerStyle = () => {
        if (variant === 'error') {
          return {
            backgroundColor:
              token.componentAlertContainerVariantErrorBackgroundColor,
            borderBottomColor:
              token.componentAlertContainerVariantErrorBorderColorBottom,
            borderLeftColor:
              token.componentAlertContainerVariantErrorBorderColorStart,
            borderRightColor:
              token.componentAlertContainerVariantErrorBorderColorEnd,
            borderTopColor:
              token.componentAlertContainerVariantErrorBorderColorTop,
          };
        } else if (variant === 'success') {
          return {
            backgroundColor:
              token.componentAlertContainerVariantSuccessBackgroundColor,
            borderBottomColor:
              token.componentAlertContainerVariantSuccessBorderColorBottom,
            borderLeftColor:
              token.componentAlertContainerVariantSuccessBorderColorStart,
            borderRightColor:
              token.componentAlertContainerVariantSuccessBorderColorEnd,
            borderTopColor:
              token.componentAlertContainerVariantSuccessBorderColorTop,
          };
        } else if (variant === 'warning') {
          return {
            backgroundColor:
              token.componentAlertContainerVariantWarningBackgroundColor,
            borderBottomColor:
              token.componentAlertContainerVariantWarningBorderColorBottom,
            borderLeftColor:
              token.componentAlertContainerVariantWarningBorderColorStart,
            borderRightColor:
              token.componentAlertContainerVariantWarningBorderColorEnd,
            borderTopColor:
              token.componentAlertContainerVariantWarningBorderColorTop,
          };
        } else if (variant === 'info') {
          return {
            backgroundColor:
              token.componentAlertContainerVariantInfoBackgroundColor,
            borderBottomColor:
              token.componentAlertContainerVariantInfoBorderColorBottom,
            borderLeftColor:
              token.componentAlertContainerVariantInfoBorderColorStart,
            borderRightColor:
              token.componentAlertContainerVariantInfoBorderColorEnd,
            borderTopColor:
              token.componentAlertContainerVariantInfoBorderColorTop,
          };
        }
      };
      expect(alertComponent).toHaveStyle(alertContainerStyle());
    });

    // Test Render Icon based on variant
    test('Should render with icon.', async () => {
      render(
        <Alert
          variant={variant}
          children="This is an alert"
          actionButtonProps={{
            children: 'Action',
            onPress: mockFn,
          }}
        />,
      ).toJSON();

      const alertComponent = await screen.findByTestId('Alert');
      if (variant === 'error') {
        const errorIcon = await screen.findByTestId('ExclamationCircleIcon');
        expect(alertComponent).toContainElement(errorIcon);
        expect(errorIcon).toHaveStyle({
          tintColor: token.componentAlertIconVariantErrorIconColor,
        });
      } else if (variant === 'success') {
        const successIcon = await screen.findByTestId('CheckCircleIcon');
        expect(alertComponent).toContainElement(successIcon);
        expect(successIcon).toHaveStyle({
          tintColor: token.componentAlertIconVariantSuccessIconColor,
        });
      } else if (variant === 'warning') {
        const warningIcon = await screen.findByTestId('WarningIcon');
        expect(alertComponent).toContainElement(warningIcon);
        expect(warningIcon).toHaveStyle({
          tintColor: token.componentAlertIconVariantWarningIconColor,
        });
      } else if (variant === 'info') {
        const infoIcon = await screen.findByTestId('InfoCircleIcon');
        expect(alertComponent).toContainElement(infoIcon);
        expect(infoIcon).toHaveStyle({
          tintColor: token.componentAlertIconVariantInfoIconColor,
        });
      }
    });
  },
);
