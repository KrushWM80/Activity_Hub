import * as React from 'react';
import {View, StyleSheet} from 'react-native';

type ButtonContainerProps = {
  children: React.ReactNode;
};

const ButtonContainer: React.FC<ButtonContainerProps> = (
  props: ButtonContainerProps,
) => {
  const {children} = props;
  return <View style={styles.container}>{children}</View>;
};

const styles = StyleSheet.create({
  container: {
    padding: 5,
  },
});

export default ButtonContainer;
