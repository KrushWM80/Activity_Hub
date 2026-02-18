import * as React from 'react';
import {View} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Popover';
import {fireEvent, render, screen} from '@testing-library/react-native';

import {Checkbox} from '../Checkbox';
import {Link} from '../Link';
import {Popover, PopoverPosition} from '../Popover';

jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');

jest.useFakeTimers({legacyFakeTimers: true});

const TestApp = ({
  position,
  hasNubbin,
  hasSpotlight,
  spotlightColor,
}: {
  position: PopoverPosition;
  hasNubbin: boolean;
  hasSpotlight: boolean;
  spotlightColor: string;
}) => {
  const [isOpen, setIsOpen] = React.useState<boolean>(false);

  return (
    <Popover
      content={
        <View style={{width: 200}}>
          <Checkbox label="I must contain at least one focusable element." />
        </View>
      }
      isOpen={isOpen}
      onClose={() => setIsOpen(false)}
      hasNubbin={hasNubbin}
      hasSpotlight={hasSpotlight}
      spotlightColor={spotlightColor}
      position={position}>
      <Link onPress={() => setIsOpen(!isOpen)}>Trigger</Link>
    </Popover>
  );
};

beforeEach(() => {
  jest.clearAllMocks();
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
])('Test Popover with position ', (position) => {
  describe.each<boolean>([true, false])(`... and nubbin`, (hasNubbin) => {
    describe.each<boolean>([true, false])(
      `... and spotlight`,
      (hasSpotlight) => {
        test(`Should render position: ${position} with nubbin: ${hasNubbin} and spotlight: ${hasSpotlight}`, async () => {
          render(
            <TestApp
              position={position}
              hasSpotlight={hasSpotlight}
              spotlightColor="blue"
              hasNubbin={true}
            />,
          );
          const link = await screen.findByText('Trigger');

          // Test that the Popover exists only after trigger is pressed
          const modalNotVisible = screen.queryByTestId('Popover');
          expect(modalNotVisible).not.toBeTruthy();

          fireEvent.press(link);
          const modalVisible = await screen.findByTestId('Popover');
          expect(modalVisible).toBeTruthy();

          expect(screen).toMatchSnapshot();

          const container = screen.getByTestId('Popover-container');
          const spotlight = hasSpotlight
            ? screen.getByTestId('Popover-spotlight')
            : undefined;
          const content = screen.getByTestId('Popover-content');
          const checkbox = screen.getByTestId('Checkbox');

          // Test Styles
          expect(content).toHaveStyle({
            backgroundColor: token.componentPopoverContainerBackgroundColor, // "#fff"
            borderRadius: token.componentPopoverContainerBorderRadius, // 4
            paddingHorizontal: token.componentPopoverContainerPaddingHorizontal, // 16
            paddingVertical: token.componentPopoverContainerPaddingVertical, // 16
          });

          hasSpotlight &&
            expect(spotlight).toHaveStyle({backgroundColor: 'blue'});

          // Test text content
          // @ts-ignore
          expect(checkbox.children[1].children[0]).toHaveTextContent(
            'I must contain at least one focusable element.',
          );

          // Test nubbin position and spotlight position
          switch (position) {
            case 'bottomRight':
              expect(container).toHaveStyle({
                alignItems: 'flex-start',
              });
              break;
            case 'bottomCenter':
              expect(container).toHaveStyle({
                alignItems: 'center',
              });
              break;
            case 'bottomLeft':
              expect(container).toHaveStyle({
                alignItems: 'flex-end',
              });
              break;
            case 'right':
              expect(container).toHaveStyle({
                flexDirection: 'row',
                alignItems: 'center',
              });
              break;
            case 'left':
              expect(container).toHaveStyle({
                flexDirection: 'row-reverse',
                alignItems: 'center',
              });
              break;
            case 'topRight':
              expect(container).toHaveStyle({
                flexDirection: 'column-reverse',
                alignItems: 'flex-start',
              });
              break;
            case 'topCenter':
              expect(container).toHaveStyle({
                flexDirection: 'column-reverse',
                alignItems: 'center',
              });
              break;
            case 'topLeft':
              expect(container).toHaveStyle({
                flexDirection: 'column-reverse',
                alignItems: 'flex-end',
              });
              break;
            default:
              break;
          }
        });
      },
    );
  });
});
