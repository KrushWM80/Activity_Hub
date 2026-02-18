import * as React from 'react';
import {FlexStyle, TextStyle} from 'react-native';

import * as tokenButton from '@livingdesign/tokens/dist/react-native/light/regular/components/Button';
import * as tokenIconButton from '@livingdesign/tokens/dist/react-native/light/regular/components/IconButton';
import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Modal';
import {render, screen} from '@testing-library/react-native';

import {getFont, Weights} from '../../../theme/font';
import {loremIpsum} from '../../utils';
import {Button} from '../Button';
import {ButtonGroup} from '../ButtonGroup';
import {Modal, ModalSize} from '../Modal';

jest.useFakeTimers({legacyFakeTimers: true});

const TestApp = ({
  size,
  withRNModal = true,
  title,
}: {
  size: ModalSize;
  withRNModal?: boolean;
  title?: String;
}) => {
  const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(true);
  const [modalActionPressed, setModalActionPressed] =
    React.useState<string>('');
  const handleModalOnClose = () => {
    setModalIsOpen(false);
  };
  const handleModalCancel = () => {
    setModalActionPressed('Cancel');
    setModalIsOpen(false);
  };
  const handleModalContinue = () => {
    setModalActionPressed('Continue');
    setModalIsOpen(false);
  };
  const handleModalOnClosed = () => {
    if (modalActionPressed !== '') {
      return `Modal action '${modalActionPressed}' was tapped`;
    }
    return '';
  };
  return (
    <>
      <Modal
        size={size}
        isOpen={modalIsOpen}
        onClose={handleModalOnClose}
        onClosed={handleModalOnClosed}
        title={title}
        withRNModal={withRNModal}
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
        {loremIpsum(1)}
      </Modal>
    </>
  );
};

