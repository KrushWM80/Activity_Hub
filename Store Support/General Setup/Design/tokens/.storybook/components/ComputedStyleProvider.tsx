import * as React from "react";

type ComputedStyleValue = CSSStyleDeclaration;

const ComputedStyleContext = React.createContext<ComputedStyleValue>(
  {} as ComputedStyleValue,
);

const getValue = (): ComputedStyleValue =>
  getComputedStyle(document.documentElement);

export interface ComputedStyleProviderProps {
  children?: React.ReactNode;
}

export const ComputedStyleProvider: React.FunctionComponent<
  ComputedStyleProviderProps
> = (props) => {
  const { children } = props;

  const [value, setValue] = React.useState<ComputedStyleValue>(getValue);

  React.useEffect(() => {
    const mutationObserver = new MutationObserver(() => {
      setValue(getValue);
    });

    mutationObserver.observe(document.documentElement, {
      attributes: true,
      /** @note The @storybook/addon-themes toggles themes via `class`. */
      attributeFilter: ["class"],
    });

    return () => mutationObserver.disconnect();
  }, []);

  return (
    <ComputedStyleContext.Provider value={value}>
      {children}
    </ComputedStyleContext.Provider>
  );
};

export const useComputedStyle = () => {
  const cssReflection = React.useContext(ComputedStyleContext);

  return cssReflection;
};
