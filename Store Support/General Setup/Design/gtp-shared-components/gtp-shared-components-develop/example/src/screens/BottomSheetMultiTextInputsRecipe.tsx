import React, {useState, SetStateAction} from 'react';
import {View} from 'react-native';
import {Section} from '../components';
import {
  BottomSheet,
  Button,
  ButtonGroup,
  TextField,
  TextArea,
} from '@walmart/gtp-shared-components';

export const BottomSheetMultiTextInputsRecipe: React.FC = () => {
  const [textValue, setTextValue] = useState({
    name: '',
    add1: '',
    add2: '',
    email1: '',
    email2: '',
    phone1: '',
    phone2: '',
    age: '',
    dob: '',
  });
  const [openModal, setOpenModal] = useState(false);
  const onTextChange = (key: string, value: SetStateAction<string>) => {
    setTextValue({...textValue, [key]: value});
  };
  return (
    <Section>
      <Button variant="primary" onPress={() => setOpenModal(true)}>
        Show
      </Button>
      <BottomSheet
        isOpen={openModal}
        onClose={() => setOpenModal(false)}
        onClosed={() => setOpenModal(false)}
        onBackButtonPress={() => setOpenModal(false)}
        keyboardShouldPersistTaps="never"
        onResize={height => console.log('BottomSheet onResize:', height)}
        actions={
          <ButtonGroup>
            <Button variant="tertiary" onPress={() => setOpenModal(false)}>
              Cancel
            </Button>
            <Button variant="primary" onPress={() => setOpenModal(false)}>
              Continue
            </Button>
          </ButtonGroup>
        }
        title="Edit On Hands">
        <View>
          <TextField
            label={'Enter your Name:'}
            value={textValue.name}
            onChangeText={val => onTextChange('name', val)}
          />
          <TextField
            label={'Enter your Add 1:'}
            value={textValue.add1}
            onChangeText={val => onTextChange('add1', val)}
          />
          <TextField
            label={'Enter your Add 2:'}
            value={textValue.add2}
            onChangeText={val => onTextChange('add2', val)}
          />
          <TextField
            label={'Enter your Email 1:'}
            value={textValue.email1}
            onChangeText={val => onTextChange('email1', val)}
          />
          <TextField
            label={'Enter your Email 2:'}
            value={textValue.email2}
            onChangeText={val => onTextChange('email2', val)}
          />
          <TextField
            label={'Enter your Ph 1:'}
            value={textValue.phone1}
            onChangeText={val => onTextChange('phone1', val)}
          />
          <TextField
            label={'Enter your Ph 2:'}
            value={textValue.phone2}
            onChangeText={val => onTextChange('phone2', val)}
          />
          <TextField
            label={'Enter your Age:'}
            value={textValue.age}
            onChangeText={val => onTextChange('age', val)}
          />
          <TextField
            label={'Enter your DOB:'}
            value={textValue.dob}
            onChangeText={val => onTextChange('dob', val)}
          />
          <TextArea
            label="Enter your Biography"
            placeholder="Placeholder text"
            maxLength={140}
            onSubmitEditing={event =>
              console.log('TextArea value captured:', event.nativeEvent.text)
            }
          />
        </View>
      </BottomSheet>
    </Section>
  );
};

export default BottomSheetMultiTextInputsRecipe;
