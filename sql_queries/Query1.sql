--Query1
--Part1
with total as
    ( select Orchestra,sum(counts) as total
    from (select 
    Orchestra,
    Country,
    count(*) counts
from programs_all
where 1=1
group by Orchestra, Country)
group by Orchestra )

select total.Orchestra,Country,total.total, counts,
    round(((counts *1.0) /total.total)*100,2) as share
from (select 
    Orchestra,
    Country,
    count(*) counts
from programs_all
where 1=1
group by Orchestra, Country) pageviews,
    total
where pageviews.Orchestra=total.Orchestra
order by total.Orchestra, share desc;



--Part2

--PArt3


--Part4 :: to query all Orcestra based on Country filter as input

select pa.event_id, pa.date_of_event, pa.country, pa.place, pa.Orchestra,group_concat(pl.program) program, group_concat(distinct c.conductor) conductor
from programs_all pa, program_list pl ,conductors c
where 1=1
and pa.event_id=pl.event_id
and pa.event_id=c.event_id
--and pa.country=
group by pa.event_id, pa.date_of_event, pa.country, pa.place, pa.Orchestra;

--test case: Verify count with below query
--select * from programs_temp where land='Argentinien';


