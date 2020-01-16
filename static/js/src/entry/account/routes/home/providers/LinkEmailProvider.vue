<script>
import userMixin from '../../../store/user/mixin';
import contextMixin from '../../../store/context/mixin';
import LinkEmail from '../components/LinkEmail.vue';

export default {
  name: 'LinkEmailProvider',

  components: { LinkEmail },

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
      return this.user.identities.map(({ email }) => email);
    },
  },

  methods: {
    async linkEmail(fields) {
      const emailToLink = fields.linkEmail.value;

      this.setAppIsFetching(true);

      await this.linkIdentity({ email: emailToLink });
      await this.getUser();

      this.submittedEmail = emailToLink;

      this.setAppIsFetching(false);

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
