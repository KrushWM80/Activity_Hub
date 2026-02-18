import React from 'react';
import {FlatList, Image, ScrollView, StyleSheet, View} from 'react-native';
import {
  BottomSheet,
  Button,
  ButtonGroup,
  Body,
  ListItem,
} from '@walmart/gtp-shared-components';
import {miniAppListData} from './screensFixtures';
import {Header, Section, VariantText} from '../components';
type listItemType = {
  id: number;
  isReturnable: boolean;
  isSelected: boolean;
  productName?: string;
  displayUpc?: string;
  isReturned?: boolean;
  currencyAmount?: string;
};
export const BottomSheetWithFlatListContentRecipe: React.FC = () => {
  const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(false);
  const [modalActionPressed, setModalActionPressed] =
    React.useState<string>('');
  const innerScrollViewRef = React.useRef<ScrollView>(null);
  const handleModalOnOpen = () => {
    console.log('BottomSheet Open inprogress');
  };
  const handleModalOnOpened = () => {
    console.log('BottomSheet Open completed');
  };
  const handleModalOnClosed = () => {
    if (modalActionPressed !== '') {
      console.log(`Modal action '${modalActionPressed}' was tapped`);
    }
  };
  const openModal = () => {
    setModalIsOpen(true);
    setModalActionPressed('');
  };
  const handleModalOnClose = () => {
    setModalIsOpen(false);
  };
  const handleModalCancel = () => {
    setModalActionPressed('Cancel');
    setModalIsOpen(false);
  };
  const handleModalContinue = () => {
    setModalActionPressed('Continue');
    setModalIsOpen(false);
  };

  const leadingItem = () => {
    return (
      <View style={ss.listItemLeading}>
        <Image
          style={ss.listItemLeadingImage}
          source={require('../assets').livingdesign}
        />
        <Button size="small" variant="tertiary" onPress={handleModalOnClose}>
          Remove
        </Button>
      </View>
    );
  };
  const contentItem = (productName: string, displayUpc: string) => {
    return (
      <View style={ss.listItemContent}>
        <Body size={'small'} numberOfLines={2}>
          {productName}
        </Body>
        <Body
          size={'small'}
          numberOfLines={1}
          UNSAFE_style={ss.listItemContentText}>
          {displayUpc}
        </Body>
      </View>
    );
  };
  const trailingItem = (currencyAmount: string) => {
    return (
      <View style={ss.listItemTrailing}>
        <Body size="small" weight="700">
          {currencyAmount}
        </Body>
      </View>
    );
  };

  const renderList = () => {
    return (
      <FlatList
        data={miniAppListData}
        showsHorizontalScrollIndicator={false}
        showsVerticalScrollIndicator={false}
        renderItem={({item}: {item: listItemType}) => {
          const {id, productName, displayUpc, currencyAmount} = item;
          return (
            <ListItem
              leading={leadingItem()}
              trailing={trailingItem(currencyAmount as string)}
              key={id}>
              <>{contentItem(productName as string, displayUpc as string)}</>
            </ListItem>
          );
        }}
      />
    );
  };
  return (
    <>
      <Header>
        BottomSheet{'\n'} <VariantText>{'with List ListItems'}</VariantText>
      </Header>
      <Section>
        <Button variant="primary" onPress={openModal}>
          Show
        </Button>
        <BottomSheet
          innerScrollViewRef={innerScrollViewRef}
          isOpen={modalIsOpen}
          childrenContainScrollableComponent={true}
          onClose={handleModalOnClose}
          onOpen={handleModalOnOpen}
          onOpened={handleModalOnOpened}
          onClosed={handleModalOnClosed}
          onBackButtonPress={handleModalOnClose}
          title={'Items being Returned'}
          actions={
            <ButtonGroup>
              <Button variant="tertiary" onPress={handleModalCancel}>
                Cancel
              </Button>
              <Button variant="primary" onPress={handleModalContinue}>
                Continue
              </Button>
            </ButtonGroup>
          }>
          {renderList()}
        </BottomSheet>
      </Section>
    </>
  );
};
const ss = StyleSheet.create({
  listItemLeading: {
    flexDirection: 'column',
    alignContent: 'center',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 26,
  },
  listItemLeadingImage: {
    width: 64,
    height: 64,
    marginBottom: 16,
  },
  listItemContent: {
    flex: 1,
  },
  listItemContentText: {
    marginVertical: 4,
  },
  listItemTrailing: {
    flex: 1,
  },
});
export default BottomSheetWithFlatListContentRecipe;
