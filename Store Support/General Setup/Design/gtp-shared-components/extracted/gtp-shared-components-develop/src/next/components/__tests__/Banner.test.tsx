import * as React from 'react';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Banner';
import {fireEvent, render, screen} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import {Banner, BannerVariant} from '../Banner';

const closeClick = jest.fn();
describe.each<BannerVariant>(['error', 'info', 'success', 'warning'])(
  'Test %s Banner',
  (variant) => {
    test('Should match snapshot correctly.', async () => {
      render(
        <Banner
          variant={variant}
          onClose={closeClick}>{`This is an ${variant} message`}</Banner>,
      ).toJSON();
      expect(screen.toJSON()).toMatchSnapshot();
      const bannerCompo = await screen.findByTestId('Banner');
      const bgColor = () => {
        if (variant === 'info') {
          return token.componentBannerContainerVariantInfoBackgroundColor;
        } else if (variant === 'success') {
          return token.componentBannerContainerVariantSuccessBackgroundColor;
        } else if (variant === 'warning') {
          return token.componentBannerContainerVariantWarningBackgroundColor;
        } else if (variant === 'error') {
          return token.componentBannerContainerVariantErrorBackgroundColor;
        }
        return token.componentBannerContainerVariantInfoBackgroundColor;
      };
      expect(bannerCompo).toHaveStyle({
        backgroundColor: bgColor(),
      });
    });

    test('Should render with leading icon.', async () => {
      const rootQueries = render(
        <Banner
          variant={variant}
          leading={<Icons.CheckIcon />}
          onClose={closeClick}>
          Test
        </Banner>,
      );
      const banner = await rootQueries.findByTestId('Banner');
      const leadingIcon = await rootQueries.findByTestId('CheckIcon');
      expect(banner).toContainElement(leadingIcon);
    });
  },
);
describe('Test Banner with close color', () => {
  test('Should render close with different Color.', async () => {
    const rootQueries = render(
      <Banner
        onClose={closeClick}
        variant={'info'}
        leading={<Icons.CheckIcon />}
        closeIconColor={'white'}>
        Test
      </Banner>,
    );
    const closeButton = await rootQueries.findByTestId('close-button');
    fireEvent.press(closeButton);
    expect(closeClick).toHaveBeenCalledTimes(1);
    const closeIcon = await rootQueries.findByTestId('CloseIcon');
    expect(closeIcon).toHaveStyle({
      tintColor: 'white',
    });
  });
});
