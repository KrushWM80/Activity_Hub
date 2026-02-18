import { pxSize } from "./pxSize";

describe("pxSize transform", () => {
  test("Should transform px tokens for Android correctly.", () => {
    expect(
      pxSize["pxSize/android"].transformer({
        attributes: {
          category: "font",
        },
        name: "name",
        value: "12px",
        path: [],
        original: {
          value: "12px",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe("12sp");

    expect(
      pxSize["pxSize/android"].transformer({
        attributes: {
          category: "space",
        },
        name: "name",
        value: "16px",
        path: [],
        original: {
          value: "16px",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe("16dp");
  });

  test("Should match px tokens for React Native correctly.", () => {
    expect(
      pxSize["pxSize/reactnative"].matcher?.({
        value: 0,
        name: "",
        path: [],
        original: {
          value: 0,
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(false);
    expect(
      pxSize["pxSize/reactnative"].matcher?.({
        value: "1",
        name: "",
        path: [],
        original: {
          value: "1",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(false);
    expect(
      pxSize["pxSize/reactnative"].matcher?.({
        value: "2px",
        name: "",
        path: [],
        original: {
          value: "2px",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(true);
  });

  test("Should transform px tokens for React Native correctly.", () => {
    expect(
      pxSize["pxSize/reactnative"].transformer({
        value: "3px",
        name: "",
        path: [],
        original: {
          value: "3px",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(3);
  });

  test("Should match px tokens for web correctly.", () => {
    expect(
      pxSize["pxSize/web"].matcher?.({
        value: 5,
        name: "",
        path: [],
        original: {
          value: 5,
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(false);
    expect(
      pxSize["pxSize/web"].matcher?.({
        value: "6",
        name: "",
        path: [],
        original: {
          value: "6",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(false);
    expect(
      pxSize["pxSize/web"].matcher?.({
        value: "7px",
        name: "",
        path: [],
        original: {
          value: "7px",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(true);
  });

  test("Should transform px tokens for web correctly", () => {
    expect(
      pxSize["pxSize/web"].transformer({
        value: "8px",
        name: "",
        path: [],
        original: {
          value: "8px",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe("0.5rem");
  });
});
