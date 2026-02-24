<template>
  <div class="grid_row_centered grid_wrap--m form-buckets">
    <div
      v-for="bucket in buckets"
      :key="bucket.id"
      :class="{
        'form-buckets__item--selected': selectedBucket === bucket.name,
        'form-buckets__item--selected_border_bottom': (bucket.isDefault || bucket.isFeatured) && selectedBucket === bucket.name,
        'form-buckets__item--unselected': !bucket.isFeatured && selectedBucket !== bucket.name,
        'form-buckets__item--unselected_border_bottom': bucket.isDefault && selectedBucket !== bucket.name,
        'form-buckets__item--featured': bucket.isFeatured && selectedBucket !== bucket.name,
      }"
      class="form-buckets__item col_4 grid_separator"
    >
      <div class="form-buckets__prompt">{{ bucket.prompt }}</div>
      <p class="form-buckets__header grid_separator">{{ bucket.heading }}</p>
      <radios
        :options="bucket.options"
        :store-module="storeModule"
        base-classes="form__radios form__radios--always-stack form__radios--serif"
        name="level"
        @updateCallback="onUpdate"
      />
      <div v-if="bucket.footer" class="form-buckets__footer">{{ bucket.footer }}</div>
    </div>
  </div>
</template>

<script>
import Radios from './Radios.vue';
import getValue from './mixins/get-value';
import updateValues from './mixins/update-values';
import addNumberCommas from '../utils/add-number-commas';

export default {
  name: 'FormBuckets',

  components: { Radios },

  mixins: [getValue, updateValues],

  props: {
    allLevels: {
      type: Object,
      required: true,
    },

    storeModule: {
      type: String,
      required: true,
    },
  },

  data() {
    return {
      selectedBucket: this.getInitialSelectedBucket(),
      buckets: this.buildBuckets(),
    };
  },

  methods: {
    buildText({ installmentPeriod, amount }) {
      return `$${addNumberCommas(amount)} ${installmentPeriod}`;
    },

    buildOptions(levelsInBucket) {
      const { allLevels } = this;
      const levelsToIter = levelsInBucket.map(levelName => ({
        ...allLevels[levelName],
        levelName,
      }));

      return levelsToIter.map((level, index) => {
        const { installmentPeriod, amount, levelName } = level;

        return {
          id: index,
          value: levelName,
          text: this.buildText({ installmentPeriod, amount }),
        };
      });
    },

    buildBuckets() {
      const tempBuckets = {};
      const { allLevels } = this;

      Object.keys(allLevels).forEach(levelName => {
        const level = allLevels[levelName];
        const { bucket, bucketFull, isFeatured, isDefault, prompt, footer } = level;

        if (tempBuckets[bucket]) {
          tempBuckets[bucket].levelNames.push(levelName);
        } else {
          tempBuckets[bucket] = {
            bucketFull,
            isFeatured,
            isDefault,
            prompt,
            footer,
            levelNames: [levelName],
          };
        }
      });

      return Object.keys(tempBuckets).map((bucketName, index) => {
        const { bucketFull, isFeatured, isDefault, prompt, footer, levelNames } = tempBuckets[bucketName];
        return {
          id: index,
          name: bucketName,
          heading: bucketFull,
          isFeatured,
          isDefault,
          prompt,
          footer,
          options: this.buildOptions(levelNames),
        };
      });
    },

    getInitialSelectedBucket() {
      const { allLevels } = this;
      const level = this.getValue({
        storeModule: this.storeModule,
        key: 'level',
      });

      return allLevels[level].bucket;
    },

    onUpdate(newLevel) {
      const { allLevels, storeModule } = this;
      const { amount, bucket, installmentPeriod } = allLevels[newLevel];
      const updates = {
        installment_period: installmentPeriod,
        amount,
      };

      this.selectedBucket = bucket;
      this.updateValues({ storeModule, updates });
    },
  },
};
</script>
