Chips allow users to make selections, filter content, or trigger actions.

```js
import {StyleSheet, View, Text} from 'react-native';
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

const [isSingleChipSmallSelected, setIsSingleChipSmallSelected] =
  React.useState(false);
const [isSingleChipLargeSelected, setIsSingleChipLargeSelected] =
  React.useState(false);

const onChipPressSmall = (chipId, selected) => {
  setIsSingleChipSmallSelected(!isSingleChipSmallSelected);
  console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
};

const onChipPressLarge = (chipId, selected) => {
  setIsSingleChipLargeSelected(!isSingleChipLargeSelected);
  console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
};

<>
  <Text style={styles.header}>Chip</Text>
  <View style={styles.outerContainer}>
    <View style={styles.innerContainer}>
      <Chip id={0} size="small" children="Sam's Choice" selected={isSingleChipSmallSelected} onPress={onChipPressSmall}/>
      <Chip id={0} size="small" disabled children="Sam's Choice" />
    </View>
    <View style={styles.innerContainer}>
      <Chip id={1} size="large" children="Sam's Choice"  selected={isSingleChipLargeSelected} onPress={onChipPressLarge}/>
      <Chip id={1} size="large" disabled children="Sam's Choice" />
    </View>
  </View>
</>
```

```js
import {StyleSheet, View, Text} from 'react-native';
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

const [isSingleChipSmallSelected, setIsSingleChipSmallSelected] =
  React.useState(false);
const [isSingleChipLargeSelected, setIsSingleChipLargeSelected] =
  React.useState(false);

const onChipPressSmall = (chipId, selected) => {
  setIsSingleChipSmallSelected(!isSingleChipSmallSelected);
  console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
};

const onChipPressLarge = (chipId, selected) => {
  setIsSingleChipLargeSelected(!isSingleChipLargeSelected);
  console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
};

<>
  <Text style={styles.header}>Chip with leading icon</Text>
  <View style={styles.outerContainer}>
    <View style={styles.innerContainer}>
      <Chip id={0} size="small" children="Sam's Choice" selected={isSingleChipSmallSelected} onPress={onChipPressSmall} leading={<Icons.ClockIcon />} />
      <Chip id={0} size="small" disabled children="Sam's Choice" leading={<Icons.ClockIcon />} />
    </View>
    <View style={styles.innerContainer}>
      <Chip id={1} size="large" children="Sam's Choice"  selected={isSingleChipLargeSelected} onPress={onChipPressLarge} leading={<Icons.ClockIcon />} />
      <Chip id={1} size="large" disabled children="Sam's Choice" leading={<Icons.ClockIcon />} />
    </View>
  </View>
</>
```

```js
import {StyleSheet, View, Text} from 'react-native';
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

const [isSingleChipSmallSelected, setIsSingleChipSmallSelected] =
  React.useState(false);
const [isSingleChipLargeSelected, setIsSingleChipLargeSelected] =
  React.useState(false);

const onChipPressSmall = (chipId, selected) => {
  setIsSingleChipSmallSelected(!isSingleChipSmallSelected);
  console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
};

const onChipPressLarge = (chipId, selected) => {
  setIsSingleChipLargeSelected(!isSingleChipLargeSelected);
  console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
};

<>
  <Text style={styles.header}>Chip with trailing icon</Text>
  <View style={styles.outerContainer}>
    <View style={styles.innerContainer}>
      <Chip id={0} size="small" children="Sam's Choice" selected={isSingleChipSmallSelected} onPress={onChipPressSmall} trailing={<Icons.HomeIcon />} />
      <Chip id={0} size="small" disabled children="Sam's Choice" trailing={<Icons.HomeIcon />} />
    </View>
    <View style={styles.innerContainer}>
      <Chip id={1} size="large" children="Sam's Choice"  selected={isSingleChipLargeSelected} onPress={onChipPressLarge} trailing={<Icons.HomeIcon />} />
      <Chip id={1} size="large" disabled children="Sam's Choice" trailing={<Icons.HomeIcon />} />
    </View>
  </View>
</>
```

```js
import {StyleSheet, View, Text} from 'react-native';
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

const [isSingleChipSmallSelected, setIsSingleChipSmallSelected] =
  React.useState(false);
const [isSingleChipLargeSelected, setIsSingleChipLargeSelected] =
  React.useState(false);

const onChipPressSmall = (chipId, selected) => {
  setIsSingleChipSmallSelected(!isSingleChipSmallSelected);
  console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
};

const onChipPressLarge = (chipId, selected) => {
  setIsSingleChipLargeSelected(!isSingleChipLargeSelected);
  console.log(`${chipId} ${selected ? 'selected' : 'default'}`);
};

<>
  <Text style={styles.header}>Chip with leading and trailing icons</Text>
  <View style={styles.outerContainer}>
    <View style={styles.innerContainer}>
      <Chip id={0} size="small" children="Sam's Choice" selected={isSingleChipSmallSelected} onPress={onChipPressSmall} leading={<Icons.StarIcon />} trailing={<Icons.CheckIcon />} />
      <Chip id={0} size="small" disabled children="Sam's Choice" leading={<Icons.StarIcon />} trailing={<Icons.CheckIcon />} />
    </View>
    <View style={styles.innerContainer}>
      <Chip id={1} size="large" children="Sam's Choice"  selected={isSingleChipLargeSelected} onPress={onChipPressLarge} leading={<Icons.StarIcon />} trailing={<Icons.CheckIcon />} />
      <Chip id={1} size="large" disabled children="Sam's Choice" leading={<Icons.StarIcon />} trailing={<Icons.CheckIcon />} />
    </View>
  </View>
</>
```

```js
import {StyleSheet, View, Text} from 'react-native';
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
  <Text style={styles.header}>Chip with disabled onPress, selected</Text>
  <View style={styles.outerContainer}>
    <View style={styles.innerContainer}>
      <Chip id={0} size="small" children="Sam's Choice" selected disableOnPress leading={<Icons.StarIcon />} trailing={<Icons.CheckIcon />} />
    </View>
    <View style={styles.innerContainer}>
      <Chip id={1} size="large" children="Sam's Choice"  selected disableOnPress leading={<Icons.StarIcon />} trailing={<Icons.CheckIcon />} />
    </View>
  </View>

  <Text style={styles.header}>Chip with disabled onPress, default</Text>
  <View style={styles.outerContainer}>
    <View style={styles.innerContainer}>
      <Chip id={0} size="small" children="Sam's Choice" disableOnPress leading={<Icons.StarIcon />} trailing={<Icons.CheckIcon />} />
    </View>
    <View style={styles.innerContainer}>
      <Chip id={1} size="large" children="Sam's Choice" disableOnPress leading={<Icons.StarIcon />} trailing={<Icons.CheckIcon />} />
    </View>
  </View>
</>
```