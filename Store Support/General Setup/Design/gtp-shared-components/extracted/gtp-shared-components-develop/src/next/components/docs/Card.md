### Card

```js
import * as React from 'react';
import {Image, Text} from 'react-native';
import {Heading, Icons, Card, CardHeader, CardMedia, CardContent, CardActions, Button, ButtonGroup} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;

<>
  {['small', 'large'].map(size => {
    return (
      <React.Fragment key={size}>
          <Heading size="large">{`Card size="${size}"`}</Heading>
          <Spacer />
          <Card size={size}>
            <CardMedia>
              <Image
                source={{
                  uri: 'https://placekitten.com/g/200/200',
                  height: 300,
                  width: '100%',
                }}
              />
            </CardMedia>
            <CardHeader
              leadingIcon={<Icons.SparkIcon size={32} />}
              title="Welcome"
              trailing={
                <Button
                  variant="tertiary"
                  onPress={() => {}}>
                  Start Here
                </Button>
              }
            />
            <CardContent>
              <Text>Lorem ipsum dolor sit amet.</Text>
            </CardContent>
            <CardActions>
              <ButtonGroup>
                <Button
                  variant="tertiary"
                  onPress={() => {}}>
                  Action1
                </Button>
                <Button
                  variant="primary"
                  onPress={() => {}}>
                  Action2
                </Button>
              </ButtonGroup>
            </CardActions>
          </Card>
          <Spacer />
      </React.Fragment>
    );
  })}

</>;
```
