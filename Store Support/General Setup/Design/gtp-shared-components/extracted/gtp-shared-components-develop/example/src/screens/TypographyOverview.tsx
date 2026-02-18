import * as React from 'react';
import {Text, StyleSheet, TextStyle, View} from 'react-native';
import {Header, Page, Section} from '../components';
import {
  colors,
  Body,
  BodyWeight,
  BodySize,
  Caption,
  CaptionWeight,
  Display,
  DisplaySize,
  DisplayWeight,
  Heading,
  HeadingSize,
  HeadingWeight,
  Weights,
  TypographyColors,
  getFont,
} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={styles.spacer} />;

const BodyVariant = ({
  weight,
  size,
  color,
  isMonospace,
}: {
  weight?: BodyWeight;
  size?: BodySize;
  color?: TypographyColors;
  isMonospace?: boolean;
}) => {
  let children = 'Body';
  if (weight) {
    children = `${children} weight="${weight}"`;
  }
  if (size) {
    children = `${children} size="${size}"`;
  }
  if (color) {
    children = `${children} color="${color}"`;
  }
  if (!size && !weight && !isMonospace) {
    children = `${children} (defaults)`;
  }
  return (
    <>
      <Body
        color={color}
        weight={weight}
        size={size}
        isMonospace={isMonospace}
        UNSAFE_style={styles.text}>
        {children}
      </Body>
    </>
  );
};

const DisplayVariant = ({
  weight,
  size,
  color,
}: {
  weight?: DisplayWeight;
  size?: DisplaySize;
  color?: TypographyColors;
}) => {
  let children = 'Display';
  if (weight) {
    children = `${children} weight="${weight}"`;
  }
  if (size) {
    children = `${children} size="${size}"`;
  }
  if (color) {
    children = `${children} color="${color}"`;
  }
  if (!size && !weight) {
    children = `${children} (defaults)`;
  }
  return (
    <>
      <Display
        color={color}
        weight={weight}
        size={size}
        UNSAFE_style={styles.text}>
        {children}
      </Display>
    </>
  );
};

const HeadingVariant = ({
  weight,
  size,
  color,
}: {
  weight?: HeadingWeight;
  size?: HeadingSize;
  color?: TypographyColors;
}) => {
  let children = 'Heading';
  if (weight) {
    children = `${children} weight="${weight}"`;
  }
  if (size) {
    children = `${children} size="${size}"`;
  }
  if (color) {
    children = `${children} color="${color}"`;
  }

  if (!size && !weight) {
    children = `${children} (defaults)`;
  }
  return (
    <>
      <Heading
        color={color}
        weight={weight}
        size={size}
        UNSAFE_style={styles.text}>
        {children}
      </Heading>
    </>
  );
};

const CaptionVariant = ({
  weight,
  color,
}: {
  weight?: CaptionWeight;
  color?: TypographyColors;
}) => {
  let children = 'Caption';
  if (weight) {
    children = `${children} weight="${weight}"`;
  }
  if (color) {
    children = `${children} color="${color}"`;
  }
  if (!weight && !color) {
    children = `${children} (defaults)`;
  }
  return (
    <>
      <Caption color={color} weight={weight} UNSAFE_style={styles.text}>
        {children}
      </Caption>
    </>
  );
};

const TextFontVariant = ({
  weight,
  isMonospace,
}: {
  weight?: Weights;
  isBold?: boolean;
  isMonospace?: boolean;
}) => {
  const font = getFont(weight, isMonospace);
  delete font?.fontStyle;
  return (
    <>
      <Text style={[styles.text, font as TextStyle]}>
        {JSON.stringify(font)}
        {'\n'}ABCDEFGHIJKLMN O P 1234567890
      </Text>
      <Spacer />
    </>
  );
};

