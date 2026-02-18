import * as React from 'react';
import {View, StyleSheet, SafeAreaView, ScrollView, Text} from 'react-native';
import {Section} from '../components/Section';
import {colors, Icons} from '@walmart/gtp-shared-icons';
import {IconBox} from '../components/IconBox';
import {DeprecatedBadge} from '../components/DeprecatedBadge';

const IconsScreen: React.FC = () => {
  return (
    <SafeAreaView style={ss.container}>
      <ScrollView contentContainerStyle={ss.scrollContent}>
        <Section inset={false} color={'white'} horizontal space={false}>
          {(Object.keys(Icons) as Array<keyof typeof Icons>).map(
            (key: keyof typeof Icons) => {
              const Icon: React.ElementType = Icons[key];
              return (
                <IconBox key={key}>
                  <Icon size="large" />
                  <View style={ss.caption}>
                    <Text style={ss.text}>
                      {(key as string).replace(/Icon/, '')}
                    </Text>
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

const ss = StyleSheet.create({
  container: {
    backgroundColor: colors.white,
  },
  scrollContent: {
    flex: 0,
    flexDirection: 'row',
    flexWrap: 'wrap',
    backgroundColor: 'white',
    alignItems: 'flex-start',
    justifyContent: 'space-between',
    marginHorizontal: 16,
  },
  caption: {
    height: 16,
    paddingHorizontal: 8,
    marginTop: 8,
  },
  text: {
    color: colors.black,
  },
  badge: {
    position: 'absolute',
    top: 4,
    right: 8,
    color: 'red',
    borderWidth: 0.5,
    borderColor: 'red',
    paddingHorizontal: 2,
    borderRadius: 10,
  },
});

export {IconsScreen};
