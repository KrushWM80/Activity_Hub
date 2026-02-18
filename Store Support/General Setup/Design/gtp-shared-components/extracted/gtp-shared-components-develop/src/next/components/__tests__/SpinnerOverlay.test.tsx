import React from 'react';
import {Text} from 'react-native';

import {cleanup, render, screen} from '@testing-library/react-native';
import {getHostChildren} from '@testing-library/react-native/build/helpers/component-tree';
import MockDate from 'mockdate';

import {SpinnerOverlay} from '../SpinnerOverlay';

beforeEach(() => {
  MockDate.set(0);
  jest.useFakeTimers({legacyFakeTimers: true});
});

afterEach(cleanup);

describe('SpinnerOverlay', () => {
  it('should render a spinner', async () => {
    render(
      <SpinnerOverlay visible={true}>
        <Text>Test Children</Text>
      </SpinnerOverlay>,
    );
    expect(screen.getByText('Test Children')).toBeDefined();
    const spinner = await screen.findByTestId('Spinner');
    expect(spinner).toBeDefined();
  });

  it('should render a spinner with a custom color', async () => {
    render(
      <SpinnerOverlay visible={true} spinnerColor="white">
        <Text>Test Children</Text>
      </SpinnerOverlay>,
    );
    const spinner = await screen.findByTestId('Spinner');
    expect(getHostChildren(spinner)[0]).toHaveStyle([
      {
        tintColor: 'white',
      },
    ]);
  });

  it('should render a spinner with a small size', async () => {
    render(
      <SpinnerOverlay visible={true} spinnerSize="small">
        <Text>Test Children</Text>
      </SpinnerOverlay>,
    );
    const spinner = await screen.findByTestId('Spinner');
    expect(spinner).toHaveStyle([{width: 24, height: 24}]);
  });

  it('should render a spinner with a large size', async () => {
    render(
      <SpinnerOverlay visible={true} spinnerSize="large">
        <Text>Test Children</Text>
      </SpinnerOverlay>,
    );
    const spinner = await screen.findByTestId('Spinner');
    expect(spinner).toHaveStyle([{width: 48, height: 48}]);
  });

  it('should render a spinner overlay with darkened background', async () => {
    render(
      <SpinnerOverlay visible={true} darken={true}>
        <Text>Test Children</Text>
      </SpinnerOverlay>,
    );
    const spinnerOverlay = await screen.findByTestId(
      'SpinnerOverlay-container',
    );
    expect(spinnerOverlay).toHaveStyle([{backgroundColor: 'rgba(0,0,0,.25)'}]);
  });

  it('should render a spinner overlay with transparent=false', async () => {
    render(
      <SpinnerOverlay visible={true} transparent={false}>
        <Text>Test Children</Text>
      </SpinnerOverlay>,
    );
    const spinnerOverlay = await screen.findByTestId('SpinnerOverlay');
    expect(spinnerOverlay).toHaveProp('transparent', false);
  });

  it('should render a spinner overlay with visible=false', async () => {
    render(
      <SpinnerOverlay visible={false}>
        <Text>Test Children</Text>
      </SpinnerOverlay>,
    );
    const spinnerOverlay = screen.queryByTestId('SpinnerOverlay');
    expect(spinnerOverlay).not.toBeTruthy();
  });
});
