module.exports = {
  semantic: {
    color: {
      background: {
        _: {
          comment: "Use for the screen's main background color",
          darkValue: "{primitive.color.gray.180}",
          themeable: true,
          value: "{primitive.color.white}",
        },

        inverse: {
          comment:
            "Use for a background color that's the opposite lightness of `color.background`",
          darkValue: "{primitive.color.white}",
          themeable: true,
          value: "{primitive.color.gray.160}",
        },

        subtle: {
          comment:
            "Use for a subtle, neutral background that accentuates overlaid surfaces",
          darkValue: "{primitive.color.gray.180}",
          themeable: true,
          value: "{primitive.color.gray.5}",
        },
      },
    },
  },
};
