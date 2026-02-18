import * as React from 'react';
import {View, ViewStyle} from 'react-native';

type WrapperProps = React.PropsWithChildren<{
  style: ViewStyle;
}>;

const Wrapper: React.FC<WrapperProps> = (props) => {
  const {style, children, ...rest} = props;
  return (
    <View style={style} {...rest}>
      {children}
    </View>
  );
};

export default Wrapper;
