### Banner variant='error'

```js
import {Banner} from '@walmart/gtp-shared-components';

const [isBannerVisible, setIsBannerVisible] = React.useState(true);

<>
  {isBannerVisible ? (
    <Banner
      variant="error"
      onClose={() => {
        setIsBannerVisible(false);
      }}>
      This is an error message.
    </Banner>
  ) : null}
</>
```

### Banner variant='info'

```js
import {Banner} from '@walmart/gtp-shared-components';

const [isBannerVisible, setIsBannerVisible] = React.useState(true);

<>
  {isBannerVisible ? (
    <Banner
      variant="info"
      onClose={() => {
        setIsBannerVisible(false);
      }}>
      This is an error message.
    </Banner>
  ) : null}
</>
```

### Banner variant='success'

```js
import {Banner} from '@walmart/gtp-shared-components';

const [isBannerVisible, setIsBannerVisible] = React.useState(true);

<>
  {isBannerVisible ? (
    <Banner
      variant="success"
      onClose={() => {
        setIsBannerVisible(false);
      }}>
      This is a success message.
    </Banner>
  ) : null}
</>
```


### Banner variant='warning'

```js
import {Banner} from '@walmart/gtp-shared-components';

const [isBannerWarningVisible, setIsBannerWarningVisible] = React.useState(true);

<>
  {isBannerWarningVisible ? (
    <Banner
      variant="warning"
      onClose={() => {
        setIsBannerWarningVisible(false);
      }}>
      This is a warning message.
    </Banner>
  ) : null}
</>
```
