import axios from 'axios';

export default {
  methods: {
    createCustomerOnServer({ token, email }) {
      return axios.post('/create-customer', {
        stripeToken: token,
        stripeEmail: email,
      });
    },
  },
};
