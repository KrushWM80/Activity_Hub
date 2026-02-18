/* eslint-disable react-native/no-inline-styles */
import React, {useState} from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableHighlight,
  Platform,
  StyleSheet,
  Pressable,
} from 'react-native';
import {Icons, colors} from '@walmart/gtp-shared-components';
import {Header, Section, VariantText} from '../components';

const TEST_ID = 'counts';

export const testId = (_testID = '') => {
  return Platform.OS === 'android'
    ? {accessible: true, accessibilityLabel: TEST_ID + '-' + _testID}
    : {testID: TEST_ID + '-' + _testID};
};

interface Props {
  updatedCount: string;
  onChange: (
    val: string,
    type: undefined | 'plus' | 'minus',
    allowDecimal: boolean,
  ) => void;
}

const Stepper: React.FC<Props> = ({updatedCount, onChange}) => {
  const [plusBtnUnderlay, setPlusBtnUnderlay] = useState(false);
  const [minusBtnUnderlay, setMinusBtnUnderlay] = useState(false);
  const minValue = 0;
  const maxValue = 9999;

  const isMinValue = Number(updatedCount) === minValue;
  const isNegValue = Number(updatedCount) < minValue;
  const isMaxValue = Number(updatedCount) === maxValue;

  return (
    <View style={styles.editCountContainer} {...testId('stepperComponent')}>
      <View style={styles.editCountContent}>
        <TouchableHighlight
          disabled={isMinValue || isNegValue}
          onPress={() => onChange(updatedCount, 'minus', false)}
          onShowUnderlay={() => setMinusBtnUnderlay(true)}
          onHideUnderlay={() => setMinusBtnUnderlay(false)}
          style={styles.fillIcon}
          {...testId('minusBtn')}>
          {isMinValue || isNegValue ? (
            <Icons.MinusIcon size={24} UNSAFE_style={styles.disabled} />
          ) : (
            <Icons.MinusIcon
              size={24}
              UNSAFE_style={
                minusBtnUnderlay ? styles.showUnderlay : styles.hideUnderlay
              }
            />
          )}
        </TouchableHighlight>
        <View style={[styles.center, styles.fullHeight]}>
          {isMinValue && updatedCount.length > 0 && (
            <View style={styles.center}>
              <Text style={styles.textRegular}>{'Min'}</Text>
            </View>
          )}
          {isMaxValue && (
            <View style={styles.center}>
              <Text style={styles.textRegular}>{'Max'}</Text>
            </View>
          )}
          <TextInput
            {...testId('stepperInput')}
            value={updatedCount}
            onChangeText={value => onChange(value, undefined, false)}
            style={[
              styles.inputText,
              styles.inputTextFont,
              {fontWeight: isMinValue || isMaxValue ? 'normal' : 'bold'},
            ]}
            keyboardType="number-pad"
            maxLength={5}
          />
        </View>
        <TouchableHighlight
          disabled={isMaxValue}
          onPress={() => onChange(updatedCount, 'plus', false)}
          onShowUnderlay={() => setPlusBtnUnderlay(true)}
          onHideUnderlay={() => setPlusBtnUnderlay(false)}
          style={styles.fillIcon}
          {...testId('plusBtn')}>
          {isMaxValue ? (
            <Icons.PlusIcon size={24} UNSAFE_style={styles.disabled} />
          ) : (
            <Icons.PlusIcon
              size={24}
              UNSAFE_style={
                plusBtnUnderlay ? styles.showUnderlay : styles.hideUnderlay
              }
            />
          )}
        </TouchableHighlight>
      </View>
    </View>
  );
};

export const StepperRefactored: React.FC<Props> = ({
  updatedCount,
  onChange,
}) => {
  const minValue = 0;
  const maxValue = 9999;

  const isMinValue = Number(updatedCount) === minValue;
  const isNegValue = Number(updatedCount) < minValue;
  const isMaxValue = Number(updatedCount) === maxValue;

  return (
    <View style={styles.editCountContainer} {...testId('stepperComponent')}>
      <View style={styles.editCountContent}>
        <Pressable
          disabled={isMinValue || isNegValue}
          onPress={() => onChange(updatedCount, 'minus', false)}
          style={styles.fillIcon}
          {...testId('minusBtn')}>
          {({pressed}) => (
            <View
              style={{
                backgroundColor: pressed ? 'black' : 'transparent',
                borderRadius: 1000,
              }}>
              {isMinValue || isNegValue ? (
                <Icons.MinusIcon size={24} UNSAFE_style={styles.disabled} />
              ) : (
                <Icons.MinusIcon
                  size={24}
                  UNSAFE_style={
                    pressed ? styles.showUnderlay : styles.hideUnderlay
                  }
                />
              )}
            </View>
          )}
        </Pressable>

        <View style={[styles.center, styles.fullHeight]}>
          {isMinValue && updatedCount.length > 0 && (
            <View style={styles.center}>
              <Text style={styles.textRegular}>{'Min'}</Text>
            </View>
          )}
          {isMaxValue && (
            <View style={styles.center}>
              <Text style={styles.textRegular}>{'Max'}</Text>
            </View>
          )}
          <TextInput
            {...testId('stepperInput')}
            value={updatedCount}
            onChangeText={value => onChange(value, undefined, false)}
            style={[
              styles.inputText,
              styles.inputTextFont,
              {fontWeight: isMinValue || isMaxValue ? 'normal' : 'bold'},
            ]}
            keyboardType="number-pad"
            maxLength={5}
          />
        </View>
        <Pressable
          disabled={isMaxValue}
          onPress={() => onChange(updatedCount, 'plus', false)}
          style={styles.fillIcon}
          {...testId('plusBtn')}>
          {({pressed}) => (
            <View
              style={{
                backgroundColor: pressed ? 'black' : 'transparent',
                borderRadius: 1000,
              }}>
              {isMaxValue ? (
                <Icons.PlusIcon size={24} UNSAFE_style={styles.disabled} />
              ) : (
                <Icons.PlusIcon
                  size={24}
                  UNSAFE_style={
                    pressed ? styles.showUnderlay : styles.hideUnderlay
                  }
                />
              )}
            </View>
          )}
        </Pressable>
      </View>
    </View>
  );
};

