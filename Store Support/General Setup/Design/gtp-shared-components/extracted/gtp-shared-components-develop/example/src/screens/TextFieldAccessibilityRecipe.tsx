import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {
  TextField,
  Icons,
  colors,
  useSimpleReducer,
  _KeyboardAvoidingView,
  TextFieldInputType,
  TextArea,
  Select,
} from '@walmart/gtp-shared-components';
import {formatWithMask, Masks} from 'react-native-mask-input';
import {Page, Header} from '../components';

type TextFieldsState = {
  creditCardMasked: string;
  creditCardUnmasked: number | null;
  creditCardError: string;
  cardNumber: string;
};

const initialState = {
  creditCardMasked: '',
  creditCardUnmasked: null,
  creditCardError: '',
  cardNumber: '',
};

const TextFieldAccessibilityRecipe = () => {
  const [state, setState] = useSimpleReducer<TextFieldsState>(initialState);

  const textFieldUI = (
    typeVal: string = 'number',
    label: string = 'Credit card number',
    helperText: string = 'Enter credit card number',
    icon?: string,
    placeholder?: string,
    error?: string,
  ) => {
    let iconEle = null;
    if (icon === 'person') {
      iconEle = <Icons.UserIcon />;
    } else if (icon === 'card') {
      iconEle = <Icons.CreditCardIcon />;
    } else if (icon === 'password') {
      iconEle = <Icons.LockIcon />;
    } else if (icon === ' ') {
      iconEle = <></>;
    } else {
      iconEle = <Icons.CreditCardIcon />;
    }
    return (
      <TextField
        type={typeVal as TextFieldInputType}
        label={label}
        helperText={helperText}
        leading={iconEle}
        placeholder={placeholder}
        error={error}
        UNSAFE_style={{marginHorizontal: 2}}
        maxLength={19}
      />
    );
  };

  const formsForAccessibility = () => {
    const selectOptions = [
      {text: 'Mug'},
      {text: 'Shirt'},
      {
        text: 'Sticker',
      },
      {text: 'Hat - not available', disabled: true},
      {text: 'Hoodie'},
    ];
    return (
      <>
        <Header>Form accessibility test</Header>
        <View style={ss.outerContainer}>
          <View style={[ss.innerContainer, {flexDirection: 'row', flex: 1}]}>
            {textFieldUI('text', 'FirstName', 'Enter first name', 'person')}
            {textFieldUI('text', 'LastName', 'Enter last name', 'person')}
          </View>
          <View style={[ss.innerContainer]}>
            <TextField
              disabled
              type="text"
              label="Date of birth"
              helperText="Enter your date of birth"
              leading={<Icons.CalendarIcon />}
              placeholder="00/00/0000"
              maxLength={10}
            />
          </View>
          <View style={[ss.innerContainer]}>
            {textFieldUI(
              'password',
              'Password',
              'Password helper text',
              'password',
            )}
          </View>
          <View style={ss.innerContainer}>
            <TextField
              type="number"
              label="Credit card number"
              helperText="Enter credit card number"
              leading={<Icons.CreditCardIcon />}
              placeholder="0000 0000 0000 0000"
              value={state.creditCardMasked as string}
              error={state.creditCardError}
              maxLength={19}
              onChangeText={txt => {
                const {masked, unmasked} = formatWithMask({
                  text: txt as string,
                  mask: Masks.CREDIT_CARD,
                });

                setState('creditCardMasked', masked);
                setState('creditCardUnmasked', unmasked);
                if (txt === '') {
                  setState('creditCardError', '');
                } else if (!/^[0-9() -#]+$/.test(txt as string)) {
                  setState('creditCardError', 'Invalid characters detected');
                } else {
                  setState('creditCardError', '');
                }
              }}
              onSubmitEditing={() =>
                console.log(
                  'TextField value captured:',
                  state.creditCardUnmasked,
                )
              }
            />
          </View>
          <View style={[ss.innerContainer]}>
            <TextArea
              label="Description"
              helperText="TextArea helper text"
              placeholder="Description here"
              onBlur={() => console.log('onBlur')}
              onSubmitEditing={event =>
                console.log('TextArea value captured:', event.nativeEvent.text)
              }
            />
          </View>

          <View
            style={[
              ss.innerContainer,
              {
                flexDirection: 'row',
                flex: 1,
                justifyContent: 'space-between',
                alignItems: 'flex-start',
              },
            ]}>
            <View
              style={{flex: 1, width: '50%', marginHorizontal: 2, zIndex: 10}}>
              <Select
                size="small"
                selectOptions={selectOptions}
                placeholder="Select"
                label="Swag"
                helperText="Swag helper text"
                onChange={() => console.log()}
              />
            </View>
            {textFieldUI('text', 'ZipCode', 'ZipCode helper text', ' ')}
          </View>

          <View
            style={[
              ss.innerContainer,
              {
                flexDirection: 'row',
                flex: 1,
                justifyContent: 'space-between',
                alignItems: 'flex-start',
              },
            ]}>
            <View
              style={{flex: 1, width: '50%', marginHorizontal: 2, zIndex: 10}}>
              <Select
                size="small"
                selectOptions={selectOptions}
                placeholder="Select"
                label="Swag"
                error="Select error text"
                helperText="Swag helper text"
                onChange={() => console.log()}
              />
            </View>
            {textFieldUI(
              'text',
              'ZipCode',
              'ZipCode helper text',
              '',
              '',
              'ZipCode error text',
            )}
          </View>
        </View>
      </>
    );
  };

  return (
    <_KeyboardAvoidingView>
      <Page>{formsForAccessibility()}</Page>
    </_KeyboardAvoidingView>
  );
};

const ss = StyleSheet.create({
  innerContainer: {
    flex: 1,
    justifyContent: 'space-around',
    flexDirection: 'column',
    padding: 10,
  },
  outerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
});

TextFieldAccessibilityRecipe.displayNameRecipe = 'TextFieldRecipe';
export {TextFieldAccessibilityRecipe};
