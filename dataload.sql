DROP TABLE IF EXISTS idx_history;
CREATE TABLE idx_history (
	index_name character varying(200),
	symbol character varying(200),
	trade_date date,
	open_index_value double precision,
	high_index_value double precision,
	low_index_value double precision,
	closing_index_value double precision,
	points_change double precision,
	change_percent double precision,
	volume double precision,
	turnover_rs_cr double precision,
	p_e double precision,
	p_b double precision,
	div_yield double precision
);

DROP TABLE IF EXISTS fno_history;
CREATE TABLE fno_history (
	instrument character varying(20),
	symbol character varying(20),
	expiry_date date,
	trade_date date,
	strike_price double precision,
	option_type character varying(6),
	open double precision,
	high double precision,
	low double precision,
	close double precision,
	settle_price double precision,
	contracts  double precision,
	value_in_lakhs double precision,
	open_interest double precision,
	chg_in_oi double precision
);

DROP TABLE IF EXISTS eq_history;
CREATE TABLE eq_history (
	symbol character varying(20),
	series character varying(10),
	isin character varying(20),
	trade_date date,
	prev_close_price double precision,
	open_price double precision,
	day_high double precision,
	day_low double precision,
	close_price double precision,
	last double precision,
	tottrdqty double precision,
	tottrdval double precision,
	totaltrades double precision
);


DROP TABLE IF EXISTS trade_dates;
CREATE TABLE trade_dates(
	trade_date date
);

DROP TABLE IF EXISTS fno_stock_symbols;
CREATE TABLE fno_stock_symbols(
	symbol character varying(20),
	active boolean,
	min_date date,
	max_date date
);

DROP TABLE IF EXISTS fno_index_symbols;
CREATE TABLE fno_index_symbols(
	symbol character varying(20),
	active boolean,
	min_date date,
	max_date date
);

-- DROP INDEX IF EXISTS idx_history_uniq;
-- DELETE FROM idx_history;
INSERT INTO idx_history 
SELECT replace(upper(index_name),' ','-') AS index_name, CASE WHEN replace(upper(index_name),' ','-') = 'NIFTY-BANK' THEN 'BANKNIFTY' WHEN replace(upper(index_name),' ','-') = 'NIFTY-50' THEN 'NIFTY' ELSE replace(upper(index_name),' ','-') END AS symbol, to_date(index_date,'DD-MM-YYYY'), (CASE WHEN open_index_value = '-' OR open_index_value = '' THEN '0' ELSE open_index_value END)::DOUBLE PRECISION AS open_index_value, (CASE WHEN high_index_value = '-' OR high_index_value = '' THEN '0' ELSE high_index_value END)::DOUBLE PRECISION AS high_index_value, (CASE WHEN low_index_value = '-' OR low_index_value = '' THEN '0' ELSE low_index_value END)::DOUBLE PRECISION AS low_index_value, (CASE WHEN closing_index_value = '-' OR closing_index_value = '' THEN '0' ELSE closing_index_value END)::DOUBLE PRECISION AS closing_index_value, (CASE WHEN points_change = '-' OR points_change = '' THEN '0' ELSE points_change END)::DOUBLE PRECISION AS points_change, (CASE WHEN change_percent = '-' OR change_percent = '' THEN '0' ELSE change_percent END)::DOUBLE PRECISION AS change_percent, (CASE WHEN volume = '-' OR volume = '' THEN '0' ELSE volume END)::DOUBLE PRECISION AS volume, (CASE WHEN turnover_rs_cr = '-' OR turnover_rs_cr = '' THEN '0' ELSE turnover_rs_cr END)::DOUBLE PRECISION AS turnover_rs_cr, (CASE WHEN p_e = '-' OR p_e = '' THEN '0' ELSE p_e END)::DOUBLE PRECISION AS p_e, (CASE WHEN p_b = '-' OR p_b = '' THEN '0' ELSE p_b END)::DOUBLE PRECISION AS p_b, (CASE WHEN div_yield = '-' OR div_yield = '' THEN '0' ELSE div_yield END)::DOUBLE PRECISION AS div_yield  FROM bhavcopy_idx;
CREATE UNIQUE INDEX idx_history_uniq ON idx_history(index_name, trade_date);

-- DROP INDEX IF EXISTS fno_history_uniq;
-- DELETE FROM fno_history;
INSERT INTO fno_history 
SELECT instrument,symbol,expiry_dt::date,timestamp::date,strike_pr,option_typ,open,high,low,close,settle_pr,contracts,val_inlakh,open_int,chg_in_oi FROM bhavcopy_fo;
CREATE UNIQUE INDEX fno_history_uniq ON fno_history(instrument,symbol,expiry_date,trade_date,strike_price,option_type);

-- DROP INDEX IF EXISTS eq_history_uniq;
-- DELETE FROM eq_history;
INSERT INTO eq_history 
SELECT symbol,series,isin,timestamp::date,prevclose,open,high,low,close,last,tottrdqty,tottrdval,totaltrades FROM bhavcopy_eq;
CREATE UNIQUE INDEX eq_history_uniq ON eq_history(symbol, trade_date, series);

-- DELETE FROM trade_dates;
INSERT INTO trade_dates
SELECT DISTINCT trade_date FROM eq_history WHERE series = 'EQ';

-- DELETE FROM fno_stock_symbols;
INSERT INTO fno_stock_symbols
SELECT symbol, CASE WHEN MAX(trade_date) = (SELECT MAX(trade_date) FROM trade_dates) THEN true ELSE false END AS active, MIN(trade_date), MAX(trade_date) FROM fno_history WHERE instrument = 'OPTSTK' OR instrument = 'FUTSTK' GROUP BY symbol;

-- DELETE FROM fno_index_symbols;
INSERT INTO fno_index_symbols
SELECT symbol, CASE WHEN MAX(trade_date) = (SELECT MAX(trade_date) FROM trade_dates) THEN true ELSE false END AS active, MIN(trade_date), MAX(trade_date) FROM fno_history WHERE instrument = 'OPTIDX' OR instrument = 'FUTIDX' GROUP BY symbol;
