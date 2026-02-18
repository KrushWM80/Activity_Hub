import * as React from 'react';
import {Text, View, StyleSheet} from 'react-native';
import {colors} from '@walmart/gtp-shared-icons';

type HeaderProps = {
  children: React.ReactNode;
};
const Header: React.FC<HeaderProps> = (props: HeaderProps) => {
  const {children} = props;
  return (
    <View style={styles.container}>
      <Text style={styles.text}>{children}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    borderTopWidth: 1,
    borderLeftWidth: 1,
    borderRightWidth: 1,
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
    borderTopColor: colors.gray['10'],
    borderLeftColor: colors.gray['10'],
    borderRightColor: colors.gray['10'],
    marginTop: 20,
    justifyContent: 'center',
  },
  text: {
    fontSize: 20,
    fontWeight: '500',
    color: colors.blue[100],
    textAlign: 'left',
    paddingVertical: 10,
    marginLeft: 12,
  },
});

export {Header};
