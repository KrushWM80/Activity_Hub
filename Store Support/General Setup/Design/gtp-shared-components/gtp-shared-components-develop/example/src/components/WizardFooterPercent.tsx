import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Header, VariantText} from '../components';
import {
  WizardFooter,
  ProgressIndicator,
  colors,
  ProgressIndicatorVariant,
} from '@walmart/gtp-shared-components';

const WizardFooterPercent: React.FC = () => {
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
        <VariantText>(indicator with % values)</VariantText>
      </Header>
      <View style={styles.outerContainer}>
        <WizardFooter
          previousActionProps={{
            disabled: step === 0,
            onPress: () => handleOnPress(step, 'down'),
          }}
          nextActionProps={{
            disabled: step === driverLength - 1,
            onPress: () => handleOnPress(step, 'up'),
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

export {WizardFooterPercent};
