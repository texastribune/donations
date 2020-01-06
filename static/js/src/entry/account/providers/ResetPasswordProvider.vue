<script>
import tokenUserMixin from '../store/token-user/mixin';
import { resetPassword } from '../utils/auth-actions';

export default {
  name: 'ResetPasswordProvider',

  mixins: [tokenUserMixin],

  data() {
    return {
      pwResetSuccess: false,
      pwResetFailure: false,
    };
  },

  methods: {
    pwReset(gaLabel) {
      const { email } = this.tokenUser;

      resetPassword(email, err => {
        if (err) {
          this.pwResetFailure = true;
        } else {
          this.pwResetSuccess = true;

          window.dataLayer.push({
            event: this.ga.customEventName,
            gaCategory: this.ga.userPortal.category,
            gaAction: this.ga.userPortal.actions['reset-password'],
            gaLabel,
          });
        }
      });
    },
  },

  render() {
    const { pwResetSuccess, pwResetFailure, pwReset } = this;

    return this.$scopedSlots.default({
      pwResetSuccess,
      pwResetFailure,
      pwReset,
    });
  },
};
</script>
