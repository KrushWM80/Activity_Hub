import * as React from 'react';
import {Text, Image, StyleSheet, View} from 'react-native';
import {Page, Section} from '../components';
import {
  colors,
  Button,
  ButtonGroup,
  Card,
  CardSize,
  CardMedia,
  CardHeader,
  CardContent,
  CardActions,
  Icons,
  Radio,
  Checkbox,
} from '@walmart/gtp-shared-components';
import {displayPopupAlert, loremIpsum} from './screensFixtures';

// @ts-ignore
import mediaImage from '@walmart/gtp-shared-components/assets/images/media-image.png';

const cardSizes: CardSize[] = ['small', 'large'];
const childrenVarient = [
  'CardWithContent',
  'CardWithHeader',
  'CardWithAction',
  'CardWithMedia',
];

export const CardPlayground: React.FC = () => {
  type Traits = {
    size?: CardSize;
    children: React.ReactNode;
    childrenTitle: string;
  };

  const CardWithContent = () => {
    return (
      <>
        <CardContent>
          <Text style={{color: colors.black}}>{loremIpsum(1)}</Text>
        </CardContent>
      </>
    );
  };
  const CardWithHeader = () => {
    return (
      <>
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
      </>
    );
  };

  const CardWithAction = () => {
    return (
      <>
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
      </>
    );
  };

  const CardWithMedia = () => {
    return (
      <>
        <CardMedia>
          <Image source={mediaImage} style={ss.mediaImage} />
        </CardMedia>
        <CardContent>
          <Text style={{color: colors.black}}>{loremIpsum(1)}</Text>
        </CardContent>
      </>
    );
  };

  const [traits, setTraits] = React.useState<Traits>({
    size: cardSizes[0],
    children: <CardWithContent />,
    childrenTitle: 'CardWithContent',
  });

  const childrenHandler = (child: string) => {
    let cardChild: React.ReactNode = <CardWithContent />;
    switch (child) {
      case 'CardWithContent':
        cardChild = <CardWithContent />;
        break;
      case 'CardWithHeader':
        cardChild = <CardWithHeader />;
        break;
      case 'CardWithAction':
        cardChild = <CardWithAction />;
        break;
      case 'CardWithMedia':
        cardChild = <CardWithMedia />;
        break;
      default:
        cardChild = <CardWithMedia />;
        break;
    }

    setTraits({
      ...traits,
      children: cardChild,
      childrenTitle: child,
    });
  };

  const variantHandler = (c_size: CardSize) => {
    setTraits({
      ...traits,
      size: c_size,
    });
  };

  return (
    <View style={ss.container}>
      <View style={ss.topContainer}>
        <View style={ss.topSubContainer}>
          <Section>
            <Card size={traits.size as CardSize}>{traits.children}</Card>
          </Section>
        </View>
      </View>
      <View style={ss.traitsContainer}>
        <Page>
          <View style={ss.header}>
            <Text style={ss.headerText}>Card traits</Text>
          </View>
          <View style={ss.innerContainer}>
            <View style={ss.traitsLeft}>
              <View>
                <Text style={ss.radioHeaderText}>children</Text>
                <Text style={ss.radioInfoText}>(example childrens)</Text>
              </View>
              {childrenVarient.map((v, i) => (
                <Checkbox
                  key={i}
                  label={v}
                  checked={v == traits.childrenTitle}
                  onPress={() => childrenHandler(v)}
                />
              ))}
            </View>

            <View style={ss.triatsRight}>
              <Text style={ss.radioHeaderText}>size</Text>
              {cardSizes.map((v, i) => (
                <Radio
                  key={i}
                  label={v}
                  checked={v == traits.size}
                  onPress={() => variantHandler(v)}
                />
              ))}
            </View>
          </View>
        </Page>
      </View>
    </View>
  );
};

const ss = StyleSheet.create({
  content: {
    flex: 0,
    paddingRight: 16,
    paddingLeft: 16,
  },
  mediaImage: {
    height: 150,
    resizeMode: 'stretch',
  },
  container: {
    flex: 1,
  },
  innerContainer: {
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.blue['90'],
    borderTopColor: colors.blue['90'],
    borderBottomColor: colors.blue['90'],
    borderLeftColor: colors.blue['90'],
    borderRightColor: colors.blue['90'],
    paddingHorizontal: 8,
    borderWidth: 1,
    flexDirection: 'row',
  },
  spacer: {
    height: 8,
  },
  traitsLeft: {
    flex: 0.5,
    borderRightWidth: 1,
    borderRightColor: colors.blue['90'],
    paddingBottom: 8,
  },
  triatsRight: {
    flex: 0.5,
    marginLeft: 10,
    paddingBottom: 8,
  },
  traitsContainer: {
    flex: 0.6,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderTopWidth: 1,
    borderLeftWidth: 1,
    borderRightWidth: 1,
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
    borderTopColor: colors.blue['90'],
    borderLeftColor: colors.blue['90'],
    borderRightColor: colors.blue['90'],
    paddingRight: 16,
    paddingVertical: 8,
    marginTop: 8,
  },
  headerText: {
    fontSize: 20,
    fontWeight: '500',
    color: colors.blue['90'],
    textAlign: 'left',
    paddingVertical: 4,
    marginLeft: 12,
  },
  radioHeaderText: {
    lineHeight: 28,
    fontSize: 20,
    color: colors.blue['90'],
  },
  radioInfoText: {
    lineHeight: 28,
    fontSize: 12,
    color: colors.blue['70'],
  },
  topSubContainer: {
    position: 'absolute',
    paddingHorizontal: 20,
    width: '100%',
  },
  topContainer: {
    flex: 1,
    position: 'relative',
  },
});
