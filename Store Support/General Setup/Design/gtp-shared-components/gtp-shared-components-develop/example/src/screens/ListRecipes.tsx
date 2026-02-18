import * as React from 'react';
import {View, StyleSheet} from 'react-native';
import {List, ListItem, Icons, Button} from '@walmart/gtp-shared-components';
import {Header, Page, Section, VariantText} from '../components';
import {displayPopupAlert} from './screensFixtures';

const ListRecipes = () => {
  type ListProps = {
    listCode1: boolean;
    listCode2: boolean;
    listCode3: boolean;
    listCode4: boolean;
    listCode5: boolean;
    listCode6: boolean;
  };

  const [listCode, setListCode] = React.useState<ListProps>({
    listCode1: false,
    listCode2: false,
    listCode3: false,
    listCode4: false,
    listCode5: false,
    listCode6: false,
  });
  const defaultListWithOnlyChild = () => {
    const buttonLabel = listCode.listCode1 ? 'Hide code' : 'Show Code';
    const codeSample = `\n<List> \n\t <ListItem> \n\t\t French fries are delicious. \n\t </ListItem> \n </List>`;
    return (
      <>
        <View>
          <Header>
            List, ListItem (with children only){'\n  '}
            {listCode.listCode1 && <VariantText>{codeSample}</VariantText>}
          </Header>
          {displayCodeButton(buttonLabel, 'listCode1')}
        </View>
        <Section space={10}>
          <List>
            <ListItem>French fries are delicious.</ListItem>
          </List>
        </Section>
      </>
    );
  };

  const listWithChildNLeading = () => {
    const buttonLabel = listCode.listCode2 ? 'Hide code' : 'Show Code';
    const codeSample = `\n<List> \n\t <ListItem \n\t\t  leading={<Icons.BoxIcon />} \n\t > \n\t\t\t French fries are delicious. \n\t </ListItem> \n </List>`;
    return (
      <>
        <View>
          <Header>
            List, ListItem (with children and leading){'\n  '}
            {listCode.listCode2 && <VariantText>{codeSample}</VariantText>}
          </Header>
          {displayCodeButton(buttonLabel, 'listCode2')}
        </View>
        <Section space={10}>
          <List>
            <ListItem leading={<Icons.BoxIcon />}>
              French fries are delicious.
            </ListItem>
          </List>
        </Section>
      </>
    );
  };

  const listWithChildLeadingNTitle = () => {
    const buttonLabel = listCode.listCode3 ? 'Hide code' : 'Show Code';
    const codeSample = `\n<List> \n\t <ListItem \n\t\t title="Potato" \n\t\t leading={<Icons.BoxIcon />} \n\t > \n\t\t\t French fries are delicious. \n\t </ListItem> \n </List>`;
    return (
      <>
        <View>
          <Header>
            List, ListItem (with children, leading and title){'\n  '}
            {listCode.listCode3 && <VariantText>{codeSample}</VariantText>}
          </Header>
          {displayCodeButton(buttonLabel, 'listCode3')}
        </View>
        <Section space={10}>
          <List>
            <ListItem title="Potato" leading={<Icons.BoxIcon />}>
              French fries are delicious.
            </ListItem>
          </List>
        </Section>
      </>
    );
  };

  const listWithChildLeadingTitleNTrailing = () => {
    const buttonLabel = listCode.listCode4 ? 'Hide code' : 'Show Code';
    const codeSample = `\n<List> \n\t <ListItem \n\t\t title="Potato" \n\t\t leading={<Icons.BoxIcon />} \n\t\t trailing={<Button \n\t\t\t onPress={actionHandler}> \n\t\t\t\t Action \n\t\t </Button>} \n\t > \n\t\t\t French fries are delicious. \n\t </ListItem> \n </List>`;
    return (
      <>
        <View>
          <Header>
            List, ListItem (with children, leading, title and trailing){'\n  '}
            {listCode.listCode4 && <VariantText>{codeSample}</VariantText>}
          </Header>
          {displayCodeButton(buttonLabel, 'listCode4')}
        </View>
        <Section space={10}>
          <List>
            <ListItem
              title="Potato"
              leading={<Icons.BoxIcon />}
              trailing={
                <Button
                  variant="tertiary"
                  onPress={() =>
                    displayPopupAlert('Action', 'Action button pressed')
                  }>
                  Action
                </Button>
              }>
              French fries are delicious.
            </ListItem>
          </List>
        </Section>
      </>
    );
  };

  const listWithMultipleListItem = () => {
    const buttonLabel = listCode.listCode5 ? 'Hide code' : 'Show Code';
    const codeSample = `\n<List> \n\t <ListItem \n\t\t title="Potato" \n\t\t leading={<Icons.BoxIcon />} \n\t\t trailing={<Button \n\t\t\t onPress={actionHandler}> \n\t\t\t\t Action \n\t\t </Button>} \n\t > \n\t\t\t French fries keep customers happy. \n\t </ListItem> \n\n\t <ListItem \n\t\t title="Potato" \n\t\t leading={<Icons.CartIcon />} \n\t\t trailing={<Button \n\t\t\t onPress={actionHandler}> \n\t\t\t\t Action \n\t\t </Button>} \n\t > \n\t\t\t French fries are delicious. \n\t </ListItem> \n </List>`;
    return (
      <>
        <View>
          <Header>
            List (with multiple ListItem){'\n  '}
            {listCode.listCode5 && <VariantText>{codeSample}</VariantText>}
          </Header>
          {displayCodeButton(buttonLabel, 'listCode5')}
        </View>
        <Section space={10}>
          <List>
            <ListItem
              title="Potato"
              leading={<Icons.BoxIcon />}
              trailing={
                <Button
                  variant="tertiary"
                  onPress={() =>
                    displayPopupAlert('Action', 'Action button pressed')
                  }>
                  Action
                </Button>
              }>
              French fries keep customers happy.
            </ListItem>
            <ListItem
              title="Potato"
              leading={<Icons.CartIcon />}
              trailing={
                <Button
                  variant="tertiary"
                  onPress={() =>
                    displayPopupAlert('Action', 'Action button pressed')
                  }>
                  Action
                </Button>
              }>
              French fries are delicious.
            </ListItem>
          </List>
        </Section>
      </>
    );
  };

  const listWithoutSeparator = () => {
    const buttonLabel = listCode.listCode6 ? 'Hide code' : 'Show Code';
    const codeSample = `\n<List separator={false}> \n\t <ListItem \n\t\t title="Potato" \n\t\t leading={<Icons.BoxIcon />} \n\t\t trailing={<Button \n\t\t\t onPress={actionHandler}> \n\t\t\t\t Action \n\t\t </Button>} \n\t > \n\t\t\t French fries keep customers happy. \n\t </ListItem>  \n\n\t <ListItem \n\t\t title="Potato" \n\t\t leading={<Icons.BoxIcon />} \n\t\t trailing={<Button \n\t\t\t onPress={actionHandler}> \n\t\t\t\t Action \n\t\t </Button>} \n\t > \n\t\t\t French fries are delicious. \n\t </ListItem> \n </List>`;
    return (
      <>
        <View>
          <Header>
            List, ListItem (without separator){'\n  '}
            {listCode.listCode6 && <VariantText>{codeSample}</VariantText>}
          </Header>
          {displayCodeButton(buttonLabel, 'listCode6')}
        </View>
        <Section space={10}>
          <List separator={false}>
            <ListItem
              title="Potato"
              leading={<Icons.BoxIcon />}
              trailing={
                <Button
                  variant="tertiary"
                  onPress={() =>
                    displayPopupAlert('Action', 'Action button pressed')
                  }>
                  Action
                </Button>
              }>
              French fries keep customers happy.
            </ListItem>
            <ListItem
              title="Potato"
              leading={<Icons.BoxIcon />}
              trailing={
                <Button
                  variant="tertiary"
                  onPress={() =>
                    displayPopupAlert('Action', 'Action button pressed')
                  }>
                  Action
                </Button>
              }>
              French fries are delicious.
            </ListItem>
          </List>
        </Section>
      </>
    );
  };

  /**
   *
   * @param buttonLabel
   * @param listName
   * @returns button ui to Show or hides sample code
   */
  const displayCodeButton = (buttonLabel: string, listName: string) => {
    const listNameVal: boolean = listCode[listName as keyof ListProps];
    return (
      <Button
        UNSAFE_style={styles.displayCodeBtn}
        variant="tertiary"
        onPress={() => setListCode({...listCode, [listName]: !listNameVal})}>
        {buttonLabel}
      </Button>
    );
  };

  return (
    <Page>
      {defaultListWithOnlyChild()}
      {listWithChildNLeading()}
      {listWithChildLeadingNTitle()}
      {listWithChildLeadingTitleNTrailing()}
      {listWithMultipleListItem()}
      {listWithoutSeparator()}
    </Page>
  );
};
const styles = StyleSheet.create({
  displayCodeBtn: {position: 'absolute', bottom: 0, right: 2},
});

export {ListRecipes};
