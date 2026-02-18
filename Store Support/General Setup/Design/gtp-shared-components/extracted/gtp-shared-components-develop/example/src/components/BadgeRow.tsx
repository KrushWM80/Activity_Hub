import * as React from 'react';
import {View, StyleSheet} from 'react-native';
import SubHeader from './SubHeader';

export const BadgeRow = ({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) => (
  <View style={styles.container}>
    <View style={styles.subheader}>
      <SubHeader>{title}</SubHeader>
    </View>
    <View style={styles.badges}>{children}</View>
  </View>
);

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    width: '100%',
  },
  subheader: {
    alignItems: 'flex-start',
  },
  badges: {
    width: '50%',
    justifyContent: 'space-between',
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 60,
  },
});
