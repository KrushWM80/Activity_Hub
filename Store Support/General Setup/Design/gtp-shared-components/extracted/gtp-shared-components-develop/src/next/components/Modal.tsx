import * as React from 'react';
import {
  Dimensions,
  FlexStyle,
  StyleProp,
  StyleSheet,
  Text,
  TextStyle,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Modal';
import {Icons} from '@walmart/gtp-shared-icons';
import RNModal from 'react-native-modal';

import {getFont, Weights} from '../../theme/font';
import type {
  CommonRNModalBaseProps,
  CommonViewProps,
} from '../types/ComponentTypes';
import {a11yRole, convertStringToMS} from '../utils';

import {_ModalContent} from './_ModalContent';
import {IconButton, IconButtonProps} from './IconButton';

// ---------------
// Props
// ---------------
export type ModalSize = 'auto' | 'small' | 'medium' | 'large';

export type ModalProps = CommonRNModalBaseProps &
  CommonViewProps & {
    /**
     * The content for the modal.
     */
    children: React.ReactNode;
    /**
     * The actions for the modal.
     * Typically a ButtonGroup
     */
    actions?: React.ReactNode;
    /**
     * The props spread to the modal's close button.
     */
    closeButtonProps?: IconButtonProps;
    /**
     * Whether the Modal is open
     * @default false
     */
    isOpen?: boolean;
    /**
     * The callback fired when the Modal open start.
     */
    onOpen?: () => void;
    /**
     * The callback fired when the Modal open completed.
     * This will be in use only with withRNModal=true props
     */
    onOpened?: () => void;
    /**
     * The callback fired when the Modal requests to close
     */
    onClose?: () => void;
    /**
     * The callback fired when the Modal transition has ended.
     * This will be in use only with withRNModal=true props
     */
    onClosed?: () => void;
    /**
     * The size of the Modal
     * Valid values: "auto" | "small" | "medium" | "large"
     * @default auto
     */
    size?: ModalSize;
    /**
     * The title for the Modal
     * Typically a <Text></Text>
     */
    title: React.ReactNode;
    /**
     * If provided, the `style` to provide to the Modal container element.
     * @note This property is prefixed with `UNSAFE` as its use
     * often results in unintended side effects.
     */
    UNSAFE_style?: StyleProp<ViewStyle>;
    /**
     * Indicates whether the component will be wrapped with RN Modal. Setting to false means
     * the application consumer is responsible for presentation, such as displaying above other
     * screen components, opening, and dismissing the Modal.
     * (see https://jira.walmart.com/browse/CEEMP-3502)
     * @default true
     */
    withRNModal?: boolean;
    //******************** NON LD PROPS *****************//
    /**
     * To hide the X (close IconButton)
     * @default false
     */
    hideCloseIcon?: boolean;
    /**
     * @internal
     * To satisfy the Select Component Modal style
     * when we use modal type options inside Select component
     * @default false
     */
    isSelectModal?: boolean;
  };

/**
 * Modals focus the user’s attention on a single task in
 * a window that sits on top of the page content.
 *
 * ## Usage
 * ```js
 * import {Button, ButtonGroup, Modal} from '@walmart/gtp-shared-components`;
 *
 * const [modalIsOpen, setModalIsOpen] = React.useState(false);
 *
 * <Modal
 *   isOpen={modalIsOpen}
 *   onOpen={() => setModalIsOpen(true)}
 *   onClose={() => setModalIsOpen(false)}
 *   title="Confirmation"
 *   actions={
 *     <ButtonGroup>
 *       <Button variant="tertiary" onPress={() => setModalIsOpen(false)}>
 *         Cancel
 *       </Button>
 *       <Button variant="primary" onPress={() => setModalIsOpen(false)}>
 *         Continue
 *       </Button>
 *     </ButtonGroup>
 *   }>
 *   Lorem ipsum
 * </Modal>
 * ```
 */
const Modal: React.FC<ModalProps> = (props) => {
  const {
    children,
    actions,
    closeButtonProps,
    isOpen = false,
    onOpen,
    onOpened,
    onClose,
    onClosed,
    size = 'auto',
    title,
    UNSAFE_style,
    withRNModal = true,
    //non LD Props
    hideCloseIcon = false,
    isSelectModal = false,
    ...rest
  } = props;

  const {height: screenHeight, width: screenWidth} = Dimensions.get('screen');
  const closeModal = async () => {
    onClose?.();
  };
  const openingModal = async () => {
    onOpen?.();
  };
  const openModalCompleted = async () => {
    onOpened?.();
  };
  // iOS only
  const afterCloseModal = () => {
    onClosed?.();
  };

  // ---------------
  // Rendering
  // ---------------
  // These will only be relevant when running on a tablet
  const containerMaxWidth = () => {
    let maxWidth: number = token.componentModalContainerSizeLargeMaxWidth;
    if (size === 'auto') {
      maxWidth = screenWidth;
    } else if (size === 'small') {
      maxWidth = token.componentModalContainerSizeSmallMaxWidth;
    } else if (size === 'medium') {
      maxWidth = token.componentModalContainerSizeMediumMaxWidth;
    }
    return {maxWidth: maxWidth};
  };

  const restSpread = () => {
    if (rest) {
      return {...rest};
    }
  };
  //animationInTiming
  const animationInTiming = convertStringToMS(
    token.componentModalContainerStateEnterActiveTransformTransitionTransitionDuration,
  );
  //backdropTransitionInTiming
  const backdropTransitionInTiming = convertStringToMS(
    token.componentModalScrimStateEnterActiveTransitionDuration,
  );
  //animationOutTiming
  const animationOutTiming =
    convertStringToMS(
      token.componentModalContainerStateExitActiveTransitionDuration,
    ) - 250; //to avoid freezing ui after closing Modal

  const closeIconAccessibilityLabel = title
    ? `close ${title} ${Modal.displayName}`
    : `close  ${Modal.displayName}`;

  const renderContent = () => {
    return (
      <View
        testID={Modal.displayName + '-container'}
        style={[
          ss(isSelectModal).container,
          {...containerMaxWidth()},
          UNSAFE_style,
        ]}>
        <View
          testID={Modal.displayName + '-title-container'}
          style={ss(isSelectModal).header}>
          <Text
            accessibilityRole={a11yRole('header')}
            testID={Modal.displayName + '-title'}
            style={ss(isSelectModal).title}>
            {title}
          </Text>
          {!hideCloseIcon && (
            <IconButton
              testID={Modal.displayName + '-close-button'}
              size="small"
              accessibilityRole={a11yRole('button')}
              accessibilityLabel={closeIconAccessibilityLabel}
              onPress={closeModal}
              {...closeButtonProps}>
              <Icons.CloseIcon />
            </IconButton>
          )}
        </View>
        <_ModalContent
          keyboardShouldPersistTaps="always"
          componentName={Modal.displayName}
          actions={actions}
          isSelectModal={isSelectModal}
          contentExtraStyle={ss(isSelectModal).content}
          actionsExtraStyle={ss(isSelectModal).actions}>
          {children}
        </_ModalContent>
      </View>
    );
  };

  return !withRNModal && isOpen ? (
    <View
      style={ss(isSelectModal).containerWithoutRNModal}
      testID={Modal.displayName}>
      {renderContent()}
    </View>
  ) : (
    <RNModal
      accessibilityViewIsModal
      accessibilityState={{expanded: isOpen}}
      testID={Modal.displayName}
      isVisible={isOpen}
      deviceHeight={screenHeight}
      onModalShow={openModalCompleted}
      onModalWillShow={openingModal}
      onModalWillHide={closeModal}
      onModalHide={afterCloseModal}
      onBackButtonPress={closeModal}
      animationIn="fadeIn"
      animationInTiming={animationInTiming}
      animationOut="fadeOut"
      animationOutTiming={animationOutTiming}
      backdropTransitionInTiming={backdropTransitionInTiming}
      backdropTransitionOutTiming={animationOutTiming}
      hasBackdrop
      backdropColor={token.componentModalScrimBackgroundColor}
      backdropOpacity={token.componentModalScrimStateEnterActiveOpacity}
      onBackdropPress={closeModal}
      useNativeDriver
      useNativeDriverForBackdrop
      supportedOrientations={['portrait', 'portrait-upside-down', 'landscape']}
      hideModalContentWhileAnimating
      statusBarTranslucent={true} // Android
      {...restSpread()}>
      {renderContent()}
    </RNModal>
  );
};

// ---------------
// Styles
// ---------------
const ss = (isSelectModal: boolean) => {
  const headerPadding = isSelectModal
    ? token.componentModalHeaderPaddingVerticalBS
    : token.componentModalHeaderPaddingVerticalBM;
  return StyleSheet.create({
    container: {
      marginHorizontal: 16,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: token.componentModalContainerBackgroundColor,
      borderRadius: token.componentModalContainerBorderRadius,
      height: 'auto',
    },
    header: {
      width: '100%',
      flexDirection: 'row',
      justifyContent: token.componentModalHeaderAlignHorizontal as Extract<
        FlexStyle,
        'justifyContent'
      >,
      alignItems: 'flex-start',
      paddingLeft: isSelectModal
        ? token.componentModalHeaderPaddingStartBS
        : token.componentModalHeaderPaddingStartBM,
      paddingRight: isSelectModal
        ? token.componentModalHeaderPaddingEndBS
        : token.componentModalHeaderPaddingEndBM,
      paddingVertical: headerPadding,
    },
    title: {
      ...getFont(token.componentModalTitleFontWeight.toString() as Weights),
      fontSize: isSelectModal
        ? token.componentModalTitleFontSizeBS
        : token.componentModalTitleFontSizeBM,
      lineHeight: isSelectModal
        ? token.componentModalTitleLineHeightBS
        : token.componentModalTitleLineHeightBM,
      flexShrink: 1,
      color: token.componentModalTitleTextColor,
    } as TextStyle,
    content: {
      paddingHorizontal: isSelectModal
        ? token.componentModalContentPaddingHorizontalBS
        : token.componentModalContentPaddingHorizontalBM,
      paddingTop: 0,
      marginBottom: -8,
    },
    actions: {
      padding: isSelectModal
        ? token.componentModalActionContentPaddingBS
        : token.componentModalActionContentPaddingBM,
      borderColor: token.componentModalActionContentBorderColorTop,
      borderBottomLeftRadius: token.componentModalContainerBorderRadius,
      borderBottomRightRadius: token.componentModalContainerBorderRadius,
      borderWidth: 1,
    },
    containerWithoutRNModal: {
      flex: 1,
    },
  });
};
Modal.displayName = 'Modal';
export {Modal};
