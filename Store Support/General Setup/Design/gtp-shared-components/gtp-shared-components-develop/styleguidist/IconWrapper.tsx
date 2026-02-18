import * as React from 'react';
import {StyleSheet, Text, View} from 'react-native';

const IconWrapper = ({
  children,
  caption = true,
}: {
  children: React.ReactElement | Array<React.ReactElement>;
  caption: boolean;
}) => {
  const sortedIcons = (
    React.Children.toArray(children) as Array<React.ReactElement>
  ).sort((a, b) => a.props.size - b.props.size);
  return (
    <View style={ss.container}>
      <View style={ss.icons}>
        {sortedIcons.map((icon) => (
          <View key={`${icon.key} ${icon.props.size}`} style={ss.iconWrapper}>
            {icon}
            {!caption ? null : (
              <Text style={ss.sizeName}>{icon.props.size}</Text>
            )}
          </View>
        ))}
      </View>
    </View>
  );
};

const ss = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    flexWrap: 'wrap',
  },
  icons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  iconWrapper: {
    justifyContent: 'space-between',
    paddingHorizontal: 12,
  },
  item: {
    padding: 16,
    width: 260,
  },
  sizeName: {
    marginTop: 16,
    textAlign: 'center',
  },
});

IconWrapper.displayName = 'IconWrapper';

export {IconWrapper};
