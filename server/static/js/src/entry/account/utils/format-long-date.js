import format from 'date-fns/format';
import parse from 'date-fns/parse';

export default function formatLongDate(date) {
  return format(parse(date), 'MMMM D, YYYY');
}
