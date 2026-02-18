### WizardFooter (indicator with % values)

```js
import {WizardFooter, ProgressIndicator} from '@walmart/gtp-shared-components';

const driver = React.useMemo(
  () => [
    {
      label: 'Location',
      labelValue: '20%',
      value: 20,
      indicatorVariant: 'info',
    },
    {
      label: 'Employment Type',
      labelValue: '40%',
      value: 40,
      indicatorVariant: 'info',
    },
    {
      label: 'Job Families',
      labelValue: '80%',
      value: 80,
      indicatorVariant: 'info',
    },
    {
      label: 'Review',
      labelValue: '100%',
      value: 100,
      indicatorVariant: 'success',
    },
  ],
  [],
);

const driverLength = driver.length;
const [label, setLabel] = React.useState('Location');
const [labelValue, setLabelValue] = React.useState('20%');
const [value, setValue] = React.useState(20);
const [step, setStep] = React.useState(0);

const handleOnPress = (stp, direction) => {
  setStep(direction === 'up' ? stp + 1 : stp - 1);
};

React.useEffect(() => {
    setLabel(driver[step].label);
    setLabelValue(driver[step].labelValue);
    setValue(driver[step].value);
  }, [driver, step]);

<>
  <WizardFooter
    previousActionProps={{
      variant: 'secondary',
      disabled: step === 0,
      onPress: () => handleOnPress(step, 'down'),
      children: 'Previous',
    }}
    nextActionProps={{
      variant: 'primary',
      disabled: step === driverLength - 1,
      onPress: () => handleOnPress(step, 'up'),
      children: 'Continue',
    }}>
    <ProgressIndicator
      variant={driver[step].indicatorVariant}
      label={label}
      valueLabel={labelValue}
      value={value}
    />
  </WizardFooter>
</>
```

### WizardFooter (indicator with number values)

```js
import {WizardFooter, ProgressIndicator} from '@walmart/gtp-shared-components';

const driver = React.useMemo(
  () => [
    {
      label: 'Name',
      labelValue: '1 of 6',
      value: 17,
      indicatorVariant: 'info',
    },
    {
      label: 'Address',
      labelValue: '2 of 6',
      value: 34,
      indicatorVariant: 'info',
    },
    {
      label: 'Phone number',
      labelValue: '3 of 6',
      value: 51,
      indicatorVariant: 'info',
    },
    {
      label: 'Email',
      labelValue: '4 of 6',
      value: 68,
      indicatorVariant: 'info',
    },
    {
      label: 'Payment info',
      labelValue: '5 of 6',
      value: 85,
      indicatorVariant: 'info',
    },
    {
      label: 'Account setup complete',
      labelValue: '6 of 6',
      value: 100,
      indicatorVariant: 'success',
    },
  ],
  [],
);

const driverLength = driver.length;
const [label, setLabel] = React.useState('Location');
const [labelValue, setLabelValue] = React.useState('20%');
const [value, setValue] = React.useState(20);
const [step, setStep] = React.useState(0);

const handleOnPress = (stp, direction) => {
  setStep(direction === 'up' ? stp + 1 : stp - 1);
};

React.useEffect(() => {
  setLabel(driver[step].label);
  setLabelValue(driver[step].labelValue);
  setValue(driver[step].value);
}, [driver, step]);

<>
  <WizardFooter
    previousActionProps={{
      variant: 'secondary',
      disabled: step === 0,
      onPress: () => handleOnPress(step, 'down'),
      children: 'Previous',
    }}
    nextActionProps={{
      variant: 'primary',
      disabled: step === driverLength - 1,
      onPress: () => handleOnPress(step, 'up'),
      children: 'Continue',
    }}>
    <ProgressIndicator
      variant={driver[step].indicatorVariant}
      label={label}
      valueLabel={labelValue}
      value={value}
    />
  </WizardFooter>
</>
```

### WizardFooter (with empty content)

```js
import {WizardFooter} from '@walmart/gtp-shared-components';

<>
  <WizardFooter
    previousActionProps={{
      variant: 'secondary',
      onPress: () => {},
      children: 'Previous',
    }}
    nextActionProps={{
      variant: 'primary',
      onPress: () => {},
      children: 'Continue',
    }}
  />
</>
```