const pages = [
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login.vue'),
        meta: {
            guest: true
        }
    },
    {
        path: '/preferences',
        name: 'Preferences',
        meta: {
            requiresAuth: true
        },
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.

        component: () => import('../views/Preferences.vue')
    },

    {
        path: '/admin/users',
        name: 'Users',
        meta: {
            sidebar: true,
            requiresAuth: true,
            admin: true
        },
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.

        component: () => import('../views/admin/Users.vue')
    },
    {
        path: '/admin/logs',
        name: 'Logs',
        meta: {
            sidebar: true,
            requiresAuth: true,
            admin: true
        },
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.

        component: () => import('../views/admin/Logs.vue'),
        children: [
            {
                path: '',
                name: 'Index',
                component: () => import('../views/admin/logs/LogIndex.vue'),
            },
            {
                path: 'event-participation',
                name: 'Participation in Events',
                component: () => import('../components/logs/LogEventParticipation.vue'),
            },
            {
                path: 'event-organization',
                name: 'Organisation of Events',
                component: () => import('../components/logs/LogEventOrganization.vue'),
            },
            {
                path: 'extension',
                name: 'Extension',
                component: () => import('../components/logs/LogExtension.vue'),
            },
            {
                path: 'supervision',
                name: 'Supervision',
                component: () => import('../components/logs/LogSupervision.vue'),
            },
            {
                path: 'jury-sci-committee',
                name: 'Jury / Scientific Committee',
                component: () => import('../components/logs/LogJurySciCommittee.vue'),
            },
            {
                path: 'referring-editorial-act',
                name: 'Refereeing Editorial Act',
                component: () => import('../components/logs/LogReferringEditorialAct.vue'),
            }
        ]
    },

    {
        path: '/',
        name: 'Index',
        meta: {
            sidebar: true,
            requiresAuth: true
        },
        component: () => import('../views/Index.vue')
    },
    {
        path: '/forms/extension',
        name: 'Extension',
        meta: {
            sidebar: true,
            requiresAuth: true
        },
        component: () => import('../views/forms/extension/ExtensionRoot.vue'),
        children: [
            {
                path: '',
                name: 'Form',
                component: () => import('../views/forms/extension/ExtensionForm.vue'),
            },
            {
                path: 'history',
                name: 'History',
                component: () => import('../views/forms/extension/ExtensionHistory.vue'),
            }
        ]
    },
    {
        path: '/forms/jury-sci-committee',
        name: 'Jury & Scientific Committee',
        meta: {
            sidebar: true,
            requiresAuth: true
        },
        component: () => import('../views/forms/jury-sci-committee/JurySciCommitteeRoot.vue'),
        children: [
            {
                path: '',
                name: 'Form',
                component: () => import('../views/forms/jury-sci-committee/JurySciCommitteeForm.vue'),
            },
            {
                path: 'history',
                name: 'History',
                component: () => import('../views/forms/jury-sci-committee/JurySciCommitteeHistory.vue'),
            }
        ]
    },
    {
        path: '/forms/event-organization',
        name: 'Organisation of Events',
        meta: {
            sidebar: true,
            requiresAuth: true
        },
        component: () => import('../views/forms/event-organization/EventOrganizationRoot.vue'),
        children: [
            {
                path: '',
                name: 'Form',
                component: () => import('../views/forms/event-organization/EventOrganizationForm.vue'),
            },
            {
                path: 'history',
                name: 'History',
                component: () => import('../views/forms/event-organization/EventOrganizationHistory.vue'),
            }
        ]
    },
    {
        path: '/forms/event-participation',
        name: 'Participation in Events',
        meta: {
            sidebar: true,
            requiresAuth: true
        },
        component: () => import('../views/forms/event-participation/EventParticipationRoot.vue'),
        children: [
            {
                path: '',
                name: 'Form',
                component: () => import('../views/forms/event-participation/EventParticipationForm.vue'),
            },
            {
                path: 'history',
                name: 'History',
                component: () => import('../views/forms/event-participation/EventParticipationHistory.vue'),
            }
        ]
    },
    {
        path: '/forms/referring-editorial-act',
        name: 'Refereeing & Editorial Board',
        meta: {
            sidebar: true,
            requiresAuth: true
        },
        component: () => import('../views/forms/referring-editorial-act/ReferringEditorialActRoot.vue'),
        children: [
            {
                path: '',
                name: 'Form',
                component: () => import('../views/forms/referring-editorial-act/ReferringEditorialActForm.vue'),
            },
            {
                path: 'history',
                name: 'History',
                component: () => import('../views/forms/referring-editorial-act/ReferringEditorialActHistory.vue'),
            }
        ]
    },
    {
        path: '/forms/supervision',
        name: 'Supervision',
        meta: {
            sidebar: true,
            requiresAuth: true
        },
        component: () => import('../views/forms/supervision/SupervisionRoot.vue'),
        children: [
            {
                path: '',
                name: 'Form',
                component: () => import('../views/forms/supervision/SupervisionForm.vue'),
            },
            {
                path: 'history',
                name: 'History',
                component: () => import('../views/forms/supervision/SupervisionHistory.vue'),
            }
        ]
    }
]

