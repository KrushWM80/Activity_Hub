import * as React from 'react';
import {GestureResponderEvent} from 'react-native';

import {
  componentIconButtonContainerSizeLargeBorderRadius,
  componentIconButtonContainerSizeLargeHeight,
  componentIconButtonContainerSizeLargeWidth,
  componentIconButtonContainerSizeMediumBorderRadius,
  componentIconButtonContainerSizeMediumHeight,
  componentIconButtonContainerSizeMediumWidth,
  componentIconButtonContainerSizeSmallBorderRadius,
  componentIconButtonContainerSizeSmallHeight,
  componentIconButtonContainerSizeSmallWidth,
} from '@livingdesign/tokens/dist/react-native/light/regular/components/IconButton';
import {fireEvent, render} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';
import renderer from 'react-test-renderer';

import {colors} from '../../utils';
import {IconButton} from '../IconButton';

jest.useFakeTimers({legacyFakeTimers: true});
let mockFn: jest.Mock | ((event: GestureResponderEvent) => void);
beforeAll(() => {
  mockFn = jest.fn();
});
beforeEach(() => {
  jest.clearAllMocks();
});

describe('Test Icon Button', () => {
  test('Should match snapshot correctly.', async () => {
    const iconButton = renderer
      .create(
        <IconButton
          size="small"
          children={<Icons.HomeIcon />}
          onPress={mockFn}
        />,
      )
      .toJSON();
    expect(iconButton).toMatchSnapshot();
  });

  test('Should trigger onPress correctly.', async () => {
    const rootQueries = render(
      <IconButton
        size="small"
        children={<Icons.HomeIcon />}
        onPress={mockFn}
      />,
    );
    expect(mockFn).toHaveBeenCalledTimes(0);
    const button = await rootQueries.findByTestId('IconButton');
    fireEvent.press(button);
    expect(mockFn).toHaveBeenCalledTimes(1);
  });

  test('Should render disabled correctly.', async () => {
    const rootQueries = render(
      <IconButton
        size="small"
        children={<Icons.HomeIcon />}
        onPress={mockFn}
        disabled
      />,
    );
    let button = await rootQueries.findByTestId('IconButton');
    expect(button).toBeDisabled();
    rootQueries.update(
      <IconButton
        size="small"
        children={<Icons.HomeIcon />}
        onPress={mockFn}
      />,
    );
    button = await rootQueries.findByTestId('IconButton');
    expect(button).toBeEnabled();
  });

  test('Should not trigger onPress when disabled.', async () => {
    const rootQueries = render(
      <IconButton
        size="small"
        children={<Icons.HomeIcon />}
        onPress={mockFn}
        disabled
      />,
    );
    expect(mockFn).toHaveBeenCalledTimes(0);
    const button = await rootQueries.findByTestId('IconButton');
    fireEvent.press(button);
    expect(mockFn).toHaveBeenCalledTimes(0);
  });

  test('Should render icon correctly.', async () => {
    const rootQueries = render(
      <IconButton
        size="small"
        children={<Icons.CheckIcon />}
        onPress={mockFn}
        disabled
      />,
    );
    const button = await rootQueries.findByTestId('IconButton');
    const iconElement = rootQueries.queryByTestId('CheckIcon');
    expect(button).toContainElement(iconElement);
  });

  test(`Should render small sized icon buttons correctly.`, async () => {
    const rootQueries = render(
      <IconButton
        size="small"
        children={<Icons.HomeIcon />}
        onPress={mockFn}
      />,
    );
    const button = await rootQueries.findByTestId('IconButton');
    expect(button).toHaveStyle({
      width: componentIconButtonContainerSizeSmallWidth,
      height: componentIconButtonContainerSizeSmallHeight,
      borderRadius: componentIconButtonContainerSizeSmallBorderRadius,
    });
  });

  test(`Should render medium sized buttons correctly.`, async () => {
    const rootQueries = render(
      <IconButton
        size="medium"
        children={<Icons.HomeIcon />}
        onPress={mockFn}
      />,
    );
    const button = await rootQueries.findByTestId('IconButton');
    expect(button).toHaveStyle({
      width: componentIconButtonContainerSizeMediumWidth,
      height: componentIconButtonContainerSizeMediumHeight,
      borderRadius: componentIconButtonContainerSizeMediumBorderRadius,
    });
  });

  test(`Should render large sized buttons correctly.`, async () => {
    const rootQueries = render(
      <IconButton
        size="large"
        children={<Icons.HomeIcon />}
        onPress={mockFn}
      />,
    );
    const button = await rootQueries.findByTestId('IconButton');
    expect(button).toHaveStyle({
      width: componentIconButtonContainerSizeLargeWidth,
      height: componentIconButtonContainerSizeLargeHeight,
      borderRadius: componentIconButtonContainerSizeLargeBorderRadius,
    });
  });

  test('It should render correctly.', async () => {
    const button = renderer
      .create(<IconButton children={<Icons.HomeIcon />} onPress={mockFn} />)
      .toJSON();
    expect(button).toMatchSnapshot();
  });

  test(`Should render buttons of different colors correctly.`, async () => {
    const rootQueries = render(
      <IconButton children={<Icons.HomeIcon />} onPress={mockFn} />,
    );
    let button = await rootQueries.findByTestId('IconButton');
    expect(button).not.toHaveProp('color');

    rootQueries.update(
      <IconButton
        color={colors.green['20']}
        children={<Icons.HomeIcon />}
        onPress={mockFn}
      />,
    );
    button = await rootQueries.findByTestId('IconButton');
    expect(button).toHaveProp('color', colors.green['20']);
  });

  test(`Should render buttons with disabledColor correctly.`, async () => {
    const rootQueries = render(
      <IconButton
        disabledColor={colors.gray['10']}
        children={<Icons.HomeIcon />}
        onPress={mockFn}
      />,
    );
    let button = await rootQueries.findByTestId('IconButton');
    expect(button).toHaveProp('disabledColor', colors.gray['10']);
    rootQueries.update(
      <IconButton
        disabledColor={colors.green['20']}
        children={<Icons.HomeIcon />}
        onPress={mockFn}
      />,
    );
    button = await rootQueries.findByTestId('IconButton');
    expect(button).toHaveProp('disabledColor', colors.green['20']);
  });
});
