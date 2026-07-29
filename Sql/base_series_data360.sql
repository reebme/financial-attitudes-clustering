select distinct substr(indicator, 11) from WB_FINDEX where
	UNIT_MEASURE = 'PT_RESP'
	and sex = '_T'
	and AGE  = 'Y_GE15'
	and URBANISATION = '_T'
	and COMP_BREAKDOWN_1 = '_T'
	and COMP_BREAKDOWN_2 = '_T'
	and COMP_BREAKDOWN_3 = '_T'
	and REF_AREA not in (
	select
		distinct REF_AREA
	from
		WB_FINDEX
	where
		REF_AREA_LABEL like '%income%'
		or REF_AREA_LABEL like '%world%'
		or REF_AREA_LABEL like '%asia%');
