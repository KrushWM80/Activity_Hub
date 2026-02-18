import path from "node:path";
import type { StorybookConfig } from "@storybook/react-webpack5";

const config: StorybookConfig = {
  stories: [
    path.join(__dirname, "../dist/storybook/**/*.stories.@(js|jsx|mjs|ts|tsx)"),
  ],
  addons: [
    "@storybook/addon-webpack5-compiler-swc",
    "@storybook/addon-essentials",
    "@storybook/addon-themes",
  ],
  framework: {
    name: "@storybook/react-webpack5",
    options: {},
  },
  typescript: {
    check: false,
  },
};

export default config;
