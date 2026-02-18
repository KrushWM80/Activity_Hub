import * as React from 'react';
import {View, StyleSheet, SafeAreaView, ScrollView} from 'react-native';
import {Section} from '../components';
import {Caption, Icons} from '@walmart/gtp-shared-components';
import {IconBox} from '../components/IconBox';
import {DeprecatedBadge} from '../components/DeprecatedBadge';

const IconsOverview: React.FC = () => {
  return (
    <SafeAreaView>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Section inset={false} horizontal space={false}>
          {(Object.keys(Icons) as Array<keyof typeof Icons>).map(
            (key: keyof typeof Icons) => {
              const Icon: React.ElementType = Icons[key];
              return (
                <IconBox key={key}>
                  <Icon size={32} />
                  <View style={styles.caption}>
                    <Caption>{key.replace(/Icon/, '')}</Caption>
                  </View>
                  {Icon.displayName?.includes('dep') && <DeprecatedBadge />}
                </IconBox>
              );
            },
          )}
        </Section>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  scrollContent: {
    flex: 0,
    flexDirection: 'row',
    flexWrap: 'wrap',
    alignItems: 'flex-start',
    justifyContent: 'space-between',
    marginHorizontal: 16,
  },
  caption: {
    height: 16,
    paddingHorizontal: 8,
    marginTop: 8,
  },
});

export {IconsOverview};
