-- includes discontinued series
select
	*
from
	series_values sv
where
	series_value = 0;
