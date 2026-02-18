module.exports = {
  semantic: {
    color: {
      border: {
        _: {
          comment: "Use for the border of generic elements",
          darkValue: "{primitive.color.white}",
          themeable: true,
          value: "{primitive.color.gray.160}",
        },

        activated: {
          comment: "Use for the border of elements in an activated state",
          darkValue: "{primitive.color.white}",
          themeable: true,
          value: "{primitive.color.blue.100}",
        },

        brand: {
          _: {
            comment: "Use for the border of elements that reinforce your brand",
            darkValue: "{primitive.color.blue.50}",
            themeable: true,
            value: "{primitive.color.blue.100}",
          },

          bold: {
            comment: "Use for bold brand border",
            darkValue: "{primitive.color.blue.160}",
            themeable: true,
            value: "{primitive.color.blue.160}",
          },
        },

        disabled: {
          comment: "Use for the border of elements in a disabled state",
          darkValue: "{primitive.color.gray.100}",
          themeable: true,
          value: "{primitive.color.gray.50}",
        },

        edited: {
          _: {
            comment: "Use for the border of elements in an edited state",
            darkValue: "{primitive.color.purple.50}",
            themeable: true,
            value: "{primitive.color.purple.100}",
          },

          bold: {
            comment: "Use for bold edited border",
            darkValue: "{primitive.color.purple.130}",
            themeable: true,
            value: "{primitive.color.purple.130}",
          },
        },

        info: {
          _: {
            comment:
              "Use for the border of elements that communicate information",
            darkValue: "{primitive.color.blue.50}",
            themeable: true,
            value: "{primitive.color.blue.100}",
          },

          bold: {
            comment: "Use for bold info border",
            darkValue: "{primitive.color.blue.130}",
            themeable: true,
            value: "{primitive.color.blue.130}",
          },
        },

        inverse: {
          comment:
            "Use for the border elements with opposite lightness of `color.border`",
          darkValue: "{primitive.color.gray.160}",
          themeable: true,
          value: "{primitive.color.white}",
        },

        magic: {
          start: {
            comment:
              "Use for the start of a gradient border that indicates the involvement of an AI agent",
            darkValue: "{primitive.color.magic.1}",
            themeable: true,
            value: "{primitive.color.magic.1}",
          },

          middle: {
            comment:
              "Use for the middle of a gradient border that indicates the involvement of an AI agent",
            darkValue: "{primitive.color.magic.2}",
            themeable: true,
            value: "{primitive.color.magic.2}",
          },

          stop: {
            comment:
              "Use for the end of a gradient border that indicates the involvement of an AI agent",
            darkValue: "{primitive.color.magic.3}",
            themeable: true,
            value: "{primitive.color.magic.3}",
          },
        },

        negative: {
          _: {
            comment:
              "Use for the border of elements that indicate danger or error state",
            darkValue: "{primitive.color.red.50}",
            themeable: true,
            value: "{primitive.color.red.100}",
          },

          bold: {
            comment: "Use for bold negative border",
            darkValue: "{primitive.color.red.130}",
            themeable: true,
            value: "{primitive.color.red.130}",
          },
        },

        positive: {
          _: {
            comment:
              "Use for the border of elements that communicate a favorable outcome",
            darkValue: "{primitive.color.green.50}",
            themeable: true,
            value: "{primitive.color.green.100}",
          },

          bold: {
            comment: "Use for bold positive border",
            darkValue: "{primitive.color.green.130}",
            themeable: true,
            value: "{primitive.color.green.130}",
          },
        },

        subtle: {
          comment: "Use for the border of generic elements with less emphasis",
          darkValue: "{primitive.color.gray.30}",
          themeable: true,
          value: "{primitive.color.gray.130}",
        },

        subtlest: {
          comment:
            "Use for the border of generic elements with the least emphasis",
          darkValue: "{primitive.color.gray.60}",
          themeable: true,
          value: "{primitive.color.gray.100}",
        },

        warning: {
          _: {
            comment: "Use for the border of elements that communicate caution",
            darkValue: "{primitive.color.spark.50}",
            themeable: true,
            value: "{primitive.color.spark.140}",
          },

          bold: {
            comment: "Use for bold warning border",
            darkValue: "{primitive.color.spark.160}",
            themeable: true,
            value: "{primitive.color.spark.160}",
          },
        },
      },
    },
  },
};
