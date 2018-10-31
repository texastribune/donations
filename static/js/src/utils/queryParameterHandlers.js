//
// Query parameters
// dirtyList - URL list of parameters of unknowm provenance
// whitelist - list of filter keys
// return values for valid keys
//
// Returns the valid query parameters based on the whitelist
// and the max number of characters filter
//
export default function queryParamWhiteListScrub(dirtyList, whiteList, maxNbrChars){
  return Object.keys(whiteList).reduce((result, key) =>
    (dirtyList[key] !== undefined
      ? (whiteList[key] = dirtyList[key].substring(0, maxNbrChars) )
      : whiteList),{});
}
