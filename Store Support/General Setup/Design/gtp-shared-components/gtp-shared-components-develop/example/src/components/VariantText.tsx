import * as React from 'react';
import {Text, StyleSheet} from 'react-native';

type VariantTextProps = {
  children: React.ReactNode;
};
const VariantText: React.FC<VariantTextProps> = (props: VariantTextProps) => {
  const {children} = props;
  return <Text style={styles.variantText}>{children}</Text>;
};

const styles = StyleSheet.create({
  variantText: {
    fontSize: 15,
  },
});

export {VariantText};
