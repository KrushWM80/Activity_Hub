import * as React from 'react';
import {Header, Page, Section} from '../components';
import {Button, Modal} from '@walmart/gtp-shared-components';
import {StyleSheet, View} from 'react-native';

export const ModalOverview: React.FC = () => {
  const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(false);
  const [isWithRNModal, setIsWithRNModal] = React.useState<boolean>(false);
  const [modalActionPressed, setModalActionPressed] =
    React.useState<string>('');

  const openModal = (withRNModal: boolean = false) => {
    setIsWithRNModal(withRNModal);
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

  const handleModalOnClosed = () => {
    if (modalActionPressed !== '') {
      console.log(`Modal action '${modalActionPressed}' was tapped`);
    }
  };
  const handleModalOnOpen = () => {
    console.log('Modal Open inprogress');
  };
  const handleModalOnOpened = () => {
    console.log('Modal Open completed');
  };
  // ---------------
  // Rendering
  // ---------------
  return (
    <Page>
      <Header>Modal</Header>
      <Section>
        <Button variant="primary" onPress={() => openModal(true)}>
          Show Modal
        </Button>
        <Button variant="primary" onPress={() => openModal()}>
          Show Modal with withRNModal=false
        </Button>
        <Modal
          isOpen={modalIsOpen}
          onOpen={handleModalOnOpen}
          onOpened={handleModalOnOpened}
          onClose={handleModalOnClose}
          onClosed={handleModalOnClosed}
          title="Confirmation"
          withRNModal={isWithRNModal}
          actions={
            <View style={ss.actionContainer}>
              <Button variant="tertiary" onPress={handleModalContinue}>
                Click here for terms & conditions
              </Button>
              <View style={ss.btnContaiiner}>
                <Button variant="tertiary" onPress={handleModalCancel}>
                  Cancel
                </Button>
                <Button variant="primary" onPress={handleModalContinue}>
                  Continue
                </Button>
              </View>
            </View>
          }>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
          minim veniam, quis nostrud exercitation ullamco laboris nisi ut
          aliquip ex ea commodo consequat.
        </Modal>
      </Section>
    </Page>
  );
};

const ss = StyleSheet.create({
  btnContaiiner: {
    flexDirection: 'row',
    justifyContent: 'space-evenly',
    alignItems: 'center',
    paddingTop: 14,
  },
  actionContainer: {
    flexDirection: 'column',
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
});
