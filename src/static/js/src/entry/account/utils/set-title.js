import { TITLE_SUFFIX } from '../constants';

export default function setTitle(title) {
  document.title = `${title} ${TITLE_SUFFIX}`;
}
