### ErrorMessage with Image and actions

```js
import {ErrorMessage,Button} from '@walmart/gtp-shared-components';
import {StyleSheet,Image} from 'react-native';

const styles = StyleSheet.create({
  padding: { padding: 15},
});

<ErrorMessage
  title={'No internet connection'}
  UNSAFE_style={styles.padding}
  media={
        <Image
          source={{
            uri: 'https://gecgithub01.walmart.com/storage/user/77503/files/ec737101-6b86-4377-b38b-2baab2eff3f9',
            height: 200,
            width: 200,
          }}
        />
      }
  actions={
        <Button
          variant="primary"
          onPress={() =>
            displayPopupAlert('No internet connection', 'Try Again')
          }>
  Try Again
  </Button>}
  >
      Make sure you’re connected to WiFi or data and try again.
</ErrorMessage>;
```
### ErrorMessage

```js
import {ErrorMessage} from '@walmart/gtp-shared-components';

<ErrorMessage
title={'No internet connection'}>
  Make sure you’re connected to WiFi or data and try again.
</ErrorMessage>
```