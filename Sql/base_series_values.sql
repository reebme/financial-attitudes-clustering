-- excludes stratifications,
-- provides values for
-- the base 280 series
select
	series_value,
	substr(observation_date, 1, 4),
	series_id,
	iso3_id,
	wave_id
from
	series_values
where
	source_code = 'WB'
	and series_id in (
	select
		distinct series_id
	from
		series
	where
		series_id not glob '*.[0-9]'
		and series_id not glob '*.1[0-2]'
		and series_id not glob '*.s'
		-- fin24other_SD_ND and fin24other_VD
		-- are stratifications of fin24other
		-- deviating from the usual stratification structure
		and series_id not glob '*D'
	)
;
