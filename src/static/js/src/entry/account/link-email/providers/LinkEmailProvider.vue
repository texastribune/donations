<script>
import userMixin from '../../store/user/mixin';
import contextMixin from '../../store/context/mixin';

import { CONTEXT_TYPES, USER_TYPES } from '../../store/types';

export default {
  name: 'LinkEmailProvider',

  mixins: [userMixin, contextMixin],

  props: {
    gaLabel: {
      type: String,
      required: true,
    },
  },

  data() {
    return { submittedEmail: '' };
  },

  computed: {
    initialFields() {
      return { linkEmail: '' };
    },

    linkedEmails() {
      return this.user.linkedEmails;
    },
  },

  methods: {
    async linkEmail(fields) {
      const emailToLink = fields.linkEmail.value;

      this[CONTEXT_TYPES.setIsFetching](true);

      await this[USER_TYPES.linkIdentity]({ email: emailToLink });
      await this[USER_TYPES.getUser]();

      this.submittedEmail = emailToLink;
      this[CONTEXT_TYPES.setIsFetching](false);

      window.dataLayer.push({
        event: this.ga.customEventName,
        gaCategory: this.ga.userPortal.category,
        gaAction: this.ga.userPortal.actions['submit-linked-email'],
        gaLabel: this.gaLabel,
      });
    },
  },

  render() {
    const { initialFields, linkedEmails, linkEmail, submittedEmail } = this;

    return this.$scopedSlots.default({
      initialFields,
      linkedEmails,
      linkEmail,
      submittedEmail,
    });
  },
};
</script>
