import * as React from 'react';
import {StyleSheet, Text, View} from 'react-native';
import {Header, Page, VariantText} from '../components';
import {colors, ProgressIndicator} from '@walmart/gtp-shared-components';

const ProgressIndicatorRecipes: React.FC = () => {
  const ProgressIndicatorDefault: React.FC = () => {
    return (
      <>
        <Header>
          ProgressIndicator
          <VariantText> (default){'\n\n '}</VariantText>
          <VariantText>{`<ProgressIndicator/>`}</VariantText>
        </Header>
        <View style={styles.outerContainer}>
          <View style={styles.innerContainer}>
            <ProgressIndicator />
          </View>
        </View>
      </>
    );
  };

  const ProgressIndicatorWithLabel: React.FC = () => {
    return (
      <>
        <Header>
          ProgressIndicator<VariantText> (with label){'\n\n '}</VariantText>
          <VariantText>{`<ProgressIndicator label={'Account setup has not yet started'} />`}</VariantText>
        </Header>
        <View style={styles.outerContainer}>
          <View style={styles.innerContainer}>
            <ProgressIndicator label={'Account setup has not yet started'} />
          </View>
        </View>
      </>
    );
  };

  const ProgressIndicatorWithValue: React.FC = () => {
    return (
      <>
        <Header>
          ProgressIndicator
          <VariantText> (with label and value){'\n\n '}</VariantText>
          <VariantText>{`<ProgressIndicator
              label={'Account setup is in progress'}
              value={25}
            />`}</VariantText>
        </Header>
        <View style={styles.outerContainer}>
          <View style={styles.innerContainer}>
            <ProgressIndicator
              label={'Account setup is in progress'}
              value={25}
            />
          </View>
        </View>
      </>
    );
  };

  const ProgressIndicatorWithValueLabel: React.FC = () => {
    return (
      <>
        <Header>
          ProgressIndicator
          <VariantText>
            {' '}
            (with label, value and valueLabel){'\n\n '}
          </VariantText>
          <VariantText>{`<ProgressIndicator
              label={'Account setup is in progress'}
              value={25}
              valueLabel="25% done"
            />`}</VariantText>
        </Header>
        <View style={styles.outerContainer}>
          <View style={styles.innerContainer}>
            <ProgressIndicator
              label={'Account setup is in progress'}
              value={25}
              valueLabel="25% done"
            />
          </View>
        </View>
      </>
    );
  };

  const ProgressIndicatorWithVariant: React.FC = () => {
    return (
      <>
        <Header>
          ProgressIndicator
          <VariantText>
            {' '}
            (with label, value, valueLabel and variant){'\n\n '}
          </VariantText>
          <VariantText>{`<ProgressIndicator
              label={'Account setup is in progress'}
              value={25}
              valueLabel="25% done"
              variant="info"
            />`}</VariantText>
        </Header>
        <View style={styles.outerContainer}>
          <View style={styles.innerContainer}>
            <ProgressIndicator
              label={'Account setup is in progress'}
              value={25}
              valueLabel="25% done"
              variant="info"
            />
          </View>
        </View>
      </>
    );
  };

  const ProgressIndicatorWithSuccessVariant: React.FC = () => {
    return (
      <>
        <Header>
          ProgressIndicator
          <VariantText> (variant="success"){'\n\n '}</VariantText>
          <VariantText>{`<ProgressIndicator
              label={'Account setup is in progress'}
              value={100}
              valueLabel="100% done"
              variant="success"
            />`}</VariantText>
        </Header>
        <View style={styles.outerContainer}>
          <View style={styles.innerContainer}>
            <ProgressIndicator
              label={'Account setup is done'}
              value={100}
              valueLabel="100% done"
              variant="success"
            />
          </View>
        </View>
      </>
    );
  };

  const ProgressIndicatorWithErrorVariant: React.FC = () => {
    return (
      <>
        <Header>
          ProgressIndicator
          <VariantText> (variant="error"){'\n\n '}</VariantText>
          <VariantText>{`<ProgressIndicator
              label={'Blocked by conveyor downtime'}
              value={25}
              valueLabel="25% loaded"
              variant="error"
            />`}</VariantText>
        </Header>
        <View style={styles.outerContainer}>
          <View style={styles.innerContainer}>
            <ProgressIndicator
              label={'Blocked by conveyor downtime'}
              value={25}
              valueLabel="25% loaded"
              variant="error"
            />
          </View>
        </View>
      </>
    );
  };

  const ProgressIndicatorWithWarningVariant: React.FC = () => {
    return (
      <>
        <Header>
          ProgressIndicator
          <VariantText> (variant="warning"){'\n\n '}</VariantText>
          <VariantText>{`<ProgressIndicator
              label={'Your membership will expire soon'}
              value={75}
              valueLabel="3 days left"
              variant="warning"
            />`}</VariantText>
        </Header>
        <View style={styles.outerContainer}>
          <View style={styles.innerContainer}>
            <ProgressIndicator
              label={'Your membership will expire soon'}
              value={75}
              valueLabel="3 days left"
              variant="warning"
            />
          </View>
        </View>
      </>
    );
  };

  const ProgressIndicatorWithValueWarningVariant: React.FC = () => {
    return (
      <>
        <Header>
          ProgressIndicator
          <VariantText> (value is greater than max){'\n\n '}</VariantText>
          <VariantText>{`<ProgressIndicator
              label={'Membership has expired!!'}
              value={175}
              max={150}
              valueLabel="Exceed limit"
              variant="error"
            />`}</VariantText>
        </Header>
        <View style={styles.outerContainer}>
          <View style={styles.innerContainer}>
            <ProgressIndicator
              label={'Membership has expired!!'}
              value={175}
              max={150}
              valueLabel="Exceed limit"
              variant="error"
            />
          </View>
        </View>
      </>
    );
  };

  const ProgressIndicatorWithLongLabel: React.FC = () => {
    return (
      <>
        <Header>
          ProgressIndicator
          <VariantText> (with long text valueLabel){'\n\n '}</VariantText>
          <VariantText>{`<View style={{width: '70%'}}>
              <ProgressIndicator
                variant='info'
                label={'1h 0m planned'}
                value={20}
                valueLabel="long valueLabel with dumy text"
              />
            </View>`}</VariantText>
        </Header>
        <View style={styles.outerContainer}>
          <View style={styles.innerContainer}>
            <View style={{width: '70%'}}>
              <ProgressIndicator
                variant="info"
                label={'1h 0m planned'}
                value={20}
                valueLabel="long valueLabel with dumy text"
              />
            </View>
          </View>
        </View>
      </>
    );
  };

  const ProgressIndicatorWithCustomLabel: React.FC = () => {
    return (
      <>
        <Header>
          ProgressIndicator
          <VariantText> (with Custom label & valueLabel){'\n\n '}</VariantText>
          <VariantText>{`<ProgressIndicator
              value={50}
              variant='success'
              valueLabel={
                <Text style={{color: 'green'}}>
                  long valueLabel with dumy text
                </Text>
              }
              label={
                <Text style={{color: 'green'}}>Lorem Ipsum</Text>
              }
            />`}</VariantText>
        </Header>
        <View style={styles.outerContainer}>
          <View style={styles.innerContainer}>
            <ProgressIndicator
              value={50}
              variant="success"
              valueLabel={
                <Text style={{color: 'green'}}>
                  long valueLabel with dumy text
                </Text>
              }
              label={<Text style={{color: 'green'}}>Lorem Ipsum</Text>}
            />
          </View>
        </View>
      </>
    );
  };

  return (
    <Page>
      <ProgressIndicatorDefault />
      <ProgressIndicatorWithLabel />
      <ProgressIndicatorWithValue />
      <ProgressIndicatorWithValueLabel />
      <ProgressIndicatorWithVariant />
      <ProgressIndicatorWithSuccessVariant />
      <ProgressIndicatorWithErrorVariant />
      <ProgressIndicatorWithWarningVariant />
      <ProgressIndicatorWithValueWarningVariant />
      <ProgressIndicatorWithLongLabel />
      <ProgressIndicatorWithCustomLabel />
    </Page>
  );
};

const styles = StyleSheet.create({
  innerContainer: {
    flex: 1,
    justifyContent: 'space-around',
    flexDirection: 'row',
    padding: 10,
  },
  outerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
  displayCodeBtn: {position: 'absolute', bottom: 0, right: 2},
});

export {ProgressIndicatorRecipes};
