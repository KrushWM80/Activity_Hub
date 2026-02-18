// @ts-nocheck
import uniqBy from 'lodash/uniqBy';
import filter from 'lodash/filter';

export const ME = 'Me';
export const MY_TEAM = 'my team';
export const WATCHLIST = {
  SIGNOFF: 'SignOff',
  CHECKED: 'CHECKED',
  NUMBER: 'registerNumber',
  USER_ID: 'userId',
  TEAM_ID: 'teamId',
  TEAM_NAME: 'teamName',
  DISPLAY_NAME: 'displayName',
  ADD: 'ADD',
  REMOVE: 'REMOVE',
  ADD_WATCHLIST: 'ADD_TO_WATCHLIST',
  REMOVE_WATCHLIST: 'REMOVE_FROM_WATCHLIST',
  ADD_MSG: 'Added to your issues.',
  REMOVE_MSG: 'Removed from your issues.',
  ERROR_MSG: 'Error updating the issues.',
};
export const getUniqFilteredList = <T>(d: T[], keyName: string = 'id'): T[] =>
  uniqBy(filter(d, keyName), keyName);

const searchForTermByKeyName =
  (keyName: string) =>
  (d: any[] = [], search: string = ''): any[] =>
    d.filter(element => {
      if (typeof element?.[keyName] === 'string') {
        return element[keyName].toUpperCase().includes(search.toUpperCase());
      }
      return false;
    });

const searchTeams = searchForTermByKeyName('teamName');
const searchDisplayNames = searchForTermByKeyName('displayName');

export const getTeamsData = (
  sectionWithTeam: any[] = [],
  searchPhrase: string,
): any[] => {
  return sectionWithTeam.reduce((result: any, sectionData) => {
    const {section, data} = sectionData;
    const filteredData = searchTeams(data, searchPhrase);
    if (filteredData.length) {
      return [...result, {data: filteredData, section, id: result.length}];
    }
    return result;
  }, []);
};

export const getListData = (section: any[] = [], searchPhrase: string = '') => {
  return section.reduce((result, sectionData) => {
    const {teamName, teamId, data} = sectionData;
    const filteredData = searchDisplayNames(data, searchPhrase);
    if (filteredData.length) {
      return [
        ...result,
        {
          teamName,
          teamId,
          data: filteredData,
        },
      ];
    }
    return result;
  }, []);
};

export const getMyTeam = (item, userTeams: any[] = []) => {
  const userTeam = userTeams.map(team => team?.teamId);
  return userTeam.includes(item?.teamId);
};

export const getLabel = (item, userTeams) => {
  const _formattedTeamName = getMyTeam(item, userTeams)
    ? ' ' + addBrackets(MY_TEAM.toLowerCase())
    : '';
  return `${toTitleCase(item?.teamName)} ${_formattedTeamName}`;
};

export const getListLabel = (item, userId) => {
  const _formattedListLabel =
    item?.userId === userId && userId ? addBrackets(ME.toLowerCase()) : '';
  return `${toTitleCase(item?.displayName)}  ${_formattedListLabel}`;
};

export const addBrackets = (data: string | number) => {
  return `(${data})`;
};
export const toTitleCase = function (text) {
  if (typeof text === 'string' || text instanceof String) {
    return text?.replace(/\w\S*/g, function (txt) {
      return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
  }
  return text;
};
