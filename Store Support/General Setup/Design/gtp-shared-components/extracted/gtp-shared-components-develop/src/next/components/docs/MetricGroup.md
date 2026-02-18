### MetricGroup With Single Title

```js
import {MetricGroup} from '@walmart/gtp-shared-components';
const threeMetricData = [
    {
      title: 'Store safety',
      timescope: 'YTD.9h ago',
      textLabel: 'Accident free days',
      value: '21',
    },
    {
      textLabel: 'Customer accidents',
      value: '7',
    },
    {
      textLabel: 'Associate accidents',
      value: '4',
    },
  ];

<MetricGroup data={threeMetricData} UNSAFE_style={{padding:12}} />
```

### MetricGroup With Individual Titles

```js
import {MetricGroup} from '@walmart/gtp-shared-components';
const individualMetricData = [
    {
      title: 'First Percentage',
      timescope: 'WTD.3h ago',
      textLabel: '5.5%TY vs LY',
      value: '95.6',
      unit: '%',
      variant: 'positiveUp',
    },
    {
      title: 'Pre-substitution',
      timescope: 'WTD.3h ago',
      textLabel: '1.2%TW vs LW',
      value: '93.7',
      unit: '%',
      variant: 'negativeUp',
    },
  ];
<MetricGroup data={individualMetricData} allowIndividualTitles={true} UNSAFE_style={{padding:12}} />
```