module.exports = {
  semantic: {
    color: {
      text: {
        onFill: {
          _: {
            comment: "Use for text on generic elements",
            darkValue: "{primitive.color.white}",
            themeable: true,
            value: "{primitive.color.gray.160}",
          },

          activated: {
            _: {
              comment: "Use for text on elements in an activated state",
              darkValue: "{primitive.color.gray.160}",
              themeable: true,
              value: "{primitive.color.white}",
            },

            disabled: {
              comment:
                "Use for text on elements in an activated state in a disabled state",
              darkValue: "{primitive.color.gray.160}",
              themeable: true,
              value: "{primitive.color.white}",
            },

            subtle: {
              _: {
                comment:
                  "Use for text on elements in an activated state but with less emphasis",
                darkValue: "{primitive.color.white}",
                themeable: true,
                value: "{primitive.color.gray.160}",
              },

              disabled: {
                comment:
                  "Use for text on elements in an activated state but with less emphasis in a disabled state",
                darkValue: "{primitive.color.white}",
                themeable: true,
                value: "{primitive.color.gray.50}",
              },
            },
          },

          brand: {
            _: {
              comment: "Use for text on elements with branded fill",
              darkValue: "{primitive.color.gray.160}",
              themeable: true,
              value: "{primitive.color.white}",
            },

            bold: {
              comment:
                "Use for text on elements with branded fill but with more emphasis",
              darkValue: "{primitive.color.gray.160}",
              themeable: true,
              value: "{primitive.color.white}",
            },

            subtle: {
              comment: "Use for text on elements with subtle branded fill",
              darkValue: "{primitive.color.blue.30}",
              themeable: true,
              value: "{primitive.color.blue.110}",
            },
          },

          disabled: {
            comment: "Use for text on generic elements in disabled state",
            darkValue: "{primitive.color.gray.160}",
            themeable: true,
            value: "{primitive.color.gray.50}",
          },

          edited: {
            _: {
              comment: "Use for text on elements in an edited state",
              darkValue: "{primitive.color.gray.160}",
              themeable: true,
              value: "{primitive.color.white}",
            },

            subtle: {
              comment:
                "Use for text on elements in an edited state but with less emphasis",
              darkValue: "{primitive.color.purple.30}",
              themeable: true,
              value: "{primitive.color.purple.130}",
            },
          },

          info: {
            _: {
              comment: "Use for text on elements that communicate information",
              darkValue: "{primitive.color.gray.160}",
              themeable: true,
              value: "{primitive.color.white}",
            },

            subtle: {
              comment:
                "Use for text on elements that communicate information but with less emphasis",
              darkValue: "{primitive.color.blue.30}",
              themeable: true,
              value: "{primitive.color.blue.130}",
            },
          },

          inverse: {
            comment: "Use for text on elements with inverse fill",
            darkValue: "{primitive.color.gray.160}",
            themeable: true,
            value: "{primitive.color.white}",
          },

          negative: {
            _: {
              comment:
                "Use for text on elements that indicate danger or error state",
              darkValue: "{primitive.color.gray.160}",
              themeable: true,
              value: "{primitive.color.white}",
            },

            subtle: {
              comment:
                "Use for text on elements that indicate danger or error state but with less emphasis",
              darkValue: "{primitive.color.red.30}",
              themeable: true,
              value: "{primitive.color.red.130}",
            },
          },

          positive: {
            _: {
              comment:
                "Use for text on elements that communicate a favorable outcome",
              darkValue: "{primitive.color.gray.160}",
              themeable: true,
              value: "{primitive.color.white}",
            },

            subtle: {
              comment:
                "Use for text on elements that communicate a favorable outcome but with less emphasis",
              darkValue: "{primitive.color.green.30}",
              themeable: true,
              value: "{primitive.color.green.130}",
            },
          },

          transparent: {
            comment: "Use for text on elements with transparent fill",
            darkValue: "{primitive.color.white}",
            themeable: true,
            value: "{primitive.color.gray.160}",
          },

          warning: {
            _: {
              comment: "Use for text on elements that emphasize caution",
              darkValue: "{primitive.color.gray.160}",
              themeable: true,
              value: "{primitive.color.gray.160}",
            },

            subtle: {
              comment:
                "Use for text on elements that emphasize caution but with less emphasis",
              darkValue: "{primitive.color.spark.30}",
              themeable: true,
              value: "{primitive.color.spark.160}",
            },
          },
        },
      },
    },
  },
};
