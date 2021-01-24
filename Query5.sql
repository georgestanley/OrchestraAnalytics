---Query5
---Orchestra(s)+composer, within a period of choice; results both in absolute and proportional figures

select * from programs_all;
select * from program_list;
select * from conductors;
select first_name||' '||last_name Name from mappings_csv;
select distinct conductor from conductors order by conductor;


select pa.*,pl.program,m.*
from programs_all pa, program_list pl, mappings_csv m
where pa.event_id = pl.event_id
and pl.program = m.link;

select * from program_list where program not in (select link from mappings_csv);--1540 

--Query whole db

select Orchestra
    ,event_id, count(*) counts
from programs_all pa
where 1=1
group by Orchestra;


--query entire db
WITH total as
    ( select Orchestra,sum(counts) as total
    from (select Orchestra
    ,pa.event_id, count(*) counts
from programs_all pa, program_list pl , mappings_csv mc
where 1=1
and pa.event_id = pl.event_id
and pl.program = mc.link
group by Orchestra
    )
    group by Orchestra ),

pageviews2 as
(select Orchestra,first_name||' '||last_name Composer , count(distinct pa.event_id) counts
from programs_all pa, program_list pl, mappings_csv mc
where pa.event_id = pl.event_id
and pl.program= mc.link
group by Orchestra,Composer)

select total.Orchestra,Composer,total.total, counts ,
    round(((counts *1.0) /total.total)*100,2) as share
from pageviews2,
    total
where pageviews2.Orchestra=total.Orchestra
order by total.Orchestra, share desc;



--query between date range
WITH total as
    (select Orchestra,sum(counts) as total
    from (select Orchestra
        ,pa.event_id, count(*) counts
        from programs_all pa, program_list pl, mappings_csv mc
        where 1=1
        and pa.event_id = pl.event_id
        and pl.program = mc.link
        and date_of_event  between '1900-01-01' and '1905-06-31' 
        --and pa.orchestra in ('Vienna Philharmonic')
        )
    group by Orchestra ),
pageviews2 as
    (select Orchestra, first_name||' '||last_name Composer, count( pa.event_id) counts
    from programs_all pa, program_list pl, mappings_csv mc
    where pa.event_id = pl.event_id
    and pl.program= mc.link
    and date_of_event  between '1900-01-01' and '1905-06-31' 
    --and pa.orchestra in ('Vienna Philharmonic')
    group by Orchestra,composer)
    
select Composer,total.total, counts ,
    round(((counts *1.0) /total.total)*100,2) as share
from pageviews2,
    total
where pageviews2.Orchestra=total.Orchestra
group by Composer
order by total.Orchestra, share desc
;
------------------

select * from programs_all pa , program_list pl where pa.event_id = pl.event_id and program like '%Mah%';

select * from mappings_csv;


select pa.*,pl.program, first_name||' '||last_name Composer
from programs_all pa, program_list pl, mappings_csv mc
where pa.event_id = pl.event_id 
and pl.program = mc.link
and date_of_event  between '1900-01-01' and '1905-12-31'
and pa.orchestra = 'Vienna Philharmonic'
and pa.event_id=12179;

select  Orchestra
    ,pa.*
    ,first_name||' '||last_name Composer
from programs_all pa, program_list pl ,  mappings_csv mc  

where 1=1
and pa.event_id = pl.event_id
and pl.program = mc.link
and date_of_event  between '1900-01-01' and '1900-06-31' 
and pa.orchestra = 'Vienna Philharmonic'
;

select * from programs_all where event_id = 12179;
select * from program_list where event_id = 12179;



