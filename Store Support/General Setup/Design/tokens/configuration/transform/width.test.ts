import { width } from "./width";

describe("width transform", () => {
  test("Should match width tokens correctly.", () => {
    expect(
      width["width/toPercent"].matcher?.({
        path: ["color", "core", "black", "value"],
        value: "color.core.black",
        name: "",
        original: {
          value: "color.core.black",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(false);

    expect(
      width["width/toPercent"].matcher?.({
        path: ["width", "fill-parent"],
        value: "fill-parent",
        name: "",
        original: {
          value: "fill-parent",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(true);

    expect(
      width["width/toPercent"].matcher?.({
        path: ["width", "fill-screen"],
        value: "fill-screen",
        name: "",
        original: {
          value: "fill-screen",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(true);

    expect(
      width["width/toPercent"].matcher?.({
        path: ["width", "hug-contents"],
        value: "hug-contents",
        name: "",
        original: {
          value: "hug-contents",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(true);

    expect(
      width["width/toPercent"].matcher?.({
        path: ["width", "100px"],
        value: "100px",
        name: "",
        original: {
          value: "100px",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(true);

    expect(
      width["width/toPercent"].matcher?.({
        path: ["width", "100px"],
        value: "100px",
        name: "",
        original: {
          value: "100px",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(true);
  });

  test("Should transform width tokens correctly.", () => {
    expect(
      width["width/toPercent"].transformer({
        value: "fill-parent",
        original: {
          value: "fill-parent",
        },
        name: "",
        path: [],
        filePath: "",
        isSource: false,
      }),
    ).toBe("100%");

    expect(
      width["width/toPercent"].transformer({
        value: "fill-screen",
        original: {
          value: "fill-screen",
        },
        name: "",
        path: [],
        filePath: "",
        isSource: false,
      }),
    ).toBe("100%");

    expect(
      width["width/toPercent"].transformer({
        value: "hug-contents",
        original: {
          value: "hug-contents",
        },
        name: "",
        path: [],
        filePath: "",
        isSource: false,
      }),
    ).toBe("100%");

    expect(
      width["width/toPercent"].transformer({
        value: "100px",
        original: {
          value: "100px",
        },
        name: "",
        path: [],
        filePath: "",
        isSource: false,
      }),
    ).toBe("100px");

    expect(
      width["width/toPercent"].transformer({
        value: "auto",
        original: {
          value: "auto",
        },
        name: "",
        path: [],
        filePath: "",
        isSource: false,
      }),
    ).toBe("auto");
  });
});
