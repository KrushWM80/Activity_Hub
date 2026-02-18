import * as React from 'react';
import {View, StyleSheet, StyleProp, ViewStyle} from 'react-native';
import SubHeader from './SubHeader';

const TagRow = ({
  title,
  children,
  UNSAFE_style = {},
}: {
  title: string;
  children: React.ReactNode;
  UNSAFE_style?: StyleProp<ViewStyle>;
}) => (
  <View style={[styles.container, UNSAFE_style]}>
    <SubHeader>{title}</SubHeader>
    <View style={styles.children}>{children}</View>
  </View>
);

const styles = StyleSheet.create({
  container: {flexDirection: 'column', alignItems: 'center'},
  children: {flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'center'},
});

export {TagRow};
