import * as React from 'react';
import {SafeAreaView, StyleSheet, View, TextStyle, Text} from 'react-native';
import {
  colors,
  Modal,
  Button,
  ButtonGroup,
  Checkbox,
  getFont,
  TextField,
  ModalSize,
  TextArea,
} from '@walmart/gtp-shared-components';
import {Header, Page, RadioGroup, Section} from '../components';

const Spacer = () => <View style={ss.spacer} />;

type ModalProps = {
  title: React.ReactNode;
  children: React.ReactNode;
  actions?: boolean;
  size?: ModalSize;
  hideCloseIcon?: boolean;
  isSelectModal?: boolean;
  withRNModal?: boolean;
};

const modalSizeVariant = ['auto', 'small', 'medium', 'large'];
const modalBodyInitContent = `Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
minim veniam, quis nostrud exercitation ullamco laboris nisi ut
aliquip ex ea commodo consequat.`;

const ModalPlayground: React.FC = () => {
  const [modalTitleLabel, setModalTitleLabel] =
    React.useState<string>('Confirmation');
  const [modalChildLabel, setModalChildLabel] =
    React.useState<string>(modalBodyInitContent);

  const [traits, setTraits] = React.useState<ModalProps>({
    title: modalTitleLabel,
    children: modalChildLabel,
    actions: true,
    size: modalSizeVariant[0] as ModalSize,
    hideCloseIcon: false,
    isSelectModal: false,
    withRNModal: true,
  });

  const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(false);
  const [modalActionPressed, setModalActionPressed] =
    React.useState<string>('');

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
  const actionHandler = () => {
    setTraits({
      ...traits,
      actions: !traits.actions,
    });
  };

  const modalsContainer = () => (
    <>
      <Header>Modal</Header>
      <Section>
        <Button variant="primary" onPress={openModal}>
          Show Modal
        </Button>
        <Modal
          isOpen={modalIsOpen}
          onOpen={handleModalOnOpen}
          onOpened={handleModalOnOpened}
          onClose={handleModalOnClose}
          onClosed={handleModalOnClosed}
          hideCloseIcon={traits.hideCloseIcon}
          isSelectModal={traits.isSelectModal}
          title={modalTitleLabel}
          size={traits.size}
          withRNModal={traits.withRNModal}
          actions={
            traits.actions ? (
              <ButtonGroup>
                <Button variant="tertiary" onPress={handleModalCancel}>
                  Cancel
                </Button>
                <Button variant="primary" onPress={handleModalContinue}>
                  Continue
                </Button>
              </ButtonGroup>
            ) : null
          }>
          {`${modalChildLabel}`}
        </Modal>
      </Section>
    </>
  );

  return (
    <SafeAreaView style={ss.container}>
      <Page>
        {modalsContainer()}
        <View style={ss.header}>
          <Text style={ss.headerText}>Modal traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Spacer />
          <Text style={ss.radioHeaderText}>size</Text>
          <RadioGroup
            category="size"
            list={modalSizeVariant}
            selected="auto"
            onChange={(_, sel) => setTraits({...traits, size: sel})}
          />
          <Spacer />
          <Checkbox
            label="actions"
            checked={!!traits.actions}
            onPress={() => actionHandler()}
          />
          <Spacer />
          <Checkbox
            label="isSelectModal"
            checked={!!traits.isSelectModal}
            onPress={() =>
              setTraits({
                ...traits,
                isSelectModal: !traits.isSelectModal,
              })
            }
          />

          <Spacer />
          <Checkbox
            label="hideCloseIcon"
            checked={!!traits.hideCloseIcon}
            onPress={() =>
              setTraits({
                ...traits,
                hideCloseIcon: !traits.hideCloseIcon,
              })
            }
          />
          <Spacer />
          <Checkbox
            label="withRNModal"
            checked={!!traits.withRNModal}
            onPress={() =>
              setTraits({
                ...traits,
                withRNModal: !traits.withRNModal,
              })
            }
          />

          <Spacer />
          <Text style={ss.radioHeaderText}>title</Text>
          <TextField
            label={'(as text)'}
            size="small"
            value={modalTitleLabel}
            onChangeText={_text => {
              setModalTitleLabel(_text);
            }}
          />
          <Text style={ss.radioHeaderText}>children</Text>
          <TextArea
            label={'(as text)'}
            value={modalChildLabel}
            onChangeText={_text => {
              setModalChildLabel(_text);
            }}
          />
        </View>
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
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.blue['90'],
    borderTopColor: colors.blue['90'],
    borderBottomColor: colors.blue['90'],
    borderLeftColor: colors.blue['90'],
    borderRightColor: colors.blue['90'],
    paddingHorizontal: 8,
    paddingBottom: 8,
  },
  spacer: {
    height: 8,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderTopWidth: 1,
    borderLeftWidth: 1,
    borderRightWidth: 1,
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
    borderTopColor: colors.blue['90'],
    borderLeftColor: colors.blue['90'],
    borderRightColor: colors.blue['90'],
    paddingRight: 16,
    paddingVertical: 8,
    marginTop: 8,
  },
  headerText: {
    fontSize: 20,
    fontWeight: '500',
    color: colors.blue['90'],
    textAlign: 'left',
    paddingVertical: 4,
    marginLeft: 12,
  },
  radioHeaderText: {
    ...getFont('500'),
    lineHeight: 28,
    fontSize: 20,
    color: colors.blue['90'],
  } as TextStyle,
});

export {ModalPlayground};
