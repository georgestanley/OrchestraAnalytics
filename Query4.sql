select * from programs_temp where dirigent in ('György Cziffra d.J.', 'György Csiffra jun', 'FL');
select * from programs_temp where dirigent like '%Csiffra%';
select * from conductors where conductor like '%FL%';


--Spelling mistakes correction . Execute if needed
update programs_temp set dirigent =  'Leopold Ludwig' where dirigent='LL';
update programs_temp set dirigent =  'Fritz Rieger' where dirigent='FR';
update programs_temp set dirigent =  'István Kertész' where dirigent='IK';
update programs_temp set dirigent =  'Marek Janowski' where dirigent='Janowski';
update programs_temp set dirigent =  'Ferdinand Leitner' where dirigent='FL';
update programs_temp set dirigent =  'Herbert Blomstedt' where dirigent='HB';
update programs_temp set dirigent =  'Bernhard Klee' where dirigent='Klee';
update programs_temp set dirigent =  'Moshe Atzmon' where dirigent='Moshe Moshe Atzmon';
update programs_temp set dirigent =  'Riccardo Chailly' where dirigent='Chailly';
update programs_temp set dirigent =  'György Cziffra' where dirigent='Györgi Csiffra jun.';
update programs_temp set dirigent =  'György Cziffra' where dirigent='György Cziffra d.J.';
update programs_temp set dirigent =  'Rafael Kubelík' where dirigent='Kubelik';
update programs_temp set dirigent =  'Wilhelm Österreicher' where dirigent='Wilheln Österreicher';
update programs_temp set dirigent =  'Wolfgang Sawallisch' where dirigent='Sawallisch';

update conductors set conductor =  'Leopold Ludwig' where conductor='LL';
update conductors set conductor =  'Fritz Rieger' where conductor='FR';
update conductors set conductor =  'István Kertész' where conductor='IK';
update conductors set conductor =  'Marek Janowski' where conductor='Janowski';
update conductors set conductor =  'Ferdinand Leitner' where conductor='FL';
update conductors set conductor =  'Herbert Blomstedt' where conductor='HB';
update conductors set conductor =  'Bernhard Klee' where conductor='Klee';
update conductors set conductor =  'Moshe Atzmon' where conductor='Moshe Moshe Atzmon';
update conductors set conductor =  'Riccardo Chailly' where conductor='Chailly';
update conductors set conductor =  'György Cziffra' where conductor='Györgi Csiffra jun.';
update conductors set conductor =  'György Cziffra' where conductor='György Cziffra d.J.';
update conductors set conductor =  'Rafael Kubelík' where conductor='Kubelik';
update conductors set conductor =  'Wilhelm Österreicher' where conductor='Wilheln Österreicher';
update conductors set conductor =  'Wolfgang Sawallisch' where conductor='Sawallisch';


--Part4
select pa.event_id, pa.date_of_event, pa.country, pa.place, pa.Orchestra,group_concat(pl.program) program, group_concat(distinct c.conductor) conductor
from programs_all pa, program_list pl ,conductors c
where 1=1
and pa.event_id=pl.event_id
and pa.event_id=c.event_id
--and c.conductor ='Eduard Kremser'
group by pa.event_id, pa.date_of_event, pa.country, pa.place, pa.Orchestra;

select * from conductors where conductor='Felix von Weingartner';


WITH total as
    ( select Orchestra,sum(counts) as total
    from (select Orchestra, conductor, count(*) counts
        from programs_all pa, conductors c
        where pa.event_id = c.event_id
        and orchestra in ("Vienna Philharmonic")
        and date_of_event  between '1900-01-01' and '1905-12-31' 
        group by Orchestra,conductor)
    group by Orchestra )

select total.Orchestra,Conductor,total.total, counts ,
    round(((counts *1.0) /total.total)*100,2) as share
from (select Orchestra, conductor, count(*) counts
    from programs_all pa, conductors c
    where pa.event_id = c.event_id
    and date_of_event  between '1900-01-01' and '1905-12-31'
group by Orchestra,conductor) pageviews,
    total
where pageviews.Orchestra=total.Orchestra
order by total.Orchestra,counts desc;




