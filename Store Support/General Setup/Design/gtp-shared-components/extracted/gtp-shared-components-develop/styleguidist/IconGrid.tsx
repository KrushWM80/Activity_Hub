/* eslint-disable react-native/no-inline-styles */
import * as React from 'react';
import {StyleSheet, Text, View} from 'react-native';

import {DeprecatedBadge} from '../example/src/components/DeprecatedBadge';
import {Icons} from '../src';
import {colors} from '../src/next/utils';

const IconGridItem = ({children}: {children: React.ReactNode}) => (
  <View style={ss.item}>{children}</View>
);

const IconGrid: React.FC = () => {
  const allIcons = (Object.keys(Icons) as Array<keyof typeof Icons>).map(
    (key: keyof typeof Icons) => {
      const Icon: React.ElementType = Icons[key];
      return (
        <IconGridItem key={key as string}>
          <Icon size={32} />
          <View style={{height: 16, paddingHorizontal: 8, marginTop: 8}}>
            <Text>{key}</Text>
          </View>
          {Icon.displayName?.includes('dep') && <DeprecatedBadge />}
        </IconGridItem>
      );
    },
  );

  return <View style={ss.container}>{allIcons}</View>;
};

const ss = StyleSheet.create({
  container: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  item: {
    width: '18%',
    minWidth: 150,
    paddingVertical: 16,
    alignItems: 'center',
    backgroundColor: colors.gray['10'],
    borderRadius: 4,
    margin: 5,
  },
});

IconGrid.displayName = 'IconGrid';

export {IconGrid};
