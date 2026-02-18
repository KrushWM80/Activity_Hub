module.exports = {
  semantic: {
    color: {
      text: {
        _: {
          comment: "Use for primary text, such as headings and body copy",
          darkValue: "{primitive.color.white}",
          themeable: true,
          value: "{primitive.color.gray.160}",
        },

        activated: {
          comment: "Use for text that indicates an activated state",
          darkValue: "{primitive.color.white}",
          themeable: true,
          value: "{primitive.color.blue.110}",
        },

        brand: {
          _: {
            comment: "Use for text that reinforces your brand",
            darkValue: "{primitive.color.blue.50}",
            themeable: true,
            value: "{primitive.color.blue.100}",
          },

          bold: {
            comment: "Use for bold brand text",
            darkValue: "{primitive.color.blue.160}",
            themeable: true,
            value: "{primitive.color.blue.160}",
          },
        },

        disabled: {
          comment: "Use for text that indicates a disabled state",
          darkValue: "{primitive.color.gray.100}",
          themeable: true,
          value: "{primitive.color.gray.50}",
        },

        edited: {
          _: {
            comment: "Use for text that indicates an edited state",
            darkValue: "{primitive.color.purple.50}",
            themeable: true,
            value: "{primitive.color.purple.100}",
          },

          bold: {
            comment: "Use for bold edited text",
            darkValue: "{primitive.color.purple.130}",
            themeable: true,
            value: "{primitive.color.purple.130}",
          },
        },

        info: {
          _: {
            comment: "Use for text that reinforces your info",
            darkValue: "{primitive.color.blue.50}",
            themeable: true,
            value: "{primitive.color.blue.100}",
          },

          bold: {
            comment: "Use for bold info text",
            darkValue: "{primitive.color.blue.130}",
            themeable: true,
            value: "{primitive.color.blue.130}",
          },
        },

        inverse: {
          comment: "Use for text that's the opposite lightness of `color.text`",
          darkValue: "{primitive.color.gray.160}",
          themeable: true,
          value: "{primitive.color.white}",
        },

        magic: {
          start: {
            comment:
              "Use for the start of gradient text that indicates the involvement of an AI agent",
            darkValue: "{primitive.color.magic.1}",
            themeable: true,
            value: "{primitive.color.magic.1}",
          },

          middle: {
            comment:
              "Use for the middle of gradient text that indicates the involvement of an AI agent",
            darkValue: "{primitive.color.magic.2}",
            themeable: true,
            value: "{primitive.color.magic.2}",
          },

          stop: {
            comment:
              "Use for the end of gradient text that indicates the involvement of an AI agent",
            darkValue: "{primitive.color.magic.3}",
            themeable: true,
            value: "{primitive.color.magic.3}",
          },
        },

        negative: {
          _: {
            comment:
              "Use for critical text that indicates an error such as input field error messaging",
            darkValue: "{primitive.color.red.50}",
            themeable: true,
            value: "{primitive.color.red.100}",
          },

          bold: {
            comment: "Use for bold negative text",
            darkValue: "{primitive.color.red.130}",
            themeable: true,
            value: "{primitive.color.red.130}",
          },
        },

        positive: {
          _: {
            comment: "Use for text that communicates a favorable outcome",
            darkValue: "{primitive.color.green.50}",
            themeable: true,
            value: "{primitive.color.green.100}",
          },

          bold: {
            comment: "Use for bold positive text",
            darkValue: "{primitive.color.green.130}",
            themeable: true,
            value: "{primitive.color.green.130}",
          },
        },

        subtle: {
          comment: "Use for navigation and form field labels",
          darkValue: "{primitive.color.gray.30}",
          themeable: true,
          value: "{primitive.color.gray.130}",
        },

        subtlest: {
          comment:
            "Use for secondary text such as supplementary helper text on an element",
          darkValue: "{primitive.color.gray.60}",
          themeable: true,
          value: "{primitive.color.gray.100}",
        },

        warning: {
          _: {
            comment:
              "Use for text that emphasizes caution such as an alert message",
            darkValue: "{primitive.color.spark.50}",
            themeable: true,
            value: "{primitive.color.spark.140}",
          },

          bold: {
            comment: "Use for bold warning text",
            darkValue: "{primitive.color.spark.160}",
            themeable: true,
            value: "{primitive.color.spark.160}",
          },
        },
      },
    },
  },
};
