import * as React from 'react';
import {View, StyleSheet} from 'react-native';
import {colors} from '@walmart/gtp-shared-icons';

const IconBox = ({children}: {children: React.ReactNode}) => (
  <View style={styles.iconBox}>{children}</View>
);

const styles = StyleSheet.create({
  iconBox: {
    width: '30%',
    paddingVertical: 22,
    alignItems: 'center',
    backgroundColor: colors.gray['5'],
    borderRadius: 20,
    marginVertical: 5,
    borderWidth: 0.5,
    borderColor: colors.blue['80'],
  },
});

export {IconBox};
