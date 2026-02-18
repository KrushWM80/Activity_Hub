### LivingDesignProvider and useSnackbar hook

NOTE: use this provider to wrap your app at the top level. Caveat for Me@Walmart miniapp developers:
make sure this provider only exists at the composite (core) level, not at the miniapp level.
(see: https://jira.walmart.com/browse/CEEMP-2883)
```js
import {Button, LivingDesignProvider, useSnackbar} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 4}} />;

const App = () => {
  const {addSnack} = useSnackbar();
  return (
    <>
      <Button
        onPress={() =>
          addSnack({
            message: 'I am a snack',
          })
        }>
        Add Snack
      </Button>
      <Spacer />
      <Button
        onPress={() =>
          addSnack({
            message: 'I am a snack',
            actionButton: {
              caption: 'Action',
              onPress: () => {
                alert('Action Button pressed');
              },
            },
            onClose: () => {},
            customPosition: '50%', // optionally you can pass a custom vertical position
                                   // it can be an absolute number (e.g. 200) or a percent (e.g 25%) of the screen height
                                   // measured from the bottom of the screen.
          })
        }>
        Add Snack w/ actionButton, customPosition
    </Button>
    </>
  )
};

<LivingDesignProvider>
  <App />
</LivingDesignProvider>
```
