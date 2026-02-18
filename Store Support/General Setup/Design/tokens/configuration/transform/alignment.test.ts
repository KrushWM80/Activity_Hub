import { alignment } from "./alignment";

describe("alignment transform", () => {
  test("Should transform alignment tokens for web correctly.", () => {
    expect(
      alignment["alignment/web"].transformer({
        original: {
          value: "center",
        },
        value: "center",
        name: "",
        path: [],
        filePath: "",
        isSource: false,
      }),
    ).toEqual("center");

    expect(
      alignment["alignment/web"].transformer({
        original: {
          value: "end",
        },
        value: "end",
        name: "",
        path: [],
        filePath: "",
        isSource: false,
      }),
    ).toEqual("flex-end");

    expect(
      alignment["alignment/web"].transformer({
        original: {
          value: "space-between",
        },
        value: "space-between",
        name: "",
        path: [],
        filePath: "",
        isSource: false,
      }),
    ).toEqual("space-between");

    expect(
      alignment["alignment/web"].transformer({
        original: {
          value: "start",
        },
        value: "start",
        name: "",
        path: [],
        filePath: "",
        isSource: false,
      }),
    ).toEqual("flex-start");
  });
});
