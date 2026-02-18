import { addons } from "@storybook/manager-api";
import { create } from "@storybook/theming";

import { name, version } from "../package.json";

const theme = create({
  base: "light",
  brandTitle: `${name} (${version})`,
});

addons.setConfig({
  theme,
});
