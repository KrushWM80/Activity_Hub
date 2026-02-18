import * as React from 'react';
import {Text, Image, StyleSheet} from 'react-native';
import {Header, Page, Section, VariantText} from '../components';
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
} from '@walmart/gtp-shared-components';
import {displayPopupAlert, loremIpsum} from './screensFixtures';

// @ts-ignore
import mediaImage from '@walmart/gtp-shared-components/assets/images/media-image.png';

export const CardRecipes: React.FC = () => {
  const CardWithContent = () => {
    return (
      <>
        <Header>
          Card{'\n  '}
          <VariantText>{`with CardContent`}</VariantText>
        </Header>
        <Section>
          <Card size={'small' as CardSize}>
            <CardContent>
              <Text style={{color: colors.black}}>{loremIpsum(1)}</Text>
            </CardContent>
          </Card>
        </Section>
      </>
    );
  };
  const CardWithHeader = () => {
    return (
      <>
        <Header>
          Card{'\n  '}
          <VariantText>{`with CardHeader and CardContent`}</VariantText>
        </Header>
        <Section>
          <Card size={'small' as CardSize}>
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
          </Card>
        </Section>
      </>
    );
  };

  const CardWithAction = () => {
    return (
      <>
        <Header>
          Card{'\n  '}
          <VariantText>{`with CardHeader, \n\t CardContent and \n\t CardActions`}</VariantText>
        </Header>
        <Section>
          <Card size={'small' as CardSize}>
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
      </>
    );
  };

  const CardWithMedia = () => {
    return (
      <>
        <Header>
          Card{'\n  '}
          <VariantText>{`with CardMedia and CardContent`}</VariantText>
        </Header>
        <Section>
          <Card size={'small' as CardSize}>
            <CardMedia>
              <Image source={mediaImage} style={styles.mediaImage} />
            </CardMedia>
            <CardContent>
              <Text style={{color: colors.black}}>{loremIpsum(1)}</Text>
            </CardContent>
          </Card>
        </Section>
      </>
    );
  };

  const CardWithSizes = () => {
    return (
      <>
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
                          displayPopupAlert(
                            'Action',
                            'Start here button pressed',
                          )
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
      </>
    );
  };

  return (
    <Page>
      <CardWithContent />
      <CardWithHeader />
      <CardWithAction />
      <CardWithMedia />
      <CardWithSizes />
    </Page>
  );
};

const styles = StyleSheet.create({
  mediaImage: {
    height: 200,
    resizeMode: 'stretch',
  },
});
