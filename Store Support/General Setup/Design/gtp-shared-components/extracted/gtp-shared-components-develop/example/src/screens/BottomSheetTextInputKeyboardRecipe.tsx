import React from 'react';
import {Header, Section, VariantText} from '../components';
import {BottomSheet, Button, TextField} from '@walmart/gtp-shared-components';

export const BottomSheetTextInputKeyboardRecipe: React.FC = () => {
  const BottomSheetWithForm = ({
    keyboardShouldPersistTaps,
  }: {
    keyboardShouldPersistTaps: 'never' | 'always' | 'handled' | undefined;
  }) => {
    const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(false);
    const [modalActionPressed, setModalActionPressed] =
      React.useState<string>('');
    const handleModalOnClosed = () => {
      if (modalActionPressed !== '') {
        console.log(`Modal action '${modalActionPressed}' was tapped`);
      }
    };
    const [text, setText] = React.useState<string>('');
    const openModal = () => {
      setModalIsOpen(true);
      setModalActionPressed('');
    };
    const handleModalOnClose = () => {
      console.log('---- text entered:', text);

      setModalIsOpen(false);
    };
    const handleModalSubmit = () => {
      setModalActionPressed('Submit');
      setModalIsOpen(false);
    };

    return (
      <>
        <Header>
          BottomSheet with TextField{'\n'}{' '}
          <VariantText>
            keyboardShouldPersistTaps={keyboardShouldPersistTaps}
          </VariantText>
        </Header>
        <Section>
          <Button variant="primary" onPress={openModal}>
            Show
          </Button>
          <BottomSheet
            keyboardShouldPersistTaps={keyboardShouldPersistTaps}
            isOpen={modalIsOpen}
            onClose={handleModalOnClose}
            onClosed={handleModalOnClosed}
            onBackButtonPress={handleModalOnClose}
            title="Confirmation"
            actions={
              <Button
                variant="primary"
                isFullWidth={true}
                onPress={handleModalSubmit}>
                Submit
              </Button>
            }>
            <>
              <TextField
                label="This is the label"
                placeholder="Placeholder text"
                helperText="Helper text"
                onChangeText={value => setText(value)}
              />
            </>
          </BottomSheet>
        </Section>
      </>
    );
  };

  return (
    <Section>
      <BottomSheetWithForm keyboardShouldPersistTaps="never" />
      <BottomSheetWithForm keyboardShouldPersistTaps="always" />
      <BottomSheetWithForm keyboardShouldPersistTaps="handled" />
    </Section>
  );
};

export default BottomSheetTextInputKeyboardRecipe;
