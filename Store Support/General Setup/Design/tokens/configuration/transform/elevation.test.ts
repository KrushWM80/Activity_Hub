import { elevation } from "./elevation";

describe("elevation transform", () => {
  test("Should match elevation tokens for iOS correctly.", () => {
    expect(
      elevation["elevation/ios"].matcher?.({
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
      elevation["elevation/ios"].matcher?.({
        path: ["elevation", "100", "value"],
        value: 100,
        name: "",
        original: {
          value: 100,
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe(true);
  });

  test("Should transform elevation tokens for iOS correctly.", () => {
    expect(
      elevation["elevation/ios"].transformer({
        filePath: "",
        isSource: true,
        name: "",
        path: [""],
        value: "",
        original: {
          value: {
            blur: "4px",
            color: "rgba(0, 0, 0, .5)",
            offsetX: "8px",
            offsetY: "12px",
            spread: "16px",
          },
        },
      }),
    ).toBe(`LivingDesignElevation(
      color: UIColor(red: 0.000, green: 0.000, blue: 0.000, alpha: 0.5),
      offset: CGSize(width: CGFloat(8.00), height: CGFloat(12.00)),
      radius: CGFloat(16.00)
    )`);
  });

  test("Should transform elevation tokens for web correctly.", () => {
    expect(
      elevation["elevation/web"].transformer({
        filePath: "",
        isSource: true,
        name: "",
        path: [""],
        value: "",
        original: {
          value: {
            blur: "4px",
            color: "rgba(0, 0, 0, .5)",
            offsetX: "8px",
            offsetY: "12px",
            spread: "16px",
          },
        },
      }),
    ).toBe("0.5rem 0.75rem 0.25rem 1rem rgba(0, 0, 0, .5)");
  });
});
