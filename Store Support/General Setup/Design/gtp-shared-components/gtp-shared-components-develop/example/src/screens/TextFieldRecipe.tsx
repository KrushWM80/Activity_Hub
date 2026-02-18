import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {
  Body,
  TextField,
  IconButton,
  Icons,
  colors,
  Link,
  useSimpleReducer,
  _KeyboardAvoidingView,
} from '@walmart/gtp-shared-components';
import {formatWithMask, Masks} from 'react-native-mask-input';
import {Page, Header, VariantText} from '../components';

type TextFieldsState = {
  hidePassword: boolean;
  showLink: boolean;
  searchValue: string;
  phoneNr: string;
  phoneNrUnmasked: number | null;
  phoneError: string;
  creditCardMasked: string;
  creditCardUnmasked: number | null;
  creditCardError: string;
  date: string;
  dateUnmasked: number | null;
  dateError: string;
  cardNumber: string;
};

const initialState = {
  hidePassword: true,
  showLink: true,
  searchValue: '',
  phoneNr: '',
  phoneNrUnmasked: null,
  phoneError: '',
  creditCardMasked: '',
  creditCardUnmasked: null,
  creditCardError: '',
  date: '',
  dateUnmasked: null,
  dateError: '',
  cardNumber: '',
};

const TextFieldRecipe = () => {
  const [state, setState] = useSimpleReducer<TextFieldsState>(initialState);

  const PHONE_MASK = [
    '(',
    /\d/,
    /\d/,
    /\d/,
    ')',
    ' ',
    /\d/,
    /\d/,
    /\d/,
    '-',
    /\d/,
    /\d/,
    /\d/,
    /\d/,
  ];

  const renderTFTelWithMask = () => (
    <>
      <Header>
        TextField{'\n  '}
        <VariantText>type="tel" with phone masking</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <TextField
            type="tel"
            label="Mobile phone"
            helperText="Enter phone number"
            leading={<Icons.PhoneIcon />}
            placeholder="(000) 000-0000"
            value={state.phoneNr as string}
            error={state.phoneError}
            maxLength={14}
            onChangeText={txt => {
              const {masked, unmasked} = formatWithMask({
                text: txt as string,
                mask: PHONE_MASK,
              });
              setState('phoneNr', masked);
              setState('phoneNrUnmasked', unmasked);
              if (txt === '') {
                setState('phoneError', '');
              } else if (!/^[0-9() -]+$/.test(txt as string)) {
                setState('phoneError', 'Invalid characters detected');
              } else {
                setState('phoneError', '');
              }
            }}
            onSubmitEditing={() =>
              console.log('TextField value captured:', state.phoneNrUnmasked)
            }
          />
        </View>
      </View>
    </>
  );

  const renderTFCreditCardWithMask = () => (
    <>
      <Header>
        TextField{'\n  '}
        <VariantText>type="number" with credit card masking</VariantText>
      </Header>
      <View style={ss.outerContainer}>
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
              console.log('TextField value captured:', state.creditCardUnmasked)
            }
          />
        </View>
      </View>
    </>
  );

  const renderDisbaledText = () => (
    <>
      <Header>
        TextField{'\n  '}
        <VariantText>type="text" with disabled</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
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
      </View>
    </>
  );

  const renderTFDateWithMask = () => (
    <>
      <Header>
        TextField{'\n  '}
        <VariantText>type="number" with date masking</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <TextField
            type="number"
            label="Date of birth"
            helperText="Enter your date of birth"
            leading={<Icons.CalendarIcon />}
            placeholder="00/00/0000"
            value={state.date as string}
            error={state.dateError}
            maxLength={10}
            onChangeText={txt => {
              const {masked, unmasked} = formatWithMask({
                text: txt as string,
                mask: Masks.DATE_DDMMYYYY,
              });

              setState('date', masked);
              setState('dateUnmasked', unmasked);
              if (txt === '') {
                setState('dateError', '');
              } else if (!/^[0-9/]+$/.test(txt as string)) {
                setState('dateError', 'Invalid characters detected');
              } else {
                setState('dateError', '');
              }
            }}
            onSubmitEditing={() =>
              console.log('TextField value captured:', state.dateUnmasked)
            }
          />
        </View>
      </View>
    </>
  );

  const renderTFPassword = () => (
    <>
      <Header>
        TextField{'\n  '}
        <VariantText>type="password" with show/hide IconButton</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <TextField
            type="password"
            label="Password"
            secureTextEntry={state.hidePassword as boolean}
            helperText=""
            placeholder="Enter your password"
            leading={<Icons.LockIcon />}
            trailing={
              <IconButton
                key="IconButton"
                size="medium"
                color={colors.gray['100']}
                onPress={() => setState('hidePassword', !state.hidePassword)}>
                {state.hidePassword ? (
                  <Icons.EyeIcon />
                ) : (
                  <Icons.EyeSlashIcon />
                )}
              </IconButton>
            }
            onSubmitEditing={event =>
              console.log('TextField value captured:', event.nativeEvent.text)
            }
          />
        </View>
      </View>
    </>
  );

  const renderTFPasswordWithLink = () => (
    <>
      <Header>
        TextField{'\n  '}
        <VariantText>type="password" with show/hide Link</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <TextField
            type="password"
            label="Password"
            secureTextEntry={state.showLink as boolean}
            helperText=""
            placeholder="Enter your password"
            leading={<Icons.LockIcon />}
            trailing={
              <Link
                UNSAFE_style={ss.trailingLink}
                onPress={() => setState('showLink', !state.showLink)}>
                {state.showLink ? 'Show' : 'Hide'}
              </Link>
            }
            onSubmitEditing={event =>
              console.log('TextField value captured:', event.nativeEvent.text)
            }
          />
        </View>
      </View>
    </>
  );

  const renderTFSearch = () => (
    <>
      <Header>
        TextField{'\n  '}
        <VariantText>type="search" with clear button</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <TextField
            type="search"
            label="Search daily deals"
            helperText="Find your deal"
            placeholder="Enter search term"
            leading={<Icons.SearchIcon />}
            value={state.searchValue as string}
            trailing={
              <IconButton
                key="IconButton"
                size="small"
                color={colors.gray['80']}
                onPress={() => {
                  setState('searchValue', '');
                }}>
                <Icons.CloseIcon />
              </IconButton>
            }
            onChangeText={txt => {
              setState('searchValue', txt as string);
            }}
            onSubmitEditing={event =>
              console.log('TextField value captured:', event.nativeEvent.text)
            }
          />
        </View>
      </View>
    </>
  );

  const renderTFwithMaxLength = () => (
    <>
      <Header>
        TextField{'\n  '}
        <VariantText> with maxLength</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <TextField
            label="CardNumber"
            helperText=""
            type="number"
            maxLength={19}
            placeholder="xxxx xxxx xxxx xxxx"
            leading={<Icons.CreditCardIcon />}
            value={state.cardNumber as string}
            onChangeText={txt => {
              let card = txt;
              if (
                card.length === 4 ||
                card.length === 9 ||
                card.length === 14
              ) {
                card = card + ' ';
              }
              setState('cardNumber', card as string);
            }}
            onSubmitEditing={event =>
              console.log('TextField value captured:', event.nativeEvent.text)
            }
          />
        </View>
      </View>
    </>
  );

  const TFControlledVsUncontrolled = () => {
    const [controlledValue, setControlledValue] = React.useState(
      'I am a controlled TextField',
    );
    const [uncontrolledValue, setUncontrolledValue] = React.useState('');
    return (
      <>
        <Header>
          TextField{'\n  '}
          <VariantText>controlled</VariantText>
        </Header>
        <View style={ss.outerContainer}>
          <View style={ss.innerContainer}>
            <TextField
              label="Controlled TextField"
              helperText="Use value prop and onChangeText prop"
              value={controlledValue}
              onChangeText={setControlledValue}
              placeholder="Placeholder text"
              leading={<Icons.EmailIcon />}
              trailing={<Icons.HomeIcon />}
              returnKeyType="done"
            />
            <Body>State Value: {controlledValue}</Body>
          </View>
        </View>
        <Header>
          TextField{'\n  '}
          <VariantText>uncontrolled</VariantText>
        </Header>
        <View style={ss.outerContainer}>
          <View style={ss.innerContainer}>
            <TextField
              label="Uncontrolled TextField"
              helperText="Init with defaultValue, capture with onSubmitEditing"
              defaultValue="I am an uncontrolled TextField"
              placeholder="Placeholder text"
              leading={<Icons.EmailIcon />}
              trailing={<Icons.HomeIcon />}
              returnKeyType="done"
              onSubmitEditing={event =>
                setUncontrolledValue(event.nativeEvent.text)
              }
            />
            <Body>State Value: {uncontrolledValue}</Body>
          </View>
        </View>
      </>
    );
  };

  return (
    <_KeyboardAvoidingView>
      <Page>
        {renderDisbaledText()}
        {renderTFDateWithMask()}
        {renderTFCreditCardWithMask()}
        {renderTFTelWithMask()}
        {renderTFPassword()}
        {renderTFPasswordWithLink()}
        {renderTFSearch()}
        {renderTFwithMaxLength()}
        <TFControlledVsUncontrolled />
      </Page>
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
  trailing: {},
  trailingLink: {
    marginRight: 12,
    marginVertical: 8,
  },
});

TextFieldRecipe.displayNameRecipe = 'TextFieldRecipe';
export {TextFieldRecipe};
