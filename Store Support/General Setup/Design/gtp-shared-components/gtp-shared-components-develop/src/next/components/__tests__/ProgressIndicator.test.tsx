import * as React from 'react';
import {FlexStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/ProgressIndicator';
import {render, screen, within} from '@testing-library/react-native';

import {
  ProgressIndicator,
  ProgressIndicatorProps,
  ProgressIndicatorVariant,
} from '../ProgressIndicator';

const resolveBackgroundColor = (v: ProgressIndicatorVariant) => {
  switch (v) {
    case 'error':
      return token.componentProgressIndicatorIndicatorVariantErrorBackgroundColor;
    case 'info':
      return token.componentProgressIndicatorIndicatorVariantInfoBackgroundColor;
    case 'success':
      return token.componentProgressIndicatorIndicatorVariantSuccessBackgroundColor;
    case 'warning':
      return token.componentProgressIndicatorIndicatorVariantWarningBackgroundColor;
    default:
      return token.componentProgressIndicatorIndicatorVariantErrorBackgroundColor;
  }
};

describe('ProgressIndicator', () => {
  it('renders correctly with default props', () => {
    // Render the ProgressIndicator component
    const defaultLabelElement = render(<ProgressIndicator />);
    expect(defaultLabelElement).toBeDefined();
  });

  it('renders correctly with custom props', () => {
    // Custom props for testing
    const customProps: ProgressIndicatorProps = {
      label: 'Custom Label',
      min: 0,
      max: 100,
      value: 50,
      valueLabel: '50%',
      variant: 'success',
    };

    // Render the ProgressIndicator component with custom props
    const {getByText} = render(<ProgressIndicator {...customProps} />);

    // Assert that the custom label is rendered
    const customLabelElement = getByText('Custom Label');
    expect(customLabelElement).toBeDefined();
  });

  it('test indicator width with value>defult_max_props_value', async () => {
    render(
      <ProgressIndicator
        label={'Test'}
        value={125}
        valueLabel="100% loaded"
        variant={'success'}
      />,
    );

    const progressIndicator = await screen.findByTestId('ProgressIndicator');
    expect(progressIndicator).toHaveStyle([
      {
        width: '100%',
        justifyContent: 'flex-start',
        alignItems: 'center',
        borderRadius: token.componentProgressIndicatorIndicatorBorderRadius,
      },
    ]);

    // Expect Track Container Styling
    const trackContainer = await screen.findByTestId(
      'ProgressIndicator-trackContainer',
    );
    expect(trackContainer).toHaveStyle([
      {
        width: '100%',
        backgroundColor: token.componentProgressIndicatorTrackBackgroundColor,
        borderRadius: token.componentProgressIndicatorTrackBorderRadius,
      },
    ]);

    // Expect Track Styling
    const track = await screen.findByTestId('ProgressIndicator-track');
    expect(track).toHaveStyle([
      {
        backgroundColor: resolveBackgroundColor('success'),
        width: '100%',
      },
    ]);
  });
});

describe.each<ProgressIndicatorVariant>([
  'error',
  'info',
  'success',
  'warning',
])('Should render ProgressIndicator correctly for all variants', (variant) => {
  test(`Test ProgressIndicator variant="${variant}"`, async () => {
    const rootQueries = render(
      <ProgressIndicator
        label={'Test'}
        value={25}
        valueLabel="25% loaded"
        variant={variant}
      />,
    );

    const progressIndicator = await rootQueries.findByTestId(
      'ProgressIndicator',
    );
    expect(progressIndicator).toHaveStyle([
      {
        width: '100%',
        justifyContent: 'flex-start',
        alignItems: 'center',
        borderRadius: token.componentProgressIndicatorIndicatorBorderRadius,
      },
    ]);

    // Expect Track Container Styling
    const trackContainer = await rootQueries.findByTestId(
      'ProgressIndicator-trackContainer',
    );
    expect(trackContainer).toHaveStyle([
      {
        width: '100%',
        backgroundColor: token.componentProgressIndicatorTrackBackgroundColor,
        borderRadius: token.componentProgressIndicatorTrackBorderRadius,
      },
    ]);

    // Expect Track Styling
    const track = await rootQueries.findByTestId('ProgressIndicator-track');
    expect(track).toHaveStyle([
      {
        backgroundColor: resolveBackgroundColor(variant),
        width: '25%',
      },
    ]);

    // Expect Label Container Styling
    const labelContainer = await rootQueries.findByTestId(
      'ProgressIndicator-labelContainer',
    );
    expect(labelContainer).toHaveStyle([
      {
        width: '100%',
        flexDirection: 'row',
        marginTop: token.componentProgressIndicatorLabelContainerMarginTop,
        justifyContent:
          token.componentProgressIndicatorLabelContainerAlignHorizontal as Extract<
            FlexStyle,
            'justifyContent'
          >,
        alignItems: 'center',
      },
    ]);
    const labelQueries = within(
      await rootQueries.findByTestId('ProgressIndicator'),
    );
    const label = await labelQueries.findByText('Test');
    const valueLabel = await labelQueries.findByText('25% loaded');

    // Expect Label Styling
    expect(label).toHaveStyle([
      {
        fontSize: token.componentProgressIndicatorTextLabelFontSize,
        color: token.componentProgressIndicatorTextLabelTextColor,
        maxWidth: '90%',
        flexWrap: 'wrap',
        alignSelf: 'flex-start',
      },
    ]);

    // Expect Value Label Styling
    expect(valueLabel).toHaveStyle([
      {
        fontSize: token.componentProgressIndicatorHelperTextFontSize,
        marginLeft: token.componentProgressIndicatorHelperTextMarginStart,
        marginTop: token.componentProgressIndicatorHelperTextMarginTop,
        color: token.componentProgressIndicatorHelperTextTextColor,
        alignSelf: 'flex-start',
        maxWidth: '90%',
        flexWrap: 'wrap',
      },
    ]);
  });
  test(`Test plain ProgressIndicator variant="${variant}"`, async () => {
    const rootQueries = render(
      <ProgressIndicator value={25} variant={variant} />,
    );
    const progressIndicator = await rootQueries.findByTestId(
      'ProgressIndicator',
    );
    expect(progressIndicator).toHaveStyle([
      {
        width: '100%',
        justifyContent: 'flex-start',
        alignItems: 'center',
        borderRadius: token.componentProgressIndicatorIndicatorBorderRadius,
      },
    ]);

    // Expect Track Container Styling
    const trackContainer = await rootQueries.findByTestId(
      'ProgressIndicator-trackContainer',
    );
    expect(trackContainer).toHaveStyle([
      {
        width: '100%',
        backgroundColor: token.componentProgressIndicatorTrackBackgroundColor,
        borderRadius: token.componentProgressIndicatorTrackBorderRadius,
      },
    ]);

    // Expect Track Styling
    const track = await rootQueries.findByTestId('ProgressIndicator-track');
    expect(track).toHaveStyle([
      {
        backgroundColor: resolveBackgroundColor(variant),
        width: '25%',
      },
    ]);

    const labelQueries = within(
      await rootQueries.findByTestId('ProgressIndicator'),
    );
    if (ProgressIndicator.displayName) {
      const label = labelQueries.queryAllByTestId(
        `${ProgressIndicator.displayName}_label`,
      );
      const valueLabel = labelQueries.queryAllByTestId(
        `${ProgressIndicator.displayName}_valueLabel`,
      );
      expect(label.length).toEqual(0);
      expect(valueLabel.length).toEqual(0);
    }
  });
});
