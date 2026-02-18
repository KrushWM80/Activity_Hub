import * as React from 'react';
import {StyleSheet, View, ViewStyle} from 'react-native';

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
  },
});

const HorizontalContainer = ({
  background,
  style,
  children,
}: React.PropsWithChildren<{background: string; style: ViewStyle}>) => (
  <View
    style={[
      styles.container,
      background ? {backgroundColor: background} : {},
      style,
    ]}>
    {children}
  </View>
);

export default HorizontalContainer;
