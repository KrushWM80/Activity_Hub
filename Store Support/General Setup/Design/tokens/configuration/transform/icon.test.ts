import { icon } from "./icon";

describe("icon transform", () => {
  test("Should transform iconNames for android correctly.", () => {
    expect(
      icon["iconName/android"].transformer({
        value: "InfoCircle",
        name: "",
        path: [],
        original: {
          value: "InfoCircle",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe("@drawable/ld_ic_info_circle");
  });

  test("Should transform iconSizes for android correctly.", () => {
    expect(
      icon["iconSize/android"].transformer({
        value: "small",
        name: "",
        path: [],
        original: {
          value: "small",
        },
        filePath: "",
        isSource: false,
      }),
    ).toBe("@dimen/ld_size_icon_small");
  });
});