describe.each<ModalSize>(['small', 'medium', 'large'])(
  'Should render Modal with correct size, ',
  (size) => {
    test(`should render correctly for size='${size}`, () => {
      const rootQueries = render(
        <TestApp size={size} title={'Confirmation'} />,
      );

      // Modal
      const modal = rootQueries.getByTestId('Modal');
      const container = rootQueries.getByTestId('Modal-container');
      const title = rootQueries.getByTestId('Modal-title');
      const closeButton = rootQueries.getByTestId('Modal-close-button');
      const closeIcon = rootQueries.getByTestId('CloseIcon');
      const content = rootQueries.getByTestId('Modal-content');
      const actions = rootQueries.getByTestId('Modal-actions');
      const buttonGroup = rootQueries.getByTestId('ButtonGroup');

      expect(modal).toContainElement(container);
      expect(modal).toContainElement(title);
      expect(modal).toContainElement(closeButton);
      expect(modal).toContainElement(content);
      expect(modal).toContainElement(actions);
      expect(modal).toContainElement(closeIcon);
      expect(modal).toContainElement(buttonGroup);

      // Modal
      expect(modal.props.visible).toBeTruthy();
      expect(modal.props.hardwareAccelerated).toBeFalsy();
      expect(modal.props.transparent).toBeTruthy();
      expect(modal.props.animationType).toEqual('none');
      expect(modal.props.useNativeDriverForBackdrop).toBeTruthy();
      expect(modal.props.supportedOrientations).toEqual([
        'portrait',
        'portrait-upside-down',
        'landscape',
      ]);
      expect(modal.props.hideModalContentWhileAnimating).toBeTruthy();
      expect(modal.props.statusBarTranslucent).toBeTruthy();
      expect(modal.props.deviceHeight).toBeGreaterThan(0);
      expect(modal.props.deviceWidth).toEqual(null);
      expect(modal.props.panResponderThreshold).toEqual(4);
      expect(modal.props.swipeThreshold).toEqual(100);
      expect(modal.props.scrollTo).toEqual(null);
      expect(modal.props.scrollOffset).toEqual(0);
      expect(modal.props.scrollOffsetMax).toEqual(0);
      expect(modal.props.scrollHorizontal).toBeFalsy();

      // Container
      expect(container).toHaveStyle({
        marginHorizontal: 16,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: token.componentModalContainerBackgroundColor,
        borderRadius: token.componentModalContainerBorderRadius,
        height: 'auto',
        maxWidth:
          size === 'small'
            ? token.componentModalContainerSizeSmallMaxWidth
            : size === 'medium'
            ? token.componentModalContainerSizeMediumMaxWidth
            : token.componentModalContainerSizeLargeMaxWidth,
      });

      // Title
      expect(title).toHaveStyle({
        ...getFont(token.componentModalTitleFontWeight.toString() as Weights),
        fontSize: token.componentModalTitleFontSizeBM,
        lineHeight: token.componentModalTitleLineHeightBM,
      } as TextStyle);

      expect(title.children[0]).toEqual('Confirmation');

      // Close button
      expect(closeButton.props.accessibilityLabel).toEqual(
        `close Confirmation ${Modal.displayName}`,
      );
      expect(closeButton).toHaveStyle({
        justifyContent: 'center',
        alignItems: 'center',
        width: tokenIconButton.componentIconButtonContainerSizeSmallWidth,
        height: tokenIconButton.componentIconButtonContainerSizeSmallHeight,
        borderRadius:
          tokenIconButton.componentIconButtonContainerSizeSmallBorderRadius,
      });

      expect(closeIcon.props.source).toEqual({
        testUri:
          '../../@walmart/gtp-shared-icons/assets/images/icons/Close-16.png',
      });

      // Content
      expect(content).toHaveStyle({
        paddingHorizontal: token.componentModalContentPaddingHorizontalBM,
        paddingTop: 0,
      });

      const text = rootQueries.getByText(/Lorem ipsum/);
      expect(text).toHaveStyle({
        ...getFont(),
        lineHeight: 20,
      } as TextStyle);

      // Actions
      expect(actions).toHaveStyle([
        {
          width: '100%',
          flexDirection: 'row',
          padding: token.componentModalActionContentPaddingBM,
          justifyContent: 'flex-end',
          borderColor: token.componentModalActionContentBorderColorTop,
          borderBottomLeftRadius: token.componentModalContainerBorderRadius,
          borderBottomRightRadius: token.componentModalContainerBorderRadius,
        },
        {borderWidth: 1},
      ]);

      expect(buttonGroup).toHaveStyle({
        justifyContent: 'center',
        alignItems: 'center',
      });

      const buttonTitleCancel = rootQueries.getByText('Cancel');
      expect(buttonTitleCancel).toHaveStyle({
        ...getFont(),
        textAlign: 'center',
        textDecorationLine:
          tokenButton.componentButtonTextLabelVariantTertiaryTextDecorationDefault,
        fontSize: 14,
        lineHeight: 32,
        color:
          tokenButton.componentButtonTextLabelVariantTertiaryTextColorDefault,
        fontWeight:
          tokenButton.componentButtonTextLabelVariantTertiaryFontWeight.toString(),
      } as TextStyle);

      const buttonTitleContinue = rootQueries.getByText('Continue');
      expect(buttonTitleContinue).toHaveStyle({
        ...getFont('bold'),
        textAlign: 'center',
        fontSize: 14,
        lineHeight: 32,
        color:
          tokenButton.componentButtonTextLabelVariantPrimaryTextColorDefault,
        fontWeight:
          tokenButton.componentButtonTextLabelVariantPrimaryFontWeight.toString(),
      } as TextStyle);
    });
  },
);

