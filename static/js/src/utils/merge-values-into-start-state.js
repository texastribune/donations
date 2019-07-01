/*
  Take a static form state object (for example,
  the one in entry/donate/constants.js) and update each
  nested object's "value" key with values from either
  query params or from a JSON blob in the template if
  the card information was invalid on submission.
*/

export default function mergeValuesIntoStartState(startState, values) {
  Object.keys(startState).forEach(key => {
    if (values[key]) {
      // eslint-disable-next-line no-param-reassign
      startState[key].value = values[key];
    }
  });

  return startState;
}
