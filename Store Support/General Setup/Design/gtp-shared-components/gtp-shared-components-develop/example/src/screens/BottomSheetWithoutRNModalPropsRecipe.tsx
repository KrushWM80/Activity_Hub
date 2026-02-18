import React from 'react';
import {
  BottomSheet,
  Button,
  ButtonGroup,
  Select,
  SelectOptions,
  Selected,
} from '@walmart/gtp-shared-components';
import {loremIpsum} from './screensFixtures';
import {StyleSheet, View} from 'react-native';

export const BottomSheetWithoutRNModalPropsRecipe: React.FC = () => {
  const handleModalOnOpen = () => {
    console.log('BottomSheet Open inprogress');
  };
  const handleModalOnOpened = () => {
    console.log('BottomSheet Open completed');
  };

  const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(false);
  const [selectModalIsOpen, setSelectModalIsOpen] =
    React.useState<boolean>(false);
  const [modalActionPressed, setModalActionPressed] =
    React.useState<string>('');
  const handleModalOnClosed = () => {
    if (modalActionPressed !== '') {
      console.log(`Modal action '${modalActionPressed}' was tapped`);
    }
  };
  const selectOptions: SelectOptions = [
    {text: 'Mug'},
    {text: 'Shirt'},
    {
      text: 'Sticker',
    },
    {text: 'Hat - not available', disabled: true},
    {text: 'Hoodie'},
  ];
  const openModal = (whichModal = '') => {
    if (whichModal === 'selectModal') {
      setSelectModalIsOpen(true);
    } else {
      setModalIsOpen(true);
    }

    setModalActionPressed('');
  };
  const handleModalOnClose = () => {
    setModalIsOpen(false);
    setSelectModalIsOpen(false);
  };
  const handleModalCancel = () => {
    setModalActionPressed('Cancel');
    setModalIsOpen(false);
    setSelectModalIsOpen(false);
  };
  const handleModalContinue = () => {
    setModalActionPressed('Continue');
    setModalIsOpen(false);
    setSelectModalIsOpen(false);
  };

  const BottomSheetWithParagraph = () => {
    return (
      <>
        <BottomSheet
          withRNModal={false}
          useNativeDriver
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
          {loremIpsum(5)}
        </BottomSheet>
      </>
    );
  };

  const BottomSheetWithSelect = () => {
    const handleOnChange = (selected: Array<Selected>) => {
      console.log('---- Picked:', selected);
    };
    return (
      <BottomSheet
        withRNModal={false}
        useNativeDriver
        isOpen={selectModalIsOpen}
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
        <Select
          selectOptions={selectOptions}
          placeholder="Select your swag..."
          label="Swag"
          isInsideModal
          componentType={{ios: 'Overlay', android: 'Overlay'}}
          helperText="Helper text"
          onChange={handleOnChange}
        />
        <Select
          selectOptions={selectOptions}
          placeholder="Select your swag..."
          label="Swag"
          isInsideModal
          componentType={{ios: 'Overlay', android: 'Overlay'}}
          helperText="Helper text"
          onChange={handleOnChange}
        />
        <Select
          selectOptions={selectOptions}
          placeholder="Select your swag..."
          label="Swag"
          isInsideModal
          componentType={{ios: 'Overlay', android: 'Overlay'}}
          helperText="Helper text"
          onChange={handleOnChange}
        />
      </BottomSheet>
    );
  };

  return (
    <View style={style.recipeContainer}>
      <Button
        UNSAFE_style={style.btn}
        variant="primary"
        onPress={() => openModal('')}>
        BottomSheet with Paragraph
      </Button>
      <Button
        UNSAFE_style={style.btn}
        variant="primary"
        onPress={() => openModal('selectModal')}>
        BottomSheet with Select
      </Button>
      <View style={style.bottomSheetContainer}>
        <BottomSheetWithParagraph />
        <BottomSheetWithSelect />
      </View>
    </View>
  );
};

const style = StyleSheet.create({
  recipeContainer: {
    backgroundColor: 'lightgray',
    flex: 1,
    paddingTop: 10,
  },
  btn: {
    marginVertical: 10,
  },
  bottomSheetContainer: {
    flex: 1,
  },
});

export default BottomSheetWithoutRNModalPropsRecipe;
