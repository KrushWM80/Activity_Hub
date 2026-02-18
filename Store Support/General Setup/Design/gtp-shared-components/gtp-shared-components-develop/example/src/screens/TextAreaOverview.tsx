import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Page, Header, VariantText} from '../components';
import {
  TextArea,
  colors,
  Checkbox,
  TextAreaRef,
  _KeyboardAvoidingView,
  Body,
} from '@walmart/gtp-shared-components';
import {useFocusEffect} from '@react-navigation/native';

const TextAreaOverview: React.FC = () => {
  const simpleTFRef = React.useRef<TextAreaRef | null>(null);
  const [disable, setDisable] = React.useState(false);
  useFocusEffect(
    React.useCallback(() => {
      if (simpleTFRef.current) {
        simpleTFRef.current.focus();
      }
    }, []),
  );

  const renderTASimple = () => (
    <>
      <Header>
        TextArea <VariantText>size="small"</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <TextArea
            ref={simpleTFRef}
            label="Label text"
            helperText="Helper text"
            placeholder="Placeholder text"
            onBlur={() => console.log('onBlur')}
            // maxLength={140}
            // numberOfLines={7}
            onSubmitEditing={event =>
              console.log('TextArea value captured:', event.nativeEvent.text)
            }
          />
        </View>
      </View>
    </>
  );

  const renderTASimpleWithCounter = () => (
    <>
      <Header>
        TextArea <VariantText>{'size="small" maxLength={140}'}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <TextArea
            label="Label text"
            helperText="Helper text"
            placeholder="Placeholder text"
            maxLength={140}
            onSubmitEditing={event =>
              console.log('TextArea value captured:', event.nativeEvent.text)
            }
          />
        </View>
      </View>
    </>
  );

  const renderTASimpleLarge = () => (
    <>
      <Header>
        TextArea <VariantText>size="large"</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <TextArea
            size="large"
            label="Label text"
            helperText="Helper text"
            placeholder="Placeholder text"
            maxLength={140}
            onSubmitEditing={event =>
              console.log('TextArea value captured:', event.nativeEvent.text)
            }
          />
        </View>
      </View>
    </>
  );

  const renderTADisabled = () => (
    <>
      <Header>
        TextArea <VariantText>disabled</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <TextArea
            disabled
            label="Label text"
            onChangeText={() => {}}
            helperText="Helper text"
            placeholder="Placeholder text"
            maxLength={140}
          />
        </View>
      </View>
    </>
  );

  const renderTADisabledWithText = () => {
    return (
      <>
        <Header>
          TextArea <VariantText>disabled with text value</VariantText>
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
            <TextArea
              value="This is a disabled TextArea"
              disabled={disable}
              label="Label text"
              onChangeText={() => {}}
              helperText="Helper text"
              placeholder="Placeholder text"
              maxLength={140}
            />
          </View>
        </View>
      </>
    );
  };

  const renderTAReadOnly = () => (
    <>
      <Header>
        TextArea <VariantText>readOnly</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <TextArea
            readOnly
            label="Label text"
            onChangeText={() => {}}
            helperText="Helper text"
            placeholder="Placeholder text"
            maxLength={140}
          />
        </View>
      </View>
    </>
  );

  const TACity = () => {
    const [error, setError] = React.useState<string>('');
    return (
      <>
        <Header>
          TextArea <VariantText>size="small" with error</VariantText>
        </Header>
        <View style={ss.outerContainer}>
          <View style={ss.innerContainer}>
            <TextArea
              size="small"
              label="City (required)"
              placeholder="Enter the capital of Tennessee"
              helperText="Enter the city name"
              error={error}
              // helperText="Helper text"
              maxLength={140}
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
  const TAEmailErrorSubmit = () => {
    const tfErrorRef = React.useRef<TextAreaRef | null>(null);
    const [error, setError] = React.useState<string>('');
    const [submittedText, setSubmittedText] = React.useState<string>('');

    const validateText = (txt: string | undefined): boolean => {
      if (txt === '' || typeof txt === 'undefined') {
        return true;
      }

      if (!/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w\w+)+$/.test(txt as string)) {
        return false;
      } else {
        return true;
      }
    };

    const updateState = (txt: string | undefined): void => {
      if (validateText(txt)) {
        setSubmittedText(txt as string);
        setError('');
      } else {
        setSubmittedText(txt as string);
        setError('Invalid email detected');
      }
    };

    const handleOnSubmitEditing = (e: {nativeEvent: {text: string}}): void => {
      const txt = e.nativeEvent.text;
      updateState(txt);
    };

    const handleOnChangeText = () => {
      setError('');
    };

    return (
      <>
        <Header>
          TextArea {''}
          <VariantText>with error on submit</VariantText>
        </Header>
        <View style={ss.outerContainer}>
          <View style={ss.innerContainer}>
            <TextArea
              ref={tfErrorRef}
              keyboardType="email-address"
              error={error}
              label="Email"
              helperText="Helper text"
              placeholder="Enter a email"
              onChangeText={handleOnChangeText}
              returnKeyType="done"
              blurOnSubmit
              onSubmitEditing={handleOnSubmitEditing}
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

  const TAControlled = () => {
    const [value, setValue] = React.useState<string>(
      'I am a controlled TextArea',
    );
    return (
      <>
        <Header>
          TextArea <VariantText>(controlled)</VariantText>
        </Header>
        <View style={ss.outerContainer}>
          <View style={ss.innerContainer}>
            <TextArea
              label="Controlled TextField"
              helperText="Use value prop and onChangeText prop"
              value={value}
              onChangeText={setValue}
            />
            <Body>State Value: {value}</Body>
          </View>
        </View>
      </>
    );
  };

  const TAUncontrolled = () => {
    const [value, setValue] = React.useState<string>('');
    return (
      <>
        <Header>
          TextArea <VariantText>(uncontrolled)</VariantText>
        </Header>
        <View style={ss.outerContainer}>
          <View style={ss.innerContainer}>
            <TextArea
              label="Uncontrolled TextField"
              helperText="Init with defaultValue, capture with onSubmitEditing"
              defaultValue="I am an uncontrolled TextField"
              onSubmitEditing={event => setValue(event.nativeEvent.text)}
            />
            <Body>State Value: {value}</Body>
          </View>
        </View>
      </>
    );
  };

  return (
    <_KeyboardAvoidingView>
      <Page>
        <TAControlled />
        <TAUncontrolled />
        {renderTASimple()}
        {renderTASimpleWithCounter()}
        {renderTASimpleLarge()}
        <TAEmailErrorSubmit />
        <TACity />
        {renderTADisabled()}
        {renderTADisabledWithText()}
        {renderTAReadOnly()}
      </Page>
    </_KeyboardAvoidingView>
  );
};

const ss = StyleSheet.create({
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
  innerContainer: {
    padding: 10,
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

TextAreaOverview.displayName = 'TextAreaOverview';
export {TextAreaOverview};
