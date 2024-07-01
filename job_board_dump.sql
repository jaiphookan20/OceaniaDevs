--
-- PostgreSQL database dump
--

-- Dumped from database version 15.6 (Homebrew)
-- Dumped by pg_dump version 15.6 (Homebrew)


--
-- Name: vector; Type: EXTENSION; Schema: -; Owner: -
--



--
-- Name: EXTENSION vector; Type: COMMENT; Schema: -; Owner: 
--



--
-- Name: country_enum; Type: TYPE; Schema: public; Owner: jai
--

    'Australia',
    'New Zealand'
);



--
-- Name: industry_type; Type: TYPE; Schema: public; Owner: jai
--

    'Government',
    'Banking & Financial Services',
    'Fashion',
    'Mining',
    'Healthcare',
    'IT - Software Development',
    'IT - Data Analytics',
    'IT - Cybersecurity',
    'IT - Cloud Computing',
    'IT - Artificial Intelligence',
    'Agriculture',
    'Automotive',
    'Construction',
    'Education',
    'Energy & Utilities',
    'Entertainment',
    'Hospitality & Tourism',
    'Legal',
    'Manufacturing',
    'Marketing & Advertising',
    'Media & Communications',
    'Non-Profit & NGO',
    'Pharmaceuticals',
    'Real Estate',
    'Retail & Consumer Goods',
    'Telecommunications',
    'Transportation & Logistics'
);



--
-- Name: job_type; Type: TYPE; Schema: public; Owner: jai
--

    'premium',
    'normal'
);



--
-- Name: salary_range_type; Type: TYPE; Schema: public; Owner: jai
--

    '20000 - 40000',
    '40000 - 60000',
    '60000 - 80000',
    '80000 - 100000',
    '100000 - 120000',
    '120000 - 140000',
    '140000 - 160000',
    '160000 - 180000',
    '180000 - 200000',
    '200000 - 220000',
    '220000 - 240000',
    '240000 - 260000',
    '260000+'
);



--
-- Name: state_enum; Type: TYPE; Schema: public; Owner: jai
--

    'VIC',
    'NSW',
    'ACT',
    'WA',
    'QLD',
    'NT',
    'TAS',
    'SA'
);



--
-- Name: update_jobs_search_vector(); Type: FUNCTION; Schema: public; Owner: jai
--

    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW.search_vector := 
  to_tsvector('english', coalesce(NEW.title, '') || ' ' || coalesce(NEW.description, '') || ' ' || coalesce(NEW.specialization, '') || ' ' || coalesce(NEW.city, '') || ' ' || coalesce(NEW.state, ''));
  RETURN NEW;
END;
$$;





--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: jai
--

    version_num character varying(32) NOT NULL
);



--
-- Name: applications; Type: TABLE; Schema: public; Owner: jai
--

    applicationid integer NOT NULL,
    userid integer,
    jobid integer,
    datetimestamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);



--
-- Name: applications_applicationid_seq; Type: SEQUENCE; Schema: public; Owner: jai
--

    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: applications_applicationid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jai
--



--
-- Name: bookmarks; Type: TABLE; Schema: public; Owner: jai
--

    bookmarksid integer NOT NULL,
    userid integer,
    jobid integer,
    datetimestamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);



--
-- Name: bookmarks_bookmarksid_seq; Type: SEQUENCE; Schema: public; Owner: jai
--

    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: bookmarks_bookmarksid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jai
--



--
-- Name: candidates; Type: TABLE; Schema: public; Owner: jai
--

    candidate_id integer NOT NULL,
    name character varying(255),
    years_experience integer,
    "position" character varying(255),
    work_experience character varying(800),
    favorite_languages character varying[],
    technologies character varying[],
    embedding public.vector(1536)
);



--
-- Name: candidates_candidate_id_seq; Type: SEQUENCE; Schema: public; Owner: jai
--

    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: candidates_candidate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jai
--



