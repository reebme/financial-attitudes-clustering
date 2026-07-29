-- select base series
-- exclude stratifications
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
	and series_id not glob '*D';
