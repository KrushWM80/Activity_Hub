import * as React from 'react';
import {StyleSheet, Text} from 'react-native';
import {useTheme} from '@react-navigation/native';

type SubHeaderProps = {
  children: React.ReactNode;
};

export default function SubHeader(props: SubHeaderProps) {
  const theme = useTheme();

  return (
    <Text style={[styles.text, {color: theme.colors.text}]}>
      {props.children}
    </Text>
  );
}

const styles = StyleSheet.create({
  text: {
    fontSize: 12,
    textAlign: 'center',
    marginVertical: 2,
  },
});
