--
-- PostgreSQL database dump
--

-- Dumped from database version 15.6 (Homebrew)
-- Dumped by pg_dump version 15.6 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: jai
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: companies; Type: TABLE DATA; Schema: public; Owner: jai
--

COPY public.companies (company_id, name, website_url, country, size, address, description, logo_url, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: recruiters; Type: TABLE DATA; Schema: public; Owner: jai
--

COPY public.recruiters (recruiter_id, company_id, first_name, last_name, "position", email, password, city, state, country, is_direct_recruiter, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: jobs; Type: TABLE DATA; Schema: public; Owner: jai
--

COPY public.jobs (job_id, recruiter_id, company_id, title, description, specialization, job_type, industry, salary_range, salary_type, work_location, min_experience_years, experience_level, tech_stack, city, state, country, expiry_date, jobpost_url, work_rights, created_at, updated_at, search_vector, embedding) FROM stdin;
\.


--
-- Data for Name: seekers; Type: TABLE DATA; Schema: public; Owner: jai
--

COPY public.seekers (uid, first_name, last_name, email, password_hash, city, state, country, datetimestamp) FROM stdin;
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
-- Name: applications_applicationid_seq; Type: SEQUENCE SET; Schema: public; Owner: jai
--

SELECT pg_catalog.setval('public.applications_applicationid_seq', 1, false);


--
-- Name: bookmarks_bookmarksid_seq; Type: SEQUENCE SET; Schema: public; Owner: jai
--

SELECT pg_catalog.setval('public.bookmarks_bookmarksid_seq', 1, false);


--
-- Name: candidates_candidate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jai
--

SELECT pg_catalog.setval('public.candidates_candidate_id_seq', 1, false);


--
-- Name: companies_company_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jai
--

SELECT pg_catalog.setval('public.companies_company_id_seq', 1, false);


--
-- Name: jobs_job_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jai
--

SELECT pg_catalog.setval('public.jobs_job_id_seq', 1, false);


--
-- Name: recruiters_recruiter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jai
--

SELECT pg_catalog.setval('public.recruiters_recruiter_id_seq', 1, false);


--
-- Name: seekers_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: jai
--

SELECT pg_catalog.setval('public.seekers_uid_seq', 1, false);


--
-- PostgreSQL database dump complete
--

