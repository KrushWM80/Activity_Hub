import * as React from 'react';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Callout';
import {fireEvent, render, screen} from '@testing-library/react-native';
import {getHostChildren} from '@testing-library/react-native/build/helpers/component-tree';

import {colors} from '../../utils';
import {Callout} from '../Callout';
import {Link} from '../Link';
import {PopoverPosition} from '../Popover';

jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');

const TestApp = ({position}: {position: PopoverPosition}) => {
  const [isOpen, setIsOpen] = React.useState<boolean>(false);

  return (
    <Callout
      content={`Example Callout ${position} content.`}
      isOpen={isOpen}
      onClose={() => setIsOpen(false)}
      closeText="Got it"
      position={position}>
      <Link onPress={() => setIsOpen(!isOpen)}>Trigger</Link>
    </Callout>
  );
};

beforeEach(() => {
  jest.clearAllMocks();
  jest.useFakeTimers({legacyFakeTimers: true});
});
describe.each<PopoverPosition>([
  'bottomCenter',
  'bottomLeft',
  'bottomRight',
  'left',
  'right',
  'topCenter',
  'topLeft',
  'topRight',
])('Test Callout with position ', (position) => {
  test(`Should render position: ${position}`, async () => {
    render(<TestApp position={position} />);
    const link = await screen.findByText('Trigger');

    // Test that the Callout exists only after trigger is pressed
    const modalNotVisible = screen.queryByTestId('Callout');
    expect(modalNotVisible).not.toBeTruthy();

    fireEvent.press(link);
    const modalVisible = await screen.findByTestId('Callout');
    expect(modalVisible).toBeTruthy();

    const content = screen.getByTestId('Callout-content');

    // Test Styles
    expect(content).toHaveStyle({
      backgroundColor: token.componentCalloutContainerBackgroundColor,
      borderRadius: token.componentCalloutContainerBorderRadius,
      paddingVertical: token.componentCalloutContainerPaddingVertical,
    });

    // Test text content
    expect(getHostChildren(content)[0]).toHaveTextContent(
      `Example Callout ${position} content.`,
    );

    // Test close text
    const close = screen.getByText('Got it');
    expect(close).toBeDefined();
    expect(close).toHaveStyle({
      color: colors.white,
      textDecorationLine: 'underline',
    });

    // Test Triangle (Nubbin) styles
    const triangle = screen.getByTestId('_Triangle');
    switch (position) {
      case 'bottomRight':
      case 'bottomCenter':
        expect(triangle).toHaveStyle([
          {
            width: 0,
            height: 0,
            backgroundColor: 'transparent',
            borderStyle: 'solid',
          },
          {
            borderTopWidth: 0,
            borderRightWidth: 8,
            borderBottomWidth: 8,
            borderLeftWidth: 8,
            borderTopColor: 'transparent',
            borderRightColor: 'transparent',
            borderBottomColor: token.componentCalloutNubbinBackgroundColor,
            borderLeftColor: 'transparent',
          },
          {},
        ]);
        break;
      case 'bottomLeft':
        expect(triangle).toHaveStyle([
          {
            width: 0,
            height: 0,
            backgroundColor: 'transparent',
            borderStyle: 'solid',
          },
          {
            borderTopWidth: 0,
            borderRightWidth: 8,
            borderBottomWidth: 8,
            borderLeftWidth: 8,
            borderTopColor: 'transparent',
            borderRightColor: 'transparent',
            borderBottomColor: token.componentCalloutNubbinBackgroundColor,
            borderLeftColor: 'transparent',
          },
          {marginRight: 24},
        ]);
        break;
      case 'right':
        expect(triangle).toHaveStyle([
          {
            width: 0,
            height: 0,
            backgroundColor: 'transparent',
            borderStyle: 'solid',
          },
          {
            borderTopWidth: 8,
            borderRightWidth: 8,
            borderBottomWidth: 8,
            borderLeftWidth: 0,
            borderTopColor: 'transparent',
            borderRightColor: token.componentCalloutNubbinBackgroundColor,
            borderBottomColor: 'transparent',
            borderLeftColor: 'transparent',
          },
          {},
        ]);
        break;
      case 'left':
        expect(triangle).toHaveStyle([
          {
            width: 0,
            height: 0,
            backgroundColor: 'transparent',
            borderStyle: 'solid',
          },
          {
            borderTopWidth: 8,
            borderRightWidth: 0,
            borderBottomWidth: 8,
            borderLeftWidth: 8,
            borderTopColor: 'transparent',
            borderRightColor: 'transparent',
            borderBottomColor: 'transparent',
            borderLeftColor: token.componentCalloutNubbinBackgroundColor,
          },
          {},
        ]);
        break;
      case 'topRight':
        expect(triangle).toHaveStyle([
          {
            width: 0,
            height: 0,
            backgroundColor: 'transparent',
            borderStyle: 'solid',
          },
          {
            borderTopWidth: 8,
            borderRightWidth: 8,
            borderBottomWidth: 0,
            borderLeftWidth: 8,
            borderTopColor: token.componentCalloutNubbinBackgroundColor,
            borderRightColor: 'transparent',
            borderBottomColor: 'transparent',
            borderLeftColor: 'transparent',
          },
          {marginLeft: 24},
        ]);
        break;
      case 'topCenter':
        expect(triangle).toHaveStyle([
          {
            width: 0,
            height: 0,
            backgroundColor: 'transparent',
            borderStyle: 'solid',
          },
          {
            borderTopWidth: 8,
            borderRightWidth: 8,
            borderBottomWidth: 0,
            borderLeftWidth: 8,
            borderTopColor: token.componentCalloutNubbinBackgroundColor,
            borderRightColor: 'transparent',
            borderBottomColor: 'transparent',
            borderLeftColor: 'transparent',
          },
          {},
        ]);
        break;
      case 'topLeft':
        expect(triangle).toHaveStyle([
          {
            width: 0,
            height: 0,
            backgroundColor: 'transparent',
            borderStyle: 'solid',
          },
          {
            borderTopWidth: 8,
            borderRightWidth: 8,
            borderBottomWidth: 0,
            borderLeftWidth: 8,
            borderTopColor: token.componentCalloutNubbinBackgroundColor,
            borderRightColor: 'transparent',
            borderBottomColor: 'transparent',
            borderLeftColor: 'transparent',
          },
          {marginRight: 24},
        ]);
        break;
      default:
        break;
    }
  });
});
