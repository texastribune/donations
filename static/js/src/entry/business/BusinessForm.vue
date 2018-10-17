<template>
  <form
    ref="form"
    action="/business"
    method="post"
    class="form business-form"
    @submit="$event.preventDefault()"
  >

    <div
      v-show="showServerErrorMessage"
      class="grid_container--l grid_separator"
    >
      <div class="grid_row">
        <div class="col">
          <p class="form__error form__error--prominent">{{ serverErrorMessage }}</p>
        </div>
      </div>
    </div>

    <div class="grid_container--l grid_separator">
      <div class="grid_row">
        <div class="col">
          <choices />
        </div>
      </div>
    </div>

    <div class="grid_container--m">
      <div class="grid_row grid_separator">
        <div class="col">
          <text-input
            :show-error="showManualErrors || showNativeErrors"
            :validation="validation.stripeEmail"
            label-text="email address"
            maxlength="80"
            type="email"
            base-classes="form__text form__text--standard"
            name="stripeEmail"
            store-module="businessForm"
            @setValidationValue="setValidationValue"
          />
        </div>
      </div>

      <div class="grid_row grid_wrap--s">
        <div class="col_6 grid_separator">
          <text-input
            :show-error="showManualErrors || showNativeErrors"
            :validation="validation.business_name"
            label-text="business name"
            maxlength="255"
            base-classes="form__text form__text--standard"
            name="business_name"
            store-module="businessForm"
            @setValidationValue="setValidationValue"
          />
        </div>
        <div class="col_6 grid_separator">
          <text-input
            :show-error="showManualErrors || showNativeErrors"
            :validation="validation.website"
            label-text="website"
            maxlength="255"
            base-classes="form__text form__text--standard"
            name="website"
            store-module="businessForm"
            @setValidationValue="setValidationValue"
          />
        </div>
      </div>

      <div class="grid_row grid_separator">
        <div class="col">
          <text-input
            :show-error="showManualErrors || showNativeErrors"
            :validation="validation.shipping_street"
            label-text="street address"
            maxlength="255"
            base-classes="form__text form__text--standard"
            name="shipping_street"
            store-module="businessForm"
            @setValidationValue="setValidationValue"
          />
        </div>
      </div>

      <div class="grid_row grid_separator grid_wrap--s">
        <div class="col_6 grid_separator">
          <text-input
            :show-error="showManualErrors || showNativeErrors"
            :validation="validation.shipping_city"
            label-text="city"
            maxlength="40"
            base-classes="form__text form__text--standard"
            name="shipping_city"
            store-module="businessForm"
            @setValidationValue="setValidationValue"
          />
        </div>
        <div class="col_4 grid_separator">
          <select-list
            :options="options"
            label-text="state"
            base-classes="form__text form__text--standard"
            name="shipping_state"
            store-module="businessForm"
          />
        </div>
        <div class="col_2 grid_separator">
          <text-input
            :show-error="showManualErrors || showNativeErrors"
            :validation="validation.shipping_postalcode"
            label-text="zip code"
            maxlength="5"
            base-classes="form__text form__text--standard"
            name="shipping_postalcode"
            store-module="businessForm"
            @setValidationValue="setValidationValue"
          />
        </div>
      </div>

      <div class="grid_row grid_wrap--s">
        <div class="col_6 grid_separator">
          <text-input
            :show-error="showManualErrors || showNativeErrors"
            :validation="validation.first_name"
            label-text="contact first name"
            base-classes="form__text form__text--standard"
            name="first_name"
            store-module="businessForm"
            @setValidationValue="setValidationValue"
          />
        </div>
        <div class="col_6 grid_separator">
          <text-input
            :show-error="showManualErrors || showNativeErrors"
            :validation="validation.last_name"
            label-text="contact last name"
            base-classes="form__text form__text--standard"
            name="last_name"
            store-module="businessForm"
            @setValidationValue="setValidationValue"
          />
        </div>
      </div>

      <div class="grid_row grid_separator grid_wrap--s">
        <div class="col grid_separator">
          <text-input
            :required="false"
            label-text="encouraged to give by"
            maxlength="255"
            base-classes="form__text form__text--standard"
            name="reason"
            store-module="businessForm"
          />
        </div>
      </div>

      <div class="grid_row grid_separator">
        <div class="col">
          <pay-fees
            base-classes="form__fees"
            amount-store-module="businessForm"
            pay-fees-value-store-module="businessForm"
            installment-period-store-module="businessForm"
          />
        </div>
      </div>

      <div class="grid_row">
        <div class="col">
          <native-pay
            :form-is-valid="nativeIsValid"
            :supported="nativeIsSupported"
            base-classes="form__native"
            amount-store-module="businessForm"
            @setValue="setValue"
            @onSubmit="onSubmit"
          />
        </div>
      </div>

      <div
        v-if="nativeIsSupported && showManualPay"
        class="grid_separator--l"
        aria-hidden="true"
      />

      <div :aria-live="nativeIsSupported ? 'polite' : false">
        <div v-if="showManualPay">
          <div class="grid_row">
            <div class="col">
              <manual-pay
                :show-error="showManualErrors"
                :validation="validation.card"
                base-classes="form__manual"
                @setValidationValue="setValidationValue"
              />
            </div>
          </div>

          <div class="grid_row">
            <div class="col">
              <manual-submit
                :form-is-valid="manualIsValid"
                :is-fetching-token="isFetchingToken"
                base-classes="form__submit button button--yellow button--l"
                value="Donate"
                @onSubmit="onSubmit"
                @setValue="setValue"
                @setValidationValue="setValidationValue"
              />
            </div>
          </div>
        </div>
      </div>

      <div
        v-if="showErrorClue"
        class="grid_separator--l"
        aria-hidden="true"
      />

      <div
        v-if="showErrorClue"
        class="grid_row"
        aria-hidden="true"
      >
        <div class="col">
          <p class="form__error form__error--normal form__error--centered">Please correct errors above</p>
        </div>
      </div>

      <local-hidden
        :value="stripeToken"
        name="stripeToken"
      />
      <hidden
        name="campaign_id"
        store-module="businessForm"
      />
      <hidden
        name="referral_id"
        store-module="businessForm"
      />
      <hidden
        name="installments"
        store-module="businessForm"
      />
      <hidden
        name="description"
        store-module="businessForm"
      />
      <hidden
        name="pay_fees_value"
        store-module="businessForm"
      />
      <hidden
        name="openended_status"
        store-module="businessForm"
      />
      <hidden
        name="customerId"
        store-module="businessForm"
      />
      <hidden
        name="installment_period"
        store-module="businessForm"
      />
      <hidden
        name="amount"
        store-module="businessForm"
      />
    </div>
  </form>
