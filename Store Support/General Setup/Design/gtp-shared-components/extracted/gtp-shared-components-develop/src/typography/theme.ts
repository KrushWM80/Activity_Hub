import {colors as allColors} from '../next/utils';
import {font, FontDetails, getFont, Weights, weights} from '../theme/font';

type FontWithColor = Record<string, FontDetails & {color: string}>;

const color = allColors.black;
const bodyVariants: FontWithColor = {};
weights.map((weight) => {
  bodyVariants[`${weight}`] = {
    ...font.text.body,
    ...getFont(weight as Weights, false),
    color,
  };
});

export const body = bodyVariants;
export const body2 = {...(font.text.body2 ?? {}), color};
export const caption = {...(font.text.caption ?? {}), color};
export const caption2 = {...(font.text.caption2 ?? {}), color};
export const display = {...(font.text.display ?? {}), color};
export const display2 = {...(font.text.display2 ?? {}), color};
export const headline = {...(font.text.headline ?? {}), color};
export const priceSmall = {...(font.price.small ?? {}), color};
export const priceMedium = {...(font.price.medium ?? {}), color};
export const priceLarge = {...(font.price.large ?? {}), color};
export const subheader = {...(font.text.subheader ?? {}), color};
export const subheader2 = {...(font.text.subheader2 ?? {}), color};
export const title = {...(font.text.title ?? {}), color};
export const title2 = {...(font.text.title2 ?? {}), color};
export const title3 = {...(font.text.title3 ?? {}), color};
export default {
  typography: {
    body,
    body2,
    caption,
    caption2,
    display,
    display2,
    headline,
    priceSmall,
    priceMedium,
    priceLarge,
    subheader,
    subheader2,
    title,
    title2,
    title3,
  },
};
