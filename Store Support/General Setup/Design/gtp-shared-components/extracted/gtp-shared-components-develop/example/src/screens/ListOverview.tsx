import * as React from 'react';
import {Header} from '../components';
import {View, Image, Pressable, StyleSheet} from 'react-native';
import {
  List,
  ListItem,
  Icons,
  Button,
  IconButton,
  Checkbox,
  Body,
  Tag,
  colors,
} from '@walmart/gtp-shared-components';
import {displayPopupAlert, miniAppListData} from './screensFixtures';

const ListOverview = () => {
  const leadingItem = (
    id: number,
    isReturnable: boolean,
    isSelected: boolean,
  ) => {
    return (
      <View style={styles.leading}>
        <Checkbox
          key={id}
          UNSAFE_style={isReturnable ? {} : styles.hidden}
          checked={isSelected}
          disabled={!isReturnable}
        />
        <Image
          style={styles.leadingImage}
          source={require('../assets').livingdesign}
        />
        {/* <Icons.TruckIcon UNSAFE_style={styles.leadingImage} /> */}
      </View>
    );
  };
  const contentItem = (
    isReturnable: boolean,
    productName: string,
    displayUpc: string,
    isReturned: boolean,
  ) => {
    return (
      <View style={styles.content}>
        <Body
          size="small"
          UNSAFE_style={[
            isReturnable ? styles.textEnabled : styles.textDisabled,
          ]}>
          {productName}
        </Body>
        <Body
          size="small"
          UNSAFE_style={[
            isReturnable ? styles.textEnabled : styles.textDisabled,
          ]}>
          {displayUpc}
        </Body>
        {!isReturnable && !isReturned && (
          <Tag
            variant="tertiary"
            color="red"
            leading={<Icons.ExclamationCircleIcon color={'red'} />}>
            {'Not eligible for return'}
          </Tag>
        )}
        {!isReturnable && isReturned && (
          <Tag
            variant="tertiary"
            color="gray"
            leading={<Icons.InfoCircleIcon color={'gray'} />}>
            {'Returned'}
          </Tag>
        )}
      </View>
    );
  };
  const trailingItem = (
    isReturnable: boolean,
    currencyAmount: string,
    isReturned: boolean,
  ) => {
    return (
      <View style={styles.trailing}>
        <Body
          size="small"
          weight="700"
          UNSAFE_style={
            isReturnable ? styles.textEnabled : styles.textDisabled
          }>
          {currencyAmount}
        </Body>
        {isReturned && (
          <View style={styles.buttonContainer}>
            <Button
              size="small"
              variant="tertiary"
              onPress={() => {}}
              testID={'itemList.reprint'}>
              {'Reprint slip'}
            </Button>
          </View>
        )}
      </View>
    );
  };

  return (
    <>
      <Header>List</Header>
      <List>
        <ListItem
          leading={<Icons.BoxIcon />}
          title="Potato"
          trailing={
            <Button
              variant="tertiary"
              onPress={() =>
                displayPopupAlert('Action', 'Action1 button pressed')
              }>
              Action1
            </Button>
          }>
          French fries are delicious, French fries keep customers happy without
          dipping into restaurant profit margins.
        </ListItem>
        <ListItem leading={<Icons.BoxIcon />} title="Potato">
          French fries are deliciousFrench fries are delicious French fries are
          delicious.
        </ListItem>
        <ListItem
          title="Potato"
          trailing={
            <IconButton
              children={<Icons.ChevronRightIcon />}
              size="small"
              onPress={() => displayPopupAlert('Action', 'icon button pressed')}
            />
          }>
          French fries are delicious.
        </ListItem>
        <ListItem title="Potato">
          French fries are deliciousFrench fries are delicious French fries are
          delicious.
        </ListItem>
        <ListItem>
          French fries are deliciousFrench fries are delicious French fries are
          delicious.
        </ListItem>
      </List>
      <Header>List Items Array</Header>
      <List>
        {miniAppListData.map(item => {
          const {
            id,
            isReturnable,
            isReturned,
            isSelected,
            productName,
            displayUpc,
            currencyAmount,
          } = item;
          return (
            <Pressable
              key={`Item-list-${id}`}
              onPress={() => {}}
              testID={`ItemListPressableContainer${id}`}>
              <ListItem
                leading={leadingItem(id, isReturnable, isSelected)}
                trailing={trailingItem(
                  isReturnable,
                  currencyAmount,
                  isReturned,
                )}
                key={id}>
                <>
                  {contentItem(
                    isReturnable,
                    productName,
                    displayUpc,
                    isReturned,
                  )}
                </>
              </ListItem>
            </Pressable>
          );
        })}
      </List>
    </>
  );
};
const styles = StyleSheet.create({
  textEnabled: {
    color: colors.gray['160'],
  },
  textDisabled: {
    color: colors.gray['100'],
  },
  content: {
    flex: 1,
  },
  leading: {
    flexDirection: 'row',
    justifyContent: 'flex-start',
    alignItems: 'center',
    paddingLeft: 8,
  },
  hidden: {
    opacity: 0,
  },
  leadingImage: {
    marginHorizontal: 8,
    width: 64,
    height: 64,
  },
  trailing: {
    alignItems: 'flex-end',
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
  },
});

export {ListOverview};
