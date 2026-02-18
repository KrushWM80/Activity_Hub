import { timing } from "./timing";

describe("timing transform", () => {
  test("Should match timing tokens for iOS correctly.", () => {
    expect(
      timing["timing/ios"].matcher?.({
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
      timing["timing/ios"].matcher?.({
        path: ["timing", "100", "value"],
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

  test("Should transform timing tokens for iOS correctly.", () => {
    expect(
      timing["timing/ios"].transformer({
        value: "linear",
        name: "",
        path: [],
        original: {
          value: "linear",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe("CAMediaTimingFunctionName.linear");

    expect(
      timing["timing/ios"].transformer({
        value: "cubic-bezier(0.42, 0.0, 0.58, 1.0)",
        name: "",
        path: [],
        original: {
          value: "cubic-bezier(0.42, 0.0, 0.58, 1.0)",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(
      "CAMediaTimingFunction(controlPoints: CGFloat(0.42), CGFloat(0.00), CGFloat(0.58), CGFloat(1.00))",
    );
  });
});
