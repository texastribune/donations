import getRandomNumber from '../../utils/getRandomNumber';

// use randomly-generated numbers for tying form labels
// to form inputs so we can avoid unintentional id duplication
export default {
  data() {
    return { randConnector: getRandomNumber() };
  },
};
