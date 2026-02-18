import * as React from 'react';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Switch';
import {act, fireEvent, render} from '@testing-library/react-native';

import {Switch} from '../Switch';

const mockFn = jest.fn();
const _switchTrack = 'Switch-track';
const _switchThumb = 'Switch-thumb';

describe('Test Switch', () => {
  jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');
  jest.useFakeTimers({legacyFakeTimers: true});
  beforeEach(() => {
    jest.clearAllMocks();
  });
  test('Should trigger onPress correctly', async () => {
    const rootQueries = render(
      <Switch label="Enabled" onValueChange={mockFn} />,
    );

    expect(mockFn).toHaveBeenCalledTimes(0);
    const element = rootQueries.getByRole('switch');
    fireEvent.press(element);
    expect(mockFn).toHaveBeenCalledTimes(1);
  });
  test('Should not trigger onPress when disabled', async () => {
    const rootQueries = render(
      <Switch label="Disabled" disabled onValueChange={mockFn} />,
    );

    expect(mockFn).toHaveBeenCalledTimes(0);
    const radio = rootQueries.getByRole('switch');
    fireEvent.press(radio);
    expect(mockFn).toHaveBeenCalledTimes(0);
  });
  test('Should render label correctly', async () => {
    const rootQueries = render(
      <Switch label="SwitchLabel" onValueChange={mockFn} />,
    );
    const label = await rootQueries.findByText('SwitchLabel');
    expect(label).toHaveStyle({
      fontFamily: 'Bogle',
      fontSize: token.componentSwitchTextLabelFontSize,
      color: token.componentSwitchTextLabelTextColor,
    });
  });
  test('Should render off and enabled correctly', async () => {
    const rootQueries = render(
      <Switch
        isOn={false}
        disabled={false}
        label="SwitchLabel"
        onValueChange={mockFn}
      />,
    );
    const track = await rootQueries.findByTestId(_switchTrack);
    expect(track).toHaveStyle({
      backgroundColor: token.componentSwitchTrackBackgroundColorDefault,
    });
    const thumb = await rootQueries.findByTestId(_switchThumb);
    expect(thumb).toHaveStyle({
      backgroundColor: token.componentSwitchHandleBackgroundColorDefault,
    });
  });
  test('Should render on and enabled correctly', async () => {
    const rootQueries = render(
      <Switch
        isOn={true}
        disabled={false}
        label="SwitchLabel"
        onValueChange={mockFn}
      />,
    );
    const track = await rootQueries.findByTestId(_switchTrack);
    expect(track).toHaveStyle({
      backgroundColor:
        token.componentSwitchTrackStateIsOnBackgroundColorDefault,
    });
    const thumb = await rootQueries.findByTestId(_switchThumb);
    expect(thumb).toHaveStyle({
      backgroundColor:
        token.componentSwitchHandleStateIsOnBackgroundColorDefault,
    });
  });
  test('Should render off and disabled correctly', async () => {
    const rootQueries = render(
      <Switch
        isOn={false}
        disabled={true}
        label="SwitchLabel"
        onValueChange={mockFn}
      />,
    );
    const track = await rootQueries.findByTestId(_switchTrack);
    expect(track).toHaveStyle({
      backgroundColor: token.componentSwitchTrackBackgroundColorDisabled,
    });
    const thumb = await rootQueries.findByTestId(_switchThumb);
    expect(thumb).toHaveStyle({
      backgroundColor: token.componentSwitchHandleBackgroundColorDisabled,
    });
  });
  test('Should render on and disabled correctly', async () => {
    const rootQueries = render(
      <Switch
        isOn={true}
        disabled={true}
        label="SwitchLabel"
        onValueChange={mockFn}
      />,
    );
    const track = await rootQueries.findByTestId(_switchTrack);
    expect(track).toHaveStyle({
      backgroundColor:
        token.componentSwitchTrackStateIsOnBackgroundColorDisabled,
    });
    const thumb = await rootQueries.findByTestId(_switchThumb);
    expect(thumb).toHaveStyle({
      backgroundColor:
        token.componentSwitchHandleStateIsOnBackgroundColorDisabled,
    });
  });
  test('Should render correctly after changing isOn state', async () => {
    const Content = () => {
      const [isOn, setIsOn] = React.useState(false);
      return (
        <Switch
          isOn={isOn}
          label="SwitchLabel"
          onValueChange={() => {
            setIsOn((previousState) => !previousState);
          }}
        />
      );
    };
    const rootQueries = render(<Content />);

    // First check if the off state is rendered correctly
    expect(rootQueries.queryByTestId(_switchTrack)).toHaveStyle({
      backgroundColor: token.componentSwitchTrackBackgroundColorDefault,
    });
    expect(rootQueries.queryByTestId(_switchThumb)).toHaveStyle({
      backgroundColor: token.componentSwitchHandleBackgroundColorDefault,
    });

    // Next press the element and check if the state is rendered as on
    const element = rootQueries.getByRole('switch');
    fireEvent.press(element);
    // @ts-ignore
    act(() => jest.runOnlyPendingTimers());
    expect(rootQueries.queryByTestId(_switchTrack)).toHaveStyle({
      backgroundColor:
        token.componentSwitchTrackStateIsOnBackgroundColorDefault,
    });
    expect(rootQueries.queryByTestId(_switchThumb)).toHaveStyle({
      backgroundColor:
        token.componentSwitchHandleStateIsOnBackgroundColorDefault,
    });
  });
});
