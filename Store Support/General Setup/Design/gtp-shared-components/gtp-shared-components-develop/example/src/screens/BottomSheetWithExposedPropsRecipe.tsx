import React from 'react';
import {BottomSheet, Button, ButtonGroup} from '@walmart/gtp-shared-components';
import {loremIpsum} from './screensFixtures';
import {Header, Section, VariantText} from '../components';

export const BottomSheetWithExposedPropsRecipe: React.FC = () => {
  const handleModalOnOpen = () => {
    console.log('BottomSheet Open inprogress');
  };
  const handleModalOnOpened = () => {
    console.log('BottomSheet Open completed');
  };

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
        BottomSheet{'\n'}
        <VariantText>{'with exposed Props'}</VariantText>
      </Header>
      <Section>
        <Button variant="primary" onPress={openModal}>
          Show
        </Button>
        <BottomSheet
          isOpen={modalIsOpen}
          onClose={handleModalOnClose}
          onOpen={handleModalOnOpen}
          onOpened={handleModalOnOpened}
          onClosed={handleModalOnClosed}
          onBackButtonPress={handleModalOnClose}
          animationInTiming={1}
          animationOutTiming={1}
          backdropTransitionInTiming={1}
          backdropTransitionOutTiming={1}
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

export default BottomSheetWithExposedPropsRecipe;