const IconTintColorRecipe: React.FC = () => {
  const [count, setCount] = React.useState<string>('10');
  const [countRefactored, setCountRefactored] = React.useState<string>('10');

  const handleOnChange = (
    val: string,
    type: 'plus' | 'minus' | undefined,
    allowDecimal: boolean,
  ) => {
    let _val = Number.parseInt(val, 10);
    const updated_val = type === 'plus' ? _val + 1 : _val - 1;

    setCount(updated_val.toString());
    console.log('---- type, allowDecimal:', type, allowDecimal);
  };

  const handleOnChangeRefactored = (
    val: string,
    type: 'plus' | 'minus' | undefined,
    allowDecimal: boolean,
  ) => {
    let _val = Number.parseInt(val, 10);
    const updated_val = type === 'plus' ? _val + 1 : _val - 1;

    setCountRefactored(updated_val.toString());
    console.log('---- type, allowDecimal:', type, allowDecimal);
  };
  return (
    <>
      <Header>
        Refactoring {'\n  '}
        <VariantText>
          {'provided to SSAE: Store Price Execution team'}
        </VariantText>
      </Header>
      <Header>
        Stepper - original {'\n  '}
        <VariantText>{'with TouchableHighlight'}</VariantText>
      </Header>
      <Section>
        <Stepper
          updatedCount={count}
          onChange={(
            val: string,
            type: 'plus' | 'minus' | undefined,
            allowDecimal: boolean,
          ) => handleOnChange(val, type, allowDecimal)}
        />
      </Section>
      <Header>
        Stepper - refactored {'\n  '}
        <VariantText>{'with Pressable'}</VariantText>
      </Header>
      <Section>
        <StepperRefactored
          updatedCount={countRefactored}
          onChange={(
            val: string,
            type: 'plus' | 'minus' | undefined,
            allowDecimal: boolean,
          ) => handleOnChangeRefactored(val, type, allowDecimal)}
        />
      </Section>
    </>
  );
};

export const styles = StyleSheet.create({
  countContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 20,
  },
  editCountContainer: {
    height: 40,
    width: 160,
    borderWidth: 2,
    borderColor: '#e3e2e1',
    borderRadius: 50,
    justifyContent: 'center',
    paddingHorizontal: 5,
  },
  editCountContent: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
  },
  center: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  fillIcon: {borderRadius: 12},
  showUnderlay: {tintColor: 'white'},
  hideUnderlay: {tintColor: 'black'},
  disabled: {tintColor: colors.gray['50']},
  textBold: {
    ...Platform.select({
      ios: {fontFamily: 'Bogle'},
      android: {fontFamily: 'Bogle-Bold'},
    }),
    fontSize: 16,
  },
  textRegular: {
    ...Platform.select({
      ios: {fontFamily: 'Bogle'},
      android: {fontFamily: 'Bogle-Regular'},
    }),
    fontSize: 14,
    color: '#2e2f32',
  },
  inputTextFont: {
    ...Platform.select({
      ios: {fontFamily: 'Bogle'},
      android: {fontFamily: 'Bogle-Regular'},
    }),
    fontSize: 16,
    color: 'black',
  },
  fullHeight: {height: '100%'},
  button: {marginTop: 20},
  inputText: {
    textAlign: 'center',
    height: '100%',
  },
  floatingText: {
    height: 36,
    fontSize: 16,
    color: '#000',
    paddingBottom: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#909196',
    textAlign: 'right',
  },
  floatingTextOnFocus: {
    height: 36,
    fontSize: 16,
    color: '#000',
    paddingBottom: 10,
    borderBottomWidth: 2,
    borderBottomColor: '#000000',
    textAlign: 'right',
  },
  inputContainer: {
    padding: 0,
    height: 40,
    width: 160,
    borderRadius: 4,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  floatingTextPriceChange: {
    borderWidth: 1,
    borderColor: colors.gray['80'],
  },
  floatingTextOnFocusPriceChange: {
    borderWidth: 2,
    borderColor: colors.black,
  },
  textPriceChange: {
    fontFamily: 'Bogle',
    fontWeight: 'normal',
    color: colors.gray['160'],
    fontSize: 16,
    marginVertical: -8,
  },
  priceChangeCountsContainer: {flexDirection: 'row', paddingVertical: 18},
  priceChangeCounts: {
    flexDirection: 'column',
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  verticalDivider: {
    borderRightColor: colors.gray['10'],
    borderRightWidth: 1,
  },
  cellTitle: {
    marginBottom: 4,
  },
  divider: {
    borderTopColor: colors.gray['10'],
    borderTopWidth: 1,
    marginTop: 0,
    paddingTop: 16,
  },
});

export {IconTintColorRecipe};
