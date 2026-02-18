import * as React from 'react';
import {StyleSheet, View, Text} from 'react-native';

const styles = StyleSheet.create({
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
    <View style={styles.container}>
      <View style={styles.icons}>
        {sortedIcons.map((icon) => (
          <View
            key={`${icon.key} ${icon.props.size}`}
            style={styles.iconWrapper}>
            {icon}
            {!caption ? null : (
              <Text style={styles.sizeName}>{icon.props.size}</Text>
            )}
          </View>
        ))}
      </View>
    </View>
  );
};

export default IconWrapper;
