import * as React from 'react';
import {
  Text,
  Image,
  TextStyle,
  ScrollView,
  StyleSheet,
  View,
} from 'react-native';
import {
  BottomSheet,
  Button,
  ButtonGroup,
  TextField,
  IconButton,
  ChevronLeftIcon,
  Body,
  List,
  ListItem,
  getFont,
  Select,
  Selected,
  SelectOptions,
  Divider,
} from '@walmart/gtp-shared-components';
import {
  LongBottomSheetContent,
  loremIpsum,
  miniAppListData,
} from './screensFixtures';
import {
  Header,
  Page,
  Section,
  VariantText,
  BottomSheetsLegacy,
  IconGrid,
} from '../components';

const BottomSheetOverview: React.FC = () => {
  const handleModalOnOpen = () => {
    console.log('BottomSheet Open started');
  };
  const handleModalOnOpened = () => {
    console.log('BottomSheet Open completed');
  };
  const BottomSheetWithText = ({size}: {size: 'small' | 'large'}) => {
    const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(false);
    const [modalActionPressed, setModalActionPressed] =
      React.useState<string>('');
    const handleModalOnClosed = () => {
      if (modalActionPressed !== '') {
        console.log(`Modal action '${modalActionPressed}' was tapped`);
      }
      console.log('BottomSheet Close completed');
    };
    const openModal = () => {
      setModalIsOpen(true);
      setModalActionPressed('');
    };
    const handleModalOnClose = () => {
      setModalIsOpen(false);
      console.log('BottomSheet Close started');
    };
    const handleModalCancel = () => {
      setModalActionPressed('Cancel');
      setModalIsOpen(false);
    };
    const handleModalContinue = () => {
      setModalActionPressed('Continue');
      setModalIsOpen(false);
    };

    return (
      <>
        <Header>
          BottomSheet{'\n'}{' '}
          <VariantText>{`with ${size} text content`}</VariantText>
        </Header>
        <Section>
          <Button variant="primary" onPress={openModal}>
            Show
          </Button>
          <BottomSheet
            isOpen={modalIsOpen}
            onClose={handleModalOnClose}
            onOpen={handleModalOnOpen}
            onOpened={handleModalOnOpened}
            onClosed={handleModalOnClosed}
            onBackButtonPress={handleModalOnClose}
            title="Confirmation"
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
            {size === 'small' ? loremIpsum(1) : loremIpsum(10)}
          </BottomSheet>
        </Section>
      </>
    );
  };
  const BottomSheetWithNoHeader = () => {
    const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(false);
    const [modalActionPressed, setModalActionPressed] =
      React.useState<string>('');
    const handleModalOnClosed = () => {
      if (modalActionPressed !== '') {
        console.log(`Modal action '${modalActionPressed}' was tapped`);
      }
      console.log('BottomSheet Close completed');
    };
    const openModal = () => {
      setModalIsOpen(true);
      setModalActionPressed('');
    };
    const handleModalOnClose = () => {
      setModalIsOpen(false);
      console.log('BottomSheet Close started');
    };

    const handleModalCancel = () => {
      setModalActionPressed('Cancel');
      setModalIsOpen(false);
    };
    const handleModalContinue = () => {
      setModalActionPressed('Continue');
      setModalIsOpen(false);
    };

    return (
      <>
        <Header>
          BottomSheet{'\n'} <VariantText>{'with No Header Title'}</VariantText>
        </Header>
        <Section>
          <Button variant="primary" onPress={openModal}>
            Show
          </Button>
          <BottomSheet
            isOpen={modalIsOpen}
            onOpen={handleModalOnOpen}
            onOpened={handleModalOnOpened}
            onClose={handleModalOnClose}
            onClosed={handleModalOnClosed}
            onBackButtonPress={handleModalOnClose}
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
            {loremIpsum(1)}
          </BottomSheet>
        </Section>
      </>
    );
  };
  const BottomSheetWithRandomContent = () => {
    const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(false);
    const [modalActionPressed, setModalActionPressed] =
      React.useState<string>('');
    const handleModalOnClosed = () => {
      if (modalActionPressed !== '') {
        console.log(`Modal action '${modalActionPressed}' was tapped`);
      }
      console.log('BottomSheet Close completed');
    };
    const openModal = () => {
      setModalIsOpen(true);
      setModalActionPressed('');
    };
    const handleModalOnClose = () => {
      setModalIsOpen(false);
      console.log('BottomSheet Close started');
    };
    return (
      <>
        <Header>
          BottomSheet{'\n'} <VariantText>with random content</VariantText>
        </Header>
        <Section>
          <Button variant="primary" onPress={openModal}>
            Show
          </Button>
          <BottomSheet
            isOpen={modalIsOpen}
            onOpen={handleModalOnOpen}
            onClose={handleModalOnClose}
            onClosed={handleModalOnClosed}
            onBackButtonPress={handleModalOnClose}
            title="Confirmation">
            <>
              <TextField
                label="This is the label"
                placeholder="Placeholder text"
                helperText="Helper text"
              />
              <LongBottomSheetContent close={handleModalOnClose} />
            </>
          </BottomSheet>
        </Section>
      </>
    );
  };

  const BottomSheetWithForm = () => {
    const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(false);
    const [modalActionPressed, setModalActionPressed] =
      React.useState<string>('');
    const handleModalOnClosed = () => {
      if (modalActionPressed !== '') {
        console.log(`Modal action '${modalActionPressed}' was tapped`);
      }
      console.log('BottomSheet Close completed');
    };
    const [text, setText] = React.useState<string>('');
    const openModal = () => {
      setModalIsOpen(true);
      setModalActionPressed('');
    };
    const handleModalOnClose = () => {
      console.log('---- text entered:', text);
      console.log('BottomSheet Close started');
      setModalIsOpen(false);
    };
    const handleModalSubmit = () => {
      setModalActionPressed('Submit');
      setModalIsOpen(false);
    };

    return (
      <>
        <Header>
          BottomSheet{'\n'} <VariantText>with TextField</VariantText>
        </Header>
        <Section>
          <Button variant="primary" onPress={openModal}>
            Show
          </Button>
          <BottomSheet
            isOpen={modalIsOpen}
            onClose={handleModalOnClose}
            onOpen={handleModalOnOpen}
            onOpened={handleModalOnOpened}
            onClosed={handleModalOnClosed}
            onBackButtonPress={handleModalOnClose}
            title="Confirmation"
            actions={
              <Button
                variant="primary"
                isFullWidth={true}
                onPress={handleModalSubmit}>
                Submit
              </Button>
            }>
            <>
              <TextField
                label="This is the label"
                placeholder="Placeholder text"
                helperText="Helper text"
                onChangeText={value => setText(value)}
              />
            </>
          </BottomSheet>
        </Section>
      </>
    );
  };

  const BottomSheetWithLongList = () => {
    const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(false);
    const [modalActionPressed, setModalActionPressed] =
      React.useState<string>('');
    const innerScrollViewRef = React.useRef<ScrollView>(null);

    const handleModalOnClosed = () => {
      if (modalActionPressed !== '') {
        console.log(`Modal action '${modalActionPressed}' was tapped`);
      }
      console.log('BottomSheet Close completed');
    };
    const openModal = () => {
      setModalIsOpen(true);
      setModalActionPressed('');
    };
    const handleModalOnClose = () => {
      setModalIsOpen(false);
      console.log('BottomSheet Close started');
    };
    const handleModalCancel = () => {
      setModalActionPressed('Cancel');
      setModalIsOpen(false);
    };
    const handleModalSubmit = () => {
      setModalActionPressed('Submit');
      setModalIsOpen(false);
    };
    const handleScroll = () => {
      innerScrollViewRef?.current?.scrollTo({y: 0, animated: true});
    };

    return (
      <>
        <Header>
          BottomSheet{'\n'} <VariantText>with long list</VariantText>
        </Header>
        <Section>
          <Button variant="primary" onPress={openModal}>
            Show
          </Button>
          <BottomSheet
            innerScrollViewRef={innerScrollViewRef}
            isOpen={modalIsOpen}
            onClose={handleModalOnClose}
            onOpen={handleModalOnOpen}
            onOpened={handleModalOnOpened}
            onClosed={handleModalOnClosed}
            onBackButtonPress={handleModalOnClose}
            title="Confirmation"
            actions={
              <ButtonGroup>
                <Button variant="tertiary" onPress={handleScroll}>
                  Scroll to Top
                </Button>
                <Button variant="tertiary" onPress={handleModalCancel}>
                  Cancel
                </Button>
                <Button variant="primary" onPress={handleModalSubmit}>
                  Submit
                </Button>
              </ButtonGroup>
            }>
            <IconGrid />
          </BottomSheet>
        </Section>
      </>
    );
  };

  const BottomSheetWithList = () => {
    const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(false);
    const [modalActionPressed, setModalActionPressed] =
      React.useState<string>('');
    const innerScrollViewRef = React.useRef<ScrollView>(null);

    const handleModalOnClosed = () => {
      if (modalActionPressed !== '') {
        console.log(`Modal action '${modalActionPressed}' was tapped`);
      }
      console.log('BottomSheet Close completed');
    };
    const openModal = () => {
      setModalIsOpen(true);
      setModalActionPressed('');
    };
    const handleModalOnClose = () => {
      setModalIsOpen(false);
      console.log('BottomSheet Close started');
    };
    const handleModalCancel = () => {
      setModalActionPressed('Cancel');
      setModalIsOpen(false);
    };
    const handleModalContinue = () => {
      setModalActionPressed('Continue');
      setModalIsOpen(false);
    };
    const handleScroll = () => {
      innerScrollViewRef?.current?.scrollTo({y: 0, animated: true});
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
        <List>
          {miniAppListData.map(item => {
            const {id, productName, displayUpc, currencyAmount} = item;
            return (
              <ListItem
                leading={leadingItem()}
                trailing={trailingItem(currencyAmount)}
                key={id}>
                <>{contentItem(productName, displayUpc)}</>
              </ListItem>
            );
          })}
        </List>
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
            onClose={handleModalOnClose}
            onOpen={handleModalOnOpen}
            onOpened={handleModalOnOpened}
            onClosed={handleModalOnClosed}
            onBackButtonPress={handleModalOnClose}
            title={'Items being Returned'}
            actions={
              <ButtonGroup>
                <Button variant="tertiary" onPress={handleScroll}>
                  Scroll to Top
                </Button>
                <Button variant="tertiary" onPress={handleModalCancel}>
                  Scan more items
                </Button>
                <Button variant="primary" onPress={handleModalContinue}>
                  Confirm
                </Button>
              </ButtonGroup>
            }>
            {renderList()}
          </BottomSheet>
        </Section>
      </>
    );
  };
  const BottomSheetWithBackButton = () => {
    const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(false);
    const [modalActionPressed, setModalActionPressed] =
      React.useState<string>('');
    const handleModalOnClosed = () => {
      if (modalActionPressed !== '') {
        console.log(`Modal action '${modalActionPressed}' was tapped`);
      }
      console.log('BottomSheet Close completed');
    };
    const openModal = () => {
      setModalIsOpen(true);
      setModalActionPressed('');
    };
    const handleModalOnClose = () => {
      setModalIsOpen(false);
      console.log('BottomSheet Close started');
    };
    const handleModalCancel = () => {
      setModalActionPressed('Cancel');
      setModalIsOpen(false);
    };
    const handleModalContinue = () => {
      setModalActionPressed('Continue');
      setModalIsOpen(false);
    };
    return (
      <>
        <Header>
          BottomSheet{'\n'} <VariantText>{'with back button'}</VariantText>
        </Header>
        <Section>
          <Button variant="primary" onPress={openModal}>
            Show
          </Button>
          <BottomSheet
            isOpen={modalIsOpen}
            onClose={handleModalOnClose}
            onOpen={handleModalOnOpen}
            onOpened={handleModalOnOpened}
            onClosed={handleModalOnClosed}
            onBackButtonPress={handleModalOnClose}
            title={
              <View style={ss.titleContainer}>
                <IconButton
                  size="large"
                  onPress={() => console.log("Modal action 'Back' was tapped")}
                  UNSAFE_style={ss.iconButton}>
                  <ChevronLeftIcon />
                </IconButton>
                <Text style={ss.title}>Confirmation</Text>
              </View>
            }
            accessibilityTitleLabel="Confirmation"
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
            {loremIpsum(2)}
          </BottomSheet>
        </Section>
      </>
    );
  };
  const BottomSheetWithSelectComponent = () => {
    const selectOptions: SelectOptions = [
      {text: 'Mug'},
      {text: 'Shirt'},
      {
        text: 'Sticker',
      },
      {text: 'Hat - not available', disabled: true},
      {text: 'Hoodie'},
    ];
    const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(false);
    const [modalActionPressed, setModalActionPressed] =
      React.useState<string>('');
    const handleModalOnClosed = () => {
      if (modalActionPressed !== '') {
        console.log(`Modal action '${modalActionPressed}' was tapped`);
      }
      console.log('BottomSheet Close completed');
    };
    const handleOnChange = (selected: Array<Selected>) => {
      console.log('---- Picked:', selected);
    };
    const openModal = () => {
      setModalIsOpen(true);
      setModalActionPressed('');
    };
    const handleModalOnClose = () => {
      setModalIsOpen(false);
      console.log('BottomSheet Close started');
    };
    return (
      <>
        <Header>
          BottomSheet{'\n'} <VariantText>with Select Component</VariantText>
        </Header>
        <Section>
          <Button variant="primary" onPress={openModal}>
            Show
          </Button>
          <BottomSheet
            isOpen={modalIsOpen}
            onClose={handleModalOnClose}
            onOpen={handleModalOnOpen}
            onOpened={handleModalOnOpened}
            onClosed={handleModalOnClosed}
            onBackButtonPress={handleModalOnClose}
            title="Confirmation">
            <>
              <Select
                selectOptions={selectOptions}
                placeholder="Select your swag..."
                label="Swag"
                isInsideModal
                componentType={{ios: 'Overlay', android: 'Overlay'}}
                helperText="Helper text"
                onChange={handleOnChange}
              />
              <Select
                selectOptions={selectOptions}
                placeholder="Select your swag..."
                label="Swag"
                isInsideModal
                componentType={{ios: 'Overlay', android: 'Overlay'}}
                helperText="Helper text"
                onChange={handleOnChange}
              />
              <Select
                selectOptions={selectOptions}
                placeholder="Select your swag..."
                label="Swag"
                isInsideModal
                componentType={{ios: 'Overlay', android: 'Overlay'}}
                helperText="Helper text"
                onChange={handleOnChange}
              />
              <Select
                selectOptions={selectOptions}
                placeholder="Select your swag..."
                label="Swag"
                isInsideModal
                componentType={{ios: 'Overlay', android: 'Overlay'}}
                helperText="Helper text"
                onChange={handleOnChange}
              />
              <Select
                selectOptions={selectOptions}
                placeholder="Select your swag..."
                label="Swag"
                isInsideModal
                componentType={{ios: 'Overlay', android: 'Overlay'}}
                helperText="Helper text"
                onChange={handleOnChange}
              />
              <Select
                selectOptions={selectOptions}
                placeholder="Select your swag..."
                label="Swag"
                isInsideModal
                componentType={{ios: 'Overlay', android: 'Overlay'}}
                helperText="Helper text"
                onChange={handleOnChange}
              />
              <Select
                selectOptions={selectOptions}
                placeholder="Select your swag..."
                label="Swag"
                isInsideModal
                componentType={{ios: 'Overlay', android: 'Overlay'}}
                helperText="Helper text"
                onChange={handleOnChange}
              />
              <Select
                selectOptions={selectOptions}
                placeholder="Select your swag..."
                label="Swag"
                isInsideModal
                componentType={{ios: 'Overlay', android: 'Overlay'}}
                helperText="Helper text"
                onChange={handleOnChange}
              />
            </>
          </BottomSheet>
        </Section>
      </>
    );
  };

  const BottomSheetWithoutPadding = () => {
    const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(false);
    const openModal = () => {
      setModalIsOpen(true);
    };
    const handleModalOnClose = () => {
      setModalIsOpen(false);
      console.log('BottomSheet Close started');
    };

    return (
      <>
        <Header>
          BottomSheet{'\n'} <VariantText>without padding</VariantText>
          {'\n'} <VariantText>without header</VariantText>
          {'\n'} <VariantText>full width divider</VariantText>
        </Header>
        <Section>
          <Button variant="primary" onPress={openModal}>
            Show
          </Button>
          <BottomSheet
            hideHeader // You may provide your own header in the children
            isOpen={modalIsOpen}
            onClose={handleModalOnClose}
            onOpen={handleModalOnOpen}
            onOpened={handleModalOnOpened}
            onBackButtonPress={handleModalOnClose}
            // Remove the padding from the bottom sheet
            UNSAFE_style={{
              paddingHorizontal: 0,
              paddingBottom: 0,
            }}>
            <>
              <Body UNSAFE_style={{marginHorizontal: 16}}>{loremIpsum(1)}</Body>
              <Divider UNSAFE_style={{marginVertical: 16}} />
              <Button
                variant="primary"
                isFullWidth={true}
                UNSAFE_style={{marginHorizontal: 16}}
                onPress={handleModalOnClose}>
                Save
              </Button>
            </>
          </BottomSheet>
        </Section>
      </>
    );
  };

  const BottomSheetWithoutRNModal = () => {
    const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(false);
    const [modalActionPressed, setModalActionPressed] =
      React.useState<string>('');

    const openModal = () => {
      setModalIsOpen(true);
      setModalActionPressed('');
    };
    const handleModalOnClose = () => {
      setModalIsOpen(false);
      console.log('BottomSheet Close started');
    };
    const handleModalOnClosed = () => {
      if (modalActionPressed !== '') {
        console.log(`Modal action '${modalActionPressed}' was tapped`);
      }
      console.log('BottomSheet Close completed');
    };
    return (
      <>
        <Header>
          BottomSheet
          {'\n'} <VariantText>withRNModal=false</VariantText>
          {'\n\n'}{' '}
          <VariantText>
            {'You can also visit Recipes screen (WithRNModal=false)'}
          </VariantText>
        </Header>
        <Section>
          <Button variant="primary" onPress={openModal}>
            Show
          </Button>
          <BottomSheet
            withRNModal={false}
            useNativeDriver
            isOpen={modalIsOpen}
            onClose={handleModalOnClose}
            onOpen={handleModalOnOpen}
            onOpened={handleModalOnOpened}
            onClosed={handleModalOnClosed}
            onBackButtonPress={handleModalOnClose}
            animationInTiming={1}
            animationOutTiming={1}
            backdropTransitionInTiming={1}
            backdropTransitionOutTiming={1}
            title="Confirmation">
            <>
              <Text>
                {
                  "It will take the parent's view's bottom position, for your example you can place it on the main component view and open it based on your logic\n\n\n"
                }
                {loremIpsum(3)}
              </Text>
            </>
          </BottomSheet>
        </Section>
      </>
    );
  };

  return (
    <>
      <Page>
        <BottomSheetWithoutRNModal />
        <BottomSheetWithSelectComponent />
        <BottomSheetWithText size="small" />
        <BottomSheetWithText size="large" />
        <BottomSheetWithNoHeader />
        <BottomSheetWithRandomContent />
        <BottomSheetWithForm />
        <BottomSheetWithList />
        <BottomSheetWithLongList />
        <BottomSheetWithBackButton />
        <BottomSheetWithoutPadding />
        <BottomSheetsLegacy />
      </Page>
    </>
  );
};

const ss = StyleSheet.create({
  titleContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingRight: '27%',
  },
  title: {
    ...getFont('700'),
    fontSize: 18,
    lineHeight: 24,
    textAlign: 'center',
    color: '#2e2f32',
  } as TextStyle,
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
  listItemTrailingTagText: {
    marginLeft: 10,
  },
  iconButton: {
    marginLeft: -12,
  },
});

export {BottomSheetOverview};
