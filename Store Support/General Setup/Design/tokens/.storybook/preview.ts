import { withThemeByClassName } from "@storybook/addon-themes";
import { Preview, ReactRenderer } from "@storybook/react";

import "@livingdesign/bogle/dist/Bogle.css";
import "@livingdesign/bogle/dist/BogleMono.css";

import "./styles/global.css";

const preview: Preview = {
  decorators: [
    withThemeByClassName<ReactRenderer>({
      defaultTheme: "Light",

      themes: {
        Light: "",
        Dark: "dark",
      },
    }),
  ],

  parameters: {
    controls: {
      disable: true,
    },
  },
};

export default preview;
