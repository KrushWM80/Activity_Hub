/* eslint-disable react-native/no-inline-styles */
// Recipe created for CEEMP-2790, based on code provided in the ticket

import React from 'react';
import {Image, ImageSourcePropType, View, StyleSheet} from 'react-native';
import {
  Body,
  Callout,
  CalloutPosition,
  colors,
  Link,
} from '@walmart/gtp-shared-components';
import {Header, Page, VariantText} from '../components';
// import EStyleSheet from 'react-native-extended-stylesheet'; // they are using this lib for styling but it is not working properly

const Spacer = () => <View style={styles.spacer} />;
interface Text {
  link?: string;
  callout?: string;
}

interface HeaderItemCardProps {
  position?: string;
  text?: Text;
  image: string;
  itemDescription: string;
  showCallout: boolean;
  onViewBuildsheet: () => void;
  onCloseCallout: () => void;
}

const HeaderItemCard = (props: HeaderItemCardProps) => {
  const {
    position = 'bottomRight',
    text = {},
    image,
    itemDescription,
    showCallout,
    onViewBuildsheet,
    onCloseCallout,
  } = props;
  const {
    link = 'View build sheet',
    callout = 'View build sheet to see what is needed to make this item.',
  } = text;

  const codeSnippet1 = `<>
    <Image source={require(image_path)}/>
    <View>
      <Body weight="700" size="medium">
        {Body text}
      </Body>
      <Callout
        content={<Text>Callout content</Text>}
        isOpen={true}
        onClose={onCloseHandler}
        position="right">
          <Link onPress={onPressHandler}>
            {link_text}
          </Link>
      </Callout>
    </View>
  </>`;

  const itemImageProps = {source: image as ImageSourcePropType};

  const content = () => (
    <View style={{width: 181, marginHorizontal: 16}}>
      <Body weight="700" size="medium" UNSAFE_style={{color: 'white'}}>
        {callout}
      </Body>
    </View>
  );

  return (
    <View style={{marginBottom: 100}}>
      <Header>
        Callout{'\n  '}
        <VariantText>{codeSnippet1}</VariantText>
      </Header>
      <View style={styles.outerContainer}>
        <View style={styles.innerContainer}>
          <Spacer />

          <Image {...itemImageProps} style={styles.image} />
          <View>
            <Body weight="700" size="medium">
              {itemDescription}
            </Body>
            <Callout
              content={content()}
              isOpen={showCallout}
              onClose={onCloseCallout}
              position={position as CalloutPosition}
              UNSAFE_style={styles.callout}>
              <Link onPress={onViewBuildsheet} UNSAFE_style={styles.link}>
                {link}
              </Link>
            </Callout>
          </View>
        </View>
      </View>
    </View>
  );
};

const CalloutRecipes = () => {
  const [showCallout, setShowCallout] = React.useState<boolean>(false);
  return (
    <Page>
      <HeaderItemCard
        image={require('../assets').sandwich}
        itemDescription="2 Foot Sub Sandwich"
        showCallout={showCallout}
        onViewBuildsheet={() => setShowCallout(true)}
        onCloseCallout={() => setShowCallout(false)}
        position={'right'}
      />
    </Page>
  );
};

export {CalloutRecipes};

// const styles = EStyleSheet.create({
const styles = StyleSheet.create({
  spacer: {
    height: 8,
  },
  image: {
    width: 48,
    height: 48,
    marginRight: 16,
  },
  link: {
    alignSelf: 'flex-start',
  },
  callout: {
    left: 100,
  },
  innerContainer: {
    padding: 10,
    alignItems: 'flex-start',
  },
  outerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
});
