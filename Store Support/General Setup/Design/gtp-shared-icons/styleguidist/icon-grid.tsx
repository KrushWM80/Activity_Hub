import * as React from 'react';
import {View, ViewStyle, Text, TextStyle} from 'react-native';
import {Icons} from '../src';
import colors from '../src/theme/colors.json';
import {DeprecatedBadge} from '../example/src/components/DeprecatedBadge';

const IconGridItem = ({children}: {children: React.ReactNode}) => (
  <View style={ss.item}>{children}</View>
);

export default class IconGrid extends React.Component {
  render() {
    const allIcons = (Object.keys(Icons) as Array<keyof typeof Icons>).map(
      (key: keyof typeof Icons) => {
        const Icon = Icons[key];
        return (
          <IconGridItem key={key as string}>
            <Icon size={32} />
            <View style={ss.textContainer}>
              <Text style={ss.text}>{key}</Text>
            </View>
            {Icon.displayName?.includes('dep') && <DeprecatedBadge />}
          </IconGridItem>
        );
      },
    );

    return <View style={ss.container}>{allIcons}</View>;
  }
}

const ss: Record<string, ViewStyle> = {
  container: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  item: {
    width: '18%',
    minWidth: 150,
    paddingVertical: 16,
    alignItems: 'center',
    backgroundColor: colors.gray['10'],
    borderRadius: 4,
    margin: 5,
  },
  textContainer: {
    height: 16,
    paddingHorizontal: 8,
    marginTop: 8,
  },
  text: {
    color: colors.black,
  } as TextStyle,
};
