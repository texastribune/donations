import store from '../store';
import { logIn } from '../utils/auth-actions';

export default {
  beforeRouteEnter(to, from, next) {
    if (!store.state.user.idToken) {
      logIn();
    } else {
      next();
    }
  },
};
