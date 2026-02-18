import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Page, Header, Section} from '../components';
import {
  Button,
  TextField,
  Icons,
  Body,
  Checkbox,
  FormGroup,
  Link,
  IconButton,
  useSimpleReducer,
  colors,
} from '@walmart/gtp-shared-components';
import {displayPopupAlert} from './screensFixtures';

type FormGroupState = {
  hidePassword: boolean;
  password: string;
  email: string;
  keepSigned: boolean;
};
const initialState = {
  hidePassword: true,
  password: '',
  email: '',
  keepSigned: false,
};
const FormGroupOverview = () => {
  const [state, setState] = useSimpleReducer<FormGroupState>(initialState);

  const renderTFSimple = () => (
    <TextField
      label="Email"
      helperText="enter valid email"
      placeholder="Enter valid email"
      leading={<Icons.EmailIcon />}
      onChangeText={txt => setState('email', txt as string)}
    />
  );

  const renderTFPassword = () => (
    <TextField
      type="password"
      label="Password"
      secureTextEntry={state.hidePassword as boolean}
      helperText=""
      placeholder="Enter your password"
      leading={<Icons.LockIcon />}
      onChangeText={text => setState('password', text as string)}
      trailing={
        <IconButton
          key="IconButton"
          size="medium"
          color={colors.gray['100']}
          onPress={() => setState('hidePassword', !state.hidePassword)}>
          {state.hidePassword ? <Icons.EyeIcon /> : <Icons.EyeSlashIcon />}
        </IconButton>
      }
    />
  );
  const forgotPassword = () => {
    return (
      <View style={ss.forgot}>
        <Button
          variant="tertiary"
          onPress={() =>
            displayPopupAlert('Forgot Password', 'Forgot Password pressed')
          }>
          Forget Password?
        </Button>
      </View>
    );
  };

  const keepMeSignedIn = () => {
    return (
      <>
        <Checkbox
          label={'Keep me signed in'}
          checked={state.keepSigned as boolean}
          onPress={() => {
            setState('keepSigned', !state.keepSigned);
          }}
        />
        <Body weight="700" size="small">
          Do not check if using a public device.{'  '}
          <Link
            onPress={() => displayPopupAlert('More', 'More pressed')}
            children={'more'}
          />
        </Body>
      </>
    );
  };
  const signInButton = () => {
    return (
      <Button
        variant="primary"
        onPress={() => {
          displayPopupAlert(
            'Login',
            `Username: ${state.email} \n Password: ${state.password}`,
          );
        }}>
        Sign In
      </Button>
    );
  };
  return (
    <Page>
      <Header>FormGroup</Header>
      <Section>
        <FormGroup>
          {renderTFSimple()}
          {renderTFPassword()}
          {forgotPassword()}
          {keepMeSignedIn()}
          {signInButton()}
        </FormGroup>
      </Section>
    </Page>
  );
};

const ss = StyleSheet.create({
  innerContainer: {
    flex: 1,
    justifyContent: 'space-around',
    flexDirection: 'row',
    padding: 10,
  },
  forgot: {
    flex: 1,
    alignItems: 'flex-end',
  },
  outerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
});

export {FormGroupOverview};
