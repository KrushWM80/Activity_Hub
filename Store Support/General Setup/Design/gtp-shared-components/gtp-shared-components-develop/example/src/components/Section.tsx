/* eslint-disable react-native/no-inline-styles */
import * as React from 'react';
import {View, ViewProps, StyleSheet, useColorScheme} from 'react-native';
import {colors} from '@walmart/gtp-shared-components';

type SectionProps = ViewProps & {
  color?: string;
  space?: false | number;
  horizontal?: boolean;
  wrap?: boolean;
  inset?: boolean;
  children: React.ReactNode;
};

const Section: React.FC<SectionProps> = (props: SectionProps) => {
  const isDark = useColorScheme() === 'dark';

  const {
    color = isDark ? 'transparent' : colors.gray['5'],
    space = 5,
    style,
    horizontal,
    inset = true,
    children,
    ...rest
  } = props;

  const childrenDisplay = !space
    ? children
    : React.Children.map(children, child => (
        <View
          style={{
            [horizontal ? 'marginHorizontal' : 'marginVertical']: space,
          }}>
          {child}
        </View>
      ));

  return (
    <View
      style={[
        styles.container,
        {backgroundColor: color, paddingHorizontal: inset ? 10 : 0},
        color === 'white' || isDark
          ? {borderWidth: 1, borderColor: colors.gray['10']}
          : {},
        style,
      ]}
      {...rest}>
      <View
        style={{
          flexDirection: horizontal ? 'row' : 'column',
          alignSelf: horizontal ? 'center' : 'stretch',
          ...(horizontal ? styles.horizontalContent : {}),
        }}>
        {childrenDisplay}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    paddingVertical: 10,
  },
  horizontalContent: {
    flexWrap: 'wrap',
    flex: 1,
    alignItems: 'flex-start',
    justifyContent: 'space-between',
  },
});

export {Section};
