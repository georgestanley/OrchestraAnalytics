--Query1
--Part1

--Part2

--PArt3


--Part4 :: to query all Orcestra based on Country filter as input

select pa.event_id, pa.date_of_event, pa.country, pa.place, pa.Orchestra,group_concat(pl.program), group_concat(distinct c.conductor)
from programs_all pa, program_list pl ,conductors c
where 1=1
and pa.event_id=pl.event_id
and pa.event_id=c.event_id
and pa.country = 'Argentina'
group by pa.event_id, pa.date_of_event, pa.country, pa.place, pa.Orchestra;

select * from programs_temp where land='Argentinien';

