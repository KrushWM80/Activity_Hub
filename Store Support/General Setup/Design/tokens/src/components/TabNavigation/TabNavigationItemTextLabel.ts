module.exports = {
  component: {
    tabNavigation: {
      itemTextLabel: {
        aliasName: {
          value: "text.body",
        },

        aliasOptions: {
          size: {
            value: "small",
          },
        },

        state: {
          activated: {
            fontWeight: {
              value: "alt",
            },

            textColor: {
              _: {
                value: "{semantic.color.pageNav.text.onFill.activated}",
              },
            },
          },
        },

        textColor: {
          _: {
            value: "{semantic.color.pageNav.text.onFill._}",
          },
        },
      },
    },
  },
};
