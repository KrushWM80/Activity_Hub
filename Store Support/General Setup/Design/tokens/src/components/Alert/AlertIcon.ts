module.exports = {
  component: {
    alert: {
      icon: {
        iconSize: {
          value: "small",
        },

        marginEnd: {
          value: "{primitive.scale.space.100}",
        },

        variant: {
          error: {
            iconColor: {
              value: "{semantic.color.text.onFill.negative.subtle}",
            },

            iconName: {
              value: "ExclamationCircle",
            },
          },

          info: {
            iconColor: {
              value: "{semantic.color.text.onFill.info.subtle}",
            },

            iconName: {
              value: "InfoCircle",
            },
          },

          success: {
            iconColor: {
              value: "{semantic.color.text.onFill.positive.subtle}",
            },

            iconName: {
              value: "CheckCircle",
            },
          },

          warning: {
            iconColor: {
              value: "{semantic.color.text.onFill.warning.subtle}",
            },

            iconName: {
              value: "Warning",
            },
          },
        },
      },
    },
  },
};