--
-- Name: companies; Type: TABLE; Schema: public; Owner: jai
--

    company_id integer NOT NULL,
    name character varying(255) NOT NULL,
    website_url character varying(255),
    country public.country_enum,
    size character varying(100),
    address character varying(255),
    description text,
    logo_url character varying(255),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);



--
-- Name: companies_company_id_seq; Type: SEQUENCE; Schema: public; Owner: jai
--

    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: companies_company_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jai
--



--
-- Name: jobs; Type: TABLE; Schema: public; Owner: jai
--

    job_id integer NOT NULL,
    recruiter_id integer,
    company_id integer,
    title character varying(255) NOT NULL,
    description text,
    specialization character varying(255),
    job_type public.job_type,
    industry public.industry_type NOT NULL,
    salary_range public.salary_range_type,
    salary_type character varying(10),
    work_location character varying(20),
    min_experience_years integer,
    experience_level character varying(50),
    tech_stack character varying[],
    city character varying(255),
    state character varying(255),
    country character varying(255),
    expiry_date date DEFAULT (CURRENT_DATE + '30 days'::interval),
    jobpost_url character varying(255),
    work_rights character varying[],
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    search_vector tsvector,
    embedding public.vector(1536)
);



--
-- Name: jobs_job_id_seq; Type: SEQUENCE; Schema: public; Owner: jai
--

    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: jobs_job_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jai
--



--
-- Name: recruiters; Type: TABLE; Schema: public; Owner: jai
--

    recruiter_id integer NOT NULL,
    company_id integer,
    first_name character varying(255),
    last_name character varying(255),
    "position" character varying(255),
    email character varying(255) NOT NULL,
    password character varying(255),
    city character varying(255),
    state public.state_enum,
    country public.country_enum,
    is_direct_recruiter boolean,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);



--
-- Name: recruiters_recruiter_id_seq; Type: SEQUENCE; Schema: public; Owner: jai
--

    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: recruiters_recruiter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jai
--



--
-- Name: seekers; Type: TABLE; Schema: public; Owner: jai
--

    uid integer NOT NULL,
    first_name character varying(255),
    last_name character varying(255),
    email character varying(255) NOT NULL,
    password_hash character varying(128),
    city character varying(255),
    state public.state_enum,
    country public.country_enum,
    datetimestamp timestamp without time zone
);



--
-- Name: seekers_uid_seq; Type: SEQUENCE; Schema: public; Owner: jai
--

    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: seekers_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jai
--



--
-- Name: applications applicationid; Type: DEFAULT; Schema: public; Owner: jai
--



--
-- Name: bookmarks bookmarksid; Type: DEFAULT; Schema: public; Owner: jai
--



--
-- Name: candidates candidate_id; Type: DEFAULT; Schema: public; Owner: jai
--



--
-- Name: companies company_id; Type: DEFAULT; Schema: public; Owner: jai
--



--
-- Name: jobs job_id; Type: DEFAULT; Schema: public; Owner: jai
--



--
-- Name: recruiters recruiter_id; Type: DEFAULT; Schema: public; Owner: jai
--



--
-- Name: seekers uid; Type: DEFAULT; Schema: public; Owner: jai
--



--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: jai
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: applications; Type: TABLE DATA; Schema: public; Owner: jai
--

COPY public.applications (applicationid, userid, jobid, datetimestamp) FROM stdin;
\.


--
-- Data for Name: bookmarks; Type: TABLE DATA; Schema: public; Owner: jai
--

COPY public.bookmarks (bookmarksid, userid, jobid, datetimestamp) FROM stdin;
\.


--
-- Data for Name: candidates; Type: TABLE DATA; Schema: public; Owner: jai
--

COPY public.candidates (candidate_id, name, years_experience, "position", work_experience, favorite_languages, technologies, embedding) FROM stdin;
\.


--
-- Data for Name: companies; Type: TABLE DATA; Schema: public; Owner: jai
--

