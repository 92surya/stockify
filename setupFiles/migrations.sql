DROP TABLE IF EXISTS bhavcopy_idx;
CREATE TABLE bhavcopy_idx (
	index_name character varying(200),
	index_date character varying(20),
	open_index_value character varying(20),
	high_index_value character varying(20),
	low_index_value character varying(20),
	closing_index_value character varying(20),
	points_change character varying(20),
	change_percent character varying(20),
	volume character varying(20),
	turnover_rs_cr character varying(20),
	p_e character varying(20),
	p_b character varying(20),
	div_yield  character varying(20)
);

DROP TABLE IF EXISTS bhavcopy_fo;
CREATE TABLE bhavcopy_fo (
	instrument character varying(20),
	symbol character varying(20),
	expiry_dt character varying(20),
	strike_pr double precision,
	option_typ character varying(6),
	open double precision,
	high double precision,
	low double precision,
	close double precision,
	settle_pr double precision,
	contracts  double precision,
	val_inlakh double precision,
	open_int double precision,
	chg_in_oi double precision,
	timestamp character varying(20),
	last_field character varying(20)
);

DROP TABLE IF EXISTS bhavcopy_eq;
CREATE TABLE bhavcopy_eq (
	symbol character varying(20),
	series character varying(10),
	open double precision,
	high double precision,
	low double precision,
	close double precision,
	last double precision,
	prevclose double precision,
	tottrdqty double precision,
	tottrdval double precision,
	timestamp character varying(20),
	totaltrades double precision,
	isin character varying(20),
	last_field character varying(20)
);

DROP TABLE IF EXISTS bhavcopy_idx_status;
CREATE TABLE bhavcopy_idx_status (
	file_name character varying(200)
);
CREATE UNIQUE INDEX bhavcopy_idx_status_uniq ON bhavcopy_idx_status(file_name);


DROP TABLE IF EXISTS bhavcopy_fo_status;
CREATE TABLE bhavcopy_fo_status (
	file_name character varying(200)
);
CREATE UNIQUE INDEX bhavcopy_fo_status_uniq ON bhavcopy_fo_status(file_name);

DROP TABLE IF EXISTS bhavcopy_eq_status;
CREATE TABLE bhavcopy_eq_status (
	file_name character varying(200)
);
CREATE UNIQUE INDEX bhavcopy_eq_status_uniq ON bhavcopy_eq_status(file_name);
