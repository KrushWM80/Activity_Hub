### Nudge
```js
import {Nudge,Link,Icons} from '@walmart/gtp-shared-components';

<Nudge
  title={'The years start coming'}
  onClose={() => mockFn()}
  leading={<Icons.EyeIcon size={24} />}
  actions={
          <Link color="default" onPress={() =>
                    displayPopupAlert('Action', 'Action1 button pressed')}>
            Look away
          </Link>
        }>
  And they don't stop coming. Fed to the rules and I hit the ground running. Didn't make sense not to:
</Nudge>
```

### Nudge with actions

```js
import {Nudge,Button,Icons} from '@walmart/gtp-shared-components';

<Nudge
  title={'Nudge without actions'}
  actions={
            <>
              <Button
                  variant="primary"
                  onPress={() =>
                    displayPopupAlert('Action', 'Primary Button pressed')
                  }>
                  Look away
               </Button>
              <Button
                  variant="tertiary"
                  onPress={() =>
                    displayPopupAlert('Action', 'Tertiary button pressed')
                  }>
                  Look away
                </Button>
              </>
  }
  >
  And they don't stop coming. Fed to the rules and I hit the ground running. Didn't make sense not to:
</Nudge>
```
### Nudge with leading and close

```js
import {Nudge,Link,SpotIcon,Icons} from '@walmart/gtp-shared-components';

<Nudge
  title={'Nudge without actions'}
  onClose={() => mockFn()}
  leading={
          <SpotIcon color="white">
            <Icons.StarIcon size={24} />
          </SpotIcon>}
  >
  And they don't stop coming. Fed to the rules and I hit the ground running. Didn't make sense not to:
</Nudge>
```