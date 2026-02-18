import * as React from 'react';

import {act, fireEvent, render} from '@testing-library/react-native';

import {useSnackbar} from '../../utils/useSnackbar';
import {SnackbarProvider} from '../SnackbarProvider';

const mockFn = jest.fn();
const _snackTime = 'Snack Time';
describe('Test useSnackbar functionality', () => {
  jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');
  beforeEach(() => {
    jest.useFakeTimers({legacyFakeTimers: true});
    jest.clearAllMocks();
  });
  test('Should render a snack with message correctly.', async () => {
    const Content = () => {
      const {addSnack} = useSnackbar();

      React.useEffect(() => {
        addSnack({
          message: _snackTime,
        });
      }, [addSnack]);

      return null;
    };

    const rootQueries = render(
      <SnackbarProvider>
        <Content />
      </SnackbarProvider>,
    );

    const snackbar = rootQueries.queryByTestId('Snackbar');
    expect(snackbar).not.toBeNull();
    const body = rootQueries.queryByTestId('Body');
    expect(body).toHaveTextContent(_snackTime);
  });

  test('Should only render the latest snack correctly.', async () => {
    const first = 'First Snack';
    const second = 'Second Snack';

    const Content = () => {
      const {addSnack} = useSnackbar();

      React.useEffect(() => {
        addSnack({
          message: first,
        });

        addSnack({
          message: second,
        });
      }, [addSnack]);

      return null;
    };

    const rootQueries = render(
      <SnackbarProvider>
        <Content />
      </SnackbarProvider>,
    );

    const body = rootQueries.queryByTestId('Body');
    expect(body).not.toHaveTextContent(first);
    expect(body).toHaveTextContent(second);
  });

  test('Should add and remove a snack correctly.', async () => {
    const Content = () => {
      const {addSnack} = useSnackbar();

      React.useEffect(() => {
        addSnack({
          message: _snackTime,
        });
      }, [addSnack]);

      return null;
    };

    const rootQueries = render(
      <SnackbarProvider>
        <Content />
      </SnackbarProvider>,
    );

    expect(rootQueries.queryByTestId('Snackbar')).not.toBeNull();

    const closeIcon = rootQueries.getByTestId('CloseIcon');
    fireEvent.press(closeIcon);
    // @ts-ignore
    act(() => jest.runOnlyPendingTimers());

    expect(rootQueries.queryByTestId('Snackbar')).toBeNull();
  });
  test('Should add a snackbar with action button and trigger it', async () => {
    const actionButtonText = 'ActionButton';
    const Content = () => {
      const {addSnack} = useSnackbar();

      React.useEffect(() => {
        addSnack({
          message: _snackTime,
          actionButton: {
            caption: actionButtonText,
            onPress: mockFn,
          },
        });
      }, [addSnack]);

      return null;
    };

    const rootQueries = render(
      <SnackbarProvider>
        <Content />
      </SnackbarProvider>,
    );

    expect(rootQueries.queryByTestId('Snackbar')).not.toBeNull();

    expect(mockFn).toHaveBeenCalledTimes(0);
    const button = rootQueries.getByText(actionButtonText);
    // Alternative ways to query for action button that also work:
    // const button = rootQueries.getByA11yRole('link');
    // const button = rootQueries.getByTestId('LinkActionButton');
    expect(button).toHaveTextContent('ActionButton');
    fireEvent.press(button);
    expect(mockFn).toHaveBeenCalledTimes(1);

    // After pressing the action button, it should now disappear after fade animation
    // @ts-ignore
    act(() => jest.runOnlyPendingTimers());
    expect(rootQueries.queryByTestId('Snackbar')).toBeNull();
  });
});
