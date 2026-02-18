Color is the foundation of Living Design. It distinguishes our brand and helps us to create consistent experiences across marketing and products. We use color in meaningful ways in all expressions of our brand. From showing the colorful complexity of teaming up at a high level all the way down to focused, meaningful colors in product, we use color to pinpoint exactly what people need to see.

We are committed to complying with AA standard contrast ratios. To do this, we use various number of shade and tint colors that support usability. This ensures sufficient color contrast between elements so that users with low vision can see and use our products.

## Color Spectrum

This library contains the color values for Living Design. These are exposed via a JSON file for easy reference.

The color families in the spectrum contain nineteen values from 05 to 180. White and Black sit outside those values. Black text is WCAG AA accessible on most colors ranging from 0 to 60. White text is accessible on most colors from 100 to 200. Palettes below demonstrate accessibility using a minimum 4.5:1 contrast ratio.

```js static
import {colors} from '@walmart/gtp-shared-icons';

console.log(colors.blue['100']); // #0071dc
```

```js noeditor
<Palette />
```

## Accessibility

### Selecting Contrasting Colors

Using various forms of contrast is the most important consideration when making user-friendly color and interface choices. Awareness of standards and best practices is the key to accessible color selection.

```js static
import {colors, contrastColors} from '@walmart/gtp-shared-icons';

const base = colors.blue['100'];
const light = colors.blue['20'];
const dark = colors.blue['150'];

console.log(contrastColors(base, light, dark)); // #cce3f8 -- colors.blue['20']
```

Calling `contrastColors` without a light / dark color will return white or black respectively.

```js static
import {colors, contrastColors} from '@walmart/gtp-shared-icons';

const base = colors.blue['100'];

console.log(contrastColors(base)); // #ffffff
```

### Checking Color Contrast

Standard text (or images of text) must have a contrast of at least **4.5**.

Large text (at least 24 if the font weight is regular or light, and 16 when bold) must have a contrast of **3**.

UI Components must also have a contrast of **3**.

```js static
import {colors, contrastColors} from '@walmart/gtp-shared-icons';

const base = colors.blue['100'];
const light = colors.blue['20'];
const dark = colors.blue['150'];

console.log(contrastColors(base, light)); // 3.619730504875145
console.log(contrastColors(base, dark)); // 2.427911501976125
console.log(contrastColors(base, '#ffffff')); // 4.395512324883211
console.log(contrastColors(base, '#000000')); // 4.7776000720366465
```
