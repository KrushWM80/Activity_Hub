### Collapse
```js
/* Sample code
import * as React from 'react';
import {StyleSheet, SafeAreaView, TextStyle, View} from 'react-native';
import {
  Icons,
  Checkbox,
  colors,
  Body,
  Collapse,
} from '@walmart/gtp-shared-components';
import {Header, Page, Section} from '../components';
const Spacer = () => <View style={ss.spacer} />;

const CollapseScreen: React.FC = () => {
  type Traits = {
    title: string;
    subtitle: string | undefined;
    icon: boolean;
    dividerTop: boolean;
    dividerBottom: boolean;
  };
  const [traits, setTraits] = React.useState<Traits>({
    title: 'Collapse',
    subtitle: undefined,
    icon: false,
    dividerTop: false,
    dividerBottom: false,
  });
  const [isExpanded, setIsExpanded] = React.useState(false);
  const onToggle = () => {
    setIsExpanded(!isExpanded);
  };
  const getTitle = () => {
    const title = traits.title;
    if (traits.subtitle && traits.icon) {
      return `${title} with Subtitle & Icon`;
    } else if (traits.subtitle) {
      return `${title} with Subtitle`;
    } else if (traits.icon) {
      return `${title} with icon`;
    }
    return `${title}`;
  };
  return (
    <SafeAreaView style={ss.container}>
      <Page>
        <View key={'Template'}>
          <Header>Collapse</Header>
          <View style={ss.innerContainer}>
            <Collapse
              title={getTitle()}
              subtitle={traits.subtitle}
              expanded={isExpanded}
              icon={
                traits.icon ? <Icons.InfoCircleIcon size={24} /> : undefined
              }
              dividerTop={traits.dividerTop}
              dividerBottom={traits.dividerBottom}
              onToggle={() => {
                onToggle();
              }}>
              <Body>Collapse content appears underneath the toggle area.</Body>
            </Collapse>
          </View>
        </View>

        <Section>
          <View style={ss.innerContainer}>
            <Checkbox
              label="With Subtitle"
              checked={!!traits.subtitle}
              onPress={() =>
                setTraits({
                  ...traits,
                  subtitle: traits.subtitle ? undefined : 'subTitle',
                })
              }
            />
            <Spacer />
            <Checkbox
              label="With icon"
              checked={traits.icon}
              onPress={() =>
                setTraits({
                  ...traits,
                  icon: !traits.icon,
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
    marginLeft: 16,
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
});

export {CollapseScreen};

*/

import * as React from 'react';
import {Image} from 'react-native';

 <>
  <Image
      source={{
        uri: 'https://gecgithub01.walmart.com/storage/user/77503/files/8daa079a-8e92-46b0-8707-d7c3906eaf43',
        height: 500,
        width: 390,
      }}
  />
</>
```