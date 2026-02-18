module.exports = {
  semantic: {
    color: {
      fill: {
        _: {
          comment: "Use for the background of generic elements",
          darkValue: "{primitive.color.transparentLight.0}",
          themeable: true,
          value: "{primitive.color.white}",
        },

        focused: {
          comment:
            "Use for the background of generic elements in focused state",
          darkValue: "{primitive.color.transparentLight.10}",
          themeable: true,
          value: "{primitive.color.gray.10}",
        },

        hovered: {
          comment:
            "Use for the background of generic elements in hovered state",
          darkValue: "{primitive.color.transparentLight.10}",
          themeable: true,
          value: "{primitive.color.gray.10}",
        },

        pressed: {
          comment:
            "Use for the background of generic elements in pressed state",
          darkValue: "{primitive.color.transparentLight.20}",
          themeable: true,
          value: "{primitive.color.gray.20}",
        },

        subtle: {
          comment:
            "Use for the background of generic elements with less emphasis",
          darkValue: "{primitive.color.gray.5}",
          themeable: true,
          value: "{primitive.color.gray.5}",
        },

        activated: {
          _: {
            comment: "Use for the background of elements in an activated state",
            darkValue: "{primitive.color.blue.50}",
            themeable: true,
            value: "{primitive.color.blue.100}",
          },

          focused: {
            comment:
              "Use for the background of elements in an activated and focused state",
            darkValue: "{primitive.color.blue.40}",
            themeable: true,
            value: "{primitive.color.blue.110}",
          },

          hovered: {
            comment:
              "Use for the background of elements in an activated and hovered state",
            darkValue: "{primitive.color.blue.40}",
            themeable: true,
            value: "{primitive.color.blue.110}",
          },

          pressed: {
            comment:
              "Use for the background of elements in an activated and pressed state",
            darkValue: "{primitive.color.blue.30}",
            themeable: true,
            value: "{primitive.color.blue.130}",
          },

          disabled: {
            comment:
              "Use for the background of elements in an activated and disabled state",
            darkValue: "{primitive.color.gray.100}",
            themeable: true,
            value: "{primitive.color.gray.50}",
          },

          subtle: {
            _: {
              comment:
                "Use for the background of elements in an activated state but with less emphasis",
              darkValue: "{primitive.color.gray.160}",
              themeable: true,
              value: "{primitive.color.blue.5}",
            },

            focused: {
              comment:
                "Use for the background of elements in an activated and focused state but with less emphasis",
              darkValue: "{primitive.color.gray.150}",
              themeable: true,
              value: "{primitive.color.blue.10}",
            },

            hovered: {
              comment:
                "Use for the background of elements in an activated and hovered state but with less emphasis",
              darkValue: "{primitive.color.gray.150}",
              themeable: true,
              value: "{primitive.color.blue.10}",
            },

            pressed: {
              comment:
                "Use for the background of elements in an activated and pressed state but with less emphasis",
              darkValue: "{primitive.color.gray.140}",
              themeable: true,
              value: "{primitive.color.blue.20}",
            },

            disabled: {
              comment:
                "Use for the background of elements in an activated and disabled state but with less emphasis",
              darkValue: "{primitive.color.gray.160}",
              themeable: true,
              value: "{primitive.color.gray.5}",
            },
          },
        },

        disabled: {
          comment:
            "Use for the background of generic elements in disabled state",
          darkValue: "{primitive.color.gray.100}",
          themeable: true,
          value: "{primitive.color.white}",
        },

        brand: {
          _: {
            comment:
              "Use for the background of elements that reinforce your brand",
            darkValue: "{primitive.color.blue.50}",
            themeable: true,
            value: "{primitive.color.blue.100}",
          },

          bold: {
            comment:
              "Use for the background of elements that reinforce your brand but with more emphasis",
            darkValue: "{primitive.color.blue.5}",
            themeable: true,
            value: "{primitive.color.blue.160}",
          },

          subtle: {
            comment:
              "Use for the background of elements that reinforce your brand, but with less emphasis",
            darkValue: "{primitive.color.blue.140}",
            themeable: true,
            value: "{primitive.color.blue.10}",
          },
        },

        edited: {
          _: {
            comment: "Use for the background of elements in an edited state",
            darkValue: "{primitive.color.purple.50}",
            themeable: true,
            value: "{primitive.color.purple.100}",
          },

          subtle: {
            comment:
              "Use for the background of elements in an edited state but with less emphasis",
            darkValue: "{primitive.color.purple.140}",
            themeable: true,
            value: "{primitive.color.purple.10}",
          },
        },

        info: {
          _: {
            comment:
              "Use for the background of elements that communicate information",
            darkValue: "{primitive.color.blue.50}",
            themeable: true,
            value: "{primitive.color.blue.100}",
          },

          subtle: {
            comment:
              "Use for the background of elements that communicate information, but with less emphasis",
            darkValue: "{primitive.color.blue.140}",
            themeable: true,
            value: "{primitive.color.blue.10}",
          },
        },

        inverse: {
          comment:
            "Use for the background of elements with opposite lightness of `color.fill`",
          darkValue: "{primitive.color.white}",
          themeable: true,
          value: "{primitive.color.gray.160}",
        },

        negative: {
          _: {
            comment:
              "Use for the background of elements that indicate danger or error state",
            darkValue: "{primitive.color.red.50}",
            themeable: true,
            value: "{primitive.color.red.100}",
          },

          subtle: {
            comment:
              "Use for the background of elements that indicate danger or error state, but with less emphasis",
            darkValue: "{primitive.color.red.140}",
            themeable: true,
            value: "{primitive.color.red.10}",
          },
        },

        positive: {
          _: {
            comment:
              "Use for the background of elements that communicate a favorable outcome",
            darkValue: "{primitive.color.green.50}",
            themeable: true,
            value: "{primitive.color.green.100}",
          },

          subtle: {
            comment:
              "Use for the background of elements that communicate a favorable outcome but with less emphasis",
            darkValue: "{primitive.color.green.140}",
            themeable: true,
            value: "{primitive.color.green.10}",
          },
        },

        transparent: {
          comment: "Use for the background of elements with transparent fill",
          darkValue: "{primitive.color.transparentLight.0}",
          themeable: true,
          value: "{primitive.color.transparentDark.0}",
        },

        warning: {
          _: {
            comment:
              "Use for the background of elements that emphasize caution",
            darkValue: "{primitive.color.spark.50}",
            themeable: true,
            value: "{primitive.color.spark.100}",
          },

          subtle: {
            comment:
              "Use for the background of elements that emphasize caution but with less emphasis",
            darkValue: "{primitive.color.spark.140}",
            themeable: true,
            value: "{primitive.color.spark.10}",
          },
        },
      },
    },
  },
};
