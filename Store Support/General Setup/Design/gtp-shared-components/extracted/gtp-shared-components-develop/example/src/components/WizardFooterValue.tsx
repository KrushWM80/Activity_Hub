import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Header, VariantText} from '../components';
import {
  WizardFooter,
  ProgressIndicator,
  colors,
  ProgressIndicatorVariant,
} from '@walmart/gtp-shared-components';

const WizardFooterValue: React.FC = () => {
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

  const handleOnPress = (stp: number, direction: 'up' | 'down') => {
    setStep(direction === 'up' ? stp + 1 : stp - 1);
  };

  React.useEffect(() => {
    setLabel(driver[step].label);
    setLabelValue(driver[step].labelValue);
    setValue(driver[step].value);
  }, [driver, step]);

  return (
    <>
      <Header>
        WizardFooter{'\n  '}
        <VariantText>(indicator with number values)</VariantText>
      </Header>
      <View style={styles.outerContainer}>
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
            variant={driver[step].indicatorVariant as ProgressIndicatorVariant}
            label={label}
            valueLabel={labelValue}
            value={value}
          />
        </WizardFooter>
      </View>
    </>
  );
};

const styles = StyleSheet.create({
  outerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
});

export {WizardFooterValue};
