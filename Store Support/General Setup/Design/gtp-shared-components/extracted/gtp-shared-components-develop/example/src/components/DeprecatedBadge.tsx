import * as React from 'react';
import {Text, StyleSheet} from 'react-native';

const DeprecatedBadge = () => {
  return <Text style={styles.badge}>dep</Text>;
};

const styles = StyleSheet.create({
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

DeprecatedBadge.displayName = 'DeprecatedBadge';
export {DeprecatedBadge};
