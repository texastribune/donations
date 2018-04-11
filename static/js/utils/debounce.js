export const CALL_AT_START_STR = 'didCallAtStart';

// https://davidwalsh.name/javascript-debounce-function
export default function debounce(func, wait, immediate) {
  let timeout;

  // eslint-disable-next-line
  return function (...args) {
    const context = this;
    const callNow = immediate && !timeout;

    clearTimeout(timeout);

    timeout = setTimeout(() => {
      timeout = null;

      if (!immediate) {
        func.apply(context, args);
      }
    }, wait);

    if (callNow) {
      func.apply(context, args);
      return CALL_AT_START_STR;
    }
  };
}
