select * from programs_all;
select distinct place, country from programs_all;
select * from programs_all where  place like '%,%';

select pa.*, pl.program,c.conductor , COALESCE(mc.First_Name, '') ||' '|| COALESCE(mc.Last_Name, '') as coomposer
from programs_all pa
    left outer join program_list pl on pa.event_id=pl.event_id
    left outer join conductors c on pa.event_id=c.event_id
    left outer join mappings_csv mc on pl.program = mc.link
and pa.event_id in ('5094')
;

select * from programs_all where event_id=5094;
select * from conductors where event_id=5094;
select * from program_list where event_id=5094;
select * from mappings_csv where link ='China Philharmonic Yellow River';

--China Philharmonic Yellow River
--China Philharmonic Yellow River

select pa.orchestra,pa.event_id,pa.date_of_event, pa.place,pa.country,pl.program, c.conductor, m.title
from programs_all pa  
left outer join  program_list pl on pa.event_id=pl.event_id
left outer join conductors c on pa.event_id=c.event_id
left outer join mappings_csv m on pl.program=m.link
where pa.place ='Provo'
and pa.date_of_event between '1900-01-01' and '1980-01-01'
order by pa.date_of_event
    
