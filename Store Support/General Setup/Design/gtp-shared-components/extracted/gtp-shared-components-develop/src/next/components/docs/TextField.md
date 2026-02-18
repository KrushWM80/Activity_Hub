### TextField type="text" (default)

```js
import {TextField, Icons} from '@walmart/gtp-shared-components';

<>
  <TextField
    label="Label text"
    helperText="Helper text"
    placeholder="Placeholder text"
    leading={[<Icons.EmailIcon />, true]}
    onSubmitEditing={event =>
      console.log('TextField value captured:', event.nativeEvent.text)
    }
  />
</>
```

### TextField type="text" (with error)

```js
import {TextField, Icons} from '@walmart/gtp-shared-components';
const [error, setError] = React.useState('');

<>
  <TextField
    error={error}
    label="Name (required)"
    placeholder="Enter first name"
    helperText={'Enter only valid characters a-z A-Z'}
    leading={[<Icons.AssociateIcon />, true]}
    onChangeText={txt => {
      if (txt === '') {
        setError('');
      } else if (!/^[a-zA-Z -]+$/.test(txt)) {
        setError('Invalid characters detected');
      } else {
        setError('');
      }
    }}
    onSubmitEditing={event => {
      if (state.withErrorError === '') {
        console.log(
          'TextField value captured:',
          event.nativeEvent.text,
        );
      }
    }}
  />
</>
```

### TextField type="number" (with error)

```js
import {TextField, Icons} from '@walmart/gtp-shared-components';
const [error, setError] = React.useState('');

<>
  <TextField
    type="number"
    error={error}
    label="Quatity"
    helperText="Helper text"
    placeholder="Enter a number"
    leading={[<Icons.KeyboardIcon />, true]}
    onChangeText={txt => {
      if (txt === '') {
        setError('');
      } else if (!/^[0-9.,]+$/.test(txt)) {
          setError('Invalid characters detected');
      } else {
        setError('');
      }
    }}
    onSubmitEditing={event => {
      if (state.typeNumberError === '') {
        console.log(
          'TextField value captured:',
          event.nativeEvent.text,
        );
      }
    }}
  />
</>

```

### TextField type="tel"

Note: for a complete recipe with validation and masking check out
the embedded `example` app [here](https://gecgithub01.walmart.com/electrode-mobile-platform/gtp-shared-components/blob/main/example/src/screens/RecipeTextFields.tsx)

```js
import {TextField, Icons} from '@walmart/gtp-shared-components';

<>
  <TextField
    type="tel"
    label="Phone Number (required)"
    placeholder="(000) 000-0000"
    leading={[<Icons.PhoneIcon />, true]}
    onSubmitEditing={event =>
      console.log('TextField value captured:', event.nativeEvent.text)
    }
  />
</>

```

### TextField type="password" (with show/hide IconButton)

```js
import {TextField, Icons, colors, IconButton} from '@walmart/gtp-shared-components';
const [error, setError] = React.useState('');
const [show, setShow] = React.useState('false');

<>
  <TextField
    type="password"
    label="Password"
    secureTextEntry={show}
    helperText=""
    placeholder="Enter your password"
    leading={[<Icons.LockIcon />, true]}
    trailing={[
      <IconButton
        key="IconButton"
        size="medium"
        color={colors.gray['100']}
        UNSAFE_style={{marginHorizontal: 12}}
        onPress={() =>
          setShow(!show)
        }>
        {show ? (
          <Icons.EyeIcon />
        ) : (
          <Icons.EyeSlashIcon />
        )}
      </IconButton>,
      false,
    ]}
    onSubmitEditing={event =>
      console.log('TextField value captured:', event.nativeEvent.text)
    }
  />
</>
```

### TextField (controlled)

```js
import {Body, TextField, Icons} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;
const [value, setValue] = React.useState('I am a controlled TextField');

<>
  <TextField
    label="Controlled TextField"
    helperText="Use value prop and onChangeText prop"
    value={value}
    onChangeText={setValue}
    leading={[<Icons.EmailIcon />, true]}
  />
  <Spacer />
  <Body>State Value: {value}</Body>
</>
```

### TextField (uncontrolled)

```js
import {Body, TextField, Icons} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;
const [value, setValue] = React.useState('');

<>
  <TextField
    label="Uncontrolled TextField"
    helperText="Init with defaultValue, capture with onSubmitEditing"
    defaultValue="I am an uncontrolled TextField"
    leading={[<Icons.EmailIcon />, true]}
    onSubmitEditing={event =>
      setValue(event.nativeEvent.text)
    }
  />
  <Spacer />
  <Body>State Value: {value}</Body>
</>
```