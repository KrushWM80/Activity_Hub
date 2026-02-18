import * as React from 'react';
import {Image} from 'react-native';

import {render} from '@testing-library/react-native';

import mediaImage from '../../../../assets/images/media-image.png';
import {CardMedia} from '../CardMedia';

describe('Testing CardMedia', () => {
  it('should display correctly', () => {
    const component = render(
      <CardMedia>
        <Image
          source={mediaImage}
          style={{height: 200, resizeMode: 'stretch'}}
        />
      </CardMedia>,
    );
    expect(component).toMatchSnapshot();
  });
});
