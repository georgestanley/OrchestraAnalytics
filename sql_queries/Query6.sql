

select pa.date_of_event,
pa.event_id,
pa.Place,
pa.country,
pa.Orchestra,
pl.program Work

from programs_all pa , program_list pl 
where pa.event_id = pl.event_id
group by  pa.date_of_event,
pa.event_id,
pa.Place,
pa.country,
pa.Orchestra,
pl.program  
having count(*) >1;




select pa.date_of_event,
pa.event_id,
pa.Place,
pa.country,
pa.Orchestra,
pl.program Work,
mc.title

from programs_all pa , program_list pl left outer join mappings_csv mc on pl.program=mc.link
where pa.event_id = pl.event_id;



select * from programs_temp where event_id=3856;
select * from programs_all where event_id in (5094,5095);

WITH total as
    ( select Orchestra,sum(counts) as total
    from (select Orchestra
    ,pa.event_id, count(*) counts
from programs_all pa, program_list pl
where 1=1
and pa.event_id = pl.event_id
and pa.date_of_event between '1900-01-01' and '1905-01-01'
group by Orchestra
    )
    group by Orchestra ),

pageviews2 as
(select Orchestra,program Work , count(distinct pa.event_id) counts
from programs_all pa, program_list pl
where pa.event_id = pl.event_id
and pa.date_of_event between '1900-01-01' and '1905-01-01'

group by Orchestra,Work)

select total.Orchestra,Work,total.total, counts ,
    round(((counts *1.0) /total.total)*100,2) as share
from pageviews2,
    total
where pageviews2.Orchestra=total.Orchestra
order by total.Orchestra, share desc;



WITH total as
    ( select Orchestra,sum(counts) as total
    from (select Orchestra
    ,pa.event_id, count(*) counts
from programs_all pa, program_list pl
where 1=1
and pa.event_id = pl.event_id
and pa.date_of_event between '1900-01-01' and '1905-01-01'
and pa.orchestra in ('Vienna Philharmonic')
group by Orchestra
    )
    group by Orchestra ),

pageviews2 as
(select Orchestra,mc.title Work , pl.program, count(distinct pa.event_id) counts
from programs_all pa, program_list pl left outer join mappings_csv mc on pl.program=mc.link
where pa.event_id = pl.event_id
and pa.date_of_event between '1900-01-01' and '1905-01-01'
and pa.orchestra in ('Vienna Philharmonic')
group by Orchestra,Work)


select total.Orchestra,Work,program,total.total, counts ,
    round(((counts *1.0) /total.total)*100,2) as share
from pageviews2,
    total
where pageviews2.Orchestra=total.Orchestra
order by total.Orchestra, share desc;


select  link, title, count(*) from mappings_csv group by link,title ;


WITH total as
    (select Orchestra,sum(counts) as total
    from (select Orchestra
        ,pa.event_id, count(*) counts
        from programs_all pa, program_list pl, mappings_csv mc
        where 1=1
        and pa.event_id = pl.event_id
        and pl.program = mc.link
and date_of_event  between '1900-01-01' and '1910-12-31' 
        --and pa.orchestra in ('Vienna Philharmonic')
        group by Orchestra)
    group by Orchestra ),
pageviews2 as
    (select Orchestra, first_name||' '||last_name Composer, count( pa.event_id) counts
    from programs_all pa, program_list pl, mappings_csv mc
    where pa.event_id = pl.event_id
    and pl.program= mc.link
and date_of_event  between '1900-01-01' and '1910-12-31' 
    --and pa.orchestra in ('Vienna Philharmonic')
    group by Orchestra,composer)
    select * from (
select total.Orchestra,Composer,total.total, counts ,
    round(((counts *1.0) /total.total)*100,2) as share
from pageviews2,
    total
where pageviews2.Orchestra=total.Orchestra
order by total.Orchestra, share desc
)
--group by Composer order by counts desc 
;


select * from mappings_csv;

select pa.*,pl.program,mc.Genre, mc.Title,mc.composition_or_premiere_date
from programs_all pa, program_list pl, mappings_csv mc
where 1=1
and pa.event_id = pl.event_id
and pl.program=mc.link
and mc.title= 'Adagio for Strings';

select * from programs_temp where datum='26/10/1974' and orchestra='Vienna Philharmonic';