</template>

<script>
import Hidden from '../../elements/Hidden.vue';
import Level from '../../elements/Level.vue';
import LocalHidden from '../../elements/LocalHidden.vue';
import PayFees from '../../elements/PayFees.vue';
import TextInput from '../../elements/TextInput.vue';
import SelectList from '../../elements/SelectList.vue';
import ManualPay from '../../elements/ManualPay.vue';
import ManualSubmit from '../../elements/ManualSubmit.vue';
import NativePay from '../../elements/NativePay.vue';
import Choices from './Choices.vue';
import updateStoreValue from '../../elements/mixins/updateStoreValue';
import formStarter from '../../mixins/form/starter';
// import addNumberCommas from '../../utils/addNumberCommas';
import { US_STATES_SELECT_LIST } from '../../utils/formSelectListConstants';

import { DEFAULT_STATE_SELECTED } from './constants';


export default {
  name: 'BusinessForm',

  components: {
    Hidden,
    LocalHidden,
    TextInput,
    SelectList,
    PayFees,
    Level,
    ManualPay,
    ManualSubmit,
    NativePay,
    Choices,
  },

  mixins: [
    formStarter,
    updateStoreValue,
  ],

  data() {
    return {
      // eslint-disable-next-line no-underscore-dangle
      serverErrorMessage: window.__TOP_FORM_SERVER_ERROR_MESSAGE__,
      validation: {
        stripeEmail: {
          manual: true,
          native: true,
          valid: false,
          message: 'Enter a valid email address',
          validator: this.isEmail,
        },
        business_name: {
          manual: true,
          native: true,
          valid: false,
          message: 'Enter a business name',
          validator: this.isNotEmpty,
        },
        website: {
          manual: true,
          native: true,
          valid: false,
          message: 'Enter a website, including https:// or http://',
          validator: this.isURL,
        },
        shipping_street: {
          manual: true,
          native: true,
          valid: false,
          message: 'Enter a street/mailing address',
          validator: this.isNotEmpty,
        },
        shipping_city: {
          manual: true,
          native: true,
          valid: false,
          message: 'Enter a city',
          validator: this.isNotEmpty,
        },
        shipping_postalcode: {
          manual: true,
          native: true,
          valid: false,
          message: 'Enter a 5-digit zip code',
          validator: this.isZip,
        },
        first_name: {
          manual: true,
          native: true,
          valid: false,
          message: 'Enter contact first name',
          validator: this.isNotEmpty,
        },
        last_name: {
          manual: true,
          native: true,
          valid: false,
          message: 'Enter contact last name',
          validator: this.isNotEmpty,
        },
      },
      options: {
        list: this.buildList(US_STATES_SELECT_LIST),
        default: DEFAULT_STATE_SELECTED,
      },
    };
  },

  methods: {

    buildList(selectList) {
      const options = [];
      selectList.forEach((listItem, index) => {
        options.push({
          index,
          value: listItem.value,
          text: listItem.text,
        });
      });
      return options;
    },
  },
};
</script>
