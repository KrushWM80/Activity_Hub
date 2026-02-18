import { alias } from "./alias";

describe("alias transform", () => {
  test("Should transform alias tokens for sass correctly.", () => {
    expect(
      alias["alias/sass"].transformer({
        value: "component.text.body",
        name: "",
        path: [],
        original: {
          value: "component.text.body",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe('"component.text.body"');
  });
});
