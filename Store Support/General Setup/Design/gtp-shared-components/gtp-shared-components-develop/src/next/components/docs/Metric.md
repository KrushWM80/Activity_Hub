### Metric neutral

```js
import {Metric} from '@walmart/gtp-shared-components';

<Metric
  title="Real-Time WOSH and overtime"
  textLabel="3 hours more then last month"
  timescope="MTD"
  value="24"
  unit="hours"
  variant="neutral"
 />
```

### Metric negativeDown

```js
import {Metric} from '@walmart/gtp-shared-components';

<Metric
  title="Sales"
  textLabel="3k (3.7%) less than last month"
  timescope="MTD"
  value="$1.23"
  unit="M"
  variant="negativeDown"
 />
```

### Metric negativeUp

```js
import {Metric} from '@walmart/gtp-shared-components';

<Metric
  title="Tire average"
  textLabel="6% slower than last month"
  timescope="MTD"
  value="27"
  unit="minutes"
  variant="negativeUp"
 />
```
### Metric positiveDown

```js
import {Metric} from '@walmart/gtp-shared-components';

<Metric
  title="Oil average"
  textLabel="4% faster YoY"
  timescope="YTD"
  value="16"
  unit="minutes"
  variant="positiveDown"
 />
```
### Metric positiveUp

```js
import {Metric} from '@walmart/gtp-shared-components';

<Metric
  title="Sales"
  textLabel="50K (3.21%) more from last month"
  timescope="Today"
  value="$500"
  unit="M"
  variant="positiveDown"
 />
```