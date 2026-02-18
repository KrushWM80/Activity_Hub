import * as React from 'react';
import {FlexStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/WizardFooter';
import {render} from '@testing-library/react-native';
import {getHostChildren} from '@testing-library/react-native/build/helpers/component-tree';

import {ProgressIndicator} from '../ProgressIndicator';
import {WizardFooter} from '../WizardFooter';

describe('first', () => {
  test('Test WizardFooter', async () => {
    const rootQueries = render(
      <WizardFooter
        previousActionProps={{
          variant: 'secondary',
          onPress: jest.fn(),
          children: 'Previous',
        }}
        nextActionProps={{
          variant: 'primary',
          onPress: jest.fn(),
          children: 'Continue',
        }}>
        <ProgressIndicator
          variant="info"
          label="Location"
          valueLabel="20%"
          value={20}
        />
      </WizardFooter>,
    );
    const wiz = await rootQueries.findByTestId('WizardFooter');
    expect(wiz).toHaveStyle({
      flex: 1,
      alignItems: token.componentWizardFooterContainerAlignVertical as Extract<
        FlexStyle,
        'alignItems'
      >,
      backgroundColor: token.componentWizardFooterContainerBackgroundColor,
      borderTopColor: token.componentWizardFooterContainerBorderColorTop,
      borderTopWidth: token.componentWizardFooterContainerBorderWidthTop,
      paddingHorizontal: token.componentWizardFooterContainerPaddingHorizontal,
      paddingVertical: token.componentWizardFooterContainerPaddingVerticalBS,
    });

    const buttons = await rootQueries.findAllByTestId('Button');
    expect(buttons[0]).toHaveStyle({
      flexDirection: 'row',
      justifyContent: 'center',
      overflow: 'visible',
    });

    expect(getHostChildren(buttons[1])[0]).toHaveStyle([
      {
        flexShrink: 1,
        flexDirection: 'row',
        borderRadius: 1000,
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden',
        borderWidth: 1,
      },
      {
        backgroundColor: '#0071dc',
        borderColor: '#0071dc',
      },
      {
        paddingHorizontal: 16,
        paddingVertical: 0,
      },
      {},
    ]);
  });
});
