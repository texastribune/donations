const BENEFITS = [
  {
    id: 0,
    component: {
      name: 'Decal',
      render(h) {
        return h('span', 'Official member decal');
      },
    },
  },
  {
    id: 1,
    component: {
      name: 'Email',
      render(h) {
        return h('span', 'Monthly members-only email');
      },
    },
  },
  {
    id: 2,
    component: {
      name: 'Festival',
      render(h) {
        return h('span', [
          'Discounted passes to our annual ',
          h(
            'a',
            {
              attrs: {
                href: 'https://festival.texastribune.org',
              },
            },
            'Texas Tribune Festival'
          ),
        ]);
      },
    },
  },
  {
    id: 3,
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
                  'https://www.texastribune.org/support-us/donors-and-members/',
              },
            },
            'donor wall'
          ),
        ]);
      },
    },
  },
  {
    id: 4,
    component: {
      name: 'Informed',
      render(h) {
        return h(
          'span',
          'Informed Members also receive: Quarterly stakeholder report'
        );
      },
    },
  },
  {
    id: 5,
    component: {
      name: 'Engaged',
      render(h) {
        return h(
          'span',
          'Engaged Members also receive: Invite to exclusive events'
        );
      },
    },
  },
  {
    id: 6,
    component: {
      name: 'Involved',
      render(h) {
        return h('span', [
          'Involved Members also receive: Discounted rental rates for ',
          h(
            'a',
            {
              attrs: {
                href:
                  'https://www.texastribune.org/studio-919/downtown-austin-event-space-congress/',
              },
            },
            'Studio 919'
          ),
        ]);
      },
    },
  },
];

export default BENEFITS;