const countryList = [
	"Afghanistan",
	"Albania",
	"Algeria",
	"American Samoa",
	"Andorra",
	"Angola",
	"Anguilla",
	"Antarctica",
	"Antigua and Barbuda",
	"Argentina",
	"Armenia",
	"Aruba",
	"Australia",
	"Austria",
	"Azerbaijan",
	"Bahamas (the)",
	"Bahrain",
	"Bangladesh",
	"Barbados",
	"Belarus",
	"Belgium",
	"Belize",
	"Benin",
	"Bermuda",
	"Bhutan",
	"Bolivia (Plurinational State of)",
	"Bonaire, Sint Eustatius and Saba",
	"Bosnia and Herzegovina",
	"Botswana",
	"Bouvet Island",
	"Brazil",
	"British Indian Ocean Territory (the)",
	"Brunei Darussalam",
	"Bulgaria",
	"Burkina Faso",
	"Burundi",
	"Cabo Verde",
	"Cambodia",
	"Cameroon",
	"Canada",
	"Cayman Islands (the)",
	"Central African Republic (the)",
	"Chad",
	"Chile",
	"China",
	"Christmas Island",
	"Cocos (Keeling) Islands (the)",
	"Colombia",
	"Comoros (the)",
	"Congo (the Democratic Republic of the)",
	"Congo (the)",
	"Cook Islands (the)",
	"Costa Rica",
	"Croatia",
	"Cuba",
	"Curaçao",
	"Cyprus",
	"Czechia",
	"Côte d'Ivoire",
	"Denmark",
	"Djibouti",
	"Dominica",
	"Dominican Republic (the)",
	"Ecuador",
	"Egypt",
	"El Salvador",
	"Equatorial Guinea",
	"Eritrea",
	"Estonia",
	"Eswatini",
	"Ethiopia",
	"Falkland Islands (the) [Malvinas]",
	"Faroe Islands (the)",
	"Fiji",
	"Finland",
	"France",
	"French Guiana",
	"French Polynesia",
	"French Southern Territories (the)",
	"Gabon",
	"Gambia (the)",
	"Georgia",
	"Germany",
	"Ghana",
	"Gibraltar",
	"Greece",
	"Greenland",
	"Grenada",
	"Guadeloupe",
	"Guam",
	"Guatemala",
	"Guernsey",
	"Guinea",
	"Guinea-Bissau",
	"Guyana",
	"Haiti",
	"Heard Island and McDonald Islands",
	"Holy See (the)",
	"Honduras",
	"Hong Kong",
	"Hungary",
	"Iceland",
	"India",
	"Indonesia",
	"Iran (Islamic Republic of)",
	"Iraq",
	"Ireland",
	"Isle of Man",
	"Israel",
	"Italy",
	"Jamaica",
	"Japan",
	"Jersey",
	"Jordan",
	"Kazakhstan",
	"Kenya",
	"Kiribati",
	"Korea (the Democratic People's Republic of)",
	"Korea (the Republic of)",
	"Kuwait",
	"Kyrgyzstan",
	"Lao People's Democratic Republic (the)",
	"Latvia",
	"Lebanon",
	"Lesotho",
	"Liberia",
	"Libya",
	"Liechtenstein",
	"Lithuania",
	"Luxembourg",
	"Macao",
	"Madagascar",
	"Malawi",
	"Malaysia",
	"Maldives",
	"Mali",
	"Malta",
	"Marshall Islands (the)",
	"Martinique",
	"Mauritania",
	"Mauritius",
	"Mayotte",
	"Mexico",
	"Micronesia (Federated States of)",
	"Moldova (the Republic of)",
	"Monaco",
	"Mongolia",
	"Montenegro",
	"Montserrat",
	"Morocco",
	"Mozambique",
	"Myanmar",
	"Namibia",
	"Nauru",
	"Nepal",
	"Netherlands (the)",
	"New Caledonia",
	"New Zealand",
	"Nicaragua",
	"Niger (the)",
	"Nigeria",
	"Niue",
	"Norfolk Island",
	"Northern Mariana Islands (the)",
	"Norway",
	"Oman",
	"Pakistan",
	"Palau",
	"Palestine, State of",
	"Panama",
	"Papua New Guinea",
	"Paraguay",
	"Peru",
	"Philippines (the)",
	"Pitcairn",
	"Poland",
	"Portugal",
	"Puerto Rico",
	"Qatar",
	"Republic of North Macedonia",
	"Romania",
	"Russian Federation (the)",
	"Rwanda",
	"Réunion",
	"Saint Barthélemy",
	"Saint Helena, Ascension and Tristan da Cunha",
	"Saint Kitts and Nevis",
	"Saint Lucia",
	"Saint Martin (French part)",
	"Saint Pierre and Miquelon",
	"Saint Vincent and the Grenadines",
	"Samoa",
	"San Marino",
	"Sao Tome and Principe",
	"Saudi Arabia",
	"Senegal",
	"Serbia",
	"Seychelles",
	"Sierra Leone",
	"Singapore",
	"Sint Maarten (Dutch part)",
	"Slovakia",
	"Slovenia",
	"Solomon Islands",
	"Somalia",
	"South Africa",
	"South Georgia and the South Sandwich Islands",
	"South Sudan",
	"Spain",
	"Sri Lanka",
	"Sudan (the)",
	"Suriname",
	"Svalbard and Jan Mayen",
	"Sweden",
	"Switzerland",
	"Syrian Arab Republic",
	"Taiwan",
	"Tajikistan",
	"Tanzania, United Republic of",
	"Thailand",
	"Timor-Leste",
	"Togo",
	"Tokelau",
	"Tonga",
	"Trinidad and Tobago",
	"Tunisia",
	"Turkey",
	"Turkmenistan",
	"Turks and Caicos Islands (the)",
	"Tuvalu",
	"Uganda",
	"Ukraine",
	"United Arab Emirates (the)",
	"United Kingdom of Great Britain and Northern Ireland (the)",
	"United States Minor Outlying Islands (the)",
	"United States of America (the)",
	"Uruguay",
	"Uzbekistan",
	"Vanuatu",
	"Venezuela (Bolivarian Republic of)",
	"Viet Nam",
	"Virgin Islands (British)",
	"Virgin Islands (U.S.)",
	"Wallis and Futuna",
	"Western Sahara",
	"Yemen",
	"Zambia",
	"Zimbabwe",
	"Åland Islands"
];

export {
    pages,
    countryList
}