
//
// Query parameters
// dirtyList - URL list of parameters of unlnowm provenance
// whitelist - list of filter keys
// return values for valid keys
//
export default function queryParamWhiteListScrub(dirtyList, whitelist) {
  // Only process whitelisted parameters; for dupes the last value will bethe one used
  return whitelist.reduce((result, key) =>
    (dirtyList[key] !== undefined
      ? Object.assign(result, { [key]: dirtyList[key] })
      : result), {});
}
