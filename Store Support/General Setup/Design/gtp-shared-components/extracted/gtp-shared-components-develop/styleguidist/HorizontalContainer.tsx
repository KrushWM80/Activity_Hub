import * as React from 'react';
import {StyleSheet, View, ViewStyle} from 'react-native';

type HorizontalContainerProps = React.PropsWithChildren<{
  background: string;
  style: ViewStyle;
}>;

const HorizontalContainer: React.FC<HorizontalContainerProps> = (props) => {
  const {background, style, children} = props;

  return (
    <View
      style={[
        ss.container,
        background ? {backgroundColor: background} : {},
        style,
      ]}>
      {children}
    </View>
  );
};

const ss = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
  },
});

export {HorizontalContainer};
