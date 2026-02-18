import React from 'react';

import {fireEvent, render} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import BannerButton from './banner-button';

jest.useFakeTimers({legacyFakeTimers: true});

describe('BannerButton', () => {
  test('Should trigger onPress correctly.', async () => {
    const mockFn = jest.fn();

    const {findByRole} = render(
      <BannerButton
        description="Description description description"
        onPress={mockFn}
        title="Title title title"
      />,
    );

    expect(mockFn).toHaveBeenCalledTimes(0);

    const button = await findByRole('button');

    fireEvent.press(button);

    expect(mockFn).toHaveBeenCalledTimes(1);
  });

  test('Should render description correctly.', async () => {
    const {findByRole} = render(
      <BannerButton
        description="Description description description"
        onPress={jest.fn()}
        title="Title title title"
      />,
    );

    expect(await findByRole('button')).toHaveTextContent(
      'Title title title\nDescription description description',
    );
  });

  test('Should render icon correctly.', async () => {
    const {findByRole, queryByTestId} = render(
      <BannerButton
        description="Description description description"
        icon={<Icons.CheckIcon />}
        onPress={jest.fn()}
        title="Title title title"
      />,
    );

    const iconElement = queryByTestId('CheckIcon');

    expect(await findByRole('button')).toContainElement(iconElement);
  });

  test('Should render selected correctly.', async () => {
    const {findByRole} = render(
      <BannerButton
        description="Description description description"
        onPress={jest.fn()}
        selected
        title="Title title title"
      />,
    );

    expect(await findByRole('button')).toHaveProp('accessibilityState', {
      selected: true,
    });
  });

  test('Should render title correctly.', async () => {
    const {findByRole} = render(
      <BannerButton
        description="Description description description"
        onPress={jest.fn()}
        title="Title title title"
      />,
    );

    expect(await findByRole('button')).toHaveTextContent(
      'Title title title\nDescription description description',
    );
  });
});
