import * as React from 'react';
import {View, StyleSheet} from 'react-native';
import {colors, Icons, StyledText} from '@walmart/gtp-shared-components';
import {Header, Page, VariantText} from '../components';

const Spacer = () => <View style={ss.spacer} />;

const DefaultBadge: React.FC = () => {
  return (
    <>
      <Header>
        StyledText (Default){'\n  '}
        <VariantText>{`<StyledText>{children}</StyledText>`}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Spacer />
          <StyledText>Gray large StyledText with Check Icon</StyledText>
        </View>
      </View>
    </>
  );
};

const SizeBadge: React.FC = () => {
  return (
    <>
      <Header>
        StyledText (size){'\n  '}
        <VariantText>{`<StyledText size='large'>{children}</StyledText>`}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Spacer />
          <StyledText size="large">
            Gray large StyledText with Check Icon
          </StyledText>
        </View>
      </View>
    </>
  );
};

const LeadingBadge: React.FC = () => {
  return (
    <>
      <Header>
        StyledText (leading & size){'\n  '}
        <VariantText>{`<StyledText size='large' leading={<Icons.CheckIcon />}>{children}</StyledText>`}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Spacer />
          <StyledText size="large" leading={<Icons.CheckIcon />}>
            Gray large StyledText with Check Icon
          </StyledText>
        </View>
      </View>
    </>
  );
};

const ColorBadge: React.FC = () => {
  return (
    <>
      <Header>
        StyledText (color & leading & size){'\n  '}
        <VariantText>{`<StyledText color='blue' size='large' leading={<Icons.CheckIcon />}>{children}</StyledText>`}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Spacer />
          <StyledText color="green" size="large" leading={<Icons.CheckIcon />}>
            Gray large StyledText with Check Icon
          </StyledText>
        </View>
      </View>
    </>
  );
};

const StyledTextRecipes: React.FC = () => {
  return (
    <Page>
      <DefaultBadge />
      <SizeBadge />
      <LeadingBadge />
      <ColorBadge />
    </Page>
  );
};

const ss = StyleSheet.create({
  section: {
    paddingVertical: 12,
    paddingHorizontal: 16,
  },
  innerContainer: {
    padding: 10,
    alignItems: 'flex-start',
  },
  outerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
  spacer: {
    height: 8,
  },
});

export {StyledTextRecipes};