const TypographyOverview: React.FC = () => {
  return (
    <Page>
      <Header>Font Regular</Header>
      <Section color={colors.gray['10']}>
        <TextFontVariant weight={'normal'} />
        <TextFontVariant weight={'bold'} />
      </Section>

      <Header>Font Monospace</Header>
      <Section color={colors.gray['10']}>
        <TextFontVariant weight={'normal'} isMonospace />
        <TextFontVariant weight={'bold'} isMonospace />
      </Section>

      <Header>Body</Header>
      <Section color={colors.gray['10']}>
        <BodyVariant />
        <Spacer />
        <BodyVariant size="small" weight="400" />
        <BodyVariant size="medium" weight="400" />
        <BodyVariant size="large" weight="400" />
        <Spacer />
        <BodyVariant size="small" weight="700" />
        <BodyVariant size="medium" weight="700" />
        <BodyVariant size="large" weight="700" />
      </Section>

      <Header>Body Monospace</Header>
      <Section color={colors.gray['10']}>
        <BodyVariant size="small" weight="400" isMonospace />
        <BodyVariant size="medium" weight="400" isMonospace />
        <BodyVariant size="large" weight="400" isMonospace />
        <Spacer />
        <BodyVariant size="small" weight="700" isMonospace />
        <BodyVariant size="medium" weight="700" isMonospace />
        <BodyVariant size="large" weight="700" isMonospace />
      </Section>

      <Header>Body color</Header>
      <Section color={colors.gray['10']}>
        <BodyVariant size="small" color="black" />
        <BodyVariant size="medium" weight="400" isMonospace />
        <BodyVariant size="large" weight="400" color="spark160" />
        <Spacer />
        <BodyVariant size="small" weight="700" color="green50" isMonospace />
        <BodyVariant size="large" color="purple120" isMonospace />
      </Section>

      <Header>Caption</Header>
      <Section color={colors.gray['10']}>
        <CaptionVariant />
        <Spacer />
        <CaptionVariant weight="400" />
        <CaptionVariant weight="700" />
      </Section>

      <Header>Caption color</Header>
      <Section color={colors.gray['10']}>
        <CaptionVariant color="spark160" />
        <CaptionVariant weight="700" color="purple120" />
      </Section>

      <Header>Display</Header>
      <Section color={colors.gray['10']}>
        <DisplayVariant />
        <Spacer />
        <DisplayVariant size="small" weight="400" />
        <DisplayVariant size="large" weight="400" />
        <Spacer />
        <DisplayVariant size="small" weight="700" />
        <DisplayVariant size="large" weight="700" />
      </Section>

      <Header>Display color</Header>
      <Section color={colors.gray['10']}>
        <DisplayVariant size="small" color="green80" />
        <DisplayVariant size="large" color="spark160" />
        <Spacer />
        <DisplayVariant size="small" weight="700" color="purple120" />
        <DisplayVariant size="large" weight="700" color="black" />
      </Section>

      <Header>Heading</Header>
      <Section color={colors.gray['10']}>
        <HeadingVariant />
        <Spacer />
        <HeadingVariant size="small" weight="400" />
        <HeadingVariant size="medium" weight="400" />
        <HeadingVariant size="large" weight="400" />
        <Spacer />
        <HeadingVariant size="small" weight="700" />
        <HeadingVariant size="medium" weight="700" />
        <HeadingVariant size="large" weight="700" />
      </Section>

      <Header>Heading color</Header>
      <Section color={colors.gray['10']}>
        <HeadingVariant size="small" color="green80" />
        <HeadingVariant size="medium" weight="400" color="spark160" />
        <HeadingVariant size="large" weight="400" />
        <Spacer />
        <HeadingVariant size="small" weight="700" color="black" />
        <HeadingVariant size="medium" color="purple120" />
        <HeadingVariant size="large" weight="700" />
      </Section>
    </Page>
  );
};

const styles = StyleSheet.create({
  text: {
    alignSelf: 'flex-start',
  },
  spacer: {
    height: 8,
  },
});

export {TypographyOverview};
