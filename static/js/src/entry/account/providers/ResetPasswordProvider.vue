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
    resetPassword() {
      const { email } = this.tokenUser;

      resetPassword(email, err => {
        if (err) {
          this.pwResetFailure = true;
        } else {
          this.pwResetSuccess = true;
        }
      });
    },
  },

  render() {
    const { pwResetSuccess, pwResetFailure } = this;

    return this.$scopedSlots.default({ pwResetSuccess, pwResetFailure });
  },
};
</script>
