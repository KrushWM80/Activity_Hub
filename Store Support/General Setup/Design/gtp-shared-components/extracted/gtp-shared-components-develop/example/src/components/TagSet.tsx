import * as React from 'react';
import {View, StyleSheet} from 'react-native';
import {Icons} from '@walmart/gtp-shared-icons';

export const TagSet = ({tag}: {tag: React.ReactElement}) => {
  const flagColorRows = [
    [undefined, 'red', 'green'],
    ['spark', 'purple', 'gray'],
  ];
  return (
    <View style={styles.container}>
      {flagColorRows.map((flagColors, i) => (
        <View key={`Row_${i}`} style={styles.flagcolors}>
          {flagColors.map(color =>
            React.cloneElement(tag, {
              key: `Tag_${color || ''}`,
              color,
              leadingIcon: <Icons.BoxIcon />,
              style: {marginLeft: 5},
            }),
          )}
        </View>
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {flexDirection: 'column'},
  flagcolors: {flexDirection: 'row', marginTop: 5},
});