COPY public.companies (company_id, name, website_url, country, size, address, description, logo_url, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: jobs; Type: TABLE DATA; Schema: public; Owner: jai
--

COPY public.jobs (job_id, recruiter_id, company_id, title, description, specialization, job_type, industry, salary_range, salary_type, work_location, min_experience_years, experience_level, tech_stack, city, state, country, expiry_date, jobpost_url, work_rights, created_at, updated_at, search_vector, embedding) FROM stdin;
\.


--
-- Data for Name: recruiters; Type: TABLE DATA; Schema: public; Owner: jai
--

COPY public.recruiters (recruiter_id, company_id, first_name, last_name, "position", email, password, city, state, country, is_direct_recruiter, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: seekers; Type: TABLE DATA; Schema: public; Owner: jai
--

COPY public.seekers (uid, first_name, last_name, email, password_hash, city, state, country, datetimestamp) FROM stdin;
\.


--
-- Name: applications_applicationid_seq; Type: SEQUENCE SET; Schema: public; Owner: jai
--



--
-- Name: bookmarks_bookmarksid_seq; Type: SEQUENCE SET; Schema: public; Owner: jai
--



--
-- Name: candidates_candidate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jai
--



--
-- Name: companies_company_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jai
--



--
-- Name: jobs_job_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jai
--



--
-- Name: recruiters_recruiter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jai
--



--
-- Name: seekers_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: jai
--



--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: jai
--

    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: applications applications_pkey; Type: CONSTRAINT; Schema: public; Owner: jai
--

    ADD CONSTRAINT applications_pkey PRIMARY KEY (applicationid);


--
-- Name: bookmarks bookmarks_pkey; Type: CONSTRAINT; Schema: public; Owner: jai
--

    ADD CONSTRAINT bookmarks_pkey PRIMARY KEY (bookmarksid);


--
-- Name: candidates candidates_pkey; Type: CONSTRAINT; Schema: public; Owner: jai
--

    ADD CONSTRAINT candidates_pkey PRIMARY KEY (candidate_id);


--
-- Name: companies companies_pkey; Type: CONSTRAINT; Schema: public; Owner: jai
--

    ADD CONSTRAINT companies_pkey PRIMARY KEY (company_id);


--
-- Name: jobs jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: jai
--

    ADD CONSTRAINT jobs_pkey PRIMARY KEY (job_id);


--
-- Name: recruiters recruiters_pkey; Type: CONSTRAINT; Schema: public; Owner: jai
--

    ADD CONSTRAINT recruiters_pkey PRIMARY KEY (recruiter_id);


--
-- Name: seekers seekers_email_key; Type: CONSTRAINT; Schema: public; Owner: jai
--

    ADD CONSTRAINT seekers_email_key UNIQUE (email);


--
-- Name: seekers seekers_pkey; Type: CONSTRAINT; Schema: public; Owner: jai
--

    ADD CONSTRAINT seekers_pkey PRIMARY KEY (uid);


--
-- Name: applications applications_jobid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jai
--

    ADD CONSTRAINT applications_jobid_fkey FOREIGN KEY (jobid) REFERENCES public.jobs(job_id);


--
-- Name: applications applications_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jai
--

    ADD CONSTRAINT applications_userid_fkey FOREIGN KEY (userid) REFERENCES public.seekers(uid);


--
-- Name: bookmarks bookmarks_jobid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jai
--

    ADD CONSTRAINT bookmarks_jobid_fkey FOREIGN KEY (jobid) REFERENCES public.jobs(job_id);


--
-- Name: bookmarks bookmarks_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jai
--

    ADD CONSTRAINT bookmarks_userid_fkey FOREIGN KEY (userid) REFERENCES public.seekers(uid);


--
-- Name: jobs jobs_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jai
--

    ADD CONSTRAINT jobs_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(company_id);


--
-- Name: jobs jobs_recruiter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jai
--

    ADD CONSTRAINT jobs_recruiter_id_fkey FOREIGN KEY (recruiter_id) REFERENCES public.recruiters(recruiter_id);


--
-- Name: recruiters recruiters_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jai
--

    ADD CONSTRAINT recruiters_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(company_id);


--
-- PostgreSQL database dump complete
--

