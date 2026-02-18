import { TransformedToken } from "style-dictionary";
import { name } from "./name";

describe("name", () => {
  test("It should transform tokens with name/custom/camel correctly.", () => {
    expect(
      name["name/custom/camel"].transformer(
        {
          path: ["primitive", "color", "blue", "100"],
        } as TransformedToken,
        {
          prefix: "ld",
        },
      ),
    ).toBe("ldColorBlue100");

    expect(
      name["name/custom/camel"].transformer({
        path: ["semantic", "color", "text"],
      } as TransformedToken),
    ).toBe("colorText");

    expect(
      name["name/custom/camel"].transformer({
        path: ["component", "button", "container", "background", "color"],
      } as TransformedToken),
    ).toBe("containerBackgroundColor");
  });

  test("It should transform tokens with name/custom/kebab correctly.", () => {
    expect(
      name["name/custom/kebab"].transformer(
        {
          path: ["primitive", "color", "blue", "100"],
        } as TransformedToken,
        {
          prefix: "ld",
        },
      ),
    ).toBe("ld-color-blue-100");

    expect(
      name["name/custom/kebab"].transformer({
        path: ["semantic", "color", "text"],
      } as TransformedToken),
    ).toBe("color-text");

    expect(
      name["name/custom/kebab"].transformer({
        path: ["component", "button", "container", "background", "color"],
      } as TransformedToken),
    ).toBe("container-background-color");
  });
});
