import { text } from "./text";

describe("textWrap transform", () => {
  test("Should match text wrap tokens for Android correctly.", () => {
    expect(
      text["text/wrap/android"].matcher?.({
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
      text["text/wrap/android"].matcher?.({
        path: ["component", "metric", "unit", "textWrap"],
        value: true,
        name: "",
        original: {
          value: true,
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(true);
  });

  test("Should transform text wrap tokens for Android correctly.", () => {
    expect(
      text["text/wrap/android"].transformer({
        attributes: {
          category: "textWrap",
        },
        name: "name",
        value: true,
        path: [],
        original: {
          value: true,
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(100);

    expect(
      text["text/wrap/android"].transformer({
        attributes: {
          category: "textWrap",
        },
        name: "name",
        value: false,
        path: [],
        original: {
          value: false,
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(1);
  });

  test("Should match text wrap tokens for iOS correctly.", () => {
    expect(
      text["text/wrap/ios"].matcher?.({
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
      text["text/wrap/ios"].matcher?.({
        path: ["component", "metric", "unit", "textWrap"],
        value: true,
        name: "",
        original: {
          value: true,
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(true);
  });

  test("Should transform text wrap tokens for iOS correctly.", () => {
    expect(
      text["text/wrap/ios"].transformer({
        attributes: {
          category: "text",
        },
        name: "name",
        value: true,
        path: [],
        original: {
          value: true,
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe("numberOfLines(0)");

    expect(
      text["text/wrap/ios"].transformer({
        attributes: {
          category: "text",
        },
        name: "name",
        value: false,
        path: [],
        original: {
          value: false,
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe("numberOfLines(1)");
  });

  test("Should match text wrap tokens for Web correctly.", () => {
    expect(
      text["text/wrap/web"].matcher?.({
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
      text["text/wrap/web"].matcher?.({
        path: ["component", "metric", "unit", "textWrap"],
        value: true,
        name: "",
        original: {
          value: true,
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(true);
  });

  test("Should transform text wrap tokens for Web correctly.", () => {
    expect(
      text["text/wrap/web"].transformer({
        attributes: {
          category: "text",
        },
        name: "name",
        value: true,
        path: [],
        original: {
          value: true,
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe("normal");

    expect(
      text["text/wrap/web"].transformer({
        attributes: {
          category: "text",
        },
        name: "name",
        value: false,
        path: [],
        original: {
          value: false,
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe("nowrap");
  });
});
