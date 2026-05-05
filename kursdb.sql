--
-- PostgreSQL database dump
--

\restrict uUkCjmp2AKkkos0Hltsz90qJvfsH8Ukmrqzi4Ck2BA2prbfeOlqzFiIGxuXmSgv

-- Dumped from database version 18.0 (Debian 18.0-1.pgdg13+3)
-- Dumped by pg_dump version 18.0 (Debian 18.0-1.pgdg13+3)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: chem_element; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chem_element (
    chem_element_id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.chem_element OWNER TO postgres;

--
-- Name: chem_element_chem_element_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.chem_element_chem_element_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.chem_element_chem_element_id_seq OWNER TO postgres;

--
-- Name: chem_element_chem_element_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.chem_element_chem_element_id_seq OWNED BY public.chem_element.chem_element_id;


--
-- Name: possible_value; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.possible_value (
    possible_value_id integer NOT NULL,
    property_id integer NOT NULL,
    value character varying(255) NOT NULL
);


ALTER TABLE public.possible_value OWNER TO postgres;

--
-- Name: possible_value_possible_value_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.possible_value_possible_value_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.possible_value_possible_value_id_seq OWNER TO postgres;

--
-- Name: possible_value_possible_value_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.possible_value_possible_value_id_seq OWNED BY public.possible_value.possible_value_id;


--
-- Name: property; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.property (
    property_id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.property OWNER TO postgres;

--
-- Name: property_for_element; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.property_for_element (
    property_for_element_id integer NOT NULL,
    chem_element_id integer NOT NULL,
    property_id integer NOT NULL
);


ALTER TABLE public.property_for_element OWNER TO postgres;

--
-- Name: property_for_element_property_for_element_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.property_for_element_property_for_element_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.property_for_element_property_for_element_id_seq OWNER TO postgres;

--
-- Name: property_for_element_property_for_element_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.property_for_element_property_for_element_id_seq OWNED BY public.property_for_element.property_for_element_id;


--
-- Name: property_property_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.property_property_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.property_property_id_seq OWNER TO postgres;

--
-- Name: property_property_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.property_property_id_seq OWNED BY public.property.property_id;


--
-- Name: value_chem_element; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.value_chem_element (
    value_chem_element_id integer NOT NULL,
    property_for_element_id integer NOT NULL,
    value character varying(500) NOT NULL
);


ALTER TABLE public.value_chem_element OWNER TO postgres;

--
-- Name: value_chem_element_value_chem_element_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.value_chem_element_value_chem_element_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.value_chem_element_value_chem_element_id_seq OWNER TO postgres;

--
-- Name: value_chem_element_value_chem_element_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.value_chem_element_value_chem_element_id_seq OWNED BY public.value_chem_element.value_chem_element_id;


--
-- Name: chem_element chem_element_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chem_element ALTER COLUMN chem_element_id SET DEFAULT nextval('public.chem_element_chem_element_id_seq'::regclass);


--
-- Name: possible_value possible_value_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.possible_value ALTER COLUMN possible_value_id SET DEFAULT nextval('public.possible_value_possible_value_id_seq'::regclass);


--
-- Name: property property_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.property ALTER COLUMN property_id SET DEFAULT nextval('public.property_property_id_seq'::regclass);


--
-- Name: property_for_element property_for_element_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.property_for_element ALTER COLUMN property_for_element_id SET DEFAULT nextval('public.property_for_element_property_for_element_id_seq'::regclass);


--
-- Name: value_chem_element value_chem_element_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.value_chem_element ALTER COLUMN value_chem_element_id SET DEFAULT nextval('public.value_chem_element_value_chem_element_id_seq'::regclass);


--
-- Data for Name: chem_element; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chem_element (chem_element_id, name) FROM stdin;
1	Алюминий
2	Магний
3	Натрий
4	Кальций
5	Железо
6	Никель
7	Медь
8	Цинк
9	Титан
10	Хром
11	Серебро
12	Олово
13	Золото
14	Свинец
15	Фосфор
16	Углерод
17	Йод
18	Германий
19	Сера
20	Селен
21	Бром
22	Теллур
23	Бор
24	Кремний
25	Мышьяк
\.


--
-- Data for Name: possible_value; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.possible_value (possible_value_id, property_id, value) FROM stdin;
1	1	10.81-207.20
3	3	0.97-20.00
2	2	139-231
4	4	металл
5	4	неметалл
6	4	полуметалл
\.


--
-- Data for Name: property; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.property (property_id, name) FROM stdin;
1	Атомная масса
2	Радиус атома
3	Плотность
4	Тип
\.


--
-- Data for Name: property_for_element; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.property_for_element (property_for_element_id, chem_element_id, property_id) FROM stdin;
1	1	1
2	1	2
3	1	3
4	1	4
5	2	1
6	2	2
7	2	3
8	2	4
9	3	1
10	3	2
11	3	3
12	3	4
13	4	1
14	4	2
15	4	3
16	4	4
17	5	1
18	5	2
19	5	3
20	5	4
21	6	1
22	6	2
23	6	3
24	6	4
25	7	1
26	7	2
27	7	3
28	7	4
29	8	1
30	8	2
31	8	3
32	8	4
33	9	1
34	9	2
35	9	3
36	9	4
37	10	1
38	10	2
39	10	3
40	10	4
41	11	1
42	11	2
43	11	3
44	11	4
45	12	1
46	12	2
47	12	3
48	12	4
49	13	1
50	13	2
51	13	3
52	13	4
53	14	1
54	14	2
55	14	3
56	14	4
57	15	1
58	15	2
59	15	3
60	15	4
61	16	1
62	16	2
63	16	3
64	16	4
65	17	1
66	17	2
67	17	3
68	17	4
69	18	1
70	18	2
71	18	3
72	18	4
73	19	1
74	19	2
75	19	3
76	19	4
77	20	1
78	20	2
79	20	3
80	20	4
81	21	1
82	21	2
83	21	3
84	21	4
85	22	1
86	22	2
87	22	3
88	22	4
89	23	1
90	23	2
91	23	3
92	23	4
93	24	1
94	24	2
95	24	3
96	24	4
97	25	1
98	25	2
99	25	3
100	25	4
\.


--
-- Data for Name: value_chem_element; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.value_chem_element (value_chem_element_id, property_for_element_id, value) FROM stdin;
1	1	26.98
2	2	184
3	3	2.70
4	4	металл
5	5	24.31
6	6	173
7	7	1.74
8	8	металл
9	9	22.99
10	10	227
11	11	0.97
12	12	металл
13	13	40.08
14	14	231
15	15	1.54
16	16	металл
17	17	55.84
18	18	194
19	19	7.87
20	20	металл
21	21	58.69
22	22	163
23	23	8.91
24	24	металл
25	25	63.55
26	26	140
27	27	8.93
28	28	металл
29	29	65.40
30	30	139
31	31	7.13
32	32	металл
33	33	47.87
34	34	187
35	35	4.50
36	36	металл
37	37	52.00
38	38	189
39	39	7.15
40	40	металл
41	41	107.87
42	42	172
43	43	10.50
44	44	металл
45	45	118.71
46	46	217
47	47	7.29
48	48	металл
49	49	196.97
50	50	166
51	51	19.28
52	52	металл
53	53	207.00
54	54	202
55	55	11.34
56	56	металл
57	57	30.97
58	58	180
59	59	1.82
60	60	неметалл
61	61	12.01
62	62	170
63	63	2.27
64	64	неметалл
65	65	126.90
66	66	198
67	67	4.93
68	68	неметалл
69	69	72.63
70	70	211
71	71	5.32
72	72	полуметалл
73	73	32.07
74	74	180
75	75	2.07
76	76	неметалл
77	77	78.97
78	78	190
79	79	4.81
80	80	неметалл
81	81	79.90
82	82	183
83	83	3.11
84	84	неметалл
85	85	127.60
86	86	206
87	87	6.23
88	88	полуметалл
89	89	10.81
90	90	192
91	91	2.37
92	92	полуметалл
93	93	28.09
94	94	210
95	95	2.33
96	96	полуметалл
97	97	74.92
98	98	185
99	99	5.78
100	100	полуметалл
\.


--
-- Name: chem_element_chem_element_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.chem_element_chem_element_id_seq', 73, true);


--
-- Name: possible_value_possible_value_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.possible_value_possible_value_id_seq', 58, true);


--
-- Name: property_for_element_property_for_element_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.property_for_element_property_for_element_id_seq', 193, true);


--
-- Name: property_property_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.property_property_id_seq', 36, true);


--
-- Name: value_chem_element_value_chem_element_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.value_chem_element_value_chem_element_id_seq', 145, true);


--
-- Name: chem_element chem_element_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chem_element
    ADD CONSTRAINT chem_element_name_key UNIQUE (name);


--
-- Name: chem_element chem_element_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chem_element
    ADD CONSTRAINT chem_element_pkey PRIMARY KEY (chem_element_id);


--
-- Name: possible_value possible_value_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.possible_value
    ADD CONSTRAINT possible_value_pkey PRIMARY KEY (possible_value_id);


--
-- Name: possible_value possible_value_property_value_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.possible_value
    ADD CONSTRAINT possible_value_property_value_unique UNIQUE (property_id, value);


--
-- Name: property_for_element property_for_element_chem_element_id_property_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.property_for_element
    ADD CONSTRAINT property_for_element_chem_element_id_property_id_key UNIQUE (chem_element_id, property_id);


--
-- Name: property_for_element property_for_element_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.property_for_element
    ADD CONSTRAINT property_for_element_pkey PRIMARY KEY (property_for_element_id);


--
-- Name: property property_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.property
    ADD CONSTRAINT property_name_key UNIQUE (name);


--
-- Name: property property_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.property
    ADD CONSTRAINT property_pkey PRIMARY KEY (property_id);


--
-- Name: value_chem_element value_chem_element_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.value_chem_element
    ADD CONSTRAINT value_chem_element_pkey PRIMARY KEY (value_chem_element_id);


--
-- Name: possible_value possible_value_property_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.possible_value
    ADD CONSTRAINT possible_value_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.property(property_id) ON DELETE CASCADE;


--
-- Name: property_for_element property_for_element_chem_element_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.property_for_element
    ADD CONSTRAINT property_for_element_chem_element_id_fkey FOREIGN KEY (chem_element_id) REFERENCES public.chem_element(chem_element_id) ON DELETE CASCADE;


--
-- Name: property_for_element property_for_element_property_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.property_for_element
    ADD CONSTRAINT property_for_element_property_id_fkey FOREIGN KEY (property_id) REFERENCES public.property(property_id) ON DELETE CASCADE;


--
-- Name: value_chem_element value_chem_element_property_for_element_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.value_chem_element
    ADD CONSTRAINT value_chem_element_property_for_element_id_fkey FOREIGN KEY (property_for_element_id) REFERENCES public.property_for_element(property_for_element_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict uUkCjmp2AKkkos0Hltsz90qJvfsH8Ukmrqzi4Ck2BA2prbfeOlqzFiIGxuXmSgv

