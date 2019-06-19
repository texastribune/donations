import format from 'date-fns/format';
import parse from 'date-fns/parse';

export default function formatShortDate(date) {
  return format(parse(date), 'MM/DD/YY');
}
