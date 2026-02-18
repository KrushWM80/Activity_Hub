import React from 'react';
import {ViewStyle} from 'react-native';
import {BottomSheet, Button, ButtonGroup} from '@walmart/gtp-shared-components';
import {loremIpsum} from './screensFixtures';
import {Header, Section, Page, VariantText} from '../components';

export const BottomSheetWithCustomHeightContentRecipe: React.FC = () => {
  const handleModalOnOpen = () => {
    console.log('BottomSheet Open inprogress');
  };
  const handleModalOnOpened = () => {
    console.log('BottomSheet Open completed');
  };

  const BottomSheetWithText = ({height}: {height: number | string}) => {
    const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(false);
    const [modalActionPressed, setModalActionPressed] =
      React.useState<string>('');
    const handleModalOnClosed = () => {
      if (modalActionPressed !== '') {
        console.log(`Modal action '${modalActionPressed}' was tapped`);
      }
    };
    const openModal = () => {
      setModalIsOpen(true);
      setModalActionPressed('');
    };
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

    return (
      <>
        <Header>
          BottomSheet{'\n'}{' '}
          <VariantText>{`with UNSAFE_style={{height: ${height}}}`}</VariantText>
        </Header>
        <Section>
          <Button variant="primary" onPress={openModal}>
            Show
          </Button>
          <BottomSheet
            isOpen={modalIsOpen}
            onClose={handleModalOnClose}
            onOpen={handleModalOnOpen}
            UNSAFE_style={{height: height} as ViewStyle}
            onOpened={handleModalOnOpened}
            onClosed={handleModalOnClosed}
            onBackButtonPress={handleModalOnClose}
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
            {loremIpsum(10)}
          </BottomSheet>
        </Section>
      </>
    );
  };
  return (
    <Page>
      <BottomSheetWithText height={500} />
      <BottomSheetWithText height={'50%'} />
      <BottomSheetWithText height={'75%'} />
      <BottomSheetWithText height={250} />
    </Page>
  );
};

export default BottomSheetWithCustomHeightContentRecipe;
