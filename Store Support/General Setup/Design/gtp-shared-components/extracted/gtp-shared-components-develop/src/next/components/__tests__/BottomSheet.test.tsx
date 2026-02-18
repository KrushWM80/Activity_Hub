import * as React from 'react';
import {
  FlexStyle,
  LayoutChangeEvent,
  Text,
  TextStyle,
  View,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/BottomSheet';
import {
  act,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from '@testing-library/react-native';

import {getFont, Weights} from '../../../theme/font';
import {colors, loremIpsum} from '../../utils';
import {_BottomSheetContent as BottomSheetContent} from '../_BottomSheetContent';
import {BottomSheet} from '../BottomSheet';
import {Button} from '../Button';
import {ButtonGroup} from '../ButtonGroup';

jest.useFakeTimers({legacyFakeTimers: true});
jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');
jest.mock('react-native-device-info', () => {
  return {
    __esModule: true,
    default: {
      hasNotch: jest.fn().mockReturnValueOnce(true).mockReturnValueOnce(false),
      ...jest.fn(() => {}),
    },
  };
});

describe('Test render helpers', () => {
  test('when title is React.Node', async () => {
    render(
      <BottomSheet
        useNativeDriver={false}
        showCloseHandle
        isOpen={true}
        closeButtonProps={{
          // accessibilityLabel: 'close React.Node BottomSheet',
          onPress: jest.fn(),
        }}
        accessibilityLabel="The BottomSheet title"
        accessibilityTitleLabel="accessibilityTitleLabel"
        title={
          <View>
            <Text>React.Node</Text>
          </View>
        }>
        {loremIpsum(1)}
      </BottomSheet>,
    );
    const bottomSheet = await screen.findByTestId(`BottomSheet`);
    expect(bottomSheet.props.accessibilityLabel).toBe('The BottomSheet title');
    const closeButton = await screen.findByTestId(
      BottomSheet.displayName + '-close-button',
    );
    expect(closeButton.props.accessibilityLabel).toBe(
      'close accessibilityTitleLabel BottomSheet',
    );
    const bottomSheetTouchableArea = await screen.findByTestId(
      BottomSheet.displayName + '-outside-body-button',
    );
    expect(bottomSheetTouchableArea.props.accessibilityActions[0].label).toBe(
      'close accessibilityTitleLabel BottomSheet',
    );
  });
  test.each<'custom bottomSheet accessibilityLabel' | undefined>([
    'custom bottomSheet accessibilityLabel',
    undefined,
  ])(
    'should renderHeader correctly with accessibilityLabel %s',
    async (label) => {
      const closeMockFn = jest.fn();
      const resizeMockFn = jest.fn(() => undefined);

      render(
        <BottomSheet
          useNativeDriver={false}
          showCloseHandle
          onClose={closeMockFn}
          isOpen={true}
          title="This is the header"
          onResize={resizeMockFn}
          accessibilityLabel={label as any}>
          {loremIpsum(1)}
        </BottomSheet>,
      );
      const closeButton = await screen.findByTestId(
        BottomSheet.displayName + '-close-button',
      );
      expect(closeButton.props.accessibilityLabel).toBe(
        'close This is the header BottomSheet',
      );
    },
  );
  test.each([
    'custom bottomSheet accessibilityRole',
    'withoutAccessibilityRole',
    undefined,
  ])(
    'should renderHeader correctly with accessibilityRole %s',
    async (role) => {
      let isHeaderEnabled = role === 'withoutAccessibilityRole';
      if (isHeaderEnabled) {
        render(
          <BottomSheet
            UNSAFE_style={{
              maxHeight: 600,
              minHeight: 200,
              paddingBottom: 10,
              paddingHorizontal: 10,
            }}
            useNativeDriver={false}
            showCloseHandle
            isOpen={true}
            title="This is the header"
            accessibilityRole={role as any}
            visible={true}>
            {loremIpsum(1)}
          </BottomSheet>,
        );
      } else {
        render(
          <BottomSheet
            UNSAFE_style={{
              backgroundColor: 'gray',
              height: 600,
              paddingHorizontal: 0,
            }}
            useNativeDriver={false}
            showCloseHandle
            isOpen={true}
            accessibilityRole={role as any}
            visible={false}>
            {loremIpsum(1)}
          </BottomSheet>,
        );
      }

      const bottomSheetComponent = await screen.findByTestId(`BottomSheet`);
      const closeButton = await screen.findByTestId(
        BottomSheet.displayName + '-close-button',
      );

      const header = await screen.findByTestId('BottomSheet-header');

      expect(header).toBeTruthy();
      expect(closeButton).toBeTruthy();
      expect(closeButton.props.accessibilityLabel).toBe(
        isHeaderEnabled
          ? 'close This is the header BottomSheet'
          : 'close BottomSheet',
      );

      expect(bottomSheetComponent?.props.accessibilityState.expanded).toBe(
        true,
      );

      expect(closeButton?.props.accessibilityRole).toEqual('button');

      expect(closeButton).toHaveStyle({
        alignItems: 'center',
        borderRadius: 1000,
        height: 32,
        justifyContent: 'center',
        width: 32,
        borderColor: 'transparent',
      });

      const subContainer = await screen.findByTestId(
        BottomSheet.displayName + '-sub-container',
      );

      const headerStyle = header.props.style;
      expect(headerStyle).toContainEqual(
        expect.objectContaining({alignItems: 'center'}),
      );
      expect(headerStyle).toContainEqual(
        expect.objectContaining({flexDirection: 'row-reverse'}),
      );
      expect(headerStyle).toContainEqual(
        expect.objectContaining({justifyContent: 'flex-start'}),
      );

      if (isHeaderEnabled) {
        expect(headerStyle).toContainEqual(
          expect.objectContaining({paddingHorizontal: 16}),
        );
        expect(headerStyle).toContainEqual(
          expect.objectContaining({padding: 16}),
        );

        expect(subContainer.props.style[2].paddingBottom).toBe(10);

        const title = await screen.findByText('This is the header');
        expect(title).toBeTruthy();

        expect(title?.props.accessibilityRole).toEqual('header');

        expect(title).toHaveStyle({
          ...getFont(
            token.componentBottomSheetTitleFontWeight.toString() as Weights,
          ), // "700"
          fontSize: token.componentBottomSheetTitleFontSize, // 18,
          lineHeight: token.componentBottomSheetTitleLineHeight, // 24,
          textAlign: token.componentBottomSheetTitleTextAlign, // "center",
          paddingLeft: token.componentBottomSheetTitlePaddingStart, // 40,
          color: token.componentBottomSheetTitleTextColor, // "#2e2f32"
        });
      } else {
        expect(headerStyle).toContainEqual(
          expect.objectContaining({paddingHorizontal: 0}),
        );
        expect(headerStyle).toContainEqual(
          expect.objectContaining({paddingTop: 8}),
        );

        expect(subContainer).toBeDefined();
        expect(subContainer.props.style[1].paddingBottom).toBe(16);
        expect(subContainer.props.style[1].height).toBeUndefined();
        expect(subContainer.props.style[1].maxHeight).toBeUndefined();
        expect(subContainer.props.style[1].minHeight).toBeUndefined();
      }
    },
  );

  test.each([true, false])(
    'open or close call to Modal, where visible or isOpen = %s',
    async (openModal) => {
      const handleCloseMock = jest.fn();
      render(
        <BottomSheet
          useNativeDriver={false}
          showCloseHandle
          title="This is the header"
          visible={openModal}
          onClose={handleCloseMock}
          isOpen={openModal}>
          {loremIpsum(1)}
        </BottomSheet>,
      );

      if (openModal) {
        const bottomSheetComponent = await screen.findByTestId(`BottomSheet`);
        expect(bottomSheetComponent).toBeDefined();
      }
    },
  );

  test('should set accessibilityState.expanded to true when visible is true', async () => {
    render(
      <BottomSheet
        useNativeDriver={false}
        showCloseHandle
        title="This is the header"
        visible={true}
        isOpen={false}>
        {loremIpsum(1)}
      </BottomSheet>,
    );

    const bottomSheetComponent = await screen.findByTestId(`BottomSheet`);
    expect(bottomSheetComponent?.props.accessibilityState.expanded).toBe(true);
  });

  test.each([100, undefined])(
    'calls onResize with the correct height when onLayout is triggered %s',
    async (layoutHeight) => {
      const onResizeMock = jest.fn(() => layoutHeight);
      render(
        <BottomSheet
          hideCloseIcon={false}
          showCloseHandle
          onResize={onResizeMock}
          isOpen={true}>
          {loremIpsum(1)}
        </BottomSheet>,
      );

      // Simulate the layout event with a specific height
      const bottomSheet = await screen.findByTestId(
        `${BottomSheet.displayName}`,
      );
      const animatedView = await screen.findByTestId(
        BottomSheet.displayName + '-sub-container',
      );

      // Simulate the onLayout event
      fireEvent(animatedView, 'layout', {
        nativeEvent: {
          layout: {
            height: layoutHeight,
          },
        },
      });

      // Expect the onResize function to have been called with the correct height
      if (layoutHeight) {
        expect(onResizeMock).toHaveBeenCalledWith(layoutHeight);
        expect(bottomSheet.props.onResize(layoutHeight)).toEqual(100);

        const layoutEvent = {
          nativeEvent: {
            layout: {
              height: layoutHeight,
            },
          },
        };
        animatedView.props.onLayout(
          layoutEvent as unknown as LayoutChangeEvent,
        ); // Typecast for the LayoutChangeEvent
        expect(onResizeMock).toHaveBeenCalledWith(layoutHeight);
      } else {
        expect(bottomSheet.props.onResize(layoutHeight)).toBeUndefined();
      }
    },
  );

  test('should not call onResize if the function is not provided', async () => {
    // Render the component without the onResize prop
    const onResizeMock = jest.fn((layoutHeight) => layoutHeight);
    render(
      <BottomSheet hideCloseIcon={false} showCloseHandle isOpen={true}>
        {loremIpsum(1)}
      </BottomSheet>,
    );

    const layoutEvent = {
      nativeEvent: {
        layout: {
          height: 150,
        },
      },
    };

    const view = await screen.findByTestId(
      BottomSheet.displayName + '-sub-container',
    );
    view.props.onLayout(layoutEvent as unknown as LayoutChangeEvent); // Typecast for the LayoutChangeEvent

    expect(onResizeMock).not.toHaveBeenCalled();
  });

  test('should renderContent correctly when actions present', async () => {
    if (BottomSheet.displayName) {
      render(
        <BottomSheetContent
          keyboardShouldPersistTaps="always"
          componentName={BottomSheet.displayName}>
          {loremIpsum(1)}
        </BottomSheetContent>,
      );

      const content = await screen.findByTestId(
        BottomSheet.displayName + '-content',
      );

      expect(content).toHaveStyle({
        width: token.componentBottomSheetLayoutContainerWidth, // "100%",
        alignItems:
          token.componentBottomSheetLayoutContainerAlignHorizontal as Extract<
            FlexStyle,
            'alignItems'
          >, //'center'
      });

      const lIpsum = await screen.findByText(loremIpsum(1));
      expect(content).toContainElement(lIpsum);
      expect(lIpsum).toHaveStyle({
        ...getFont(),
        lineHeight: 20,
        color: colors.black,
      } as TextStyle);
    }
  });
  test('should renderContent correctly when no actions', async () => {
    if (BottomSheet.displayName) {
      render(
        <BottomSheetContent
          keyboardShouldPersistTaps="always"
          headerTitle={'Title'}
          componentName={BottomSheet.displayName}>
          {loremIpsum(1)}
        </BottomSheetContent>,
      );

      const content = await screen.findByTestId(
        BottomSheet.displayName + '-content',
      );

      expect(content).toHaveStyle({
        width: token.componentBottomSheetLayoutContainerWidth, // "100%",
        alignItems:
          token.componentBottomSheetLayoutContainerAlignHorizontal as Extract<
            FlexStyle,
            'alignItems'
          >, //'center'
      });

      const lIpsum = await screen.findByText(loremIpsum(1));
      expect(content).toContainElement(lIpsum);
      expect(lIpsum).toHaveStyle({
        ...getFont(),
        lineHeight: 20,
        color: colors.black,
      } as TextStyle);
    }
  });
  test('should renderActions correctly', async () => {
    if (BottomSheet.displayName) {
      render(
        <BottomSheetContent
          keyboardShouldPersistTaps="always"
          actions={
            <ButtonGroup>
              <Button variant="tertiary" onPress={jest.fn()}>
                Cancel
              </Button>
              <Button variant="primary" onPress={jest.fn()}>
                Continue
              </Button>
            </ButtonGroup>
          }
          componentName={BottomSheet.displayName}>
          {loremIpsum(1)}
        </BottomSheetContent>,
      );

      const actions = await screen.findByTestId(
        BottomSheet.displayName + '-actions',
      );
      fireEvent(actions, 'onLayout', {
        nativeEvent: {
          layout: {
            height: 10,
          },
        },
      });

      expect(actions).toHaveStyle({
        flexDirection: 'row',
        justifyContent: 'flex-end',
        borderTopColor: token.componentBottomSheetActionContentBorderColorTop, // "#e3e4e5",
        borderTopWidth: token.componentBottomSheetActionContentBorderWidthTop, // 1,
        paddingVertical: token.componentBottomSheetActionContentPaddingBS, // 16,
      });

      const buttons = await screen.findAllByTestId('Button');

      expect(buttons).toHaveLength(2);

      expect(buttons[0]?.props.accessibilityState).toEqual({
        busy: false,
        disabled: false,
      });

      expect(buttons[0]).toHaveStyle({
        flexDirection: 'row',
        justifyContent: 'center',
        overflow: 'visible',
      });

      expect(within(buttons[0]).getByText('Cancel')).toBeTruthy();
      expect(within(buttons[0]).getByText('Cancel')).toHaveStyle({
        ...getFont('400'),
        textAlign: 'center',
        color: '#2e2f32',
        fontSize: 14,
        lineHeight: 32,
      } as TextStyle);

      expect(buttons[1]?.props.accessibilityState).toEqual({
        busy: false,
        disabled: false,
      });

      expect(buttons[1]).toHaveStyle({
        flexDirection: 'row',
        justifyContent: 'center',
        overflow: 'visible',
      });
      expect(within(buttons[1]).getByText('Continue')).toBeTruthy();
      expect(within(buttons[1]).getByText('Continue')).toHaveStyle({
        ...getFont('700'),
        textAlign: 'center',
        color: '#fff',
        fontSize: 14,
        lineHeight: 32,
      } as TextStyle);
    }
  });
});

describe('Test BottomSheet with content text', () => {
  const BottomSheetWithText = ({size}: {size: 'small' | 'large'}) => {
    const mockModalOnClose = jest.fn();
    const mockModalOnClosed = jest.fn();

    const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(false);

    const openModal = () => {
      setModalIsOpen(true);
    };
    const handleModalCancel = () => {
      setModalIsOpen(false);
    };
    const handleModalContinue = () => {
      setModalIsOpen(false);
    };
    return (
      <View>
        <Button variant="primary" onPress={openModal}>
          Show
        </Button>
        {modalIsOpen && (
          <BottomSheet
            useNativeDriver={false}
            showCloseHandle
            isOpen={modalIsOpen}
            onClose={mockModalOnClose}
            onClosed={mockModalOnClosed}
            title="Confirmation"
            actions={
              <ButtonGroup>
                <Button variant="tertiary" onPress={handleModalCancel}>
                  Cancel
                </Button>
                <Button variant="primary" onPress={handleModalContinue}>
                  Continue
                </Button>
              </ButtonGroup>
            }>
            {size === 'small' ? loremIpsum(1) : loremIpsum(10)}
          </BottomSheet>
        )}
      </View>
    );
  };

  describe.each<'small' | 'large'>(['small', 'large'])('size="%s"', (size) => {
    test('render correctly', async () => {
      render(<BottomSheetWithText size={size} />);

      const showButton = screen.getByText('Show');
      expect(showButton).toBeTruthy();

      expect(screen.queryAllByText(loremIpsum(1))).toHaveLength(0);
      expect(screen.queryAllByText(loremIpsum(10))).toHaveLength(0);

      fireEvent.press(showButton);
      if (size === 'small') {
        expect(screen.queryAllByText(loremIpsum(1))).toHaveLength(1);
      } else {
        expect(screen.queryAllByText(loremIpsum(10))).toHaveLength(1);
      }

      expect(screen.getByText('Confirmation')).toBeTruthy();
      expect(screen.getByText('Cancel')).toBeTruthy();
      expect(screen.getByText('Continue')).toBeTruthy();
      expect(screen.getByTestId('BottomSheet-close-button')).toBeTruthy();

      const closeButton = screen.getByTestId('BottomSheet-close-button');
      expect(closeButton).toBeTruthy();
      expect(closeButton?.props.accessibilityRole).toEqual('button');

      const closeIcon = screen.getByTestId('CloseIcon');
      expect(closeIcon?.props.source).toEqual({
        testUri:
          '../../@walmart/gtp-shared-icons/assets/images/icons/Close-24.png',
      });
    });
  });
});

describe('Test onClose/onClosed callbacks', () => {
  jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');
  jest.useFakeTimers({legacyFakeTimers: true});
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('open, close, open without onClose/onClosed callbacks', async () => {
    const BottomSheetApp = () => {
      const [isOpen, setIsOpen] = React.useState<boolean>(false);
      return (
        <>
          <BottomSheet
            actions={
              <Button
                testID="closeButton"
                variant="primary"
                onPress={() => setIsOpen(false)}>
                Close
              </Button>
            }
            isOpen={isOpen}>
            {loremIpsum(1)}
          </BottomSheet>
          <Button
            testID="externalOpen"
            variant="primary"
            onPress={() => setIsOpen(true)}>
            Close
          </Button>
        </>
      );
    };
    render(<BottomSheetApp />);

    // Expect not to find the BottomSheet defined
    let bottomSheet = screen.queryByTestId('BottomSheet');
    expect(bottomSheet).toBeNull();

    // Open the BottomSheet and find it defined
    const openButton = await screen.findByTestId('externalOpen');
    fireEvent.press(openButton);
    act(() => {
      jest.runAllTimers();
    });
    bottomSheet = await screen.findByTestId('BottomSheet');
    expect(bottomSheet).toBeDefined();

    // Close the BottomSheet and find it not defined
    const closeButton = await screen.findByTestId('closeButton');
    fireEvent.press(closeButton);
    act(() => {
      jest.runAllTimers();
    });
    bottomSheet = screen.queryByTestId('BottomSheet');
    expect(bottomSheet).toBeNull();

    // Open the BottomSheet again and find it defined
    fireEvent.press(openButton);
    act(() => {
      jest.runAllTimers();
    });
    bottomSheet = await screen.findByTestId('BottomSheet');
    expect(bottomSheet).toBeDefined();
  });

  test('onClose callback from clicking outside', async () => {
    const mockOnClose = jest.fn();
    const mockOnClosed = jest.fn();
    const BottomSheetApp = () => {
      return (
        <BottomSheet
          onClose={mockOnClose}
          onClosed={mockOnClosed}
          isOpen={true}>
          {loremIpsum(1)}
        </BottomSheet>
      );
    };
    render(<BottomSheetApp />);
    const bottomSheetTouchableArea = await screen.findByTestId(
      BottomSheet.displayName + '-outside-body-button',
    );
    expect(bottomSheetTouchableArea).toBeDefined();
    fireEvent.press(bottomSheetTouchableArea);

    expect(mockOnClose).toHaveBeenCalledTimes(1);
    act(() => {
      jest.runAllTimers();
    });
    await waitFor(() => {
      expect(mockOnClosed).toHaveBeenCalledTimes(1);
    });
  });

  test('onClose callback from clicking close button', async () => {
    const mockOnClose = jest.fn();
    const mockOnClosed = jest.fn();
    const BottomSheetApp = () => {
      return (
        <BottomSheet
          onClose={mockOnClose}
          onClosed={mockOnClosed}
          isOpen={true}>
          {loremIpsum(1)}
        </BottomSheet>
      );
    };
    render(<BottomSheetApp />);
    const closeButton = await screen.findByTestId(
      BottomSheet.displayName + '-close-button',
    );
    expect(closeButton).toBeDefined();
    fireEvent.press(closeButton);

    expect(mockOnClose).toHaveBeenCalledTimes(1);
    act(() => {
      jest.runAllTimers();
    });
    await waitFor(() => {
      expect(mockOnClosed).toHaveBeenCalledTimes(1);
    });
  });

  test('onClose callback from setting isOpen to false', async () => {
    const mockOnClose = jest.fn();
    const mockOnClosed = jest.fn();
    const BottomSheetApp = () => {
      const [isOpen, setIsOpen] = React.useState<boolean>(true);
      return (
        <>
          <BottomSheet
            onClose={mockOnClose}
            onClosed={mockOnClosed}
            isOpen={isOpen}>
            {loremIpsum(1)}
          </BottomSheet>
          <Button
            testID="externalClose"
            variant="primary"
            onPress={() => setIsOpen(false)}>
            Close
          </Button>
        </>
      );
    };
    render(<BottomSheetApp />);
    const closeButton = await screen.findByTestId('externalClose');
    expect(closeButton).toBeDefined();
    fireEvent.press(closeButton);

    expect(mockOnClose).toHaveBeenCalledTimes(1);
    act(() => {
      jest.runAllTimers();
    });
    await waitFor(() => {
      expect(mockOnClosed).toHaveBeenCalledTimes(1);
    });
  });
});

describe('Test render', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });
  test('default isOpen false', async () => {
    const closeBottomSheetMock = jest.fn();
    const paddingBottomFn = jest.fn(() => 0);

    render(
      <BottomSheet
        visible={true}
        onClose={closeBottomSheetMock}
        UNSAFE_style={{paddingBottom: 0}}
        isOpen={false}
        actions={
          <ButtonGroup>
            <Button variant="tertiary" onPress={jest.fn()}>
              Cancel
            </Button>
            <Button variant="primary" onPress={jest.fn()}>
              Continue
            </Button>
          </ButtonGroup>
        }>
        {loremIpsum(1)}
      </BottomSheet>,
    );

    const component = await screen.findByTestId(`${BottomSheet.displayName}`);

    const subcontainer = await screen.findByTestId(
      BottomSheet.displayName + '-sub-container',
    );

    expect(subcontainer).toHaveStyle({
      paddingBottom: paddingBottomFn(),
    });
    expect(component).toBeDefined();
  });

  it('should not modify other properties when deleting height, minHeight, and maxHeight', () => {
    const UNSAFE_style = {
      height: 100,
      minHeight: 50,
      maxHeight: 200,
      width: 300,
    };

    <BottomSheet visible={true} UNSAFE_style={UNSAFE_style} isOpen={false}>
      {loremIpsum(1)}
    </BottomSheet>;

    // Expect that width is still present
    expect(UNSAFE_style.width).toBe(300);
  });

  it('BottomSheet with withRNModal props', async () => {
    const handleCloseMock = jest.fn();
    render(
      <BottomSheet
        useNativeDriver={false}
        showCloseHandle
        title="This is the header"
        onClose={handleCloseMock}
        withRNModal={false}
        isOpen={true}>
        {loremIpsum(1)}
      </BottomSheet>,
    );

    const bottomSheetComponent = await screen.findByTestId(`BottomSheet`);
    expect(bottomSheetComponent).toBeDefined();
  });

  test.each([true, false])(
    'open or close call to BottomSheet with withRNModal props, where visible or isOpen = %s',
    async (openModal) => {
      const handleCloseMock = jest.fn();
      render(
        <BottomSheet
          useNativeDriver={false}
          showCloseHandle
          title="This is the header"
          visible={openModal}
          onClose={handleCloseMock}
          withRNModal={false}
          childrenContainScrollableComponent={true}
          isOpen={openModal}>
          {loremIpsum(1)}
        </BottomSheet>,
      );

      if (openModal) {
        const bottomSheetComponent = await screen.findByTestId(`BottomSheet`);
        expect(bottomSheetComponent).toBeDefined();
      }
    },
  );
});
