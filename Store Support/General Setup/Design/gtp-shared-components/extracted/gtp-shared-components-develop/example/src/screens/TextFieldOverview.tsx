import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Page, Header, VariantText} from '../components';
import {
  TextField,
  colors,
  Icons,
  Checkbox,
  TextFieldRef,
  _KeyboardAvoidingView,
  Body,
} from '@walmart/gtp-shared-components';
import {useFocusEffect} from '@react-navigation/native';

const TextFieldOverview: React.FC = () => {
  const simpleTFRef = React.useRef<TextFieldRef | null>(null);
  const [disable, setDisable] = React.useState(false);
  useFocusEffect(
    React.useCallback(() => {
      if (simpleTFRef.current) {
        simpleTFRef.current.focus();
      }
    }, []),
  );

  const TFPhone = () => {
    const [error, setError] = React.useState<string>('');
    return (
      <>
        <Header>
          TextField <VariantText>type="tel" with error</VariantText>
        </Header>
        <View style={ss.outerContainer}>
          <View style={ss.innerContainer}>
            <TextField
              type="tel"
              label="Phone Number (required)"
              placeholder="(000) 000-0000"
              error={error}
              leading={<Icons.PhoneIcon />}
              trailing={<Icons.HomeIcon />}
              returnKeyType="done"
              onChangeText={txt => {
                if (txt === '') {
                  setError('');
                } else if (!/^[0-9.,]+$/.test(txt as string)) {
                  setError('Invalid characters detected');
                } else {
                  setError('');
                }
              }}
              onSubmitEditing={event => {
                if (error === '') {
                  console.log(
                    'TextField value captured:',
                    event.nativeEvent.text,
                  );
                }
              }}
            />
          </View>
        </View>
      </>
    );
  };

  const renderTFSimple = () => (
    <>
      <Header>
        TextField <VariantText>type="text"</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <TextField
            ref={simpleTFRef}
            label="Label text"
            helperText="Helper text"
            placeholder="Placeholder text"
            onBlur={() => console.log('onBlur')}
            leading={<Icons.EmailIcon />}
            trailing={<Icons.HomeIcon accessibilityLabel="Home" accessible />}
            returnKeyType="done"
            onSubmitEditing={event =>
              console.log('TextField value captured:', event.nativeEvent.text)
            }
          />
        </View>
      </View>
    </>
  );

  const renderTFSimpleLarge = () => (
    <>
      <Header>
        TextField <VariantText>type="text" size="large"</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <TextField
            size="large"
            label="Label text"
            helperText="Helper text"
            placeholder="Placeholder text"
            leading={<Icons.EmailIcon />}
            trailing={<Icons.HomeIcon />}
            returnKeyType="done"
            onSubmitEditing={event =>
              console.log('TextField value captured:', event.nativeEvent.text)
            }
          />
        </View>
      </View>
    </>
  );

  const TFNumber = () => {
    const [error, setError] = React.useState<string>('');
    return (
      <>
        <Header>
          TextField <VariantText>type="number" with error</VariantText>
        </Header>
        <View style={ss.outerContainer}>
          <View style={ss.innerContainer}>
            <TextField
              type="number"
              error={error}
              label="Quantity"
              helperText="Helper text"
              placeholder="Enter a number"
              leading={<Icons.KeyboardIcon />}
              returnKeyType="done"
              onChangeText={txt => {
                if (txt === '') {
                  setError('');
                } else if (!/^[0-9.,]+$/.test(txt as string)) {
                  setError('Invalid characters detected');
                } else {
                  setError('');
                }
              }}
              onSubmitEditing={event => {
                if (error === '') {
                  console.log(
                    'TextField value captured:',
                    event.nativeEvent.text,
                  );
                }
              }}
            />
          </View>
        </View>
      </>
    );
  };
  const TFEmailErrorSubmit = () => {
    const [error, setError] = React.useState<string>('');
    const [submittedText, setSubmittedText] = React.useState<string>('');
    return (
      <>
        <Header>
          TextField <VariantText>type="email" with error on submit</VariantText>
        </Header>
        <View style={ss.outerContainer}>
          <View style={ss.innerContainer}>
            <TextField
              type="email"
              returnKeyType="done"
              error={error}
              label="Email"
              helperText="Helper text"
              placeholder="Enter a email"
              leading={<Icons.KeyboardIcon />}
              onChange={() => setError('')}
              onSubmitEditing={event => {
                const txt = event.nativeEvent.text;
                if (txt === '') {
                  setError('');
                  setSubmittedText('');
                } else if (
                  // eslint-disable-next-line no-useless-escape
                  !/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w\w+)+$/.test(
                    txt as string,
                  )
                ) {
                  setError('Invalid email detected');
                  setSubmittedText('');
                } else {
                  setError('');
                  setSubmittedText(txt);
                }
                if (error === '') {
                  console.log(
                    'TextField value captured:',
                    event.nativeEvent.text,
                  );
                } else {
                  console.log('Error:', error);
                }
              }}
            />
          </View>
          <View style={ss.textSubmittedContainer}>
            <Body UNSAFE_style={ss.textSubmittedLabel}>Submitted:</Body>
            <Body UNSAFE_style={ss.textSubmittedLabel}>{submittedText}</Body>
          </View>
        </View>
      </>
    );
  };

  const TFCity = () => {
    const [error, setError] = React.useState<string>('');
    return (
      <>
        <Header>
          TextField <VariantText>type="text" with error</VariantText>
        </Header>
        <View style={ss.outerContainer}>
          <View style={ss.innerContainer}>
            <TextField
              error={error}
              label="City (required)"
              placeholder="Enter the capital of Tennessee"
              helperText="Enter the city name"
              leading={<Icons.LocationIcon />}
              autoCapitalize={'words'}
              returnKeyType="done"
              onChangeText={txt => {
                if (txt === '') {
                  setError(txt);
                } else if (txt === 'Nash') {
                  setError(
                    "This isn't a real city, it's from the 'Cloudy With A Chance of Meatballs' movie",
                  );
                } else if (
                  txt &&
                  !/Nashville\s*$/.test(txt as string) &&
                  (txt as string)?.length > 4
                ) {
                  setError('Invalid city');
                } else {
                  setError('');
                }
              }}
              onSubmitEditing={event => {
                if (error === '') {
                  console.log(
                    'TextField value captured:',
                    event.nativeEvent.text,
                  );
                }
              }}
            />
          </View>
        </View>
      </>
    );
  };

  const TFName = () => {
    const [error, setError] = React.useState<string>('');
    return (
      <>
        <Header>
          TextField <VariantText>type="text" with error</VariantText>
        </Header>
        <View style={ss.outerContainer}>
          <View style={ss.innerContainer}>
            <TextField
              error={error}
              label="Name (required)"
              placeholder="Enter first name"
              helperText={'Enter only valid characters [a-zA-Z -]'}
              leading={<Icons.AssociateIcon />}
              returnKeyType="done"
              onChangeText={txt => {
                if (txt === '') {
                  setError('');
                } else if (!/^[a-zA-Z -]+$/.test(txt as string)) {
                  setError('Invalid characters detected');
                } else {
                  setError('');
                }
              }}
              onSubmitEditing={event => {
                if (error === '') {
                  console.log(
                    'TextField value captured:',
                    event.nativeEvent.text,
                  );
                }
              }}
            />
          </View>
        </View>
      </>
    );
  };

  const renderTFDisabled = () => (
    <>
      <Header>
        TextField <VariantText>disabled</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <TextField
            disabled
            label="Label text"
            onChangeText={() => {}}
            helperText="Helper text"
            placeholder="Placeholder text"
            leading={<Icons.PhoneIcon />}
            trailing={<Icons.HomeIcon />}
          />
        </View>
      </View>
    </>
  );

  const renderTFDisabledWithText = () => {
    return (
      <>
        <Header>
          TextField <VariantText>disabled with text value</VariantText>
        </Header>

        <View style={ss.outerContainer}>
          <View style={ss.innerContainer}>
            <Checkbox
              label={'Disabled'}
              checked={disable}
              UNSAFE_style={ss.checkboxStyle}
              onPress={() => {
                setDisable(!disable);
              }}
            />
            <TextField
              disabled={disable}
              value="This is a disabled text field"
              label="Label text"
              onChangeText={() => {}}
              helperText="Helper text"
              placeholder="Placeholder text"
              leading={<Icons.PhoneIcon />}
              trailing={<Icons.HomeIcon />}
            />
          </View>
        </View>
      </>
    );
  };

  const renderTFReadOnly = () => (
    <>
      <Header>
        TextField <VariantText>readOnly</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <TextField
            readOnly
            value="4444 3333 2222 1111"
            label="Label text"
            onChangeText={() => {}}
            helperText="Helper text"
            placeholder="Placeholder text"
            leading={<Icons.CreditCardIcon />}
          />
        </View>
      </View>
    </>
  );

  return (
    <_KeyboardAvoidingView>
      <Page>
        <Header>
          See Recipes{'\n  '}{' '}
          <VariantText>for more advanced examples</VariantText>
        </Header>
        {renderTFSimple()}
        {renderTFSimpleLarge()}
        {renderTFDisabled()}
        {renderTFDisabledWithText()}
        {renderTFReadOnly()}
        <TFEmailErrorSubmit />
        <TFPhone />
        <TFCity />
        <TFName />
        <TFNumber />
      </Page>
    </_KeyboardAvoidingView>
  );
};

const ss = StyleSheet.create({
  innerContainer: {
    padding: 10,
  },
  textSubmittedContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'flex-start',
    paddingBottom: 10,
    paddingHorizontal: 10,
  },
  textSubmittedLabel: {
    marginLeft: 20,
  },
  outerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
  checkboxStyle: {marginVertical: 10},
});

TextFieldOverview.displayName = 'TextFieldOverview';
export {TextFieldOverview};
