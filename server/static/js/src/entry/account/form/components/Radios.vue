<template>
    <ul :class="classes">
      <li v-for="(option, index) in options" :key="option.id">
        <input
          :id="index"
          :value="option.value"
          :name="name"
          :checked="value === option.value"
          type="radio"
          @change="onChange"
        />
        <label>{{ option.text }}</label>
      </li>
    </ul>
</template>
  
<script>
  import formElementMixin from '../mixins/element';
  
  export default {
    name: 'Frequency',
  
    mixins: [formElementMixin],

    props: {
      options: {
        type: Array,
        required: true,
      },
    },
  
    methods: {
      onChange(event) {
        this.$emit('input', event.target.value);
      },
    },
  };
  </script>
  