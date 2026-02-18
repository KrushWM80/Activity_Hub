import * as React from 'react';
import {Image, SafeAreaView, StyleSheet, Text} from 'react-native';
import {
  colors,
  Modal,
  Button,
  ButtonGroup,
  useSimpleReducer,
} from '@walmart/gtp-shared-components';
import {Header, Page, Section} from '../components';

type MenuOpenState = {
  singleButtonModalOpen: boolean;
  twoButtonModalOpen: boolean;
  threeButtonModalOpen: boolean;
  consumerSampleModalOpen: boolean;
  extraPropsModalOpen: boolean;
};
const initialState = {
  singleButtonModalOpen: false,
  twoButtonModalOpen: false,
  threeButtonModalOpen: false,
  consumerSampleModalOpen: false,
  extraPropsModalOpen: false,
};
const ModalRecipes: React.FC = () => {
  const [state, setState] = useSimpleReducer<MenuOpenState>(initialState);
  const [modalActionPressed, setModalActionPressed] =
    React.useState<string>('');

  const openModal = (type: string) => {
    setState(type, !state[type]);
    setModalActionPressed('');
  };

  const handleModalOnClose = (type: string) => {
    setState(type, false);
  };

  const handleModalCancel = (type: string) => {
    setModalActionPressed('Cancel');
    setState(type, false);
  };

  const handleModalContinue = (type: string) => {
    setModalActionPressed('Continue');
    setState(type, false);
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

  const [withRNModalOpen, setWithRNModalOpen] = React.useState(false);
  return (
    <SafeAreaView style={ss.container}>
      <Page>
        <Header>Modal</Header>
        <Section>
          <Button
            variant="primary"
            onPress={() => {
              setWithRNModalOpen(true);
              console.log('Opening modal....');
            }}>
            Show Modal withRNModal=false
          </Button>

          <Modal
            isOpen={withRNModalOpen}
            onOpen={handleModalOnOpen}
            onOpened={() => {
              handleModalOnOpened();
            }}
            onClose={() => {
              setWithRNModalOpen(false);
              console.log('Closed using Close icon button..');
            }}
            title={'Confirmation'}
            withRNModal={false}
            actions={
              <ButtonGroup>
                <Button
                  variant="tertiary"
                  onPress={() => {
                    setWithRNModalOpen(false);
                    console.log('Closed using Cancel button..');
                  }}>
                  Cancel
                </Button>
                <Button
                  variant="primary"
                  onPress={() => {
                    setWithRNModalOpen(false);
                    console.log('Closed using Continue button..');
                  }}>
                  Continue
                </Button>
              </ButtonGroup>
            }>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
            ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
            aliquip ex ea commodo consequat.
          </Modal>

          <Button
            variant="primary"
            onPress={() => openModal('singleButtonModalOpen')}>
            Modal with image
          </Button>
          <Modal
            isOpen={state.singleButtonModalOpen as boolean}
            onOpen={handleModalOnOpen}
            onOpened={handleModalOnOpened}
            onClose={() => handleModalOnClose('singleButtonModalOpen')}
            onClosed={handleModalOnClosed}
            title="Confirmation">
            <>
              <Image
                source={require('../assets/index').battery}
                style={ss.image}
              />
              <Text>Some text here.</Text>
            </>
          </Modal>
          <Button
            variant="primary"
            onPress={() => openModal('singleButtonModalOpen')}>
            Show Single Button Modal
          </Button>
          <Modal
            isOpen={state.singleButtonModalOpen as boolean}
            onOpen={handleModalOnOpen}
            onOpened={handleModalOnOpened}
            onClose={() => handleModalOnClose('singleButtonModalOpen')}
            onClosed={handleModalOnClosed}
            title="Confirmation"
            actions={
              <Button
                variant="primary"
                onPress={() => handleModalContinue('singleButtonModalOpen')}>
                Continue
              </Button>
            }>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
            ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
            aliquip ex ea commodo consequat.
          </Modal>
          <Button
            variant="primary"
            onPress={() => openModal('twoButtonModalOpen')}>
            Show Modal with Two actions
          </Button>
          <Modal
            isOpen={state.twoButtonModalOpen as boolean}
            onOpen={handleModalOnOpen}
            onOpened={handleModalOnOpened}
            onClose={() => handleModalOnClose('twoButtonModalOpen')}
            onClosed={handleModalOnClosed}
            title="Confirmation"
            actions={
              <ButtonGroup>
                <Button
                  variant="tertiary"
                  onPress={() => handleModalCancel('twoButtonModalOpen')}>
                  Cancel
                </Button>
                <Button
                  variant="primary"
                  onPress={() => handleModalContinue('twoButtonModalOpen')}>
                  Continue
                </Button>
              </ButtonGroup>
            }>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
            ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
            aliquip ex ea commodo consequat.
          </Modal>

          <Button
            variant="primary"
            onPress={() => openModal('threeButtonModalOpen')}>
            Show threeButton Modal
          </Button>
          <Modal
            isOpen={state.threeButtonModalOpen as boolean}
            onOpen={handleModalOnOpen}
            onOpened={handleModalOnOpened}
            onClose={() => handleModalOnClose('threeButtonModalOpen')}
            onClosed={handleModalOnClosed}
            title="Confirmation"
            actions={
              <ButtonGroup>
                <Button
                  variant="tertiary"
                  onPress={() => handleModalCancel('threeButtonModalOpen')}>
                  Click here for terms & conditions
                </Button>
                <Button
                  variant="tertiary"
                  onPress={() => handleModalCancel('threeButtonModalOpen')}>
                  Cancel
                </Button>
                <Button
                  variant="primary"
                  onPress={() => handleModalContinue('threeButtonModalOpen')}>
                  Continue
                </Button>
              </ButtonGroup>
            }>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
            ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
            aliquip ex ea commodo consequat.
          </Modal>
          <Button
            variant="primary"
            onPress={() => openModal('consumerSampleModalOpen')}>
            Consumer Sample
          </Button>
          <Modal
            isOpen={state.consumerSampleModalOpen as boolean}
            onOpen={handleModalOnOpen}
            onOpened={handleModalOnOpened}
            onClose={() => handleModalOnClose('consumerSampleModalOpen')}
            onClosed={handleModalOnClosed}
            title="Confirmation"
            actions={
              <ButtonGroup>
                <Button
                  variant="tertiary"
                  onPress={() => handleModalCancel('consumerSampleModalOpen')}>
                  Cancel
                </Button>
                <Button
                  variant="destructive"
                  onPress={() =>
                    handleModalContinue('consumerSampleModalOpen')
                  }>
                  yes delete 1 message
                </Button>
              </ButtonGroup>
            }>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
            ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
            aliquip ex ea commodo consequat.
          </Modal>
          <Button
            variant="primary"
            onPress={() => openModal('extraPropsModalOpen')}>
            Consumer Sample with animation props
          </Button>
          <Modal
            isOpen={state.extraPropsModalOpen as boolean}
            onOpen={handleModalOnOpen}
            onOpened={handleModalOnOpened}
            onClose={() => handleModalOnClose('extraPropsModalOpen')}
            onClosed={handleModalOnClosed}
            backdropColor="#B4B3DB"
            backdropOpacity={0.8}
            animationInTiming={600}
            animationOutTiming={600}
            backdropTransitionInTiming={600}
            backdropTransitionOutTiming={600}
            title="Confirmation"
            actions={
              <ButtonGroup>
                <Button
                  variant="tertiary"
                  onPress={() => handleModalCancel('extraPropsModalOpen')}>
                  Cancel
                </Button>
                <Button
                  variant="destructive"
                  onPress={() => handleModalContinue('extraPropsModalOpen')}>
                  yes delete 1 message
                </Button>
              </ButtonGroup>
            }>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
            ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
            aliquip ex ea commodo consequat.
          </Modal>
        </Section>
      </Page>
    </SafeAreaView>
  );
};

const ss = StyleSheet.create({
  container: {
    flex: 1,
    paddingBottom: 18,
  },

  innerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
  spacer: {
    height: 8,
  },
  image: {
    width: 300,
    height: 300,
  },
});

export {ModalRecipes};
