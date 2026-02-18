import * as React from 'react';
import {Text, Image, StyleSheet} from 'react-native';
import {Controller, Header, Page, Section, VariantText} from '../components';
import {
  colors,
  Body,
  Button,
  ButtonGroup,
  Card,
  CardSize,
  CardMedia,
  CardHeader,
  CardContent,
  CardActions,
  Carousel,
  Collapse,
  Divider,
  Icons,
  IconButton,
  List,
  ListItem,
  SeeDetails,
  Modal,
  Skeleton,
  SkeletonText,
} from '@walmart/gtp-shared-components';
import {
  displayPopupAlert,
  carouselHeader,
  carouselFooter,
  carouselItems,
  itemsForSimpleList,
  loremIpsum,
} from './screensFixtures';

// @ts-ignore
import mediaImage from '@walmart/gtp-shared-components/assets/images/media-image.png';

export const LayoutOverview: React.FC = () => {
  const [modalIsOpen, setModalIsOpen] = React.useState<boolean>(false);
  const [modalActionPressed, setModalActionPressed] =
    React.useState<string>('');

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

  const handleModalOnClosed = () => {
    if (modalActionPressed !== '') {
      console.log(`Modal action '${modalActionPressed}' was tapped`);
    }
  };
  const handleModalOnOpen = () => {
    console.log('Modal Open inprogress');
  };
  const handleModalOnOpened = () => {
    console.log('Modal Open completed');
  };
  // ---------------
  // Rendering
  // ---------------
  return (
    <Page>
      {['small', 'large'].map(size => {
        return (
          <React.Fragment key={size}>
            <Header>
              Card{'\n  '}
              <VariantText>{`size="${size}"`}</VariantText>
            </Header>
            <Section>
              <Card size={size as CardSize}>
                <CardMedia>
                  <Image source={mediaImage} style={styles.mediaImage} />
                </CardMedia>
                <CardHeader
                  leading={<Icons.SparkIcon size={32} />}
                  title="Welcome"
                  trailing={
                    <Button
                      variant="tertiary"
                      onPress={() =>
                        displayPopupAlert('Action', 'Start here button pressed')
                      }>
                      Start Here
                    </Button>
                  }
                />
                <CardContent>
                  <Text style={{color: colors.black}}>{loremIpsum(1)}</Text>
                </CardContent>
                <CardActions>
                  <ButtonGroup>
                    <Button
                      variant="tertiary"
                      onPress={() =>
                        displayPopupAlert('Action', 'Action1 button pressed')
                      }>
                      Action1
                    </Button>
                    <Button
                      variant="primary"
                      onPress={() =>
                        displayPopupAlert('Action', 'Action2 button pressed')
                      }>
                      Action2
                    </Button>
                  </ButtonGroup>
                </CardActions>
              </Card>
            </Section>
          </React.Fragment>
        );
      })}
      <Header>List</Header>
      <Section inset={false} space={false}>
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
            French fries are delicious, French fries keep customers happy
            without dipping into restaurant profit margins.
          </ListItem>
          <ListItem leading={<Icons.BoxIcon />} title="Potato">
            French fries are deliciousFrench fries are delicious French fries
            are delicious.
          </ListItem>
          <ListItem
            title="Potato"
            trailing={
              <IconButton
                children={<Icons.ChevronRightIcon />}
                size="small"
                onPress={() =>
                  displayPopupAlert('Action', 'icon button pressed')
                }
              />
            }>
            French fries are delicious.
          </ListItem>
          <ListItem title="Potato">
            French fries are deliciousFrench fries are delicious French fries
            are delicious.
          </ListItem>
          <ListItem>
            French fries are deliciousFrench fries are delicious French fries
            are delicious.
          </ListItem>
        </List>
      </Section>
      <Header>List Items Array</Header>
      <Section inset={false} space={false}>
        <List>
          {itemsForSimpleList.map((item, index) => {
            const {title, content, leading, trailing} = item;
            return (
              <ListItem
                title={title}
                leading={leading}
                trailing={trailing}
                key={index}>
                {content}
              </ListItem>
            );
          })}
        </List>
      </Section>
      <Header>Divider</Header>
      <Section>
        <Divider />
      </Section>
      <Header>Modal</Header>
      <Section>
        <Button variant="primary" onPress={openModal}>
          Show Modal
        </Button>
        <Modal
          isOpen={modalIsOpen}
          onOpen={handleModalOnOpen}
          onOpened={handleModalOnOpened}
          onClose={handleModalOnClose}
          onClosed={handleModalOnClosed}
          title="Confirmation"
          actions={
            <ButtonGroup>
              <Button variant="tertiary" onPress={handleModalCancel}>
                Click here for terms & conditions
              </Button>
              <Button variant="tertiary" onPress={handleModalCancel}>
                Cancel
              </Button>
              <Button variant="primary" onPress={handleModalContinue}>
                Continue
              </Button>
            </ButtonGroup>
          }>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
          minim veniam, quis nostrud exercitation ullamco laboris nisi ut
          aliquip ex ea commodo consequat.
        </Modal>
      </Section>
      <Header>Collapse</Header>
      <Section inset={false} space={false}>
        <Controller setValueProp="onToggle" controlProp="expanded">
          <Collapse dividerTop title="Single Line Collapse" onToggle={() => {}}>
            <Body>Collapse content appears underneath the toggle area.</Body>
          </Collapse>
        </Controller>
        <Controller setValueProp="onToggle" controlProp="expanded">
          <Collapse
            dividerTop
            icon={<Icons.InfoCircleIcon size={24} />}
            title="Collapse with Subtitle and Icon"
            subtitle="Subtitle Text"
            onToggle={() => {}}>
            <Body>Collapse content appears underneath the toggle area.</Body>
          </Collapse>
        </Controller>
        <Controller setValueProp="onToggle" controlProp="expanded">
          <Collapse
            dividerTop
            title="Get beauty finds from $8 and how-to tutorials"
            onToggle={() => {}}>
            <Body>Collapse content appears underneath the toggle area.</Body>
          </Collapse>
        </Controller>
        <Controller setValueProp="onToggle" controlProp="expanded">
          <SeeDetails
            style={styles.seeDetails}
            dividerTop
            dividerBottom
            onToggle={() => {}}>
            <Body>See Details Content appears above the toggle area.</Body>
          </SeeDetails>
        </Controller>
        <Controller setValueProp="onToggle" controlProp="expanded">
          <SeeDetails
            showText="Show my content"
            hideText="Hide my content"
            style={styles.seeDetails}
            dividerTop
            dividerBottom
            onToggle={() => {}}>
            <Body>See Details with custom captions.</Body>
          </SeeDetails>
        </Controller>
      </Section>
      <Header>Carousel</Header>
      <Section space={false} inset={false}>
        <Carousel
          style={styles.carousel}
          header={carouselHeader}
          footer={carouselFooter}
          items={carouselItems}
          onItemPress={() => {}}
          onAddPress={() => {}}
        />
        <Carousel
          style={styles.carousel}
          header={{
            title: 'Carousel Without Footer',
          }}
          items={carouselItems}
          onItemPress={() => {}}
        />
        <Carousel
          small
          style={styles.carousel}
          header={{
            title: 'Small Carousel With Footer',
          }}
          items={carouselItems}
          onItemPress={() => {}}
          onAddPress={() => {}}
          footer={carouselFooter}
        />
      </Section>
      <Header>Skeleton</Header>
      <Section space={8} color="white">
        <Skeleton />
        <Skeleton variant="rounded" />
      </Section>
      <Section space={8} color="white" horizontal>
        <Skeleton height={50} width={50} />
        <Skeleton height={50} width={50} variant="rounded" />
        <Skeleton height={50} width={100} />
      </Section>
      <Section space={8} color="white">
        <SkeletonText lines={3} />
      </Section>
    </Page>
  );
};

const styles = StyleSheet.create({
  overlay: {
    backgroundColor: 'white',
    padding: 16,
    paddingBottom: 100,
    marginBottom: -100,
  },
  carousel: {
    marginHorizontal: -16,
  },
  seeDetails: {
    marginTop: 0,
  },
  card: {
    marginVertical: 8,
  },
  overlayBody: {
    textAlign: 'center',
    margin: 16,
  },
  cardStyle: {
    backgroundColor: colors.yellow['30'],
  },
  cardOverlayContentContainer: {
    marginLeft: 6,
  },
  cardOverlayContentTitle: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  cardOverlayContentBody: {
    fontSize: 16,
    textAlign: 'left',
    marginLeft: 0,
    marginRight: 8,
    marginBottom: 16,
  },
  subheaderText: {
    fontSize: 15,
  },
  mediaImage: {
    height: 200,
    resizeMode: 'stretch',
  },
});
