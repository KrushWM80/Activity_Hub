import { mega } from "./mega";

describe("mega", () => {
  test("It should match tokens correctly.", () => {
    expect(
      mega["mega"].matcher?.({
        filePath: "",
        isSource: true,
        name: "",
        original: {
          value: 0,
        },
        path: [""],
        value: 0,
      }),
    ).toBe(false);

    expect(
      mega["mega"].matcher?.({
        filePath: "",
        isSource: true,
        name: "",
        original: {
          value: "center",
        },
        path: [""],
        value: "center",
      }),
    ).toBe(false);

    expect(
      mega["mega"].matcher?.({
        filePath: "",
        isSource: true,
        name: "",
        original: {
          value: "600px",
        },
        path: ["size", "breakpoint", "medium"],
        value: "600px",
      }),
    ).toBe(false);

    expect(
      mega["mega"].matcher?.({
        filePath: "",
        isSource: true,
        name: "",
        original: {
          value: "12px",
        },
        path: ["font", "size", "12"],
        value: "12px",
      }),
    ).toBe(true);

    expect(
      mega["mega"].matcher?.({
        filePath: "",
        isSource: true,
        name: "",
        original: {
          value: "1px",
        },
        path: ["component", "alert", "container", "borderWidthStart"],
        value: "1px",
      }),
    ).toBe(true);

    expect(
      mega["mega"].matcher?.({
        filePath: "",
        isSource: true,
        name: "",
        original: {
          value: "12px",
        },
        path: ["font", "size", "25"],
        value: "12px",
      }),
    ).toBe(true);

    expect(
      mega["mega"].matcher?.({
        filePath: "",
        isSource: true,
        name: "",
        original: {
          value: [],
        },
        path: ["elevation", "100"],
        value: [],
      }),
    ).toBe(true);

    expect(
      mega["mega"].matcher?.({
        filePath: "",
        isSource: true,
        name: "",
        original: {
          value: "1px",
        },
        path: [
          "component",
          "datePicker",
          "rangeCalendarMonthsSeparator",
          "width",
        ],
        value: "1px",
      }),
    ).toBe(true);
  });

  describe("It should transform tokens correctly.", () => {
    test("It should transform border and separator width correctly.", () => {
      expect(
        mega["mega"].transformer({
          filePath: "",
          isSource: true,
          name: "",
          original: {
            value: "2px",
          },
          path: ["component", "button", "borderWidth", "focus"],
          value: "2px",
        }),
      ).toBe("4px");

      expect(
        mega["mega"].transformer({
          filePath: "",
          isSource: true,
          name: "",
          original: {
            value: "1px",
          },
          path: ["component", "alert", "container", "borderWidthStart"],
          value: "1px",
        }),
      ).toBe("2px");

      expect(
        mega["mega"].transformer({
          filePath: "",
          isSource: true,
          name: "",
          original: {
            value: "1px",
          },
          path: ["component", "datePicker", "separator", "width"],
          value: "1px",
        }),
      ).toBe("2px");

      expect(
        mega["mega"].transformer({
          filePath: "",
          isSource: true,
          name: "",
          original: {
            value: "1px",
          },
          path: [
            "component",
            "datePicker",
            "rangeCalendarMonthsSeparator",
            "width",
          ],
          value: "1px",
        }),
      ).toBe("2px");
    });

    test("It should transform elevation correctly.", () => {
      expect(
        mega["mega"].transformer({
          filePath: "",
          isSource: true,
          name: "",
          original: {
            value: [
              {
                blur: 2,
                color: "rgba(0, 0, 0, .25)",
                offsetX: 0,
                offsetY: 3,
                spread: 4,
              },
            ],
          },
          path: ["elevation", "100"],
          value: [
            {
              blur: 2,
              color: "rgba(0, 0, 0, .25)",
              offsetX: 0,
              offsetY: 3,
              spread: 4,
            },
          ],
        }),
      ).toEqual([
        {
          blur: 3,
          color: "rgba(0, 0, 0, .25)",
          offsetX: 0,
          offsetY: 4.5,
          spread: 6,
        },
      ]);
    });

    test("It should transform size correctly.", () => {
      expect(
        mega["mega"].transformer({
          filePath: "",
          isSource: true,
          name: "",
          original: {
            value: "12px",
          },
          path: ["font", "size", "12"],
          value: "12px",
        }),
      ).toBe("18px");
    });
  });
});
