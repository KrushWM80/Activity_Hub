import * as React from "react";
import classNames from "classnames";

import styles from "./TokenTable.module.css";
import { ComputedStyleProvider } from "./ComputedStyleProvider";
import { Platform, Token, platformTokenName } from "./utility";
import { TokenPreview } from "./TokenPreview";

export interface TokenTableProps extends React.ComponentPropsWithoutRef<"div"> {
  tokens: Token[];
}

export const TokenTable: React.FunctionComponent<TokenTableProps> = (props) => {
  const { className, tokens, ...rest } = props;

  const [filter, setFilter] = React.useState("");
  const [platform, setPlatform] = React.useState<Platform>("css");
  const [showInteractive, setShowInteractive] = React.useState(false);
  const showInteractiveControlId = React.useId();
  const platformPickerId = React.useId();

  const hasDarkValue = tokens.some((token) => !!token.darkValue);

  return (
    <ComputedStyleProvider>
      <div className={classNames(styles.container, className)} {...rest}>
        <div className={styles.toolbar}>
          <div className={styles.field}>
            <div className={styles.filterContainer}>
              <input
                aria-label="Filter by name"
                onChange={(event) => setFilter(event.target.value)}
                type="search"
                value={filter}
              />
            </div>
          </div>

          <div style={{ display: "flex", gap: "1rem" }}>
            <div className={styles.field}>
              <label htmlFor={showInteractiveControlId}>Interactive:</label>

              <input
                checked={showInteractive}
                id={showInteractiveControlId}
                onChange={() => setShowInteractive((x) => !x)}
                type="checkbox"
                value="1"
              />
            </div>

            <div className={styles.field}>
              <label htmlFor={platformPickerId}>Platform:</label>

              <div className={styles.platformPickerContainer}>
                <select
                  id={platformPickerId}
                  onChange={(event) =>
                    setPlatform(event.target.value as Platform)
                  }
                  value={platform}
                >
                  <option value="css">CSS</option>
                  <option value="js">JavaScript</option>
                  <option value="json">JSON</option>
                  <option value="scss">Sass</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <table className={styles.table}>
          <thead>
            <tr>
              <th>Token and Description</th>
              {hasDarkValue ? (
                <>
                  <th>Light Value</th>
                  <th>Dark Value</th>
                </>
              ) : (
                <th>Value</th>
              )}
              <th>Themeable</th>
            </tr>
          </thead>
          <tbody>
            {tokens.map((token, index) => {
              const name = platformTokenName[platform](token);

              if (
                (!showInteractive &&
                  (token.name.endsWith("-focused") ||
                    token.name.endsWith("-hovered") ||
                    token.name.endsWith("-pressed"))) ||
                (filter.length > 0 &&
                  !name
                    .replace(/ -\./g, "")
                    .includes(filter.replace(/ -\./g, "")))
              ) {
                return null;
              }

              return (
                <tr key={index}>
                  <td>
                    <code className={styles.name}>{name}</code>

                    {token.comment && (
                      <p className={styles.comment}>{token.comment}</p>
                    )}
                  </td>
                  {hasDarkValue ? (
                    <>
                      <td>
                        <TokenPreview
                          platform={platform}
                          theme="light"
                          token={token}
                        />
                      </td>
                      <td>
                        {!!token.darkValue && (
                          <TokenPreview
                            platform={platform}
                            theme="dark"
                            token={token}
                          />
                        )}
                      </td>
                    </>
                  ) : (
                    <td>
                      <TokenPreview platform={platform} token={token} />
                    </td>
                  )}
                  <td
                    className={classNames(
                      styles.themeable,
                      token.themeable && styles.true,
                    )}
                  >
                    {token.themeable ? "Yes" : "No"}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </ComputedStyleProvider>
  );
};
