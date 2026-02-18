import iconKeywords from "@livingdesign/icons/dist/keywords.json";

type IconTokenDefinition = Record<
  string,
  {
    value: keyof typeof iconKeywords;
    themeable?: boolean;
  }
>;

const semanticIconTokenDefinitions: IconTokenDefinition = {
  calendar: {
    value: "Calendar",
    themeable: true,
  },

  close: {
    value: "Close",
    themeable: true,
  },

  edit: {
    value: "Pencil",
    themeable: true,
  },

  error: {
    value: "ExclamationCircle",
    themeable: true,
  },

  errorText: {
    value: "ExclamationCircleFill",
    themeable: true,
  },

  info: {
    value: "InfoCircle",
    themeable: true,
  },

  metricDown: {
    value: "ArrowDown",
    themeable: true,
  },

  metricUp: {
    value: "ArrowUp",
    themeable: true,
  },

  more: {
    value: "More",
    themeable: true,
  },

  pageNext: {
    value: "ChevronRight",
    themeable: true,
  },

  pagePrevious: {
    value: "ChevronLeft",
    themeable: true,
  },

  save: {
    value: "CheckCircleFill",
    themeable: true,
  },

  selected: {
    value: "Check",
    themeable: true,
  },

  selectExpand: {
    value: "CaretDown",
    themeable: true,
  },

  sortAscending: {
    value: "ArrowUp",
    themeable: true,
  },

  sortDescending: {
    value: "ArrowDown",
    themeable: true,
  },

  success: {
    value: "CheckCircle",
    themeable: true,
  },

  warning: {
    value: "Warning",
    themeable: true,
  },
};

module.exports = {
  semantic: {
    icon: semanticIconTokenDefinitions,
  },
};
