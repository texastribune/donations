<script>
import userMixin from '../../../store/user/mixin';
import contextMixin from '../../../store/context/mixin';
import LinkEmail from '../components/LinkEmail.vue';

export default {
  name: 'LinkEmailProvider',

  components: { LinkEmail },

  mixins: [userMixin, contextMixin],

  data() {
    return { submittedEmail: '' };
  },

  computed: {
    initialFields() {
      return {
        linkEmail: {
          name: 'linkEmail',
          value: '',
          label: 'email address to link',
          rules: { required: true, email: true },
          isVisible: true,
        },
      };
    },

    linkedEmails() {
      return this.user.identities.map(({ email }) => email);
    },
  },

  methods: {
    async linkEmail({ linkEmail: { value } }) {
      this.setAppIsFetching(true);

      await this.linkIdentity({ email: value });
      await this.getUser();

      this.submittedEmail = value;
      this.setAppIsFetching(false);
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
