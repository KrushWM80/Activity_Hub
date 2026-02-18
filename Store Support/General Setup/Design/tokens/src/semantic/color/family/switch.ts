module.exports = {
  semantic: {
    color: {
      switch: {
        fill: {
          _: {
            darkValue: "{primitive.color.gray.50}",
            themeable: true,
            value: "{primitive.color.gray.100}",
          },

          hovered: {
            darkValue: "{primitive.color.gray.40}",
            themeable: true,
            value: "{primitive.color.gray.110}",
          },

          focused: {
            darkValue: "{primitive.color.gray.40}",
            themeable: true,
            value: "{primitive.color.gray.110}",
          },

          pressed: {
            darkValue: "{primitive.color.gray.30}",
            themeable: true,
            value: "{primitive.color.gray.130}",
          },

          disabled: {
            darkValue: "{primitive.color.gray.100}",
            themeable: true,
            value: "{primitive.color.gray.20}",
          },

          activated: {
            _: {
              darkValue: "{primitive.color.white}",
              themeable: true,
              value: "{primitive.color.blue.100}",
            },

            hovered: {
              darkValue: "{primitive.color.gray.10}",
              themeable: true,
              value: "{primitive.color.blue.110}",
            },

            focused: {
              darkValue: "{primitive.color.gray.10}",
              themeable: true,
              value: "{primitive.color.blue.110}",
            },

            pressed: {
              darkValue: "{primitive.color.gray.20}",
              themeable: true,
              value: "{primitive.color.blue.130}",
            },

            disabled: {
              darkValue: "{primitive.color.gray.100}",
              themeable: true,
              value: "{primitive.color.gray.20}",
            },
          },
        },

        indicator: {
          _: {
            darkValue: "{primitive.color.gray.160}",
            themeable: true,
            value: "{primitive.color.white}",
          },

          disabled: {
            darkValue: "{primitive.color.gray.160}",
            themeable: true,
            value: "{primitive.color.gray.50}",
          },
        },
      },
    },
  },
};
