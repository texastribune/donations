const BENEFITS = [
  {
    id: 0,
    component: {
      name: 'Wall',
      render(h) {
        return h('span', [
          'Our utmost gratitude and a special place on our ',
          h(
            'a',
            {
              attrs: {
                href:
                  'https://support.wacobridge.org/members/',
              },
            },
            'growing donor wall'
          ),
        ]);
      },
    },
  },
  {
    id: 1,
    component: {
      name: 'Engaged',
      render(h) {
        return h(
          'span',
          'Engaged Members also receive: Invites to exclusive events'
        );
      },
    },
  },
];

export default BENEFITS;
