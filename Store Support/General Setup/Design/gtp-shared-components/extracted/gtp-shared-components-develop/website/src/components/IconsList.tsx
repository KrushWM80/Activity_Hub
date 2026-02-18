import React, {useState} from 'react';

// @ts-ignore
import gtpSharedIcons from '@walmart/gtp-shared-icons/assets/icons.json';

export default function IconsList() {
  const [query, setQuery] = useState('');

  //getting all the keys as icons names
  const iconNames = Object.keys(gtpSharedIcons).filter(
    (item) =>
      item.includes(query.replace(/\s/g, '-')) ||
      item.replace(/-/g, '').includes(query),
  );

  return (
    <div className="icons-list-container">
      <input
        className="icons-list-searchbar"
        type="search"
        value={query}
        onChange={(event) => {
          setQuery(event.target.value);
        }}
        placeholder="Find icon by name…"
      />
      {iconNames.length ? (
        <div className="icons-list-results">
          {iconNames.map((name) => (
            <div className="icons-list-icon-container" key={name}>
              <span className="icons-list-icon">
                <img
                  alt=""
                  width="48"
                  height="48"
                  src={`data:image/svg+xml;base64,${gtpSharedIcons[name]}`}
                />
              </span>
              <span className="icons-list-icon-name">{`${name}Icon`}</span>
            </div>
          ))}
        </div>
      ) : (
        <p>No matching icon found :(</p>
      )}
    </div>
  );
}
