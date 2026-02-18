import * as React from 'react';
import {Image, Text} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Card';
import {render} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import mediaImage from '../../../../assets/images/media-image.png';
import {loremIpsum} from '../../utils';
import {Button} from '../Button';
import {ButtonGroup} from '../ButtonGroup';
import {Card, CardSize} from '../Card';
import {CardActions} from '../CardActions';
import {CardContent} from '../CardContent';
import {CardHeader} from '../CardHeader';
import {CardMedia} from '../CardMedia';

describe.each<CardSize>(['large', 'small'])(
  'Should support different sizes: ',
  (size) => {
    test(`Test Card size = "${size}".`, async () => {
      const rootQueries = render(
        <Card size={size}>
          <CardMedia>
            <Image
              source={mediaImage}
              style={{height: 200, resizeMode: 'stretch'}}
            />
          </CardMedia>
          <CardHeader
            leading={<Icons.SparkIcon size={32} />}
            title="Welcome"
            trailing={
              <Button variant="tertiary" onPress={() => {}}>
                Start Here
              </Button>
            }
          />
          <CardContent>
            <Text>{loremIpsum(1)}</Text>
          </CardContent>
          <CardActions>
            <ButtonGroup>
              <Button variant="tertiary" onPress={() => {}}>
                Action1
              </Button>
              <Button variant="primary" onPress={() => {}}>
                Action2
              </Button>
            </ButtonGroup>
          </CardActions>
        </Card>,
      );
      const cardContent = await rootQueries.findByTestId('CardContent');
      expect(cardContent).toHaveStyle({
        marginVertical:
          size === 'small'
            ? token.componentCardContentContainerSizeSmallMarginVertical
            : token.componentCardContentContainerSizeLargeMarginVertical,
      });

      const cardHeader = await rootQueries.findByTestId('CardHeader');
      expect(cardHeader).toHaveStyle({
        marginVertical:
          size === 'small'
            ? token.componentCardHeaderContainerSizeSmallMarginVertical
            : token.componentCardContentContainerSizeLargeMarginVertical,
        paddingHorizontal:
          size === 'small'
            ? token.componentCardHeaderContainerSizeSmallPaddingHorizontal
            : token.componentCardHeaderContainerSizeLargePaddingHorizontal,
      });

      const cardMedia = await rootQueries.findByTestId('CardMedia');
      expect(cardMedia).toHaveStyle({
        justifyContent: 'center',
        alignItems: 'center',
        width: '100%',
        overflow: 'hidden',
      });
      // @ts-ignore
      expect(cardMedia.children[0].props.source.testUri).toContain(
        'media-image',
      );

      const cardActions = await rootQueries.findByTestId('CardActions');
      // @ts-ignore
      expect(cardActions.children[0].children[0].props.style).toEqual({
        alignSelf: 'flex-end',
        marginRight: size === 'small' ? '-9%' : '-12%',
        marginTop:
          size === 'small'
            ? token.componentCardActionsContainerSizeSmallMarginVertical
            : token.componentCardActionsContainerSizeLargeMarginVertical,
      });
    });
  },
);
