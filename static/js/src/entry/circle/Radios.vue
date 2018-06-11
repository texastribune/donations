<template>
  <ul
    :class="classes"
  >
    <li
      v-for="(option, index) in options"
      :key="option.id"
    >
      <input
        :value="option.value"
        :name="name"
        :checked="value === option.value"
        :id="getLabelConnector(index)"
        type="radio"
        @input="onInput"
      >
      <label
        :for="getLabelConnector(index)"
      >
        {{ option.text }}
      </label>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'Radios',

  props: {
    options: {
      type: Array,
      required: true,
    },

    value: {
      type: String,
      required: true,
    },
  },

  methods: {
    getLabelConnector(index) {
      return `${this.name}-${index}`;
    },

    onInput({ target: { value } }) {
      this.$emit('input', value);
      this.$emit('updateCallback', value);
    },
  },
};
</script>
