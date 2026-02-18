import * as React from 'react';
import {FlexStyle, StyleSheet, View} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/WizardFooter';

import type {CommonViewProps} from '../types/ComponentTypes';

import {Button, ButtonProps} from './Button';

// ---------------
// Props
// ---------------
export type WizardFooterProps = CommonViewProps & {
  /**
   * The content for the WizardFooter
   * Typically a ProgressIndicator
   */
  children?: React.ReactNode;
  /**
   * The next action button props for the WizardFooter.
   *
   * We provide these defaults {children: 'Previous', size: 'small', variant: 'secondary'}
   *
   * You can override them, or just provide {onPress: ..., disabled: ...}, etc
   */
  nextActionProps: ButtonProps;
  /**
   * The previous action button props for the WizardFooter.
   *
   * We provide these defaults {children: 'Continue', size: 'small', variant: 'primary'}
   *
   * You can override them, or just provide {onPress: ..., disabled: ...}, etc
   */
  previousActionProps: ButtonProps;
};

/**
 * Wizards provide context for the process such as name of the process, total steps,
 * and current step, as well as navigation between steps.
 *
 * ```js
 * import {WizardFooter, ProgressIndicator} from '@walmart/gtp-shared-components';
 *
 * const driver = React.useMemo(
 *   () => [
 *     {
 *       label: 'Location',
 *       labelValue: '20%',
 *       value: 20,
 *       indicatorVariant: 'info',
 *     },
 *     {
 *       label: 'Employment Type',
 *       labelValue: '40%',
 *       value: 40,
 *       indicatorVariant: 'info',
 *     },
 *     {
 *       label: 'Job Families',
 *       labelValue: '80%',
 *       value: 80,
 *       indicatorVariant: 'info',
 *     },
 *     {
 *       label: 'Review',
 *       labelValue: '100%',
 *       value: 100,
 *       indicatorVariant: 'success',
 *     },
 *   ],
 *   [],
 * );
 *
 * const driverLength = driver.length;
 * const [label, setLabel] = React.useState('Location');
 * const [labelValue, setLabelValue] = React.useState('20%');
 * const [value, setValue] = React.useState(20);
 * const [step, setStep] = React.useState(0 * );
 *
 * const handleOnPress = (stp, direction) => {
 *   setStep(direction === 'up' ? stp + 1 : stp - 1); *
 * };
 *
 * React.useEffect(() => {
 *     setLabel(driver[step].label);
 *     setLabelValue(driver[step].labelValue);
 *     setValue(driver[step].value);
 *   }, [driver, step] * );
 *
 * <>
 *   <WizardFooter
 *     previousActionProps={{
 *       variant: 'secondary',
 *       disabled: step === 0,
 *       onPress: () => handleOnPress(step, 'down'),
 *       children: 'Previous',
 *     }}
 *     nextActionProps={{
 *       variant: 'primary',
 *       disabled: step === driverLength - 1,
 *       onPress: () => handleOnPress(step, 'up'),
 *       children: 'Continue',
 *     }}>
 *     <ProgressIndicator
 *       variant={driver[step].indicatorVariant}
 *       label={label}
 *       valueLabel={labelValue}
 *       value={value}
 *     />
 *   </WizardFooter>
 * </>
 * ```
 */
const WizardFooter: React.FC<WizardFooterProps> = (props) => {
  const {children, nextActionProps, previousActionProps} = props;

  // ---------------
  // Rendering
  // ---------------
  return (
    <View testID={WizardFooter.displayName} style={ss.container}>
      <View style={ss.content}>{children}</View>
      <View style={ss.buttonContainer}>
        <Button
          children="Previous"
          size="small"
          variant="secondary"
          {...previousActionProps}
        />
        <Button
          children="Continue"
          size="small"
          variant="primary"
          {...nextActionProps}
        />
      </View>
    </View>
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: token.componentWizardFooterContainerAlignVertical as Extract<
      FlexStyle,
      'alignItems'
    >,
    backgroundColor: token.componentWizardFooterContainerBackgroundColor,
    borderTopColor: token.componentWizardFooterContainerBorderColorTop,
    borderTopWidth: token.componentWizardFooterContainerBorderWidthTop,
    paddingHorizontal: token.componentWizardFooterContainerPaddingHorizontal,
    paddingVertical: token.componentWizardFooterContainerPaddingVerticalBS,
  },
  content: {
    justifyContent:
      token.componentWizardFooterContentAlignHorizontal as Extract<
        FlexStyle,
        'justifyContent'
      >,
    marginBottom: token.componentWizardFooterContentMarginBottomBS,
    maxWidth: token.componentWizardFooterContentMaxWidth,
    width: token.componentWizardFooterContentWidthBS,
  },
  buttonContainer: {
    width: token.componentWizardFooterContentWidthBS,
    flexDirection: 'row',
    justifyContent:
      token.componentWizardFooterContainerAlignHorizontal as Extract<
        FlexStyle,
        'justifyContent'
      >,
    alignItems: token.componentWizardFooterContainerAlignVertical as Extract<
      FlexStyle,
      'alignItems'
    >,
  },
  previousButton: {
    marginRight: token.componentWizardFooterPreviousButtonMarginEndBS,
  },
  nextButton: {
    marginLeft: token.componentWizardFooterNextButtonMarginStartBS,
  },
});

WizardFooter.displayName = 'WizardFooter';
export {WizardFooter};
