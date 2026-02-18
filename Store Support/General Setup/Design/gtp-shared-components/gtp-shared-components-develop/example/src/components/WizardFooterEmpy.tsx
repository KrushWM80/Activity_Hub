import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Header, VariantText} from '../components';
import {WizardFooter, colors} from '@walmart/gtp-shared-components';
import {displayPopupAlert} from '../screens/screensFixtures';

const WizardFooterEmpty: React.FC = () => {
  return (
    <>
      <Header>
        WizardFooter{'\n  '}
        <VariantText>(with empty content)</VariantText>
      </Header>
      <View style={styles.outerContainer}>
        <WizardFooter
          previousActionProps={{
            variant: 'secondary',
            onPress: () =>
              displayPopupAlert('Action', 'Previous button tapped'),
            children: 'Previous',
          }}
          nextActionProps={{
            variant: 'primary',
            onPress: () =>
              displayPopupAlert('Action', 'Continue button tapped'),
            children: 'Continue',
          }}
        />
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

export {WizardFooterEmpty};
