import * as React from 'react';
import {StyleSheet, SafeAreaView, TextStyle, View} from 'react-native';
import {
  Checkbox,
  colors,
  Body,
  SeeDetails,
} from '@walmart/gtp-shared-components';

import {Header, Page, Section} from '../components';
const Spacer = () => <View style={ss.spacer} />;

const SeeDetailsPlayground: React.FC = () => {
  type Traits = {
    showText?: string | undefined;
    hideText?: string | undefined;
    dividerTop?: boolean;
    dividerBottom?: boolean;
    customStyle?: boolean;
    title_style?: TextStyle;
  };
  const [traits, setTraits] = React.useState<Traits>({
    showText: undefined,
    hideText: undefined,
    dividerTop: false,
    dividerBottom: false,
    customStyle: false,
    title_style: {},
  });
  const [isExpanded, setIsExpanded] = React.useState(false);
  const onToggle = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <SafeAreaView style={ss.container}>
      <Page>
        <View key={'Template'}>
          <Header>SeeDetails</Header>
          <View style={ss.innerContainer}>
            <SeeDetails
              expanded={isExpanded}
              showText={traits.showText}
              hideText={traits.hideText}
              dividerTop={traits.dividerTop}
              size={traits.customStyle ? 'small' : 'large'}
              UNSAFE_style={traits.customStyle ? ss.seeDetailsStyle : {}}
              dividerBottom={traits.dividerBottom}
              title_style={traits.customStyle ? traits.title_style : {}}
              onToggle={() => {
                onToggle();
              }}>
              <Body>Collapse content appears underneath the toggle area.</Body>
            </SeeDetails>
          </View>
        </View>

        <Section>
          <View style={ss.innerContainer}>
            <Checkbox
              label="With showText"
              checked={!!traits.showText}
              onPress={() =>
                setTraits({
                  ...traits,
                  showText: traits.showText ? undefined : 'Show My Content',
                })
              }
            />
            <Spacer />
            <Checkbox
              label="With hideText"
              checked={!!traits.hideText}
              onPress={() =>
                setTraits({
                  ...traits,
                  hideText: traits.hideText ? undefined : 'Hide My Content',
                })
              }
            />
            <Spacer />
            <Checkbox
              label="with dividerTop"
              checked={traits.dividerTop}
              onPress={() =>
                setTraits({
                  ...traits,
                  dividerTop: !traits.dividerTop,
                })
              }
            />
            <Spacer />
            <Checkbox
              label="With dividerBottom"
              checked={traits.dividerBottom}
              onPress={() =>
                setTraits({
                  ...traits,
                  dividerBottom: !traits.dividerBottom,
                })
              }
            />
            <Spacer />
            <Checkbox
              label="With title_style"
              checked={traits.customStyle}
              onPress={() =>
                setTraits({
                  ...traits,
                  customStyle: !traits.customStyle,
                  title_style: ss.seeDetailsTitleStyle,
                })
              }
            />
            <Spacer />
          </View>
        </Section>
      </Page>
    </SafeAreaView>
  );
};

const ss = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.gray['100'],
    height: '15%',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderTopWidth: 1,
    borderLeftWidth: 1,
    borderRightWidth: 1,
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
    borderTopColor: colors.blue['90'],
    borderLeftColor: colors.blue['90'],
    borderRightColor: colors.blue['90'],
    paddingRight: 16,
    paddingVertical: 8,
    marginTop: 20,
    backgroundColor: colors.white,
  },
  headerText: {
    fontSize: 20,
    fontWeight: '500',
    color: colors.blue['90'],
    textAlign: 'left',
    paddingVertical: 10,
    marginLeft: 12,
  },
  imageContainer: {
    backgroundColor: colors.gray['100'],
    borderRadius: 16,
    marginHorizontal: 16,
    paddingVertical: 16,
    marginTop: 8,
  },
  image: {
    width: '100%',
    resizeMode: 'contain',
  },
  innerContainer: {
    marginHorizontal: 16,
    padding: 8,
    justifyContent: 'flex-start',
  },
  spacer: {
    height: 8,
  },
  radioHeaderText: {
    color: colors.blue['90'],
  } as TextStyle,
  rbGroup: {
    marginLeft: 16,
  },
  seeDetailsStyle: {
    flex: 1,
    justifyContent: 'flex-end',
    alignItems: 'flex-end',
    marginBottom: -8,
    marginRight: -17,
  },
  seeDetailsTitleStyle: {
    fontFamily: 'Bogle-Regular',
    fontSize: 12,
    fontWeight: '400',
    color: colors.black,
    lineHeight: 15,
    marginRight: -4,
  },
});

export {SeeDetailsPlayground};
