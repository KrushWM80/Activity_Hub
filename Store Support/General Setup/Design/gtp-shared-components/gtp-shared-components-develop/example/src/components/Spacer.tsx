import React from 'react';
import {StyleSheet, View} from 'react-native';

export const Spacer = () => <View style={styles.spacer} />;

const styles = StyleSheet.create({
  spacer: {
    height: 8,
  },
});
