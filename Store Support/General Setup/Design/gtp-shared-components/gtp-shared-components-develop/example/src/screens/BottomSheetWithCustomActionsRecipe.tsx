import React from 'react';
import {View, StyleSheet} from 'react-native';
import {
  BottomSheet,
  ButtonGroup,
  Button,
  Alert,
} from '@walmart/gtp-shared-components';
import {loremIpsum} from './screensFixtures';
import {Header, Section, Page, VariantText} from '../components';

export const BottomSheetWithCustomActionsRecipe: React.FC = () => {
  const handleModalOnOpen = () => {
    console.log('BottomSheet Open inprogress');
  };
  const handleModalOnOpened = () => {
    console.log('BottomSheet Open completed');
  };

  const BottomSheetWithText = () => {
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

    const handleModalContinue = () => {
      setModalActionPressed('Continue');
      setModalIsOpen(false);
    };

    return (
      <>
        <Header>
          BottomSheet{'\n'}{' '}
          <VariantText>{'with Custom action button'}</VariantText>
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
            title="Confirmation"
            actions={
              <View style={ss.actionsContainer}>
                <Button
                  isFullWidth={true}
                  onPress={handleModalContinue}
                  size={'medium'}
                  variant={'primary'}>
                  {'continue'}
                </Button>
              </View>
            }>
            {loremIpsum(1)}
          </BottomSheet>
        </Section>
      </>
    );
  };
  const BottomSheetWithAlertInActions = () => {
    const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(false);
    const [showAlert, setShowAlert] = React.useState<boolean>(false);
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

    const handleModalContinue = () => {
      setModalActionPressed('Continue');
      setModalIsOpen(false);
    };

    return (
      <>
        <Header>
          BottomSheet{'\n'}{' '}
          <VariantText>{'with Custom action button'}</VariantText>
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
            title="Confirmation"
            actions={
              <View style={ss.actionsContainer}>
                {showAlert && (
                  <Alert
                    variant={'info'}
                    children={'Reservation about to expire'}
                    UNSAFE_style={ss.alertStyle}
                  />
                )}
                <ButtonGroup>
                  <Button
                    onPress={() => setShowAlert(!showAlert)}
                    size={'medium'}
                    variant={'secondary'}>
                    {showAlert ? 'HideAlert' : 'ShowAlert'}
                  </Button>
                  <Button
                    onPress={handleModalContinue}
                    size={'medium'}
                    variant={'primary'}>
                    {'continue'}
                  </Button>
                </ButtonGroup>
              </View>
            }>
            {loremIpsum(1)}
          </BottomSheet>
        </Section>
      </>
    );
  };
  return (
    <Page>
      <BottomSheetWithText />
      <BottomSheetWithAlertInActions />
    </Page>
  );
};

const ss = StyleSheet.create({
  actionsContainer: {
    flexDirection: 'column',
    justifyContent: 'space-evenly',
    alignItems: 'flex-end',
    flex: 1,
  },
  alertStyle: {
    marginBottom: 12,
  },
});
export default BottomSheetWithCustomActionsRecipe;
