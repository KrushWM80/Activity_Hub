### TextArea size="small" (default)

```js
import {TextArea} from '@walmart/gtp-shared-components';
  <>
    <TextArea
      label="Label text"
      helperText="Helper text"
      placeholder="Placeholder text"
      onSubmitEditing={event =>
        console.log('TextArea value captured:', event.nativeEvent.text)
      }
      UNSAFE_style={{outline: 'none'}}
    />
  </>
```

### TextArea maxLength={140} (with character counter)

```js
import {TextArea} from '@walmart/gtp-shared-components';
<>
  <TextArea
    label="Label text"
    helperText="Helper text"
    placeholder="Placeholder text"
    maxLength={140}
    onSubmitEditing={event =>
      console.log('TextArea value captured:', event.nativeEvent.text)
    }
  />
</>
```

### TextArea size="large"

```js
import {TextArea} from '@walmart/gtp-shared-components';
<>
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
</>
```

### TextArea with error

```js
import * as React from 'react';
import {TextArea} from '@walmart/gtp-shared-components';

const [error, setError] = React.useState('');
  <>
    <TextArea
      size="small"
      label="City (required)"
      placeholder="Enter the capital of Tennessee"
      helperText="Enter the city name"
      error={error}
      helperText="Helper text"
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
          !/Nashville\s*$/.test(txt) &&
          txt.length > 4
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
  </>
```

### TextArea disabled

```js
import {TextArea} from '@walmart/gtp-shared-components';
  <>
    <TextArea
      disabled
      label="Label text"
      helperText="Helper text"
      placeholder="Placeholder text"
      maxLength={140}
    />
  </>
```

### TextArea readOnly

```js
import {TextArea} from '@walmart/gtp-shared-components';
  <>
    <TextArea
      readOnly
      label="Label text"
      helperText="Helper text"
      placeholder="Placeholder text"
    />
  </>
```

### TextArea (controlled)

```js
import {Body, TextArea, Icons} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;
const [value, setValue] = React.useState('I am a controlled TextArea');

<>
  <TextArea
    label="Controlled TextArea"
    helperText="Use value prop and onChangeText prop"
    value={value}
    onChangeText={setValue}
    leading={[<Icons.EmailIcon />, true]}
  />
  <Spacer />
  <Body>State Value: {value}</Body>
</>
```

### TextArea (uncontrolled)

```js
import {Body, TextArea, Icons} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;
const [value, setValue] = React.useState('');

<>
  <TextArea
    label="Uncontrolled TextArea"
    helperText="Init with defaultValue, capture with onBlur"
    defaultValue="I am an uncontrolled TextArea"
    leading={[<Icons.EmailIcon />, true]}
    onSubmitEditing={event =>
      setValue(event.nativeEvent.text)
    }
    onBlur={event => {
      setValue(event.nativeEvent.text);
    }}
  />
  <Spacer />
  <Body>State Value: {value}</Body>
</>
```