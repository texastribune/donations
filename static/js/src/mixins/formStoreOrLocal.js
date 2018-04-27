import { mapGetters, mapActions } from 'vuex';

export default {
  props: {
    identifier: {
      type: String,
      required: true,
    },

    initialValue: {
      type: String,
      default: '',
    },

    paramValue: {
      type: String,
      default: '',
    },

    reactToParam: {
      type: Boolean,
      required: true,
    },

    useStore: {
      type: Boolean,
      required: true,
    },
  },

  data() {
    let localValue;

    if (this.reactToParam) {
      localValue = this.paramValue;
    } else {
      localValue = this.initialValue;
    }

    return { localValue };
  },

  computed: {
    ...mapGetters('form', [
      'storeValue',
    ]),

    value() {
      if (this.useStore) {
        return this.storeValue(this.identifier);
      }
      return this.localValue;
    },
  },

  watch: {
    paramValue(newValue, oldValue) {
      const shouldUpdate =
        (oldValue !== newValue) &&
        this.reactToParam;

      if (shouldUpdate) {
        this.updateValue(newValue);
      }
    },
  },

  methods: {
    ...mapActions('form', ['updateStoreValue']),

    updateValue(newValue) {
      if (this.useStore) {
        this.updateStoreValue({
          key: this.identifier,
          value: newValue,
        });
      } else {
        this.localValue = newValue;
      }
    },
  },
};
