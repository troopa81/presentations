CREATE EXTENSION postgis;

CREATE SCHEMA locations;

CREATE TABLE locations.airports
(
   id serial NOT NULL,
   geom geometry(Point, 4326) NOT NULL,
   airport_name text NOT NULL,
   CONSTRAINT airports_pkey PRIMARY KEY (id)
);

CREATE INDEX airports_geom_idx ON locations.airports USING gist (geom);

CREATE TABLE locations.airlines
(
   id serial NOT NULL,
   geom geometry(Point, 4326) NOT NULL,
   airline_name text NOT NULL,
   CONSTRAINT airlines_pkey PRIMARY KEY (id)
);

CREATE INDEX airlines_geom_idx ON locations.airlines USING gist (geom);

CREATE TABLE locations.airports_airlines
(
   id serial NOT NULL,
   airport_fk integer NOT NULL,
   airline_fk integer NOT NULL,
   CONSTRAINT airports_airlines_pkey PRIMARY KEY (id),
   CONSTRAINT airports_airlines_airport_fk_fkey FOREIGN KEY (airport_fk)
      REFERENCES locations.airports (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
      DEFERRABLE INITIALLY DEFERRED,
   CONSTRAINT airports_airlines_airline_fk_fkey FOREIGN KEY (airline_fk)
      REFERENCES locations.airlines (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
      DEFERRABLE INITIALLY DEFERRED
 );

--
-- Data for Name: airlines; Type: TABLE DATA; Schema: locations; Owner: julien
--

COPY locations.airlines (id, geom, airline_name) FROM stdin;
1	0101000020E6100000CC62EC7A3E620340BCA0386DA77C4840	AirFrance
2	0101000020E61000000485DF95167AC1BF5305795B51D74940	EasyJet
3	0101000020E61000004C2EE42AAD182740CD377723BF1A4840	lufthansa
4	0101000020E6100000CEEE140B8B2619C0CDEE1C382EB34A40	RyanAir
\.


--
-- Data for Name: airports; Type: TABLE DATA; Schema: locations; Owner: julien
--

COPY locations.airports (id, geom, airport_name) FROM stdin;
1	0101000020E6100000DAA5669B2AC2F53F06FEE6C5BAD04540	Toulouse Blagnac
2	0101000020E6100000B4ACF12EC45A144060CB1460B1DC4640	Lyon Saint-Exupery
\.


--
-- Data for Name: airports_airlines; Type: TABLE DATA; Schema: locations; Owner: julien
--

COPY locations.airports_airlines (id, airport_fk, airline_fk) FROM stdin;
1	1	1
2	1	2
3	2	1
4	2	3
\.

SELECT pg_catalog.setval('locations.airlines_id_seq', 4, true);
SELECT pg_catalog.setval('locations.airports_airlines_id_seq', 4, true);
SELECT pg_catalog.setval('locations.airports_id_seq', 3, true);

