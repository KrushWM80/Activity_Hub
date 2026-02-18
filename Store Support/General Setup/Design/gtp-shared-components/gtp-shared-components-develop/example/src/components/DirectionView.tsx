import * as React from 'react';
import {View, StyleSheet} from 'react-native';

export const DirectionView = ({
  children,
  direction = 'row',
}: {
  children: React.ReactNode;
  direction?: 'row' | 'column' | 'column-reverse' | 'row-reverse';
}) => (
  <View style={[styles.container, {flexDirection: direction}]}>{children}</View>
);

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'space-around',
    width: '100%',
  },
});
