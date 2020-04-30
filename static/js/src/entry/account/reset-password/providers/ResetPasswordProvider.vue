<script>
import userMixin from '../../store/user/mixin';
import contextMixin from '../../store/context/mixin';

import { resetPassword } from '../../utils/auth-actions';

export default {
  name: 'ResetPasswordProvider',

  mixins: [userMixin, contextMixin],

  data() {
    return {
      pwResetSuccess: false,
      pwResetFailure: false,
    };
  },

  methods: {
    pwReset(gaLabel) {
      const { isViewingAs } = this.context;

      if (!isViewingAs) {
        const { email } = this.user;

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
      }
    },
  },

  render() {
    const { pwResetSuccess, pwResetFailure, pwReset } = this;

    return this.$scopedSlots.default({
      pwReset: {
        pwResetSuccess,
        pwResetFailure,
        pwReset,
      },
    });
  },
};
</script>
