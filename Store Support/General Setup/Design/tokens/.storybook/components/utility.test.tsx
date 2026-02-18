import { Token, platformTokenName } from "./utility";

describe("Storybook utility", () => {
  test("Should format CSS name correctly.", () => {
    expect(
      platformTokenName.css({
        path: ["component", "bottomSheet", "actionContent", "padding", "bS"],
      } as unknown as Token),
    ).toBe("--ld-component-bottom-sheet-action-content-padding-b-s");
  });

  test("Should format JS name correctly.", () => {
    expect(
      platformTokenName.js({
        path: ["component", "bottomSheet", "actionContent", "padding", "bS"],
      } as unknown as Token),
    ).toBe("componentBottomSheetActionContentPaddingBS");
  });

  test("Should format JSON name correctly.", () => {
    expect(
      platformTokenName.json({
        path: ["component", "bottomSheet", "actionContent", "padding", "bS"],
      } as unknown as Token),
    ).toBe("component.bottomSheet.actionContent.padding.bS");
  });

  test("Should format SCSS name correctly.", () => {
    expect(
      platformTokenName.scss({
        path: ["component", "bottomSheet", "actionContent", "padding", "bS"],
      } as unknown as Token),
    ).toBe("$component-bottom-sheet-action-content-padding-b-s");
  });
});
