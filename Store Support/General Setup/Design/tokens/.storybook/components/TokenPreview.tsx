import * as React from "react";
import classNames from "classnames";
import tinycolor from "tinycolor2";

import styles from "./TokenPreview.module.css";
import { Platform, Token, platformTokenName } from "./utility";
import { useComputedStyle } from "./ComputedStyleProvider";

export interface TokenPreviewProps
  extends React.ComponentPropsWithoutRef<"span"> {
  platform: Platform;
  theme?: "dark" | "light";
  token: Token;
}

export const TokenPreview: React.FunctionComponent<TokenPreviewProps> = (
  props,
) => {
  const { className, platform, theme = "light", token, ...rest } = props;
  const { darkValue, darkValueReference, name, value, valueReference } = token;

  const computedStyle = useComputedStyle();

  const themeValue = theme === "light" ? value : darkValue;
  const themeValueReference =
    theme === "light" ? valueReference : darkValueReference;
  const previewValue = themeValueReference
    ? `var(${platformTokenName.css(themeValueReference)})`
    : themeValue;

  let preview: React.ReactNode;

  if (name.includes("border-radius")) {
    preview = (
      <span
        className={styles.previewBorderRadius}
        style={{
          borderRadius: previewValue,
        }}
      />
    );
  } else if (name.includes("-border-width")) {
    preview = (
      <span
        className={styles.previewBorderWidth}
        style={{
          borderWidth: previewValue,
        }}
      />
    );
  } else if (name.includes("color")) {
    let isLowContrast = false;

    if (typeof previewValue === "string" && previewValue.startsWith("var(--")) {
      const propertyValue = computedStyle.getPropertyValue(
        platformTokenName.css(themeValueReference!),
      );
      const color = tinycolor(propertyValue);

      isLowContrast =
        (theme === "dark"
          ? color.getBrightness() < 55
          : color.getBrightness() > 200) || color.getAlpha() < 0.2;
    }

    preview = (
      <span
        className={classNames(
          styles.previewColor,
          isLowContrast && styles.isLowContrast,
        )}
        style={{
          background: previewValue,
          fontSize: "100rem !important",
        }}
      />
    );
  } else if (name.includes("elevation") && typeof previewValue === "string") {
    preview = (
      <span
        className={styles.previewElevation}
        style={{
          boxShadow: previewValue,
        }}
      />
    );
  } else if (name.includes("font-family") && typeof previewValue === "string") {
    preview = (
      <span className={styles.previewFont} style={{ fontFamily: previewValue }}>
        Hamburgfontsiv
      </span>
    );
  } else if (name.includes("font-size")) {
    preview = (
      <span
        className={styles.previewFont}
        style={{
          fontSize: previewValue,
        }}
      >
        Aa
      </span>
    );
  } else if (name.includes("font-weight")) {
    preview = (
      <span className={styles.previewFont} style={{ fontWeight: previewValue }}>
        Hamburgfontsiv
      </span>
    );
  } else if (
    name.includes("-height") ||
    (name.includes("-width") && !name.includes("max-width")) ||
    name.includes("scale-space") ||
    name.includes("scale-icon") ||
    (typeof previewValue === "string" && previewValue.includes("scale-space"))
  ) {
    preview = (
      <span
        className={styles.previewSpace}
        style={{
          height: previewValue,
          width: previewValue,
        }}
      />
    );
  }

  return (
    <span
      className={classNames(
        styles.container,
        theme === "dark" && styles.dark,
        theme === "light" && styles.light,
        className,
      )}
      {...rest}
    >
      {preview && <span className={styles.preview}>{preview}</span>}

      <code className={styles.value}>
        {themeValueReference
          ? platformTokenName[platform](themeValueReference)
          : themeValue}
      </code>
    </span>
  );
};
