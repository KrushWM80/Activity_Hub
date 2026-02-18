### Alert variant='info'

```js
import {Alert} from '@walmart/gtp-shared-components';

<Alert
  variant="info"
  children={'Reservation about to expire'}
  actionButtonProps={{
    children: 'Reserve now',
    onPress: () => {
      displayPopupAlert('Action', 'Reserve now pressed');
    },
  }}
/>
```

### Alert variant='error'

```js
import {Alert} from '@walmart/gtp-shared-components';

<Alert
  variant="error"
  children={'Reservation expired'}
  actionButtonProps={{
    children: 'Find another time',
    onPress: () => {
      displayPopupAlert('Action', 'Find another time pressed');
    },
  }}
/>
```

### Alert variant='success'

```js
import {Alert} from '@walmart/gtp-shared-components';

<Alert
  variant="success"
  children={'Pickup reservation booked.'}
  actionButtonProps={{
    children: 'Pickup now',
    onPress: () => {
      displayPopupAlert('Action', 'Pickup now pressed');
    },
  }}
/>
```

### Alert variant='warning'

```js
import {Alert} from '@walmart/gtp-shared-components';

<Alert
  variant="warning"
  children={'Reservation about to expire'}
  actionButtonProps={{
    children: 'Reserve now',
    onPress: () => {
      displayPopupAlert('Action', 'Reserve now pressed');
    },
  }}
/>
```
