import { mapGetters, mapActions } from 'vuex';

export default {
  props: {
    identifier: {
      type: String,
      required: true,
    },
  },

  computed: {
    ...mapGetters('form', [
      'storeValue',
    ]),

    value() {
      return this.storeValue(this.identifier);
    },
  },

  methods: {
    ...mapActions('form', ['updateStoreValue']),

    updateValue(newValue) {
      this.updateStoreValue({
        key: this.identifier,
        value: newValue,
      });
    },
  },
};
