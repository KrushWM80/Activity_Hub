import * as React from 'react';
import {GestureResponderEvent, Image} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/ErrorMessage';
import * as textToken from '@livingdesign/tokens/dist/react-native/light/regular/components/Text';
import {fireEvent, render} from '@testing-library/react-native';

import noInternetError from '../../../../assets/images/no_internet_error.png';
import {Button} from '../Button';
import {ErrorMessage} from '../ErrorMessage';

let mockFn: jest.Mock | ((event: GestureResponderEvent) => void);
beforeAll(() => {
  mockFn = jest.fn();
});
const errorTitle = 'No internet connection';
const errorContent =
  'Make sure you’re connected to WiFi or data and try again.';
describe('Test ErrorMessage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('ErrorMessage with title and content only', async () => {
    const rootQueries = render(
      <ErrorMessage title={errorTitle}>{errorContent}</ErrorMessage>,
    );
    const title = rootQueries.getByText(errorTitle);
    expect(title).toHaveStyle({
      marginBottom: token.componentErrorMessageTitleMarginBottom, //8
      fontWeight: `${token.componentErrorMessageTitleAliasOptionsWeight}`, //"700"
      fontSize:
        token.componentErrorMessageTitleAliasOptionsSize.toString() === 'small'
          ? textToken.componentTextHeadingSizeSmallFontSizeBS
          : token.componentErrorMessageTitleAliasOptionsSize.toString() ===
            'medium'
          ? textToken.componentTextHeadingSizeMediumFontSizeBS
          : textToken.componentTextHeadingSizeLargeFontSizeBS,
    });

    const content = rootQueries.getByText(errorContent);
    const getFontSize = () => {
      switch (token.componentErrorMessageTextLabelAliasOptionsSize) {
        case 'medium':
          return textToken.componentTextBodySizeMediumFontSize;
        case 'small':
          return textToken.componentTextBodySizeSmallFontSize;
        default:
          return textToken.componentTextBodySizeLargeFontSize;
      }
    };

    expect(content).toHaveStyle({
      fontSize: getFontSize(),
      color: token.componentErrorMessageTextLabelTextColor, //"#74767c"});
    });
    const media = rootQueries.queryAllByTestId('ErrorMessage-media');
    expect(media.length).toEqual(0);
    const actions = rootQueries.queryAllByTestId('ErrorMessage-actions');
    expect(actions.length).toEqual(0);
  });
  test('ErrorMessage with  Image & Actions', async () => {
    const rootQueries = render(
      <ErrorMessage
        title={errorTitle}
        media={<Image source={noInternetError} />}
        actions={
          <Button variant="primary" onPress={mockFn}>
            Try Again
          </Button>
        }>
        {errorContent}
      </ErrorMessage>,
    );
    const media = rootQueries.getByTestId('ErrorMessage-media');
    expect(media).toHaveStyle({
      marginBottom: token.componentErrorMessageMediaMarginBottom,
    });
    const actions = rootQueries.getByTestId('ErrorMessage-actions');
    expect(actions).toHaveStyle({
      marginTop: token.componentErrorMessageActionContentMarginTop,
    });
    const button = rootQueries.getByText('Try Again');
    fireEvent.press(button);
    expect(mockFn).toHaveBeenCalledTimes(1);
  });
});