describe('Should render Modal with withRNModal, ', () => {
  test(`Modal should render correctly`, () => {
    const rootQueries = render(<TestApp size={'medium'} withRNModal={false} />);

    // Modal
    const modal = rootQueries.getByTestId('Modal');
    const container = rootQueries.getByTestId('Modal-container');
    const title = rootQueries.getByTestId('Modal-title');
    const closeButton = rootQueries.getByTestId('Modal-close-button');
    const closeIcon = rootQueries.getByTestId('CloseIcon');
    const content = rootQueries.getByTestId('Modal-content');
    const actions = rootQueries.getByTestId('Modal-actions');
    const buttonGroup = rootQueries.getByTestId('ButtonGroup');

    expect(modal).toBeDefined();
    expect(modal).toContainElement(container);
    expect(modal).toContainElement(title);
    expect(modal).toContainElement(closeButton);
    expect(modal).toContainElement(content);
    expect(modal).toContainElement(actions);
    expect(modal).toContainElement(closeIcon);
    expect(modal).toContainElement(buttonGroup);

    // Container
    expect(container).toHaveStyle({
      marginHorizontal: 16,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: token.componentModalContainerBackgroundColor,
      borderRadius: token.componentModalContainerBorderRadius,
      height: 'auto',
      maxWidth: token.componentModalContainerSizeMediumMaxWidth,
    });

    // Title
    expect(title).toHaveStyle({
      ...getFont(token.componentModalTitleFontWeight.toString() as Weights),
      fontSize: token.componentModalTitleFontSizeBM,
      lineHeight: token.componentModalTitleLineHeightBM,
    } as TextStyle);

    expect(title.children[0]).toBeUndefined();
    expect(closeButton.props.accessibilityLabel).toEqual(
      `close  ${Modal.displayName}`,
    );
    // Close button
    expect(closeButton).toHaveStyle({
      justifyContent: 'center',
      alignItems: 'center',
      width: tokenIconButton.componentIconButtonContainerSizeSmallWidth,
      height: tokenIconButton.componentIconButtonContainerSizeSmallHeight,
      borderRadius:
        tokenIconButton.componentIconButtonContainerSizeSmallBorderRadius,
    });

    expect(closeIcon.props.source).toEqual({
      testUri:
        '../../@walmart/gtp-shared-icons/assets/images/icons/Close-16.png',
    });

    // Content
    expect(content).toHaveStyle({
      paddingHorizontal: token.componentModalContentPaddingHorizontalBM,
      paddingTop: 0,
    });

    const text = rootQueries.getByText(/Lorem ipsum/);
    expect(text).toHaveStyle({
      ...getFont(),
      lineHeight: 20,
    } as TextStyle);

    // Actions
    expect(actions).toHaveStyle([
      {
        width: '100%',
        flexDirection: 'row',
        padding: token.componentModalActionContentPaddingBM,
        justifyContent: 'flex-end',
        borderColor: token.componentModalActionContentBorderColorTop,
        borderBottomLeftRadius: token.componentModalContainerBorderRadius,
        borderBottomRightRadius: token.componentModalContainerBorderRadius,
      },
      {borderWidth: 1},
    ]);

    expect(buttonGroup).toHaveStyle({
      justifyContent: 'center',
      alignItems: 'center',
    });

    const buttonTitleCancel = rootQueries.getByText('Cancel');
    expect(buttonTitleCancel).toHaveStyle({
      ...getFont(),
      textAlign: 'center',
      textDecorationLine:
        tokenButton.componentButtonTextLabelVariantTertiaryTextDecorationDefault,
      fontSize: 14,
      lineHeight: 32,
      color:
        tokenButton.componentButtonTextLabelVariantTertiaryTextColorDefault,
      fontWeight:
        tokenButton.componentButtonTextLabelVariantTertiaryFontWeight.toString(),
    } as TextStyle);

    const buttonTitleContinue = rootQueries.getByText('Continue');
    expect(buttonTitleContinue).toHaveStyle({
      ...getFont('bold'),
      textAlign: 'center',
      fontSize: 14,
      lineHeight: 32,
      color: tokenButton.componentButtonTextLabelVariantPrimaryTextColorDefault,
      fontWeight:
        tokenButton.componentButtonTextLabelVariantPrimaryFontWeight.toString(),
    } as TextStyle);
  });
});

describe('Should render modal with props on/off', () => {
  test('modal with isSelectModal props', async () => {
    const mockfn = jest.fn();
    render(
      <Modal
        size={'medium'}
        isOpen={true}
        onClose={mockfn}
        onClosed={mockfn}
        title={'title'}
        isSelectModal={true}
        actions={
          <ButtonGroup>
            <Button variant="tertiary" onPress={mockfn}>
              Cancel
            </Button>
            <Button variant="primary" onPress={mockfn}>
              Continue
            </Button>
          </ButtonGroup>
        }>
        {loremIpsum(1)}
      </Modal>,
    );

    const modal = screen.getByTestId('Modal');
    expect(modal).toBeDefined();
    const container = screen.getByTestId('Modal-container');
    expect(container).toBeDefined();
    const titleContainer = screen.getByTestId('Modal-title-container');
    expect(titleContainer).toHaveStyle({
      width: '100%',
      flexDirection: 'row',
      justifyContent: token.componentModalHeaderAlignHorizontal as Extract<
        FlexStyle,
        'justifyContent'
      >,
      alignItems: 'flex-start',
      paddingLeft: token.componentModalHeaderPaddingStartBS,
      paddingRight: token.componentModalHeaderPaddingEndBS,
      paddingVertical: token.componentModalHeaderPaddingVerticalBS,
    } as TextStyle);

    const title = screen.findByTestId('Modal-title');
    expect(title).toBeDefined();

    const content = screen.findByTestId('Modal-content');
    expect(content).toBeDefined();

    const actions = screen.findByTestId('Modal-actions');
    expect(actions).toBeDefined();
  });
});
