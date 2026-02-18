import { duration } from "./duration";

describe("duration transform", () => {
  test("It should match duration tokens for Android.", () => {
    expect(
      duration["duration/android"].matcher?.({
        path: ["size", "space", "100"],
        value: "100",
        name: "",
        original: {
          value: "100",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(false);

    expect(
      duration["duration/android"].matcher?.({
        path: ["duration", "100"],
        value: "100",
        name: "",
        original: {
          value: "100",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(true);
  });

  test("Should match duration tokens for iOS correctly.", () => {
    expect(
      duration["duration/ios"].matcher?.({
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
      duration["duration/ios"].matcher?.({
        path: ["duration", "100"],
        value: "100",
        name: "",
        original: {
          value: "100",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(true);
  });

  test("It should transform duration tokens for Android.", () => {
    expect(
      duration["duration/android"].transformer({
        value: "0.2s",
        name: "",
        path: [""],
        original: {
          value: "0.2s",
        },
        filePath: "",
        isSource: true,
      }),
    ).toBe(200);
  });

  test("Should transform duration tokens for iOS correctly.", () => {
    expect(
      duration["duration/ios"].transformer({
        value: "0.5s",
        name: "",
        path: [""],
        original: {
          value: "0.5s",
        },
        filePath: "",
        isSource: true,
      }),
    ).toBe(0.5);
  });
});
