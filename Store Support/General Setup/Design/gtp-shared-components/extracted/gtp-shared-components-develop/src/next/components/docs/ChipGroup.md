Chip group displays multiple related chips in a horizontal row to help with arrangement and spacing.

```js
import {StyleSheet, View, Text, ScrollView} from 'react-native';
import {Chip, Icons, colors} from '@walmart/gtp-shared-components';

const styles = StyleSheet.create({
  innerContainer: {
    flex: 1,
    justifyContent: 'space-around',
    flexDirection: 'row',
    padding: 10,
  },
  outerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
  header: {
    marginTop: 24,
  },
});

<>
  <Text style={styles.header}>ChipGroup (single selection)</Text>

  <View style={styles.outerContainer}>
    <View style={styles.innerContainer} />
      <ChipGroup
        onPress={selectedIds =>
          console.log('--- selected Chips: ', selectedIds)
        }>
        <Chip id={0}>All</Chip>
        <Chip id={1}>Last 7 Days</Chip>
        <Chip id={2}>Last Month</Chip>
      </ChipGroup>
    </View>

  <Text style={styles.header}>ChipGroup (multiple selection)</Text>

  <View style={styles.outerContainer}>
    <View style={styles.innerContainer} />
      <ChipGroup
        multiple
        onPress={selectedIds =>
          console.log('--- selected Chips: ', selectedIds)
        }>
        <Chip id={0}>All</Chip>
        <Chip id={1}>Last 7 Days</Chip>
        <Chip id={2}>Last Month</Chip>
      </ChipGroup>
    </View>
</>;
```
