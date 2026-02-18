module.exports = {
  semantic: {
    color: {
      surface: {
        _: {
          comment:
            "Use for elevated UIs such as cards, modals or dropdown menus",
          darkValue: "{primitive.color.gray.170}",
          themeable: true,
          value: "{primitive.color.white}",
        },

        focused: {
          comment: "Use for elevated UI containers in a focused state",
          darkValue: "{primitive.color.gray.160}",
          themeable: true,
          value: "{primitive.color.gray.10}",
        },

        hovered: {
          comment: "Use for elevated UI containers in a hovered state",
          darkValue: "{primitive.color.gray.160}",
          themeable: true,
          value: "{primitive.color.gray.10}",
        },

        pressed: {
          comment: "Use for elevated UI containers in a pressed state",
          darkValue: "{primitive.color.gray.150}",
          themeable: true,
          value: "{primitive.color.gray.20}",
        },

        activated: {
          _: {
            comment: "Use for elevated UI containers in an activated state",
            darkValue: "{primitive.color.gray.170}",
            themeable: true,
            value: "{primitive.color.blue.5}",
          },

          focused: {
            comment:
              "Use for elevated UI containers in an activated and focused state",
            darkValue: "{primitive.color.gray.160}",
            themeable: true,
            value: "{primitive.color.blue.10}",
          },

          hovered: {
            comment:
              "Use for elevated UI containers in an activated and hovered state",
            darkValue: "{primitive.color.gray.160}",
            themeable: true,
            value: "{primitive.color.blue.10}",
          },

          pressed: {
            comment:
              "Use for elevated UI containers in an activated and pressed state",
            darkValue: "{primitive.color.gray.150}",
            themeable: true,
            value: "{primitive.color.blue.20}",
          },
        },

        brand: {
          comment:
            "Use for elevated UI containers with a branded background color",
          darkValue: "{primitive.color.blue.140}",
          themeable: true,
          value: "{primitive.color.blue.10}",
        },

        overlay: {
          comment:
            "Use for the background color of overlays such as Modal, Bottom Sheet and Panel",
          darkValue: "{primitive.color.gray.160}",
          themeable: true,
          value: "{primitive.color.white}",
        },

        subtle: {
          _: {
            comment: "Use for elevated UI containers with less emphasis",
            darkValue: "{primitive.color.gray.170}",
            themeable: true,
            value: "{primitive.color.gray.5}",
          },

          focused: {
            comment:
              "Use for elevated UI containers with less emphasis with a focused state",
            darkValue: "{primitive.color.gray.160}",
            themeable: true,
            value: "{primitive.color.gray.10}",
          },

          hovered: {
            comment:
              "Use for elevated UI containers with less emphasis with a hovered state",
            darkValue: "{primitive.color.gray.160}",
            themeable: true,
            value: "{primitive.color.gray.10}",
          },

          pressed: {
            comment:
              "Use for elevated UI containers with less emphasis with a pressed state",
            darkValue: "{primitive.color.gray.150}",
            themeable: true,
            value: "{primitive.color.gray.20}",
          },
        },
      },
    },
  },
};
